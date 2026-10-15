"""系统信息动态性能用例的页面操作。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class MmsDynamicCase(DynamicAppCase):
    PACKAGE = 'com.android.mms'

    def main_ready(self):
        return self.has(text='短信', rid='action_bar_title_expand')

    def launch(self):
        self.start()
        if not self.main_ready():
            self.main_page()
        self.wait_for(self.main_ready, '信息主界面未加载')

    def open_sender(self, name):
        quoted = name.replace('"', '\\"')
        path = ('//*[@resource-id="com.android.mms:id/from" and '
                '@text="{}"]/../..').format(quoted)
        target = self.d.xpath(path)
        if not target.exists:
            target = self.d.xpath('//*[@text="{}"]/../..'.format(quoted))
        if not target.exists:
            raise RuntimeError('信息列表没有会话：{}'.format(name))
        target.click()
        self.wait_for(lambda: self.has(text=name, rid='action_bar_title_expand'),
                      '未打开会话：{}'.format(name))

    def notifications(self):
        # 当前系统版本将“通知信息”归并为“验证码”，优先兼容旧入口。
        name = '通知信息' if self.has(text='通知信息') else '验证码'
        self.open_sender(name)
        self._notification_name = name

    def view_two_messages(self):
        # 通知聚合页卡片在当前版本没有详情动作，改为查看两条实际通知会话。
        self.main_page()
        names = []
        for node in self.nodes(rid='from'):
            name = node.get('text', '').strip()
            if name and name not in names and name != '验证码':
                names.append(name)
        if not names and self.has(text='验证码'):
            names = ['验证码']
        if len(names) == 1:
            names.append(names[0])
        for name in names[:2]:
            self.open_sender(name)
            time.sleep(1)
            self.back()
            self.wait_for(self.main_ready, '查看通知后未返回信息主界面')

    def main_page(self):
        self.return_to(self.main_ready, '未返回信息主界面', limit=4)
