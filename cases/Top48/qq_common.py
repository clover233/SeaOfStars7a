"""QQ 9.3.70 实机控件；主屏输入、比例手势与逐步性能结果。"""
import json
import logging
import os
import time
import uuid

from Cases.Top48.dynamic_apps_common import DynamicAppCase
from aw_new import SeaOfStarsAW


class QQStepSkipped(Exception):
    pass


class QQDynamicBase(DynamicAppCase):
    def shell(self, command):
        result = self.d.shell(command)
        if result.exit_code or result.output.startswith('Unknown command:'):
            raise RuntimeError('设备命令失败：' + result.output)
        return result.output

    def point(self, x, y):
        self.foreground()
        self.shell('input mouse -d 0 tap {} {}'.format(round(x), round(y)))

    def swipe(self, x1=.5, y1=.78, x2=.5, y2=.32, duration=400):
        self.foreground()
        width, height = self.screen_size()
        self.shell('input mouse -d 0 swipe {} {} {} {} {}'.format(
            round(width*x1), round(height*y1), round(width*x2), round(height*y2), duration))

    def back(self):
        super().back()
        time.sleep(.5)

    def adapt(self, reason):
        self._adaptation = reason
        logging.info('适配替代：%s', reason)

    def choose(self, label):
        for kw in ({'text': label}, {'desc': label}):
            if self.has(**kw):
                self.click(**kw)
                return
        raise RuntimeError('未找到控件：' + label)

    def home(self):
        self.foreground()
        width, height = self.screen_size()
        self.shell('input touchscreen -d 0 swipe {} {} {} {} 300'.format(
            round(width*.5), round(height*.995), round(width*.5), round(height*.62)))
        time.sleep(1)
        if 'launcher' not in self.current_app()['activity'].lower():
            self.shell('input -d 0 keyevent 3')
            self.adapt('上滑未返回桌面，使用系统 Home 键替代')
        self.wait_for(lambda:'launcher' in self.current_app()['activity'].lower(), '未返回桌面')

    @SeaOfStarsAW.function_log
    def run_case(self):
        if not getattr(self, '_prepared', False):
            self.set_up()
        records = []
        for run in range(self.TEST_TIME):
            for number, (name, action, stay) in enumerate(self.steps(), 1):
                row = dict(run=run+1, step=number, name=name, status='PASS')
                self._adaptation = None
                logging.info('%s、%s', number, name)
                SeaOfStarsAW.start_perfetto_trace()
                try:
                    action()
                    time.sleep(stay)
                    if self._adaptation:
                        row.update(status='ADAPTED', reason=self._adaptation)
                except QQStepSkipped as error:
                    row.update(status='SKIP', reason=str(error))
                    logging.warning('SKIP %s：%s', name, error)
                except Exception as error:
                    row.update(status='FAIL', reason=str(error))
                    logging.exception('步骤失败：%s', name)
                    raise
                finally:
                    records.append(row)
                    with open(os.path.join(self.result_dir_path, 'step_results.json'), 'w', encoding='utf-8') as f:
                        json.dump(records, f, ensure_ascii=False, indent=2)
                    try:
                        SeaOfStarsAW.stop_and_get_perfetto_trace(
                            self.trace_dir_path, self.__class__.__name__,
                            'step_{}、{}_{}'.format(number, name, row['status']), '', self.screenshot_dir_path)
                    except Exception:
                        if row['status'] != 'FAIL':
                            raise
                        logging.exception('失败步骤 trace 导出失败')


