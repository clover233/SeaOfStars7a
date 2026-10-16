"""微信 8.0.79 动态性能场景：控件优先、截图核对、比例手势和逐步结果。

微信基础、搜索/支付及小程序/存储操作统一在本模块，保留原有三层继承关系。
主屏控件未导出时，macOS 使用内嵌的本地 Vision OCR。其他系统可设置
WEIXIN_OCR_COMMAND，命令接收截图路径，输出 text/x/y/w/h 的比例框 JSON。
仅向用户授权的置顶会话“测试”实发；朋友圈评论、推荐名片只验证编辑/选择页。
"""
import functools
import hashlib
import json
import logging
import os
from pathlib import Path
import platform
import re
import shlex
import struct
import subprocess
import tempfile
import time
import xml.etree.ElementTree as ET
import zlib

from Cases.Top48.dynamic_apps_common import DynamicAppCase
from aw_new import SeaOfStarsAW


# 内嵌 macOS Vision OCR 源码，按内容哈希缓存编译结果。
_WEIXIN_OCR_SOURCE = r'''// macOS 上的可选本地截图文字定位；不上传图片，不需要第三方 OCR 服务。
import Foundation
import Vision

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["zh-Hans", "en-US"]
request.customWords = ["测试", "测试账号", "微信", "朋友圈", "发送", "预览", "拍摄"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
var rows = (request.results ?? []).compactMap { item -> [String: Any]? in
    guard let candidate = item.topCandidates(1).first else { return nil }
    let box = item.boundingBox
    return ["text": candidate.string, "x": box.minX, "y": 1-box.maxY,
            "w": box.width, "h": box.height, "confidence": candidate.confidence]
}
let json = try JSONSerialization.data(withJSONObject: rows)
print(String(data: json, encoding: .utf8)!)
'''


class WeixinStepSkipped(Exception):
    """功能、素材或前置步骤不可用；不能记为 PASS。"""


def optional(key):
    def decorate(method):
        @functools.wraps(method)
        def wrapped(self, *args, **kwargs):
            if key in self.unavailable:
                raise WeixinStepSkipped(self.unavailable[key])
            try:
                return method(self, *args, **kwargs)
            except WeixinStepSkipped as error:
                self.unavailable[key] = str(error)
                raise
        return wrapped
    return decorate


