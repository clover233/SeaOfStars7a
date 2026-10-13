"""小米相机动态场景；实机控件、比例变焦及拍摄结果校验。"""
import logging
from pathlib import Path
import re
import time
import xml.etree.ElementTree as ET

from Cases.Top48.baidu_common import BaiduDynamicCase


class CameraDynamicCase(BaiduDynamicCase):
    PACKAGE = 'com.android.camera'
    GALLERY = 'com.miui.gallery'
    all_app_package_list = [PACKAGE]
    PERMISSIONS = ('CAMERA', 'RECORD_AUDIO')
    ALLOW_UNSUPPORTED = True

    def shell(self, command):
        result = self.d.shell(command)
        if result.exit_code:
            raise RuntimeError('设备命令失败：{} {}'.format(command, result.output))
        return result.output

    def current_app(self):
        # 折叠屏副屏可能持有输入焦点；只按主屏 Display #0 判断本用例页面。
        output = self.d.shell('dumpsys activity activities').output
        match = re.search(r'Display #0 \(activities from top to bottom\):([\s\S]*?)(?=\n\s*Display #\d+|\Z)', output)
        if match:
            activity = re.search(r'topResumedActivity=ActivityRecord\{[^\n]*?\su\d+\s+([\w.]+)/([\w.$]+)', match.group(1))
            if activity:
                return {'package': activity.group(1), 'activity': activity.group(2)}
        return super().current_app()

    def foreground(self):
        current = self.current_app()
        if current['package'] not in (self.PACKAGE, self.GALLERY, 'com.miui.voiceassist'):
            raise RuntimeError('前台不在相机流程中：{}'.format(current))

    def nodes(self, rid=None, package=None, **selector):
        package = package or self.PACKAGE
        if rid:
            selector['resource-id'] = rid if ':' in rid else package+':id/'+rid
        return [n for n in ET.fromstring(self.d.dump_hierarchy()).iter('node')
                if n.get('package') == package and n.get('display-id', '0') == '0'
                and n.get('visible-to-user') != 'false'
                and all(n.get(k) == v for k, v in selector.items())]

    def has(self, rid=None, **selector):
        return bool(self.nodes(rid, **selector))

    @staticmethod
    def bounds(node):
        return tuple(map(int, re.findall(r'-?\d+', node.get('bounds'))))

    def click_point(self, x, y):
        self.foreground()
        self.shell('input -d 0 swipe {0} {1} {0} {1} 100'.format(round(x), round(y)))

    def click_node(self, node):
        l, t, r, b = self.bounds(node)
        self.click_point((l+r)/2, (t+b)/2)

    def click(self, rid=None, **selector):
        ns = self.nodes(rid, **selector)
        if len(ns) != 1:
            raise RuntimeError('控件不存在或不唯一：{}'.format((rid, selector)))
        self.click_node(ns[0])

    def swipe(self, x1, y1, x2, y2, duration=400):
        self.foreground()
        w, h = self.d.window_size()
        self.shell('input -d 0 swipe {} {} {} {} {}'.format(
            round(w*x1), round(h*y1), round(w*x2), round(h*y2), duration))

    def skip(self, reason, optional=False):
        if not optional and not self.ALLOW_UNSUPPORTED:
            raise RuntimeError(reason)
        logging.warning('设备不支持，跳过：%s', reason)
        if not hasattr(self, 'skipped_steps'):
            self.skipped_steps = []
        self.skipped_steps.append(reason)
        with (Path(self.result_dir_path)/'skipped_steps.txt').open('a', encoding='utf-8') as report:
            report.write(reason+'\n')

    def preview(self):
        return self.has('shutter_button') and self.has('mode_select_view')

    def return_preview(self):
        for _ in range(6):
            if self.preview():
                return
            self.foreground()
            self.shell('input -d 0 keyevent 4')
            time.sleep(.7)
        self.wait_for(self.preview, '未返回相机预览')

    def mode(self, title):
        self.return_preview()
        self.transition(lambda: self.click('mode_select_item', text=title),
                        lambda: self.has('mode_select_view', **{'content-desc': title}),
                        '未切换相机模式：'+title)
        time.sleep(.7)

    def launch(self):
        self.d.app_start(self.PACKAGE, use_monkey=True)
        self.wait_for(lambda: self.current_app()['package'] == self.PACKAGE, '相机未启动')
        time.sleep(1)
        self.return_preview()
        self.mode('拍照')
        if self.has('v9_camera_picker', **{'content-desc': '前后置切换,前置'}):
            self.switch_camera('后置')
        self.zoom(1)

    def zoom_value(self):
        tips = self.nodes('zoom_panel_tip_text')
        if tips and re.fullmatch(r'\d+(\.\d+)?', tips[0].get('content-desc', '')):
            self._last_zoom = float(tips[0].get('content-desc'))
            return self._last_zoom
        ns = self.nodes('zoom_toggle_button')
        if ns:
            match = re.match(r'([\d.]+)倍变焦', ns[0].get('content-desc', ''))
            if match:
                self._last_zoom = float(match.group(1))
                return self._last_zoom
        # 转盘刚展开、尚未拖动时不显示倍率提示，保留展开前已校验的值。
        if self.has('zoom_panel') and hasattr(self, '_last_zoom'):
            return self._last_zoom
        raise RuntimeError('无法读取当前变焦倍率')

    def zoom(self, target):
        # 先定位镜头预设，任意数字倍率由转盘小步调节并读取实际倍率闭环校验。
        choices = []
        for n in self.nodes():
            match = re.fullmatch(r'([\d.]+)倍变焦', n.get('content-desc', ''))
            if match and n.get('clickable') == 'true':
                choices.append((float(match.group(1)), n))
        if not choices:
            raise RuntimeError('变焦预设不可定位')
        _, nearest = min(choices, key=lambda item: abs(item[0]-target))
        self.click_node(nearest)
        time.sleep(.8)
        if abs(self.zoom_value()-target) < .05:
            if self.has('zoom_panel'):
                self.relative_click(.5, .45)
                self.wait_for(lambda: not self.has('zoom_panel'), '变焦转盘未收起')
            return
        for _ in range(16):
            if not self.has('zoom_panel'):
                n = self.nodes('zoom_toggle_button')[0]
                l, t, r, b = self.bounds(n)
                x, y = round((l+r)/2), round((t+b)/2)
                self.shell('input -d 0 swipe {0} {1} {0} {1} 700'.format(x, y))
                time.sleep(.4)
            current = self.zoom_value()
            if abs(current-target) < .05:
                break
            n = self.nodes('zoom_panel')[0]
            l, t, r, b = self.bounds(n)
            w, _ = self.d.window_size()
            # 转盘左拖放大，右拖缩小；步长按屏宽换算，最小步长也随分辨率缩放。
            delta = max(.002, min(.12, abs(target-current)/max(current, 1)*.20))
            direction = -1 if target > current else 1
            x, y = round(w*.55), round(t+(b-t)*.55)
            self.shell('input -d 0 swipe {} {} {} {} 300'.format(x, y, round(x+direction*w*delta), y))
            time.sleep(.6)
        else:
            raise RuntimeError('未能精确调节到{}X，当前{}X'.format(target, self.zoom_value()))
        self.relative_click(.5, .45)
        self.wait_for(lambda: self.has('zoom_toggle_button') and abs(self.zoom_value()-target) < .05,
                      '变焦倍率未保持在{}X'.format(target))

    def media_files(self, video=False):
        suffix = ('.mp4',) if video else ('.jpg', '.jpeg', '.heic', '.heif')
        return {f for f in self.shell('ls -1 /sdcard/DCIM/Camera').splitlines()
                if f.lower().endswith(suffix)}

    def photograph(self):
        if not self.has('mode_select_view', **{'content-desc': '拍照'}):
            raise RuntimeError('当前不是拍照模式')
        before = self.media_files()
        self.click('shutter_button')
        self.wait_for(lambda: bool(self.media_files()-before), '拍照后没有新增照片', timeout=20)
        time.sleep(.8)

    def zoom_photo(self, target):
        self.zoom(target)
        self.photograph()

    def five_photos(self):
        for _ in range(5):
            self.relative_click(.5, .45)
            self.photograph()

    def open_menu(self):
        self.transition(lambda: self.click('menu_indicator'),
                        lambda: self.has('menu_indicator', **{'content-desc': '功能菜单：展开'})
                        and self.has('extra_tootle_item_text', text='设置'),
                        '未展开相机功能菜单')

    def settings(self):
        self.open_menu()
        self.click('extra_tootle_item_text', text='设置')
        self.wait_for(lambda: self.has('android:id/text1', text='通用'), '未进入相机设置')
        self.click('android:id/text1', text='拍照')

    def browse(self, up=1, down=1):
        for count, start, end in ((up, .78, .32), (down, .32, .78)):
            for _ in range(count):
                self.swipe(.5, start, .5, end)
                time.sleep(1)

    def browse_settings(self):
        for _ in range(3):
            self.browse()

    def find_setting(self, title):
        for _ in range(6):
            if self.has('android:id/title', text=title):
                self.click('android:id/title', text=title)
                return True
            self.browse(up=1, down=0)
        return False

    def photo_ratio(self):
        # 此版MIUI把“照片比例”放在预览菜单的“画幅”，不是设置列表。
        self.return_preview()
        self.open_menu()
        self.click('extra_tootle_item_text', text='画幅')
        self.wait_for(lambda: self.has(text='3:4') or self.has(text='9:16')
                      or self.has(**{'content-desc': '画幅三比四'}), '未打开画幅选项')

    def cancel_ratio(self):
        self.shell('input -d 0 keyevent 4')
        time.sleep(.6)
        self.return_preview()
        self.settings()

    def photo_format(self):
        if not self.find_setting('照片格式'):
            raise RuntimeError('没有照片格式设置')
        self.wait_for(lambda: self.has('android:id/title', text='HEIF'), '未打开照片格式选项')

    def cancel_format(self):
        self.shell('input -d 0 keyevent 4')
        self.wait_for(lambda: self.has('android:id/text1', text='拍照'), '未返回相机设置')

    def voice_shutter(self):
        # 扫描拍照/通用分类；设备缺失时明确记录，不把其它拍摄功能冒充声控。
        self._voice_open = False
        for category in ('拍照', '通用'):
            self.click('android:id/text1', text=category)
            self.browse(up=0, down=5)
            if self.find_setting('声控拍照'):
                self._voice_open = True
                return
        self.skip('当前小米相机没有声控拍照设置')

    def cancel_voice(self):
        if self._voice_open:
            self.shell('input -d 0 keyevent 4')
        else:
            self.skip('没有声控拍照弹框可取消')

    def side_to_preview(self):
        self.swipe(.005, .5, .4, .5, 250)
        time.sleep(.6)
        self.return_preview()

    def visual(self):
        self._visual_open = False
        entries = self.nodes(text='小艺视觉')
        if entries:
            self.click_node(entries[0])
            self._visual_open = True
        else:
            self.skip('没有小艺视觉入口', optional=True)

    def visual_photo(self):
        if self._visual_open:
            self.click(**{'content-desc': '拍照'})
        else:
            self.skip('小艺视觉不可用，其拍照步骤不执行', optional=True)

    def visual_back(self):
        if self._visual_open:
            self.swipe(.005, .5, .4, .5, 250)
        else:
            self.skip('小艺视觉不可用，无扫一扫页面可返回', optional=True)

    def visual_gallery(self):
        self._visual_gallery_open = False
        if self._visual_open and self.has(**{'content-desc': '图库'}):
            self.click(**{'content-desc': '图库'})
            self._visual_gallery_open = True
        else:
            self.skip('扫一扫图库入口不可用', optional=True)

    def browse_visual_gallery(self):
        if self._visual_gallery_open:
            self.browse(up=3, down=3)
        else:
            self.skip('扫一扫图库不可用，跳过图库浏览', optional=True)

    def visual_gallery_back(self):
        if self._visual_gallery_open:
            self.swipe(.005, .5, .4, .5, 250)
        else:
            self.skip('扫一扫图库不可用，无图库页面可返回', optional=True)

    def gallery(self):
        self.click('v9_thumbnail_image')
        self.wait_for(lambda: self.current_app()['package'] == self.GALLERY, '未进入照片/视频预览')
        time.sleep(1)

    def browse_photos(self):
        if self.current_app()['package'] != self.GALLERY:
            raise RuntimeError('不在图库预览')
        for _ in range(8):
            self.swipe(.80, .5, .20, .5)
            time.sleep(1)

    def switch_camera(self, target):
        self.transition(lambda: self.click('v9_camera_picker'),
                        lambda: self.has('v9_camera_picker', **{'content-desc': '前后置切换,'+target}),
                        '未切换到'+target)
        time.sleep(.7)

    def video_config(self, zoom, fps):
        self.zoom(zoom)
        for prefix, expected in (('分辨率,', '1080P'), ('帧率,', str(fps)+'FPS')):
            for _ in range(5):
                ns = [n for n in self.nodes() if n.get('content-desc', '').startswith(prefix)]
                if len(ns) != 1:
                    raise RuntimeError('录像参数控件不可定位：'+prefix)
                if ns[0].get('content-desc') == prefix+expected:
                    break
                self.click_node(ns[0])
                time.sleep(.7)
            else:
                raise RuntimeError('未设置录像参数：'+expected)

    def start_recording(self):
        if not self.has('mode_select_view', **{'content-desc': '录像'}):
            raise RuntimeError('不在录像模式')
        self._videos_before = self.media_files(video=True)
        self._own_recording = True
        self.click('shutter_button')
        self.wait_for(lambda: self.has('alert_recording_time_view'), '录像未开始')

    def stop_after_ten(self):
        def ten_seconds():
            ns = self.nodes('alert_recording_time_view')
            if not ns:
                raise RuntimeError('录像已意外结束')
            parts = ns[0].get('text', '').split(':')
            return len(parts) == 2 and all(p.isdigit() for p in parts) and int(parts[0])*60+int(parts[1]) >= 10
        self.wait_for(ten_seconds, '录像计时未达到10秒', timeout=15)
        self.click('shutter_button')
        self.wait_for(lambda: not self.has('alert_recording_time_view'), '录像未停止')
        self._own_recording = False
        self.wait_for(lambda: bool(self.media_files(video=True)-self._videos_before), '录像未保存')
        time.sleep(1)

    def play_video(self):
        def controls():
            return self.has(package=self.GALLERY, **{'content-desc': '暂停播放'}) or self.has(
                package=self.GALLERY, **{'content-desc': '播放视频'})
        self.transition(lambda: self.relative_click(.5, .45), controls, '图库未显示播放控件')
        # 新版图库自动播放，先暂停再点击播放，仍执行表格要求的播放按钮操作。
        if self.has(package=self.GALLERY, **{'content-desc': '暂停播放'}):
            self.click(package=self.GALLERY, **{'content-desc': '暂停播放'})
        self.wait_for(lambda: self.has(package=self.GALLERY, **{'content-desc': '播放视频'}),
                      '图库视频没有播放控件')
        self.click(package=self.GALLERY, **{'content-desc': '播放视频'})
        self.wait_for(lambda: self.has(package=self.GALLERY, **{'content-desc': '暂停播放'}), '视频未播放')

    def swipe_photo_mode(self):
        self.swipe(.25, .5, .75, .5)
        time.sleep(.7)
        # MIUI模式顺序与模型表不同，执行右滑后用命名控件确保落在拍照模式。
        if not self.has('mode_select_view', **{'content-desc': '拍照'}):
            self.mode('拍照')

    def open_ai(self):
        self.return_preview()
        self.mode('AI帮拍')
        if self.has(text='“AI帮拍模式”服务确认'):
            raise RuntimeError('AI帮拍首次服务协议尚未同意，请由用户确认后重试')
        if self.has(text='尝试AI'):
            self.click(text='尝试AI')
        else:
            # 本机 AI帮拍只有构图指导。通过小爱公开的 mainpage 链接继续提问。
            self.shell('am start --display 0 -a android.intent.action.VIEW '
                       '-d xiaoai://mainpage -p com.miui.voiceassist')
        self.wait_for(lambda: self.current_app()['package'] == 'com.miui.voiceassist',
                      '未唤起小爱同学')
        if self.has(package='com.miui.voiceassist', text='应用收藏自动同步'):
            self.click('android:id/button2', package='com.miui.voiceassist', text='暂不开启')
        self.wait_for(lambda: self.has('input_asr_text_view', package='com.miui.voiceassist')
                      or self.has('et_min_input', package='com.miui.voiceassist'),
                      '小爱没有显示对话输入区')

    def ask_ai(self):
        assistant = 'com.miui.voiceassist'
        question = '我要拍夕阳应该怎么拍'
        if self.has('input_asr_text_view', package=assistant):
            self.transition(lambda: self.click('input_asr_text_view', package=assistant),
                            lambda: self.has('et_min_input', package=assistant),
                            '小爱文字输入框未打开')
        self.wait_for(lambda: self.has('et_min_input', package=assistant),
                      '小爱文字输入框未打开')
        self.d(resourceId=assistant+':id/et_min_input').set_text(question)
        self.wait_for(lambda: self.has('et_min_input', package=assistant, text=question)
                      and self.has('btn_text_send', package=assistant, **{'content-desc': '发送'}),
                      '小爱未正确填入问题')
        # AdbKeyboard 会盖住屏幕底部的发送键；先收起，再按该控件实时 bounds 点击。
        self.d.hide_keyboard()
        self.wait_for(lambda: 'mInputShown=false' in self.shell('dumpsys input_method'),
                      '输入法遮住小爱发送按钮')
        send = self.nodes('btn_text_send', package=assistant, **{'content-desc': '发送'})
        if len(send) != 1:
            raise RuntimeError('小爱发送按钮不可定位')
        l, t, r, b = self.bounds(send[0])
        x, y = round((l+r)/2), round((t+b)/2)
        self.shell('input -d 0 swipe {0} {1} {0} {1} 200'.format(x, y))
        # 发送后聊天记录会自动滚到回复底部，刚发出的提问气泡可能离开控件树。
        self.wait_for(lambda: self.has('input_asr_text_view', package=assistant)
                      and not self.has('et_min_input', package=assistant, text=question),
                      '小爱未发送夕阳摄影问题')

    def close_ai(self):
        time.sleep(10)
        self.return_preview()

    def launcher_gesture(self):
        self.transition(lambda: self.swipe(.5, .995, .5, .62, 250),
                        lambda: 'launcher' in self.current_app()['activity'].lower(), '上滑未返回桌面')

    def run_case(self):
        try:
            super().run_case()
        finally:
            # 性能采集或后续断言失败时，也结束本用例启动的录像。
            if getattr(self, '_own_recording', False):
                try:
                    if self.has('alert_recording_time_view'):
                        self.click('shutter_button')
                        self.wait_for(lambda: not self.has('alert_recording_time_view'), '清理录像失败')
                except Exception:
                    logging.exception('异常退出时停止录像失败')
                self._own_recording = False