class QQDynamicCase(QQDynamicBase):
    PACKAGE = 'com.tencent.mobileqq'
    all_app_package_list = [PACKAGE]
    NEED_TEST_IMAGE = False
    SEND_GROUP = '多媒体消息'
    # 用户已明确授权向“多媒体消息”发送文字、表情和专用测试图片。
    SEND_MESSAGES = True

    def set_up(self):
        super().set_up()
        from Cases.Top48.screen_text import ScreenshotText
        self._picture_text = ScreenshotText()
        if self.NEED_TEST_IMAGE:
            # 素材准备放在性能步骤之外，避免推图/扫描计入发送图片的采集区间。
            self.prepare_image()

    def main_ready(self):
        return self.has(rid='kbi', text='消息') and self.has(rid='ba1', desc='账户及设置')

    def message_ready(self):
        return self.main_ready() and self.has(rid='aua')

    def messages(self):
        self.return_to(self.main_ready, '未返回 QQ 主界面', limit=8)
        self.transition(lambda:self.click(rid='kbi', text='消息'), self.message_ready, '未切到消息列表')

    def launch(self):
        self._space_reason = None
        self._picture_reason = None
        self._send_reason = None
        self._draft_owned = None
        self.start()
        if self.has(text='登录') and not self.main_ready():
            raise RuntimeError('QQ 尚未登录，请先完成账号登录')
        self.messages()

    def dynamics(self):
        self.messages()
        self.transition(lambda:self.click(rid='kbi', text='动态'),
                        lambda:self.has(rid='letsTextView', text='空间动态'), 'QQ 动态页未打开')

    def space_ready(self):
        return self.has(rid='08k', desc='我的头像') or self.has(rid='znh', text='空间动态')

    def space(self):
        if not self.has(rid='letsTextView', text='空间动态'):
            self.dynamics()
        self.transition(lambda:self.click(rid='letsTextView', text='空间动态'),
                        self.space_ready, '空间动态未打开')

    def browse_space(self):
        if self._space_reason:
            raise QQStepSkipped(self._space_reason)
        if not self.space_ready():
            raise RuntimeError('不在空间动态页')
        self.browse(5, 5)

    def picture_ready(self):
        return self.has(rid='r90') or self.has(rid='1eh')

    def expired_picture(self):
        if self.has(text='图片已过期') or self.has(text='原图已过期'):
            return True
        return any('已过期' in row['text'] or '已被清理' in row['text']
                   for row in self._picture_text.read(self.d))

    def space_picture(self):
        for _ in range(7):
            pictures = [n for n in self.nodes(desc='图片第', prefix=True)
                        if self.bounds(n)[1] > self.screen_size()[1]*.13
                        and self.bounds(n)[3] < self.screen_size()[1]*.94]
            if pictures:
                self.transition(lambda:self.click_node(pictures[0]), self.picture_ready, '动态图片未打开')
                self.adapt('使用当前可见空间动态图片；当前实机素材为本人动态，替代好友动态图片')
                return
            self.swipe()
            time.sleep(1)
        self._space_reason = '空间动态中没有可浏览的图片'
        raise QQStepSkipped(self._space_reason)

    def slide_pictures(self, right=0, left=0, reason=None):
        if reason:
            raise QQStepSkipped(reason)
        if not self.picture_ready():
            raise RuntimeError('没有进入 QQ 图片大图')
        for count, start, end in ((right, .2, .8), (left, .8, .2)):
            for _ in range(count):
                self.swipe(start, .5, end, .5)
                time.sleep(1)
                if not self.picture_ready():
                    if self.expired_picture():
                        raise QQStepSkipped('群聊图片已过期，跳过剩余图片滑动；继续后续消息浏览')
                    raise RuntimeError('滑动图片后离开大图页')

    def space_slides(self):
        self.slide_pictures(left=3, reason=self._space_reason)

    def chat_ready(self, name):
        return self.has(rid='3kc', text=name) and self.has(rid='input')

    def open_chat(self, names, purpose):
        self.messages()
        for name in names:
            rows = [n for n in self.nodes(rid='aua')
                    if n.get('content-desc', '').split(',')[0] == name]
            if rows:
                self.transition(lambda:self.click_node(rows[0]), lambda:self.chat_ready(name),
                                '未进入群聊：' + name)
                if name != names[0]:
                    self.adapt('使用本机“{}”替代表中“{}”'.format(name, names[0]))
                return name
        reason = '当前消息列表没有{}：{}'.format(purpose, '/'.join(names))
        if purpose == '图片测试群':
            self._picture_reason = reason
        else:
            self._send_reason = reason
        raise QQStepSkipped(reason)

    def picture_chat(self):
        self._picture_group = self.open_chat(('测试图片群', '图片测试群'), '图片测试群')

    def browse_chat(self):
        if self._picture_reason:
            raise QQStepSkipped(self._picture_reason)
        if not self.chat_ready(self._picture_group):
            raise RuntimeError('不在图片测试群')
        self.browse(2, 2)

    def chat_pictures(self):
        if self._picture_reason:
            raise QQStepSkipped(self._picture_reason)
        pictures = self.nodes(rid='mkj', desc='图片')
        if not pictures:
            self._picture_reason = '图片测试群当前没有可见图片消息'
            raise QQStepSkipped(self._picture_reason)
        self.transition(lambda:self.click_node(pictures[0]), self.picture_ready, '群聊图片未打开')
        self.slide_pictures(right=4, left=4)

    def side_to_messages(self):
        self.foreground()
        width, height = self.screen_size()
        self.shell('input touchscreen -d 0 swipe {} {} {} {} 300'.format(
            round(width*.005), round(height*.5), round(width*.45), round(height*.5)))
        time.sleep(1)
        self.messages()

    def multimedia_chat(self):
        self.open_chat((self.SEND_GROUP,), '多媒体测试群')

    def send_guard(self):
        if self._send_reason:
            raise QQStepSkipped(self._send_reason)
        if not self.SEND_MESSAGES:
            raise QQStepSkipped('本次运行关闭了实发消息')
        if not self.chat_ready(self.SEND_GROUP):
            raise RuntimeError('发送目标不等于已授权的测试群：' + self.SEND_GROUP)

    def send_input(self, value):
        self.send_guard()
        previous = self.node(rid='input').get('text', '')
        if previous:
            raise QQStepSkipped('测试群输入框有未发送草稿，保留草稿并跳过本次发送')
        self._draft_owned = value
        self.d(resourceId=self.PACKAGE+':id/input').set_text(value)
        self.wait_for(lambda:self.has(rid='input', text=value), '消息内容未填入')
        self.send_guard()
        # 发送只点击一次，不能按导航重试逻辑重复发消息。
        self.click(rid='send_btn', text='发送')
        self.wait_for(lambda:self.has(rid='input', text='') and self.has(text=value),
                      '未确认发送成功，不自动重发', timeout=20)
        self._draft_owned = None

    def send_text(self):
        self.send_input('你好，动态')

    def send_emoji(self):
        # Unicode 表情属于文字输入，不依赖表情包商城，不会误发付费/第三方贴纸。
        self.send_input('☺')
        self.adapt('使用兼容当前输入法的 Unicode BMP 笑脸表情替代原生表情面板')

    def prepare_image(self):
        from PIL import Image, ImageDraw
        self._image_album = 'SeaOfStarsQQ_' + uuid.uuid4().hex
        self._image_name = self._image_album + '.png'
        self._image_local = os.path.join(self.result_dir_path, self._image_name)
        image = Image.new('RGB', (640, 480), '#dff1ff')
        draw = ImageDraw.Draw(image)
        draw.rectangle((40, 40, 600, 440), outline='#2465a0', width=6)
        draw.text((100, 220), 'SeaOfStars QQ dynamic test', fill='#163955')
        image.save(self._image_local)
        self._image_remote = '/sdcard/Pictures/{}/{}'.format(self._image_album, self._image_name)
        self.shell('mkdir -p /sdcard/Pictures/' + self._image_album)
        self.d.push(self._image_local, self._image_remote)
        self.shell('am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://' + self._image_remote)
        time.sleep(2)

    def send_image(self):
        self.send_guard()
        if not getattr(self, '_image_remote', None):
            raise RuntimeError('未准备专用测试图片，请先执行 set_up')
        # 唯一测试相册只含本次生成的测试图，不能从全部照片随机选取个人图片。
        self.transition(lambda:self.choose('相册'),
                        lambda:bool(self.album_picker_controls()), 'QQ 相册面板未打开')
        controls=self.album_picker_controls()
        self.click_node(controls[0])
        try:
            self.wait_for(lambda:self.has(text=self._image_album) or self.has(desc=self._image_album),
                          '列表未出现本次测试相册', timeout=8)
        except RuntimeError as error:
            self.back()
            raise QQStepSkipped('相册选择器未提供专用测试相册，未选择或发送个人图片：' + str(error))
        self.choose(self._image_album)
        self.wait_for(lambda:self.has(rid='xkh', text=self._image_album), '未进入专用测试相册')
        # 勾选框本身不可点击，但中心落在其可点击父容器内；仅在专用相册内选图。
        items=self.nodes(rid='xjs')
        boxes=[n for item in items for n in item.iter('node')
               if n.get('class')=='android.widget.CheckBox' and n.get('checkable')=='true']
        if len(items)!=1 or len(boxes)!=1:
            self.back()
            raise QQStepSkipped('未定位到唯一测试图片的勾选控件')
        self.click_node(boxes[0])
        self.wait_for(lambda:any(n.get('checked')=='true' for item in self.nodes(rid='xjs')
                                for n in item.iter('node') if n.get('checkable')=='true'),
                      '专用测试图片未勾选')
        sends=[n for n in self.nodes(rid='xka') if n.get('text','').startswith('发送')
               and ('1' in n.get('text','')) and n.get('enabled')=='true']
        if len(sends)!=1:
            raise RuntimeError('测试图未形成唯一的发送1张按钮，不发送')
        self.click_node(sends[0])
        self.wait_for(lambda:self.chat_ready(self.SEND_GROUP) and self.test_image_visible(),
                      '测试图片发送后未返回群聊，不自动重发', timeout=25)

    def album_picker_controls(self):
        return self.nodes(rid='xkb')

    def test_image_visible(self):
        # 检查新发的4:3蓝色测试图，不能以历史图片消息存在作为发送成功依据。
        candidates=[]
        for n in self.nodes(rid='mkj',desc='图片'):
            l,t,r,b=self.bounds(n)
            if abs((r-l)/(b-t)-640/480)<.12:
                candidates.append((l,t,r,b))
        if not candidates:
            return False
        screenshot=self.d.screenshot().convert('RGB')
        for l,t,r,b in candidates:
            if not (0<=l<r<=screenshot.width and 0<=t<b<=screenshot.height):
                continue
            sample=screenshot.getpixel((round(l+(r-l)*.12),round(t+(b-t)*.12)))
            if sum(abs(a-b) for a,b in zip(sample,(223,241,255)))<90:
                return True
        return False

    def clean_up(self):
        try:
            draft=getattr(self,'_draft_owned',None)
            if draft and self.chat_ready(self.SEND_GROUP) and self.has(rid='input',text=draft):
                self.d(resourceId=self.PACKAGE+':id/input').set_text('')
                logging.info('已清理本次测试未发送的草稿')
            remote=getattr(self,'_image_remote',None)
            if remote:
                self.shell('rm -f '+remote)
                self.d.shell('rmdir /sdcard/Pictures/'+self._image_album)
                self.shell('am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://'+remote)
        except Exception:
            logging.exception('测试素材清理未完成，保留原始用例错误')
        finally:
            super().clean_up()
