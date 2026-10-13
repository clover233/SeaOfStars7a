"""腾讯元宝三轮问答；等待本轮回答实际完成再浏览。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_yuanbao_0010(DynamicAppCase):
    PACKAGE = 'com.tencent.hunyuan.app.chat'
    all_app_package_list = [PACKAGE]
    QUESTIONS = ('什么是AI', '华为终端的主要产品有哪些', '介绍几款市面上主流的手机')

    def main_ready(self):
        return self.has(desc='临时对话模式开关-', prefix=True)

    def main_page(self):
        if self.main_ready():
            return
        self.open_control(self.main_ready, '元宝未返回新对话主界面', desc='新建对话')

    def launch(self):
        self.start()
        self.wait_for(lambda: self.has(desc='抽屉页入口'), '元宝对话页未就绪，请确认已登录', timeout=30)
        self.main_page()

    def send_button(self):
        # weditor/u2 树中发送箭头无文案；加号也是 Button，但 clickable=false。
        # 只取输入框右侧、可点击的 Button，避免点开附件面板。
        edits = [n for n in self.nodes() if n.get('class') == 'android.widget.EditText']
        if len(edits) != 1:
            raise RuntimeError('元宝输入框不唯一')
        left, top, right, bottom = self.bounds(edits[0])
        buttons = [n for n in self.nodes() if n.get('class') == 'android.widget.Button'
                   and n.get('clickable') == 'true' and n.get('enabled') == 'true'
                   and self.bounds(n)[0] >= right and self.bounds(n)[1] < bottom
                   and self.bounds(n)[3] > top]
        if len(buttons) != 1:
            raise RuntimeError('元宝发送按钮不唯一或未就绪')
        return buttons[0]

    def send_question(self, question):
        self.foreground()
        edit = self.d(className='android.widget.EditText', packageName=self.PACKAGE)
        if not edit.exists:
            self.click(text='发消息或按住说话...')
            self.wait_for(lambda: edit.exists, '元宝输入框未就绪')
        edit.set_text(question)
        self.wait_for(lambda: any(n.get('text') == question and
                      n.get('class') == 'android.widget.EditText' for n in self.nodes()),
                      '元宝问题未输入')
        self.click_node(self.send_button())
        # 输入框内的文本不算发送成功；先确认草稿清空，防止重复发送。
        def sent():
            nodes = self.nodes()
            return (not any(n.get('class') == 'android.widget.EditText' and n.get('text') == question
                            for n in nodes) and
                    any(n.get('class') != 'android.widget.EditText' and n.get('text') == question
                        for n in nodes))
        self.wait_for(sent, '元宝问题未发送')

        def answered():
            nodes = self.nodes()
            if any(any(word in n.get('text', '') for word in ('网络异常', '网络连接失败', '请求失败'))
                   for n in nodes):
                raise RuntimeError('元宝本轮回答出现网络错误')
            # 长回答结束时操作栏可能在屏幕下方；先跟随到本轮回答底部。
            if self.has(desc='滚动到底部'):
                self.click(desc='滚动到底部')
                return False
            questions = [i for i, n in enumerate(nodes) if n.get('text') == question and
                         n.get('class') != 'android.widget.EditText']
            # 本轮问题仍可见时，只认可其后的回答操作栏，排除上一轮操作栏。
            tail = nodes[questions[-1] + 1:] if questions else nodes
            return (any(n.get('content-desc') == '复制本次模型回答' for n in tail) and
                    self.has(desc='切换语音'))

        self.wait_for(answered, '元宝本轮回答未完成', timeout=150)
        # 防止末尾卡片加载时短暂遮挡输入区。
        time.sleep(1)

    def steps(self):
        return [
            ('启动腾讯元宝', self.launch, 3),
            ('点击对话框，输入什么是AI', lambda: self.send_question(self.QUESTIONS[0]), 1),
            ('浏览搜索结果，上下滑动3次', lambda: self.browse(3, 3), 0),
            ('点击对话框，输入华为终端的主要产品有哪些', lambda: self.send_question(self.QUESTIONS[1]), 1),
            ('浏览搜索结果，上下滑动3次', lambda: self.browse(3, 3), 0),
            ('点击对话框，输入介绍几款市面上主流的手机', lambda: self.send_question(self.QUESTIONS[2]), 1),
            ('浏览搜索结果，上下滑动3次', lambda: self.browse(3, 3), 0),
            ('返回腾讯元宝主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 1),
        ]
