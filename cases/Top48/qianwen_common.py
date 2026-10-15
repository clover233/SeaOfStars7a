"""通义千问动态性能用例的页面操作。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class QianwenDynamicCase(DynamicAppCase):
    PACKAGE = 'com.aliyun.tongyi'

    def point(self, x, y):
        self.foreground()
        self.d.click(round(x), round(y))

    def swipe(self, x1=.5, y1=.78, x2=.5, y2=.32, duration=400):
        self.foreground()
        width, height = self.d.window_size()
        self.d.swipe(round(width * x1), round(height * y1),
                     round(width * x2), round(height * y2),
                     duration=duration / 1000)

    def input_hint_ready(self):
        return self.has(text='发消息或按住说话...')

    def launch(self):
        self.start()
        if not self.input_hint_ready():
            self.main_page()
        self.wait_for(self.input_hint_ready, '千问对话主界面未加载', timeout=30)

    def ask(self, question):
        hint = self.d.xpath('//*[@text="发消息或按住说话..."]/..')
        if not hint.exists:
            raise RuntimeError('千问消息输入入口不可用')
        hint.click()
        self.wait_for(lambda: bool(self.d(className='android.widget.EditText').count),
                      '千问输入框未展开')
        edit = self.d(className='android.widget.EditText')
        edit.set_text(question)

        edit_bottom = edit.info['bounds']['bottom']
        width, height = self.d.window_size()
        buttons = [node for node in self.nodes()
                   if node.get('class') == 'android.widget.FrameLayout'
                   and node.get('clickable') == 'true'
                   and self.bounds(node)[1] >= edit_bottom
                   and self.bounds(node)[2] - self.bounds(node)[0] < width * .16
                   and self.bounds(node)[3] < height * .96]
        if not buttons:
            raise RuntimeError('千问发送按钮不可用')
        send = max(buttons, key=lambda node: self.bounds(node)[0])
        self.click_node(send)
        self.wait_for(lambda: self.has(text=question), '千问问题未发送')
        self.wait_for(self.input_hint_ready, '千问回答未完成', timeout=75)

    def main_page(self):
        if self.d(className='android.widget.EditText').exists:
            self.back()
        self.wait_for(self.input_hint_ready, '未返回千问主界面')