class WeixinDynamicCase(DynamicAppCase):
    PACKAGE = 'com.tencent.mm'
    all_app_package_list = [PACKAGE]
    TEST_CONTACT = '测试'
    PROFILE_CONTACT = '测试账号'
    MEDIA_SENDER = '测试账号'
    # 用户最新授权：仅向置顶会话“测试”实发和拨号。
    ALLOW_SEND = True
    NEED_IMAGES = False
    ALBUM = '微信性能素材'

    def set_up(self):
        super().set_up()
        self.unavailable = {}
        self._screen_cache = None
        self._locators = set()
        self._ocr_command = None
        self._original_ime = self.d.current_ime()
        self._ime_changed = False
        # 编译和素材准备在性能采集之前完成。
        self.prepare_ocr()
        if self.NEED_IMAGES:
            self.prepare_images()

    def prepare_ocr(self):
        command = os.environ.get('WEIXIN_OCR_COMMAND')
        if command:
            self._ocr_command = shlex.split(command)
        elif platform.system() == 'Darwin':
            digest = hashlib.sha256(_WEIXIN_OCR_SOURCE.encode('utf-8')).hexdigest()[:12]
            binary = Path(tempfile.gettempdir()) / ('seaofstars-weixin-ocr-' + digest)
            if not binary.exists():
                with tempfile.TemporaryDirectory(prefix='weixin-ocr-source-') as folder:
                    source = Path(folder) / 'main.swift'
                    source.write_text(_WEIXIN_OCR_SOURCE, encoding='utf-8')
                    subprocess.run(['/usr/bin/swiftc', str(source), '-o', str(binary)],
                                   check=True, capture_output=True, timeout=120)
            self._ocr_command = [str(binary)]

    def prepare_images(self):
        # 自生成纯色测试图，固定专用相册，不选择用户的个人图片。
        remote = '/sdcard/Pictures/' + self.ALBUM
        self.d.shell(['mkdir', '-p', remote])
        def chunk(kind, data):
            return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind + data))
        with tempfile.TemporaryDirectory(prefix='weixin-fixtures-') as folder:
            for index in range(9):
                name = 'SeaOfStars_weixin_{:02d}.png'.format(index + 1)
                destination = remote + '/' + name
                if self.d.shell(['test', '-f', destination]).exit_code == 0:
                    continue
                rgb = (30 + index * 22, 180 - index * 12, 70 + index * 17)
                raw = b''.join(b'\x00' + bytes(rgb) * 320 for _ in range(320))
                png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!2I5B', 320, 320, 8, 2, 0, 0, 0))
                       + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))
                local = Path(folder) / name
                local.write_bytes(png)
                self.d.push(str(local), destination)
                self.d.shell(['am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE',
                              '-d', 'file://' + destination])

    @staticmethod
    def normalized(text):
        return re.sub(r'[^\w\u4e00-\u9fff]', '', text).lower()

    def invalidate(self):
        self._screen_cache = None

    def screen(self):
        if self._screen_cache and time.monotonic() - self._screen_cache[0] < .35:
            return self._screen_cache[1]
        width, height = self.d.window_size()
        root = ET.fromstring(self.d.dump_hierarchy())
        rows = []
        for node in root.iter('node'):
            if (node.get('package') != self.PACKAGE or node.get('display-id', '0') != '0'
                    or node.get('visible-to-user') == 'false'):
                continue
            box = self.bounds(node)
            if len(box) != 4 or box[2] <= box[0] or box[3] <= box[1]:
                continue
            label = node.get('text') or node.get('content-desc')
            if label:
                rows.append(dict(text=label, x=box[0]/width, y=box[1]/height,
                                 w=(box[2]-box[0])/width, h=(box[3]-box[1])/height, source='tree'))
        # 此实机微信正文返回 [0,0][0,0] 的不可见根，弹出菜单偶尔有空白布局节点。
        if self._ocr_command:
            with tempfile.TemporaryDirectory(prefix='weixin-screen-') as folder:
                shot = str(Path(folder) / 'screen.png')
                self.d.screenshot(shot)
                result = subprocess.run(self._ocr_command + [shot], check=True, capture_output=True,
                                        text=True, timeout=30)
                recognized = json.loads(result.stdout)
                native_rows, rows = rows, []
                for row in recognized:
                    row['source'] = 'screenshot-ocr'
                    # 弹层后面的节点有时仍标为 visible。截图确认文字在前景可见，
                    # 再优先使用同一行的原生边界，避免点击被遮挡的主界面控件。
                    matches = [native for native in native_rows
                               if self.normalized(native['text']) == self.normalized(row['text'])
                               and abs(native['y']+native['h']/2-row['y']-row['h']/2) < .025]
                    rows.append(matches[0] if len(matches) == 1 else row)
        self._screen_cache = (time.monotonic(), rows)
        return rows

    def find(self, label, contains=False, region=None):
        query = self.normalized(label)
        found = []
        for row in self.screen():
            text = self.normalized(row['text'])
            x, y = row['x'] + row['w']/2, row['y'] + row['h']/2
            if (query in text if contains else query == text):
                if region is None or region[0] <= x <= region[2] and region[1] <= y <= region[3]:
                    found.append(row)
        return sorted(found, key=lambda row: (row['y'], row['x']))

    def visible(self, label, contains=False, region=None):
        return bool(self.find(label, contains, region))

    def choose(self, label, contains=False, region=None, index=None):
        rows = self.find(label, contains, region)
        if not rows:
            raise WeixinStepSkipped('当前页面没有“{}”入口'.format(label))
        if index is None and len(rows) != 1:
            raise RuntimeError('控件不唯一：{}，匹配 {} 项'.format(label, len(rows)))
        row = rows[0 if index is None else index]
        self._locators.add(row['source'])
        self.pct(row['x'] + row['w']/2, row['y'] + row['h']/2, record=False)

    def point(self, x, y):
        self.foreground()
        # 与本工程 QQ 用例一致：Android 17 上鼠标源主屏注入可稳定关闭微信风险弹层。
        result = self.d.shell('input mouse -d 0 tap {} {}'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('主屏点击失败：' + result.output)
        self.invalidate()

    def pct(self, x, y, record=True):
        if record:
            self._locators.add('verified-ratio')
        super().pct(x, y)
        time.sleep(.4)

    def swipe(self, x1=.5, y1=.78, x2=.5, y2=.32, duration=400):
        self.foreground()
        width, height = self.d.window_size()
        result = self.d.shell('input mouse -d 0 swipe {} {} {} {} {}'.format(
            round(width*x1), round(height*y1), round(width*x2), round(height*y2), duration))
        if result.exit_code:
            raise RuntimeError('主屏滑动失败：' + result.output)
        self.invalidate()

    def back(self):
        self.foreground()
        self.d.press('back')
        self.invalidate()
        time.sleep(.7)

    def activity_is(self, *names):
        activity = self.current_app()['activity'].lower()
        return any(name.lower() in activity for name in names)

    def await_text(self, label, contains=False, timeout=12, region=None):
        self.wait_for(lambda:self.visible(label, contains, region), '页面未出现“{}”'.format(label), timeout)

    def main_ready(self):
        return self.visible('通讯录', region=(0, .90, 1, 1)) and self.visible('我', region=(.7, .90, 1, 1))

    def main_page(self):
        for _ in range(12):
            if self.main_ready():
                self._verified_chat = None
                return
            if self.call_warning_reason():
                self.choose('我知道了')
            elif self.visible('不保留'):
                if self._owned_draft:
                    self.choose('不保留')
                    self._owned_draft = False
                elif self.visible('保留'):
                    self.choose('保留')
                else:
                    raise RuntimeError('发现非本用例创建的草稿，未自动丢弃')
            elif self.visible('放弃编辑'):
                self.choose('放弃编辑')
            else:
                self.back()
        raise RuntimeError('未能返回微信主界面')

    def tab(self, label):
        self.main_page()
        # 底部图标的文字偶有 OCR 错字；已按截图核对四个等宽标签。
        slots = {'微信': .125, '通讯录': .375, '发现': .625, '我': .875}
        def action():
            if self.find(label, region=(0, .90, 1, 1)):
                self.choose(label, region=(0, .90, 1, 1))
            else:
                self.pct(slots[label], .943)
        def ready():
            if label == '发现':
                return self.main_ready() and self.visible('朋友圈')
            if label in ('微信', '通讯录'):
                return self.main_ready() and self.visible(label, label == '微信', (.2, .05, .8, .11))
            return self.main_ready()
        self.transition(action, ready, '未切换到底部标签：' + label)
        if label == '发现':
            self.await_text('朋友圈')
        elif label == '通讯录':
            self.await_text('通讯录', region=(.2, .05, .8, .11))
            for _ in range(5):
                if self.visible('新的朋友'):
                    break
                self.swipe(y1=.30, y2=.8)
                time.sleep(.5)
        else:
            self.wait_for(self.main_ready, '底部标签切换后未显示主界面')

    def launch(self):
        self.unavailable = {}
        self._album_selected = 0
        self._camera_origin = None
        self._owned_draft = False
        self._panel_open = False
        self._call_active = False
        self._recording = False
        self._verified_chat = None
        self.d.shell(['am', 'start', '-W', '--display', '0', '-n', self.PACKAGE + '/.ui.LauncherUI'])
        self.invalidate()
        time.sleep(2)
        if self.visible('登录') and not self.main_ready():
            raise RuntimeError('微信尚未登录')
        if not self.screen():
            raise RuntimeError('微信未导出控件，且本机没有可用 OCR；请配置 WEIXIN_OCR_COMMAND')
        self.main_page()
        self.tab('微信')

    def home(self):
        self.main_page()
        self.swipe(.5, .995, .5, .60, 300)
        time.sleep(1)
        if self.current_app()['package'] == self.PACKAGE:
            self.d.press('home')
        self.wait_for(lambda:'launcher' in self.current_app()['activity'].lower(), '未返回 Home')

    def wechat_home(self):
        self.main_page()
        self.tab('微信')

    def browse_contacts(self):
        self.await_text('新的朋友')
        self.browse(3, 3)

    def video_call(self):
        self.dial(video=True)

    def voice_call(self):
        self.dial(video=False)

    def contacts(self):
        self.tab('通讯录')

    def discover(self):
        self.tab('发现')

    def open_chat(self, names):
        self.tab('微信')
        for _ in range(5):
            for name in names:
                if self.visible(name, region=(.12, .11, .8, .9)):
                    self.transition(lambda:self.choose(name, region=(.12, .11, .8, .9)),
                                    lambda:self.chat_ready(name), '未进入群聊：' + name)
                    self._chat = name
                    return
            self.swipe()
            time.sleep(.6)
        raise WeixinStepSkipped('会话列表未找到：' + '/'.join(names))

    def chat_ready(self, name=None):
        name = name or getattr(self, '_chat', self.TEST_CONTACT)
        title_ok = self.visible(name, name != self.TEST_CONTACT, (.15, .055, .85, .105))
        # 免打扰铃铛会被 OCR 连在短标题后读成 A；仅在聊天信息页精确核验后接受。
        if (name == self.TEST_CONTACT and getattr(self, '_verified_chat', None) == name
                and self.visible(name+'A', region=(.15, .055, .85, .105))):
            title_ok = True
        return (self.activity_is('ChattingUI', 'LauncherUI')
                and title_ok
                and not self.main_ready())

    @optional('test-chat')
    def test_chat(self):
        # 用户指定的是置顶会话，不从通讯录中两个同名“测试”联系人里猜选。
        self.wechat_home()
        def open_pinned():
            self.invalidate()
            matches = self.find(self.TEST_CONTACT, region=(.13, .11, .8, .89))
            if len(matches) != 1:
                raise WeixinStepSkipped('首页未唯一找到置顶会话“{}”'.format(self.TEST_CONTACT))
            self.choose(self.TEST_CONTACT, region=(.13, .11, .8, .89))
        self.transition(open_pinned,
                        lambda:not self.main_ready() and self.visible(self.TEST_CONTACT, True, (.15, .055, .85, .105)),
                        '未打开置顶会话')
        self._chat = self.TEST_CONTACT
        self.invalidate()
        self.await_text(self.TEST_CONTACT, True, region=(.15, .055, .85, .105))
        self.pct(.93, .083)
        self.await_text('聊天信息', True)
        if not self.visible(self.TEST_CONTACT, region=(0, .12, .9, .30)):
            raise RuntimeError('聊天信息页姓名不等于授权会话“{}”'.format(self.TEST_CONTACT))
        self._verified_chat = self.TEST_CONTACT
        self.back()
        self.wait_for(lambda:self.chat_ready(self.TEST_CONTACT), '未进入置顶会话“{}”'.format(self.TEST_CONTACT))
        self.adapt('按用户最新要求，使用置顶会话“{}”替代表中的测试账号'.format(self.TEST_CONTACT))
        if self.visible('拒收', True):
            self.unavailable['delivery'] = '授权会话拒收消息，后续实发和通话步骤跳过'
            self.adapt(self.unavailable['delivery'])

    def require_test_chat(self):
        if 'test-chat' in self.unavailable:
            raise WeixinStepSkipped(self.unavailable['test-chat'])
        if not self.ALLOW_SEND:
            raise WeixinStepSkipped('ALLOW_SEND已关闭实发与拨号')
        self.wait_for(lambda:self.chat_ready(self.TEST_CONTACT),
                      '实发/拨号前未确认授权的置顶“{}”聊天页'.format(self.TEST_CONTACT), timeout=8)

    def require_delivery(self):
        if self.visible('拒收', True) or self.visible('对方没有加你为朋友', True):
            self.unavailable['delivery'] = '授权会话拒收消息或未互加好友，无法完成实发/通话'
        if 'delivery' in self.unavailable:
            raise WeixinStepSkipped(self.unavailable['delivery'])

    @optional('pictures')
    def picture_chat(self):
        self.open_chat(('性能测试图片群', '性能图片群'))

    def media_ready(self):
        if self.visible('已过期', True) or self.visible('已被清理', True):
            raise WeixinStepSkipped('聊天媒体已过期或已被清理，不能作为有效浏览素材')
        return (self.activity_is('ImageGalleryUI', 'ImagePreviewUI', 'VideoPlayerUI', 'SnsBrowseUI')
                or self.visible('倍速'))

    def media_slides(self, right=3, left=3):
        if not self.media_ready():
            raise WeixinStepSkipped('没有进入图片/视频查看页面')
        for count, start, end in ((right, .2, .8), (left, .8, .2)):
            for _ in range(count):
                self.swipe(start, .5, end, .5, 500)
                time.sleep(2)
                if not self.media_ready():
                    raise RuntimeError('横向浏览时离开媒体查看页')

    def open_chat_media(self, kind):
        if not self.chat_ready():
            raise WeixinStepSkipped('对应的媒体测试群未打开')
        candidates = self.nodes(desc='图片' if kind == 'picture' else '视频', prefix=True)
        if candidates:
            action = lambda:self.click_node(candidates[0])
        else:
            # 实机截图：收到的图片在发送者昵称下方。视频优先以时长文字定位。
            rows = [r for r in self.screen() if .13 < r['y'] < .84
                and (re.fullmatch(r'\d{1,2}:\d{2}', r['text']) if kind == 'video' else r['text'] == self.MEDIA_SENDER)]
            if not rows:
                raise WeixinStepSkipped('当前群聊没有可核对的{}素材'.format(kind))
            row = rows[0]
            x, y = (.30, row['y'] - .06) if kind == 'video' else (.34, row['y'] + .12)
            action = lambda:self.pct(x, y)
        self.transition(action, self.media_ready, '点击素材后未进入媒体查看页')

    @optional('pictures')
    def browse_pictures(self):
        self.open_chat_media('picture')
        self.media_slides()

    @optional('video')
    def video_chat(self):
        self.open_chat(('性能测试群',))

    @optional('video')
    def browse_video(self):
        self.open_chat_media('video')
        self.media_slides()

    @optional('video')
    def video_menu(self):
        if not self.media_ready():
            raise WeixinStepSkipped('视频查看页不可用')
        self.d.long_click(.5, .5, 1)
        self.invalidate()
        self.await_text('发送给朋友')

    @optional('video')
    def forward_picker(self):
        self.choose('发送给朋友')
        self.await_text('选择聊天')

    @optional('video')
    def forward_recipient(self):
        self.choose(self.TEST_CONTACT, region=(.13, .15, .85, .9))
        self.await_text('发送给', True)
        if not self.visible(self.TEST_CONTACT, region=(.1, .35, .9, .75)):
            raise RuntimeError('转发确认页收件人不是授权会话“{}”'.format(self.TEST_CONTACT))

    @optional('video')
    def forward_send(self):
        if not self.ALLOW_SEND or not self.visible('发送给', True) or not self.visible(self.TEST_CONTACT, region=(.1, .35, .9, .75)):
            raise RuntimeError('没有确认授权收件人，停止转发')
        self.choose('发送', region=(.5, .5, .9, .95))
        self.wait_for(lambda:not self.visible('发送给', True), '转发确认框没有关闭')

    @optional('voice')
    def voice_chat(self):
        self.open_chat(('性能测试语音群', '性能测试语音'))

    @optional('voice')
    def play_voice(self):
        if not self.chat_ready():
            raise WeixinStepSkipped('语音测试群未打开')
        nodes = self.nodes(desc='语音', prefix=True)
        if nodes:
            self.click_node(nodes[0])
        else:
            rows = [r for r in self.screen() if re.search(r'\d+\s*["”″]$', r['text']) and .12 < r['y'] < .90]
            if not rows:
                raise WeixinStepSkipped('没有可识别的语音消息控件/时长')
            row = rows[-1]
            self.pct(.26, row['y'] + row['h']/2)
        # 短语音可能在下一次截图前结束；记录点击，不把它当成已确认播放。
        self.adapt('已点击语音消息；短语音播放状态不导出控件，保留截图供核对')

    def plus_menu(self):
        self.tab('微信')
        nodes = self.nodes(desc='更多功能按钮')
        if nodes:
            self.click_node(nodes[0])
        else:
            self.pct(.93, .083)
        self.await_text('添加朋友')

    def add_friend(self):
        self.choose('添加朋友')
        self.await_text('添加朋友', region=(.2, .05, .8, .11))

    def input_text(self, text):
        if not self._ime_changed:
            self.d.set_input_ime(True)
            self._ime_changed = True
        self.d.send_keys(text, clear=True)
        self.invalidate()

    def friend_query(self):
        if not self.visible('添加朋友', region=(.2, .05, .8, .11)):
            raise WeixinStepSkipped('添加朋友页面不可用')
        self.pct(.5, .14)
        time.sleep(.6)
        # 查询微信内公开的官方账号标识，不提交添加好友申请。
        self.input_text(os.environ.get('WEIXIN_FRIEND_QUERY', 'weixin'))
        self.await_text('搜索', True)
        matches = self.find('搜索', True, (0, .13, 1, .5))
        if matches:
            self.choose('搜索', True, (0, .13, 1, .5), index=0)
        else:
            self.d.press('search')
        self.invalidate()
        time.sleep(2)
        self.adapt('未提供好友微信号，以官方账号 weixin 查询替代，不发送好友申请')

    def moments_ready(self):
        return self.activity_is('SnsTimeLineUI')

    def moments(self):
        self.discover()
        self.choose('朋友圈')
        self.wait_for(self.moments_ready, '朋友圈未打开')
        time.sleep(1)

    def browse_moments(self):
        # 用户最新要求：浏览场景使用“测试账号”的个人朋友圈。
        self.friend_profile()
        self.friend_moments()
        self.browse(3, 3)
        self.adapt('按用户要求浏览“测试账号”的个人朋友圈')

    def comment(self):
        # 当前授权仅涵盖指定测试会话，未授权公开评论他人的朋友圈。
        raise WeixinStepSkipped('朋友圈评论“真不错”会公开发送；当前仅获准对置顶“测试”实发')

    def moments_camera(self):
        if not self.moments_ready():
            self.moments()
        self.pct(.93, .083)
        time.sleep(.5)
        if self.visible('我知道了'):
            self.choose('我知道了')
            time.sleep(.5)
            if not self.visible('从手机相册选择'):
                self.pct(.93, .083)
        self.await_text('从手机相册选择')

    def camera_ready(self):
        return self.activity_is('MMSightCaptureUI', 'CameraActivity', 'CameraKit', 'MMRecordUI') and not self.visible('完成')

    def camera_from_moments(self):
        self.choose('拍摄')
        self._camera_origin = 'moments'
        self.wait_for(self.camera_ready, '朋友圈拍摄页未打开')

    def cancel_moments_camera(self):
        self.return_to(self.moments_ready, '未返回朋友圈', limit=5)

    def camera_and_back(self):
        self.camera_from_moments()
        self.cancel_moments_camera()
        self.moments_camera()

    @optional('album')
    def select_album(self, count=3):
        self.choose('从手机相册选择')
        self.await_text('预览')
        self.pct(.5, .083)
        self.await_text(self.ALBUM, True)
        self.choose(self.ALBUM, True)
        self.await_text(self.ALBUM)
        # 专用相册仅有九张生成图片。实机为四列正方形网格，勾选在单元右上。
        # 用屏幕宽度计算行高；不能把像素或全屏高度直接当作网格行高。
        width, height = self.d.window_size()
        header = self.find(self.ALBUM, region=(.15, .05, .85, .12))[0]
        grid_top = (header['y'] + header['h']) * height + width * .035
        for index in range(count):
            col, row = index % 4, index // 4
            self.pct((col + .87)/4, (grid_top + row*width/4 + width*.03)/height)
        self.await_text('完成{}'.format(count), region=(.7, .9, 1, 1))
        self._album_selected = count
        self.adapt('使用专用“微信性能素材”相册的 {} 张生成图片'.format(count))

    def nine_photos(self):
        if not self.visible('从手机相册选择'):
            self.moments_camera()
        self.select_album(9)

    @optional('album')
    def album_preview(self):
        self.choose('预览', True, region=(0, .9, .3, 1))
        self.await_text('完成', True)

    @optional('album')
    def preview_slides(self):
        if not self._album_selected or not self.activity_is('ImagePreviewUI'):
            raise WeixinStepSkipped('三张图片的预览页未打开')
        for _ in range(2):
            self.swipe(.8, .5, .2, .5, 500)
            time.sleep(2)

    @optional('album')
    def album_done(self):
        if self._album_selected != 3:
            raise WeixinStepSkipped('未选择三张测试图片')
        if self.visible('完成', True, region=(.65, .04, 1, .13)):
            self.choose('完成', True, region=(.65, .04, 1, .13))
        else:
            self.choose('完成', True, region=(.65, .90, 1, 1))
            self.adapt('本版本预览完成按钮位于右下角，替代旧版右上角入口')
        self.await_text('所在位置')
        self._owned_draft = True

    @optional('location')
    def location(self):
        if not self._owned_draft:
            raise WeixinStepSkipped('朋友圈图片草稿未创建')
        self.choose('所在位置')
        time.sleep(2)
        if self.visible('使用时允许') or self.visible('仅在使用该应用时允许'):
            raise WeixinStepSkipped('位置权限尚未授予，跳过位置选择')
        self.await_text('不显示位置')

    @optional('location')
    def select_location(self):
        rows = [r for r in self.screen() if .20 < r['y'] < .8 and .12 < r['x'] < .5
                and len(r['text']) >= 4 and '不显示' not in r['text']]
        if not rows:
            raise WeixinStepSkipped('当前位置没有可选地点')
        row = rows[0]
        self.pct(row['x'] + row['w']/2, row['y'] + row['h']/2)
        if self.visible('完成', region=(.7, .04, 1, .12)):
            self.choose('完成', region=(.7, .04, 1, .12))
        self.await_text('所在位置', timeout=10)

    def leave_draft(self):
        if not self._owned_draft:
            raise WeixinStepSkipped('没有本用例创建的朋友圈草稿')
        # 先从位置页返回编辑页，再以侧滑触发放弃草稿确认框。
        if self.visible('不显示位置'):
            self.back()
        self.swipe(.005, .5, .7, .5, 450)
        time.sleep(.7)
        if not self.visible('不保留') and not self.visible('放弃编辑'):
            self.back()

    def discard_draft(self):
        if not self._owned_draft:
            raise WeixinStepSkipped('没有本用例创建的草稿')
        if self.visible('不保留'):
            self.choose('不保留')
        elif self.visible('放弃编辑'):
            self.choose('放弃编辑')
        else:
            raise RuntimeError('没有出现丢弃草稿确认框')
        self._owned_draft = False
        self.wait_for(self.moments_ready, '丢弃草稿后未返回朋友圈')

    def adapt(self, reason):
        self._adaptations.append(reason)

    @optional('friend')
    def friend_profile(self):
        self.contacts()
        self.choose(self.PROFILE_CONTACT, region=(.13, .15, .8, .89))
        self.await_text('发消息', True)
        time.sleep(1)

    @optional('friend')
    def friend_avatar(self):
        if not self.visible('发消息', True):
            raise WeixinStepSkipped('好友详情页不可用')
        self.pct(.12, .17)
        self.wait_for(lambda:self.activity_is('ContactRemarkImagePreviewUI', 'ProfileAvatar', 'ImagePreviewUI', 'ImageGalleryUI', 'ProfileHdHeadImg'),
                      '好友头像大图未打开')
        self.back()
        self.await_text('发消息', True)

    @optional('friend-moments')
    def friend_moments(self):
        if 'friend' in self.unavailable:
            raise WeixinStepSkipped(self.unavailable['friend'])
        if not self.visible('朋友圈'):
            raise WeixinStepSkipped('测试账号没有可见的朋友圈入口')
        self.choose('朋友圈')
        self.wait_for(lambda:self.activity_is('SnsUserUI'), '好友朋友圈未打开')

    @optional('friend-moments')
    def friend_pictures(self):
        images = [n for n in self.nodes(desc='图片', prefix=True) if self.bounds(n)[1] > self.d.window_size()[1]*.2]
        if images:
            self.click_node(images[0])
        else:
            dates = [r for r in self.screen() if re.search(r'\d.*月', r['text']) and r['x'] < .22 and .3 < r['y'] < .85]
            if not dates:
                raise WeixinStepSkipped('好友相册没有可核对的图片缩略图')
            self.pct(.36, dates[0]['y'] + .025)
        if not self.activity_is('SnsBrowseUI', 'ImageGalleryUI', 'SnsGalleryUI'):
            raise WeixinStepSkipped('未确认进入好友图片大图')
        for direction in range(6):
            self.swipe(.8 if direction % 2 == 0 else .2, .5, .2 if direction % 2 == 0 else .8, .5, 500)
            time.sleep(2)

    def return_profile(self):
        if 'friend' in self.unavailable:
            raise WeixinStepSkipped(self.unavailable['friend'])
        self.return_to(lambda:self.visible('发消息', True), '未返回好友资料页', limit=5)

    def recommend_friend(self):
        self.return_profile()
        self.pct(.93, .083)
        self.await_text('把他推荐给朋友')
        self.choose('把他推荐给朋友')
        self.await_text('选择聊天')
        self.adapt('验证推荐名片的收件人选择页后返回；不向未授权对象发送名片')

    @optional('scan')
    def scan(self):
        self.choose('扫一扫')
        self.wait_for(lambda:self.activity_is('ScanUI', 'BaseScanUI'), '扫一扫未打开')

    @optional('scan')
    def scan_album(self):
        if not self.activity_is('ScanUI', 'BaseScanUI'):
            raise WeixinStepSkipped('扫一扫不可用')
        if self.visible('相册'):
            self.choose('相册')
        else:
            # 扫一扫右下角的相册入口，按当前屏幕尺寸换算。
            self.pct(.885, .842)
        self.wait_for(lambda:self.activity_is('AlbumPreviewUI', 'ImageFolderMgrUI', 'ImageGalleryUI', 'SelectPicUI'),
                      '扫码相册未打开')

    @optional('scan')
    def scan_picture(self):
        # 不识别私人二维码；从专用素材相册选一张无二维码测试图。
        self.pct(.5, .083)
        if not self.visible(self.ALBUM, True):
            raise WeixinStepSkipped('扫码相册中未找到专用测试素材')
        self.choose(self.ALBUM, True)
        self.pct(.12, .16)
        time.sleep(1)
        self.adapt('使用专用测试图验证相册选图；该图不含二维码')

    def edit_message(self):
        self.require_test_chat()
        editors = [n for n in self.nodes() if n.get('class') == 'android.widget.EditText']
        if editors:
            self.click_node(editors[0])
        else:
            self.pct(.42, .945)

    def send_text(self):
        self.require_test_chat()
        self.require_delivery()
        self.input_text('哈哈哈')
        self.await_text('发送', region=(.7, .3, 1, .98))
        self.choose('发送', region=(.7, .3, 1, .98))
        self.wait_for(lambda:not self.visible('发送', region=(.7, .3, 1, .98)), '发送后输入框未清空')
        self.await_text('哈哈哈')
        if self.visible('未发送', True) or self.visible('发送失败', True):
            raise WeixinStepSkipped('微信报告消息未发送，保留失败消息，不自动重复发送')
        # 广播输入法没有可见键盘，不能盲目 Back（会退出当前会话）。
        if self.keyboard_shown():
            self.back()

    def keyboard_shown(self):
        state = self.d.shell('dumpsys input_method').output
        # 服务的 mIsInputViewShown 会在键盘隐藏后保留 true，不能用它判断屏幕键盘。
        return 'mInputShown=true' in state

    def send_voice(self):
        self.require_test_chat()
        self.require_delivery()
        if not self.visible('按住 说话'):
            self.pct(.06, .945)
        self.await_text('按住 说话')
        row = self.find('按住 说话')[0]
        width, height = self.d.window_size()
        self.d.long_click(round(width*(row['x']+row['w']/2)), round(height*(row['y']+row['h']/2)), 1.5)
        self.invalidate()
        time.sleep(.5)
        self.wait_for(lambda:self.chat_ready(self.TEST_CONTACT), '发送语音后未返回授权会话')
        self.adapt('录制并发送约1.5秒测试语音，短语音回执不导出控件')

    def emoji_panel(self):
        self.require_test_chat()
        self.pct(.84, .945)
        time.sleep(.5)
        # 页面出现标准表情的命名节点时直接使用它们；否则按核对过的网格选择。
        self._emoji_open = True
        self._panel_open = True

    def send_emoji(self):
        self.require_test_chat()
        self.require_delivery()
        if not getattr(self, '_emoji_open', False):
            raise WeixinStepSkipped('表情面板未打开')
        names = ('微笑', '撇嘴', '色')
        for index, name in enumerate(names):
            if self.visible(name):
                self.choose(name)
            else:
                # 微信标准表情页：八列，第一行前三个；先核对“发送”按钮存在。
                if not self.visible('所有表情'):
                    raise WeixinStepSkipped('当前表情面板未导出标准表情且布局无法核对')
                self.pct((index+.65)/8, .745)
        self.choose('发送', region=(.7, .4, 1, 1))
        self._emoji_open = False

    def chat_more(self):
        self.require_test_chat()
        if self.visible('拍摄') and self.visible('视频通话'):
            return
        # 先关闭表情/键盘到聊天底部，再打开工具栏。
        if self._panel_open or self.keyboard_shown():
            self.back()
            self._panel_open = False
        self.pct(.94, .945)
        self.await_text('拍摄')

    def call_picker(self):
        self.require_test_chat()
        self.choose('视频通话')
        self.await_text('语音通话', True)

    def call_warning_reason(self):
        if not self.visible('我知道了'):
            return None
        for row in self.screen():
            if any(word in row['text'] for word in ('风险', '无法进行通话', '无法通话', '不能视频通话',
                                                    '不能语音通话', '无法接通', '对方没有加你为朋友')):
                return row['text']
        return None

    def dismiss_call_warning(self, reason):
        self.transition(lambda:self.choose('我知道了'),
                        lambda:self.chat_ready(self.TEST_CONTACT) and not self.visible('我知道了'),
                        '点击我知道了后未关闭通话提示')
        self._call_active = False
        self._last_call_warning = reason
        if '没有加你为朋友' in reason:
            self.unavailable['delivery'] = reason
        raise WeixinStepSkipped('已点击我知道了：' + reason)

    def dial(self, video=True):
        self.require_test_chat()
        self._last_call_warning = None
        try:
            self.require_delivery()
        except WeixinStepSkipped:
            if self.visible('取消') and self.visible('语音通话', True):
                self.choose('取消')
            raise
        label = '视频通话' if video else '语音通话'
        self.choose(label, True, region=(.2, .72, .8, .93))
        self._call_active = True
        self.wait_for(lambda:self.activity_is('VideoActivity', 'Voip') or self.call_warning_reason(), '通话页未打开')
        time.sleep(1)
        self.invalidate()
        reason = self.call_warning_reason()
        if reason:
            self.dismiss_call_warning(reason)

    def hang_up(self):
        reason = self.call_warning_reason()
        if reason:
            self.dismiss_call_warning(reason)
        if getattr(self, '_last_call_warning', None) and not getattr(self, '_call_active', False):
            raise WeixinStepSkipped(self._last_call_warning)
        if 'delivery' in self.unavailable and not getattr(self, '_call_active', False):
            raise WeixinStepSkipped(self.unavailable['delivery'])
        if not self.activity_is('VideoActivity', 'Voip'):
            if self.chat_ready(self.TEST_CONTACT):
                self.adapt('通话已由对端或超时结束，当前已返回聊天页')
                self._call_active = False
                return
            raise RuntimeError('不在测试通话页')
        if self.visible('挂断'):
            self.choose('挂断')
        elif self.visible('取消'):
            self.choose('取消')
        else:
            # 实机视频/语音呼叫中红色挂断按钮在底部正中。
            self.pct(.5, .88)
        self.wait_for(lambda:self.chat_ready(self.TEST_CONTACT), '挂断后未返回授权会话')
        self._call_active = False

    @optional('capture')
    def chat_camera(self):
        self.require_test_chat()
        self.choose('拍摄')
        self._camera_origin = 'chat'
        self.wait_for(self.camera_ready, '聊天拍摄页未打开')

    @optional('capture')
    def photo(self):
        if self._camera_origin != 'chat' or not self.camera_ready():
            raise WeixinStepSkipped('授权会话的拍摄页未打开')
        self.pct(.5, .898)
        self.await_text('完成')

    def send_capture(self):
        if self._camera_origin != 'chat':
            raise WeixinStepSkipped(self.unavailable.get('capture', '本次拍摄未成功进入预览页'))
        if not self.ALLOW_SEND or getattr(self, '_chat', None) != self.TEST_CONTACT:
            raise RuntimeError('拍摄内容没有授权的接收人')
        try:
            self.require_delivery()
        except WeixinStepSkipped:
            self.return_to(lambda:self.chat_ready(self.TEST_CONTACT), '取消拍摄后未返回聊天', limit=5)
            self._camera_origin = None
            raise
        self.choose('完成', region=(.65, .7, 1, .97))
        time.sleep(.6)
        if self.visible('发送', region=(.7, .7, 1, .98)):
            self.choose('发送', region=(.7, .7, 1, .98))
        self.wait_for(lambda:self.chat_ready(self.TEST_CONTACT), '拍摄内容发送后未返回授权会话')
        self._camera_origin = None
        self.require_delivery()

    @optional('capture')
    def video_mode(self):
        if not self.camera_ready():
            raise WeixinStepSkipped('录像拍摄页未打开')
        self.adapt('微信8.0.79拍照与录像共用快门，使用长按录制替代独立录像模式按钮')

    @optional('capture')
    def start_recording(self):
        if not self.camera_ready() or self._camera_origin != 'chat':
            raise WeixinStepSkipped('授权会话录像入口未准备好')
        width, height = self.d.window_size()
        self._shutter = (round(width*.5), round(height*.898))
        self.d.touch.down(*self._shutter)
        self._recording = True
        self.invalidate()
        time.sleep(1)

    def stop_recording(self):
        if not getattr(self, '_recording', False):
            raise WeixinStepSkipped('录像没有开始')
        self.d.touch.up(*self._shutter)
        self._recording = False
        self.invalidate()
        self.await_text('完成')

    @optional('official-list')
    def official_list(self):
        self.contacts()
        self.choose('公众号')
        self.await_text('公众号', region=(.2, .05, .8, .11))

    def find_official(self, names):
        for _ in range(5):
            for name in names:
                if self.visible(name, region=(.1, .12, .9, .91)):
                    self.choose(name, region=(.1, .12, .9, .91))
                    self._official = name
                    time.sleep(1.5)
                    return
            self.swipe()
            time.sleep(.8)
        raise WeixinStepSkipped('公众号列表没有：' + '/'.join(names))

    @optional('huawei')
    def huawei(self):
        if 'official-list' in self.unavailable:
            raise WeixinStepSkipped(self.unavailable['official-list'])
        self.find_official(('华为手机', '华为'))
        if self.visible('文章') or self.visible('已关注公众号'):
            self.adapt('本版本从通讯录直接进入公众号资料页，省略旧版本会话右上角头像入口')
        else:
            self.pct(.93, .083)
            time.sleep(1)
        if self.visible('全部消息'):
            self.choose('全部消息')

    @optional('huawei')
    def browse_official(self):
        self.browse(3, 3)

    @optional('article')
    def first_article(self):
        if 'huawei' in self.unavailable:
            raise WeixinStepSkipped(self.unavailable['huawei'])
        if self.visible('取消') and self.visible('更多信息'):
            self.choose('取消')
        if self.visible('文章', region=(0, .12, 1, .8)):
            self.choose('文章', region=(0, .12, 1, .8))
            time.sleep(1)
        rows = [r for r in self.screen() if .45 < r['y'] < .87 and len(r['text']) >= 6
                and not re.fullmatch(r'[\d年月日:/.-]+', r['text'])
                and not any(word in r['text'] for word in ('微信号', '功能介绍', '认证', '关注', '视频号', '服务'))]
        if not rows:
            raise WeixinStepSkipped('当前公众号未展示可识别的文章标题')
        row = rows[0]
        self.pct(row['x']+row['w']/2, row['y']+row['h']/2)
        self.wait_for(lambda:self.activity_is('WebViewUI', 'MMWebViewUI', 'TmplWebViewMMUI'), '文章页面未打开')

    @optional('article')
    def browse_article(self):
        self.browse(3, 0)

    def return_official(self):
        self.main_page()
        self.official_list()

    @optional('harmony')
    def harmony(self):
        if 'official-list' in self.unavailable:
            raise WeixinStepSkipped(self.unavailable['official-list'])
        self.find_official(('HarmonyOS',))

    @optional('harmony-site')
    def harmony_site(self):
        if 'harmony' in self.unavailable:
            raise WeixinStepSkipped(self.unavailable['harmony'])
        if not self.visible('HMOS'):
            raise WeixinStepSkipped('当前HarmonyOS公众号没有HMOS菜单')
        self.choose('HMOS')
        time.sleep(.7)
        self.choose('官网直达')
        self.wait_for(lambda:self.activity_is('WebViewUI', 'MMWebViewUI'), 'HarmonyOS官网未打开')

    @optional('harmony-site')
    def browse_harmony(self):
        self.browse(2, 2)

    @optional('mini')
    def recent_minis(self):
        self.tab('微信')
        self.swipe(.5, .23, .5, .82, 600)
        self.await_text('最近使用的小程序')

    @optional('mini')
    def luckin(self):
        self.choose('瑞幸咖啡', index=0)
        time.sleep(2)
        # 小程序会恢复上一次的商品详情；先归一到含底部菜单的页面。
        for _ in range(5):
            if self.visible('菜单', region=(0, .88, 1, 1)):
                break
            if not self.activity_is('AppBrandUI'):
                raise WeixinStepSkipped('瑞幸小程序没有成功进入前台')
            self.back()
        self.await_text('菜单', timeout=30, region=(0, .88, 1, 1))

    def dismiss_luckin_prompts(self):
        if self.visible('拒绝') and self.visible('申请', True):
            self.choose('拒绝')
            time.sleep(.6)
        if self.visible('距你最近的门店', True):
            # 实机门店推荐底部弹层的关闭 X；关闭推荐不改变已有门店。
            self.pct(.897, .60)

    @optional('mini')
    def luckin_menu(self):
        self.choose('菜单', region=(0, .88, .5, 1))
        time.sleep(1)
        self.dismiss_luckin_prompts()
        self.await_text('人气Top', timeout=20)

    @optional('mini')
    def luckin_top(self):
        self.dismiss_luckin_prompts()
        self.choose('人气Top', region=(0, .2, .22, .8))
        time.sleep(.8)

    @optional('mini')
    def luckin_product(self):
        self.dismiss_luckin_prompts()
        rows = [r for r in self.screen() if .42 < r['x'] < .9 and .32 < r['y'] < .36 and len(r['text']) >= 4]
        if not rows:
            raise WeixinStepSkipped('当前人气Top菜单未展示首个商品标题')
        row = rows[0]
        self.pct(row['x']+row['w']/2, row['y']+row['h']/2)
        time.sleep(.8)
        self.dismiss_luckin_prompts()
        if not self.visible('加入购物车'):
            # 新品订阅提醒可能拦截第一次导航，仅在确认仍为菜单时再次打开。
            if self.visible('人气Top'):
                self.pct(row['x']+row['w']/2, row['y']+row['h']/2)
        self.await_text('加入购物车', timeout=20)

    @optional('mini')
    def luckin_cart(self):
        self.choose('加入购物车')
        time.sleep(1)
        if self.visible('手机号', True) or self.visible('登录'):
            raise WeixinStepSkipped('加入购物车需要登录，停在登录入口')
        self.wait_for(lambda:not self.visible('加入购物车'), '商品没有加入购物车')
        self.adapt('仅加入一件默认规格商品，不提交订单或支付')

    def save_results(self, records):
        path = Path(self.result_dir_path) / 'step_results.json'
        path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')

    @SeaOfStarsAW.function_log
    def run_case(self):
        if not getattr(self, '_prepared', False):
            self.set_up()
        records = []
        try:
            for run in range(self.TEST_TIME):
                for number, (name, action, stay) in enumerate(self.steps(), 1):
                    self._adaptations = []
                    self._locators = set()
                    record = dict(run=run+1, step=number, name=name, status='PASS')
                    logging.info('%s、%s', number, name)
                    SeaOfStarsAW.start_perfetto_trace()
                    try:
                        action()
                        time.sleep(stay)
                        if self._adaptations:
                            record.update(status='ADAPTED', reason='；'.join(self._adaptations))
                    except WeixinStepSkipped as error:
                        record.update(status='SKIP', reason=str(error))
                        logging.warning('SKIP %s：%s', name, error)
                    except Exception as error:
                        record.update(status='FAIL', reason=str(error))
                        logging.exception('步骤失败：%s', name)
                        raise
                    finally:
                        record['locators'] = sorted(self._locators)
                        records.append(record)
                        try:
                            SeaOfStarsAW.stop_and_get_perfetto_trace(
                                self.trace_dir_path, self.__class__.__name__,
                                'step_{}、{}_{}'.format(number, name, record['status']), '', self.screenshot_dir_path)
                            record['trace_exported'] = True
                        except Exception as error:
                            record['trace_exported'] = False
                            record['trace_error'] = str(error)
                            if record['status'] != 'FAIL':
                                record['status'] = 'FAIL'
                                raise
                            logging.exception('失败步骤 trace 导出失败')
                        finally:
                            self.save_results(records)
        finally:
            if getattr(self, '_recording', False):
                self.d.touch.up(*self._shutter)
                self._recording = False
            if getattr(self, '_call_active', False):
                try:
                    self.hang_up()
                except WeixinStepSkipped:
                    logging.info('通话不可用提示已关闭')
            self.restore_ime()

    def restore_ime(self):
        if getattr(self, '_ime_changed', False) and self._original_ime:
            self.d.shell(['ime', 'set', self._original_ime])
            self._ime_changed = False

    def clean_up(self):
        try:
            self.restore_ime()
        finally:
            super().clean_up()


class WeixinExtendedCase(WeixinDynamicCase):
    def point(self, x, y):
        self.foreground()
        # 本机短促 tap 偶尔被过滤；鼠标源原地按住 200ms，低于长按阈值。
        result = self.d.shell('input mouse -d 0 swipe {0} {1} {0} {1} 200'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('主屏点击失败：' + result.output)
        self.invalidate()

    def main_page(self):
        # 首页加号菜单仍保留底部标签，不能将弹层当作已经返回首页。
        if (self.main_ready() and self.visible('添加朋友', region=(.55, .1, 1, .45))
                and self.visible('发起群聊', region=(.55, .1, 1, .45))):
            self.back()
        super().main_page()
        if getattr(self, '_live_started', False):
            self.close_live_float()

    def live_float_box(self):
        width, height = self.d.window_size()
        boxes = []
        for node in ET.fromstring(self.d.dump_hierarchy()).iter('node'):
            box = self.bounds(node)
            if len(box) != 4 or node.get('package') != self.PACKAGE:
                continue
            left, top, right, bottom = box
            if (node.get('class') == 'android.widget.FrameLayout'
                    and not node.get('resource-id') and not node.get('content-desc')
                    and .15 < (right-left)/width < .4 and .1 < (bottom-top)/height < .35
                    and (left < width*.05 or right > width*.95)):
                boxes.append(box)
        return max(boxes, key=lambda b: (b[2]-b[0])*(b[3]-b[1])) if boxes else None

    def close_live_float(self):
        """只关闭本用例打开的直播浮窗，并确认其消失。"""
        def close():
            box = self.live_float_box()
            if not box:
                return
            buttons = self.nodes(desc='关闭')
            if len(buttons) == 1:
                self._locators.add('tree')
                self.click_node(buttons[0])
            else:
                # 浮窗有时不导出子控件；按截图核对的浮窗边界比例定位 X。
                left, top, right, bottom = box
                width, height = self.d.window_size()
                self.pct((left+(right-left)*.74)/width, (top+(bottom-top)*.83)/height)
        self.transition(close, lambda: self.live_float_box() is None and not self.live_ready(),
                        '直播浮窗未关闭，停止以免遮挡后续入口')
        self._live_started = False

    def clean_up(self):
        try:
            if getattr(self, '_live_started', False):
                self.main_page()
        finally:
            super().clean_up()

    def plus_menu(self):
        self.wechat_home()
        self.transition(lambda: self.pct(.93, .083),
                        lambda: self.visible('添加朋友', region=(.55, .1, 1, .45)),
                        '首页加号菜单未打开')

    def tab(self, label):
        if label not in ('我', '发现'):
            return super().tab(label)
        self.main_page()
        # “我”也有朋友圈入口，必须校验对应页面，不能仅凭底部标签判断成功。
        ready = (lambda: self.main_ready() and self.visible('服务') and self.visible('收藏')) if label == '我' else (
            lambda: self.main_ready() and self.visible('发现', region=(.2, .05, .8, .11)))
        self.transition(lambda: self.pct(.875 if label == '我' else .625, .943),
                        ready, '未切换到' + label)

    def needs(self, *keys):
        for key in keys:
            if key in self.unavailable:
                raise WeixinStepSkipped('前置功能不可用：' + self.unavailable[key])

    def content_wait(self, predicate, message, timeout=25):
        """有入口但内容受网络/账号/协议限制时，明确记录 SKIP。"""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():
                return
            self.foreground()
            if any(self.visible(word, True) for word in ('同意并', '同意协议', '暂不支持', '加载失败', '网络不可用')):
                raise WeixinStepSkipped(message + '；页面要求协议确认或内容不可用')
            time.sleep(.7)
        raise WeixinStepSkipped(message + '；等待内容超时')

    def me(self):
        self.tab('我')

    @optional('search')
    def search_page(self):
        self.wechat_home()
        def open_search():
            native = self.nodes(desc='搜索')
            if native:
                self.click_node(native[0])
            else:
                # 首页右上角搜索图标，已经实机截图核对。
                self.pct(.827, .083)
        self.transition(open_search, lambda: self.activity_is('FTSMainUI')
                        and self.visible('搜索', True, (0, .05, 1, .15)), '微信搜索输入页未打开')

    @optional('search')
    def search_huawei(self):
        self.needs('search')
        self.input_text('华为手机')
        self.await_text('华为手机', True)
        self.d.press('search')
        self.invalidate()
        self.content_wait(lambda: self.visible('搜索网络结果', True) or self.visible('综合'), '搜索建议未加载')
        if self.visible('搜索网络结果', True):
            heading = self.find('搜索网络结果', True)[0]
            rows = [r for r in self.find('华为手机', True) if r['y'] > heading['y']+heading['h']]
            if not rows:
                raise WeixinStepSkipped('没有华为手机的网络搜索入口')
            row = rows[0]
            self._locators.add(row['source'])
            self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
        self.content_wait(lambda: self.visible('华为手机', True) and (
            self.visible('搜一搜', True) or self.visible('公众号', True) or self.visible('综合')),
            '华为手机搜索结果未显示')

    @optional('scan')
    def scan_qr(self):
        def open_scan():
            if not self.visible('添加朋友', region=(.55, .1, 1, .45)):
                raise WeixinStepSkipped('首页加号菜单不可用')
            # 截图中“扫一扫”偶尔识别为“扫一千”；在已确认的菜单内匹配“扫”。
            self.choose('扫', True, (.55, .2, 1, .33))
        self.transition(open_scan, lambda: self.activity_is('ScanUI', 'BaseScanUI'), '扫一扫取景页未打开')
        # 表中未提供二维码素材；避免扫描到环境中未知的付款/登录二维码。
        self.adapt('未提供指定二维码，以进入扫一扫取景页面并停留替代扫码结果')

    @optional('pay-code')
    def pay_codes(self):
        self.choose('收付款', True, (.55, .2, 1, .45))
        time.sleep(1)
        current = self.current_app()['activity'].lstrip('.')
        windows = self.d.shell('dumpsys window windows').output.split('Window #')
        secure = any(current in part.splitlines()[0] and ' SECURE ' in part[:2000]
                     for part in windows if part.splitlines())
        if secure and not self.nodes() and not any(.12 < row['y'] < .9 for row in self.screen()):
            raise WeixinStepSkipped('收付款窗口启用 SECURE，截图正文为空且控件树无可用节点，无法核对二维码收款入口')
        self.content_wait(lambda: self.visible('二维码收款') or self.visible('收款码'), '收付款页面未显示')

    @optional('pay-code')
    def receive_code(self):
        self.needs('pay-code')
        self.choose('二维码收款' if self.visible('二维码收款') else '收款码')
        self.content_wait(lambda: self.visible('二维码收款', True) and (
            self.visible('设置金额') or self.visible('收款小账本') or self.visible('保存收款码')),
            '二维码收款页面未显示')

    @optional('channels')
    def channels(self):
        self.choose('视频号', region=(0, .12, 1, .9))
        self.content_wait(lambda: self.activity_is('FinderHome', 'FinderTimelineUI') and (
            self.visible('推荐') or self.visible('朋友') or self.visible('关注')), '视频号内容未加载')

    @optional('channels')
    def browse_channels(self):
        self.needs('channels')
        if not self.activity_is('Finder'):
            raise WeixinStepSkipped('当前不在视频号页面')
        self.browse(6, 0)

    @optional('live-list')
    def live_list(self):
        self.choose('直播', region=(0, .12, 1, .9))
        self.content_wait(lambda: self.activity_is('Finder', 'WebView') and (
            self.visible('直播', True) or self.visible('推荐')), '直播列表未加载')

    @optional('live-room')
    def first_live(self):
        self.needs('live-list')
        if not self.activity_is('FinderLiveSquare'):
            raise WeixinStepSkipped('当前不是已核对的双列直播列表')
        if not any(.2 < r['y'] < .85 for r in self.screen()):
            raise WeixinStepSkipped('直播列表未展示内容卡片')
        # 首张卡片的画面区域；卡片底部主播名字会进入资料页，不能点击名字。
        self.transition(lambda: self.pct(.25, .34), self.live_ready, '第一直播间未打开')
        self._live_started = True

    def live_ready(self):
        return self.activity_is('FinderLive') and not self.activity_is('Square')

    @optional('live-room')
    def browse_live(self):
        self.needs('live-list', 'live-room')
        if not self.live_ready():
            raise WeixinStepSkipped('当前不在直播间')
        self.browse(6, 0)

    @optional('games')
    def games(self):
        self.choose('游戏', region=(0, .12, 1, .9))
        self.content_wait(lambda: self.activity_is('GameTabUI', 'GameCenterUI') and (
            self.visible('找游戏') or self.visible('微信游戏', True)), '游戏首页未加载')
        if self.visible('圈子'):
            self.adapt('当前微信游戏默认显示圈子信息流，替代旧版游戏首页浏览')

    @optional('games')
    def browse_games(self):
        self.needs('games')
        if self.main_ready():
            raise WeixinStepSkipped('当前不在游戏首页')
        self.browse(6, 6)

    @optional('service')
    def service(self):
        self.me()
        self.choose('服务')
        self.await_text('钱包')

    @optional('wallet')
    def wallet(self):
        self.needs('service')
        self.choose('钱包')
        self.await_text('零钱')

    @optional('wallet')
    def balance(self):
        self.needs('wallet')
        self.choose('零钱')
        self.await_text('我的零钱')

    def return_service(self):
        self.needs('service')
        self.return_to(lambda: self.visible('钱包') and self.visible('手机充值'), '未返回服务页面', limit=8)

    @optional('top-up')
    def top_up(self):
        self.needs('service')
        self.choose('手机充值')
        self.content_wait(lambda: self.visible('手机充值', region=(.2, .05, .75, .12))
                          and self.visible('充话费'), '手机充值小程序未加载', timeout=40)

    @optional('utilities')
    def utilities(self):
        self.needs('service')
        self.choose('生活缴费')
        self.content_wait(lambda: self.visible('新增缴费') and self.visible('电费'),
                          '生活缴费小程序未加载', timeout=40)

    @optional('electricity')
    def electricity(self):
        self.needs('utilities')
        self.choose('电费')
        self.content_wait(lambda: self.visible('选择缴费单位'), '缴费单位列表未加载')

    @optional('electricity')
    def first_provider(self):
        self.needs('utilities', 'electricity')
        self.await_text('选择缴费单位')
        rows = [r for r in self.screen() if .2 < r['y'] < .85 and r['x'] < .6
                and any(word in r['text'] for word in ('电费', '电网', '电力', '能源'))]
        if not rows:
            raise WeixinStepSkipped('未识别到电费缴费单位')
        row = rows[0]
        self._locators.add(row['source'])
        self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
        self.content_wait(lambda: self.visible('缴费户号', True), '电费户号填写页未加载')
        if '电网' not in row['text']:
            self.adapt('当前城市第一项为“{}”，替代表中的电网公司；不输入户号'.format(row['text']))

    def favorites(self):
        self.me()
        self.choose('收藏')
        self.await_text('收藏', region=(.2, .05, .8, .12))

    @optional('red-packet')
    def red_packet_preview(self):
        self.require_test_chat()
        self.choose('红包')
        self.content_wait(lambda: self.visible('红包个数') or self.visible('塞钱进红包')
                          or self.visible('单个金额') or self.visible('金额'), '红包编辑页未加载')
        self.back()
        self.wait_for(self.chat_ready, '未返回测试聊天')
        self._panel_open = False

    @optional('transfer')
    def transfer(self):
        self.require_test_chat()
        self.choose('转账')
        self.content_wait(lambda: self.visible('添加转账说明', True), '转账编辑页未加载')

    @optional('transfer-memo')
    def transfer_memo(self):
        self.needs('transfer')
        self.choose('添加转账说明', True)
        self.await_text('确定')

    @optional('transfer-memo')
    def edit_memo(self):
        self.needs('transfer', 'transfer-memo')
        self.await_text('确定')
        self.input_text('修改')
        self.await_text('修改')

    @optional('transfer-memo')
    def confirm_memo(self):
        self.needs('transfer', 'transfer-memo')
        self.await_text('修改')
        self.choose('确定')
        self.content_wait(lambda: self.visible('修改', True, (.04, .36, .8, .55))
                          and not self.visible('确定'), '转账说明未保存到编辑页')

    def return_test_chat(self):
        self.needs('test-chat')
        self.return_to(self.chat_ready, '未返回测试聊天', limit=8)
        self._panel_open = False

    def browse_test_chat(self):
        self.require_test_chat()
        self.browse(0, 3)

    @optional('tencent-card')
    def tencent_card(self):
        self.needs('official-list')
        self.find_official(('腾讯新闻',))
        self.await_text('腾讯新闻', region=(0, .1, 1, .35))

    @optional('cctv')
    def cctv_card(self):
        self.needs('official-list')
        self.find_official(('央视新闻',))
        self.await_text('央视新闻', region=(0, .1, 1, .35))

    def cctv_ready(self):
        return (self.visible('央视新闻', region=(.2, .05, .8, .12))
                and self.visible('夜读', True, (0, .89, 1, .98)))

    def cctv_thread(self):
        self.needs('cctv')
        if self.cctv_ready():
            return
        if self.visible('私信') and self.visible('央视新闻', region=(0, .1, 1, .35)):
            self.choose('私信')
        else:
            self.return_to(self.cctv_ready, '未返回央视新闻对话界面', limit=8)
        self.wait_for(self.cctv_ready, '央视新闻对话界面未打开')

    @optional('culture')
    def culture_menu(self):
        self.cctv_thread()
        if self.visible('文博日历', True, (0, .89, 1, .98)):
            self.choose('文博日历', True, (0, .89, 1, .98))
        elif self.visible('打卡笔记', True, (0, .89, 1, .98)):
            self.choose('打卡笔记', True, (0, .89, 1, .98))
            self.adapt('当前菜单“打卡笔记”替代旧版“文博日历”')
        else:
            raise WeixinStepSkipped('央视新闻没有文博日历或打卡笔记菜单')
        self.web_content('文博/打卡页面未加载')

    def web_content(self, message):
        self.content_wait(lambda: self.activity_is('WebView', 'UIPageFragmentActivity')
                          and any(.13 < r['y'] < .88 and len(r['text']) >= 4 for r in self.screen()), message)
        if any(self.visible(word, True) for word in ('无法打开', '停止访问', '已删除', '页面不存在')):
            raise WeixinStepSkipped(message + '；链接已失效或不可访问')

    @optional('culture')
    def browse_culture(self):
        self.needs('culture')
        self.web_content('主题页面不可用')
        self.browse(2, 2)

    @optional('cctv')
    def return_cctv(self):
        self.cctv_thread()

    @optional('night')
    def night_menu(self):
        self.cctv_thread()
        self.choose('夜读', True, (0, .89, 1, .98))
        # 夜读有时先弹出子菜单；从可见菜单中选择夜读主题。
        time.sleep(.7)
        if self.cctv_ready():
            rows = self.find('夜读', True, (0, .5, 1, .89))
            if not rows:
                raise WeixinStepSkipped('夜读子菜单没有可识别的主题')
            row = rows[0]
            self._locators.add(row['source'])
            self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
        self.web_content('夜读详情页未加载')

    @optional('subscriptions')
    def subscriptions(self):
        self.wechat_home()
        for _ in range(5):
            for label in ('订阅号消息', '订阅号', '公众号'):
                if self.visible(label, region=(.12, .11, .9, .92)):
                    self.choose(label, region=(.12, .11, .9, .92))
                    self.content_wait(lambda: not self.main_ready() and (
                        self.visible('公众号', region=(.2, .05, .8, .12))
                        or self.visible('订阅号', True, (.2, .05, .8, .12))), '订阅号内容未加载')
                    if label == '公众号':
                        self.adapt('首页“公众号”替代旧版本“订阅号”聚合入口')
                    return
            self.swipe()
            time.sleep(.7)
        raise WeixinStepSkipped('首页未找到订阅号或公众号聚合入口')

    @optional('tencent-news')
    def tencent_news(self):
        self.needs('subscriptions')
        for _ in range(5):
            if self.visible('腾讯新闻', region=(0, .12, 1, .9)):
                self.choose('腾讯新闻', region=(0, .12, 1, .9), index=0)
                self.content_wait(lambda: self.visible('腾讯新闻', True, (0, .05, 1, .35))
                                  and not self.visible('公众号', region=(.2, .05, .8, .12)),
                                  '腾讯新闻页面未打开')
                return
            self.swipe()
            time.sleep(.7)
        # 账号未出现在当前订阅信息流时，沿用通讯录中已关注的同一个公众号。
        self.return_official()
        self.tencent_card()
        self.adapt('当前订阅信息流未展示腾讯新闻，改从已关注公众号进入腾讯新闻资料/文章页')

    @optional('tencent-news')
    def browse_tencent(self):
        self.needs('subscriptions', 'tencent-news')
        if self.main_ready():
            raise WeixinStepSkipped('腾讯新闻内容页不可用')
        self.browse(0, 3)


class WeixinRemainingCase(WeixinExtendedCase):
    @optional('mini-list')
    def recent_programs(self):
        self.wechat_home()
        for _ in range(2):
            self.swipe(.5, .18, .5, .85, 600)
            time.sleep(.8)
            if self.visible('最近使用', True):
                return
        self.discover()
        self.choose('小程序', region=(0, .12, 1, .9))
        self.content_wait(lambda: self.visible('最近使用', True), '小程序最近使用列表未加载')
        self.adapt('首页下拉未显示最近小程序，改从发现→小程序进入最近使用列表')

    def program_ready(self):
        return self.activity_is('AppBrandUI') and not self.activity_is('AppBrandPluginUI')

    def open_program(self, names):
        self.needs('mini-list')
        # 先查最近使用和我的常用；若缺失，再展开完整最近列表。
        for attempt in range(5):
            for name in names:
                rows = self.find(name, True, (0, .18, 1, .9))
                if rows:
                    row = rows[0]
                    self._locators.add(row['source'])
                    def open_row():
                        self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
                    self.transition(open_row, self.program_ready, '小程序未打开：' + names[0])
                    self._program = names[0]
                    return
            if attempt == 0 and self.visible('最近使用', True):
                self.choose('最近使用', True, index=0)
            else:
                self.swipe()
            time.sleep(.8)
        raise WeixinStepSkipped('最近小程序中没有“{}”，不选用其他商户替代'.format('/'.join(names)))

    def program_content(self, key, labels):
        self.needs(key)
        self.content_wait(lambda: self.program_ready() and any(self.visible(s, True) for s in labels),
                          '小程序内容未加载：' + '/'.join(labels), timeout=35)
        if any(self.visible(s, True) for s in ('同意并', '授权登录', '允许获取', '获取你的', '隐私保护指引')):
            raise WeixinStepSkipped('当前小程序要求登录、授权或协议确认，停在提示页')

    @optional('heytea')
    def heytea(self):
        self.open_program(('喜茶GO', '喜茶'))
        self.program_content('heytea', ('到店取', '门店自取', '到店自取'))

    @optional('heytea-menu')
    def heytea_menu(self):
        self.needs('heytea')
        for label in ('到店取', '门店自取', '到店自取'):
            if self.visible(label, True):
                self.choose(label, True, index=0)
                if label != '到店取':
                    self.adapt('当前入口“{}”替代表中“到店取”'.format(label))
                break
        else:
            raise WeixinStepSkipped('喜茶没有到店取入口')
        self.program_content('heytea', ('时令上新', '推荐榜', '商品', '热销', '人气', '菜单', '当前门店已休息'))
        if self.visible('当前门店已休息'):
            self.adapt('当前门店已休息，继续只读浏览菜单，不修改门店或下单')

    @optional('heytea-menu')
    def browse_heytea(self):
        self.needs('heytea', 'heytea-menu')
        self.program_content('heytea', ('门店', '商品', '菜单', '人气'))
        # 向下浏览内容用上滑手势，再反向回到起始区域。
        self.browse(3, 3)
        self.adapt('按三次反向滑动回到起始区域；自绘列表不导出滚动位置，不能断言已到顶部')

    @optional('meituan')
    def meituan(self):
        self.open_program(('美团',))
        self.program_content('meituan', ('外卖', '美食', '酒店', '美团'))

    @optional('meituan')
    def browse_meituan(self):
        self.program_content('meituan', ('外卖', '美食', '酒店', '美团'))
        self.browse(3, 3)

    @optional('mixue')
    def mixue(self):
        self.open_program(('蜜雪冰城',))
        self.program_content('mixue', ('点餐', '点单', '门店自取', '到店自取', '更快更优惠'))

    @optional('mixue-menu')
    def mixue_menu(self):
        self.needs('mixue')
        self.dismiss_mixue_ad()
        for label in ('点餐', '点单', '门店自取', '到店自取', '更快更优惠'):
            if self.visible(label, True):
                self.choose(label, True, index=0)
                if label != '点餐':
                    self.adapt('当前“{}”替代旧版“点餐”入口'.format(label))
                break
        else:
            raise WeixinStepSkipped('蜜雪冰城没有点餐入口')
        self.program_content('mixue', ('菜单', '商品', '选择门店', '附近门店', '热销', '冰淇淋'))

    def dismiss_mixue_ad(self):
        if self.visible('邀请好友', True) and self.visible('立即邀请', True):
            buttons = self.nodes(desc='关闭')
            if len(buttons) == 1:
                self.click_node(buttons[0])
            else:
                # 已核对“邀请好友得85折券”弹窗，下方圆形 X，不点击邀请按钮。
                self.pct(.5, .742)
            self.content_wait(lambda: not self.visible('得85折券', True)
                              and self.visible('更快更优惠'), '蜜雪广告弹窗未关闭')

    @optional('mixue-menu')
    def browse_mixue(self):
        self.needs('mixue', 'mixue-menu')
        self.dismiss_mixue_ad()
        self.program_content('mixue', ('菜单', '商品', '门店', '冰淇淋'))
        self.browse(3, 3)

    @optional('jd')
    def jd(self):
        self.open_program(('京东购物', '京东'))
        self.program_content('jd', ('京东', '百亿补贴', '购物车', '秒杀'))

    @optional('jd')
    def browse_jd(self):
        self.program_content('jd', ('京东', '购物车', '秒杀'))
        self.browse(3, 3)

    @optional('tongcheng')
    def tongcheng(self):
        self.open_program(('同程旅行',))
        self.program_content('tongcheng', ('火车票', '火车', '机票', '酒店'))

    @optional('train')
    def train(self):
        self.needs('tongcheng')
        if self.visible('火车票查询') and self.departure_date_rows():
            self.adapt('当前同程首页已内置火车票表单，直接浏览该栏目，替代旧版独立火车票页')
        elif self.visible('火车票'):
            self.choose('火车票', index=0)
        elif self.visible('火车'):
            self.choose('火车', index=0)
        else:
            raise WeixinStepSkipped('同程没有火车票表单或入口')
        self.program_content('tongcheng', ('查询', '出发', '到达'))

    def departure_date_rows(self):
        return [r for r in self.screen() if .2 < r['y'] < .85 and r['x'] < .6
                and re.search(r'\d{1,2}月\d{1,2}日', r['text'])]

    @optional('train')
    def browse_train(self):
        self.needs('train')
        self.program_content('tongcheng', ('查询', '出发', '到达'))
        self.browse(3, 3)

    @optional('train-date')
    def train_date(self):
        self.needs('tongcheng', 'train')
        if self.visible('更多日期', True):
            self.choose('更多日期', True)
        else:
            rows = self.departure_date_rows()
            if len(rows) != 1:
                raise WeixinStepSkipped('没有更多日期入口，也未识别到唯一出发日期行')
            row = rows[0]
            self._locators.add(row['source'])
            self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
            self.adapt('点击当前出发日期行，替代旧版右上角“更多日期”')
        self.content_wait(lambda: self.visible('选择日期', True) or self.visible('出发日期', True)
                          or self.visible('日历'), '火车票日期页未打开')

    @optional('train')
    def return_train(self):
        self.needs('tongcheng', 'train')
        self.return_to(lambda: self.visible('查询', True) and self.program_ready(), '未返回火车票页')

    @optional('tongcheng')
    def return_tongcheng(self):
        self.needs('tongcheng')
        self.return_to(lambda: self.visible('酒店') and self.visible('机票'), '未返回同程首页')

    @optional('chat-album')
    def chat_album(self):
        self.require_test_chat()
        self._album_origin_verified = False
        label = '照片' if self.visible('照片') else '相册'
        self.choose(label)
        self.await_text('预览', True, region=(0, .85, .4, 1))
        self.pct(.5, .083)
        self.await_text(self.ALBUM, True)
        self.choose(self.ALBUM, True)
        self.await_text(self.ALBUM, region=(.1, .05, .9, .12))
        self._album_origin_verified = True
        self._album_selected = 0
        self.adapt('仅浏览专用“{}”生成图片；不选个人照片'.format(self.ALBUM))

    def require_fixture_album(self):
        self.needs('test-chat', 'chat-album')
        if (not getattr(self, '_album_origin_verified', False)
                or getattr(self, '_verified_chat', None) != self.TEST_CONTACT
                or not self.visible(self.ALBUM, region=(.1, .05, .9, .12))):
            raise WeixinStepSkipped('未核对授权会话来源和专用测试相册')

    @optional('chat-album')
    def browse_chat_album(self):
        self.require_fixture_album()
        self.browse(3, 3)

    def fixture_grid_top(self):
        width, height = self.d.window_size()
        header = self.find(self.ALBUM, region=(.1, .05, .9, .12))[0]
        return (header['y']+header['h'])*height + width*.035

    @optional('chat-album-selection')
    def select_chat_photos(self):
        self.require_fixture_album()
        width, height = self.d.window_size()
        top = self.fixture_grid_top()
        for col in range(3):
            self.pct((col+.87)/4, (top+width*.03)/height)
        self.await_text('发送3', True, region=(.65, .85, 1, 1))
        self._album_selected = 3
        self.adapt('“多张图片”具体选取三张生成的测试图片')

    @optional('chat-album-selection')
    def send_chat_photos(self):
        self.needs('chat-album', 'chat-album-selection')
        self.require_fixture_album()
        if not self.ALLOW_SEND or self._album_selected != 3 or getattr(self, '_chat', None) != self.TEST_CONTACT:
            raise RuntimeError('测试相册发送前接收人或选图数量校验失败')
        self.require_delivery()
        self.choose('发送3', True, region=(.65, .85, 1, 1))
        # 实发按钮只点一次，页面未返回时停止，不重复发送。
        self.wait_for(lambda: self.chat_ready(self.TEST_CONTACT), '发送照片后未返回授权会话')
        self._album_origin_verified = False
        self._album_selected = 0
        self.require_delivery()

    @optional('chat-album')
    def first_chat_photo(self):
        self.require_fixture_album()
        width, height = self.d.window_size()
        self.pct(.125, (self.fixture_grid_top()+width*.125)/height)
        time.sleep(.7)
        if not self.activity_is('ImagePreviewUI') and self.visible('预览1', True, (0, .85, .4, 1)):
            self.choose('预览1', True, (0, .85, .4, 1))
            self._album_selected = 1
            self.adapt('当前相册点击缩略图先选中，通过“预览(1)”查看第一张大图，不发送该图')
        self.wait_for(lambda: self.activity_is('ImagePreviewUI') and self.visible('发送', True), '未进入照片大图')

    @optional('favorites')
    def favorites_page(self):
        self.favorites()

    @optional('favorites')
    def browse_favorites(self):
        self.needs('favorites')
        self.await_text('收藏', region=(.2, .05, .8, .12))
        self.browse(3, 3)

    @optional('favorite-detail')
    def first_favorite(self):
        self.needs('favorites')
        self.await_text('收藏', region=(.2, .05, .8, .12))
        if self.visible('暂无收藏', True) or self.visible('没有收藏', True):
            raise WeixinStepSkipped('当前收藏为空，没有第一条内容')
        rows = [r for r in self.screen() if .18 < r['y'] < .8 and len(r['text']) >= 3
                and not any(s in r['text'] for s in ('搜索', '图片与视频', '链接', '文件', '音乐', '聊天记录', '标签'))]
        if not rows:
            raise WeixinStepSkipped('收藏列表没有可识别的内容标题')
        row = rows[0]
        self._locators.add(row['source'])
        self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
        self.wait_for(lambda: not self.activity_is('FavIndexUI'), '第一条收藏未打开')

    @optional('settings')
    def settings(self):
        self.me()
        self.choose('设置', True, region=(0, .15, .8, .9))
        self.await_text('通用')

    @optional('general')
    def general(self):
        self.needs('settings')
        self.choose('通用')
        self.await_text('存储空间')

    @optional('storage')
    def storage(self):
        self.needs('settings', 'general')
        self.choose('存储空间')
        self.content_wait(lambda: self.visible('存储空间', True) and (
            self.visible('缓存', True) or self.visible('聊天记录', True)), '存储空间统计未加载', timeout=45)
