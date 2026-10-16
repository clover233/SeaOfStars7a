"""复用已验证的主屏控件/截图定位和逐步采集，提供跨应用页面导航。"""
import time
import xml.etree.ElementTree as ET

from Cases.Top48.weixin_common import WeixinStepSkipped as StepUnavailable, optional
from Cases.Top48.weixin_extended import WeixinExtendedCase


class ObservedAppCase(WeixinExtendedCase):
    COMPONENT = ''

    def set_up(self):
        super().set_up()
        # 搜索页弹出系统输入法前就准备广播输入法，避免首次输入法协议打断采集。
        self.d.set_input_ime(True)
        self._ime_changed = True

    def dismiss_system_prompt(self):
        package = self.current_app()['package']
        if package not in ('com.miui.securitycenter', 'com.android.permissioncontroller', 'com.google.android.permissioncontroller'):
            return
        for node in ET.fromstring(self.d.dump_hierarchy()).iter('node'):
            if node.get('package') == package and node.get('text') in ('不同意', '不允许', '拒绝', '取消'):
                box = self.bounds(node)
                if len(box) == 4:
                    self._locators.add('tree')
                    self.d.shell('input mouse -d 0 tap {} {}'.format(round((box[0]+box[2])/2), round((box[1]+box[3])/2)))
                    self.invalidate()
                    time.sleep(.7)
                    if self.current_app()['package'] == package:
                        self.d.press('back')
                        self.invalidate()
                        time.sleep(.5)
                    return
        raise StepUnavailable('系统提示未提供可核对的拒绝或取消入口')

    def launch(self):
        self.unavailable = {}
        self._recording = False
        self._call_active = False
        self._live_started = False
        self._owned_draft = False
        result = self.d.shell(['am', 'start', '-W', '--display', '0', '-n', self.COMPONENT])
        if result.exit_code:
            raise RuntimeError('应用启动失败：' + result.output)
        time.sleep(2)
        self.invalidate()
        self.wait_for(lambda: self.current_app()['package'] == self.PACKAGE, '应用未进入前台')
        self.dismiss_system_prompt()
        self.dismiss_ads()
        self.main_page()

    def dismiss_ads(self):
        self.dismiss_system_prompt()
        # 仅关闭明确命名的广告/提示，不接受协议、登录或授权。
        for _ in range(3):
            for text in ('跳过广告', '跳过', '关闭广告', '以后再说', '暂不升级', '暂不更新', '下次再说'):
                matches = self.find(text, True)
                if len(matches) == 1:
                    self.choose(text, True)
                    time.sleep(.5)
                    break
            else:
                return

    def content_wait(self, predicate, message, timeout=25):
        def ready():
            self.dismiss_system_prompt()
            return predicate()
        return super().content_wait(ready, message, timeout)

    def go(self, action, ready, message):
        self.dismiss_ads()
        self.transition(action, ready, message)

    def home(self):
        self.foreground()
        self.swipe(.5, .995, .5, .62, 300)
        time.sleep(.7)
        if 'launcher' not in self.current_app()['activity'].lower():
            self.d.press('home')
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(), '未返回 Home')

    def labels(self):
        return [r['text'] for r in self.screen()]

    def browse_up(self, count):
        self.browse(count, 0)

    def browse_down(self, count):
        self.browse(0, count)

    def bottom_node(self, label):
        height = self.d.window_size()[1]
        rows = [n for n in self.nodes() if self.bounds(n)[1] > height*.85
                and (n.get('text') == label or n.get('content-desc') == label)]
        if rows:
            self._locators.add('tree')
            self.click_node(rows[0])
        else:
            self.choose(label, region=(0, .87, 1, .99))
