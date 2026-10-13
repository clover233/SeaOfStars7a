"""DeepSeek 三轮对话；等待实际回答完成后再浏览。"""
import logging

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_deepseek_0010(DynamicAppCase):
    PACKAGE = 'com.deepseek.chat'
    all_app_package_list = [PACKAGE]
    QUESTIONS = ('什么是AI', '华为终端的主要产品有哪些', '介绍几款市面上主流的手机')

    def launch(self):
        self.start()
        self.wait_for(lambda: self.has(text='发消息或按住说话') or
                      self.d(className='android.widget.EditText', packageName=self.PACKAGE).exists,
                      'DeepSeek 对话页未就绪，请确认已登录')
        self.wait_for(lambda: not self.has(desc='停止'), '上一轮回答尚未完成', timeout=120)

    def send_question(self, question):
        self.foreground()
        edit = self.d(className='android.widget.EditText', packageName=self.PACKAGE)
        if not edit.exists:
            self.open_control(lambda: edit.exists, 'DeepSeek 输入框不可用', text='发消息或按住说话')
        edit.set_text(question)
        self.wait_for(lambda: self.has(desc='发送'), '发送按钮未就绪')
        # 不以输入框内的相同文本判断发送成功，避免输入未发送时误通过。
        self.transition(lambda: self.click(desc='发送'),
                        lambda: not self.has(desc='发送') and self.has(text=question),
                        '问题未发送')
        for attempt in range(3):
            busy_seen = self.has(desc='停止')
            network_error = False

            def answered():
                nonlocal busy_seen, network_error
                nodes = self.nodes()
                if any(n.get('content-desc') == '停止' for n in nodes):
                    busy_seen = True
                    return False
                questions = [i for i, n in enumerate(nodes) if n.get('text') == question and
                             n.get('class') != 'android.widget.EditText']
                tail = nodes[questions[-1] + 1:] if questions else (nodes if busy_seen else [])
                if any('请检查网络后重试' in n.get('text', '') for n in tail):
                    network_error = True
                    return True
                if any(n.get('content-desc') == '复制' for n in tail):
                    return True
                # 长回答结束后操作栏可能在屏幕下方。
                if busy_seen and any(n.get('content-desc') == '转至底部' for n in nodes):
                    self.click(desc='转至底部')
                return False

            self.wait_for(answered, 'DeepSeek 回答未完成或网络异常', timeout=120)
            if not network_error:
                return
            if attempt == 2:
                raise RuntimeError('DeepSeek 网络错误，两次重试后仍未获得回答')
            logging.warning('DeepSeek 网络错误，重试本轮回答 %s/2', attempt + 1)
            def retry():
                buttons = self.nodes(desc='重试')
                if not buttons:
                    raise RuntimeError('DeepSeek 网络异常且未找到本轮重试按钮')
                self.click_node(buttons[-1])
            self.transition(retry,
                            lambda: self.has(desc='停止') or not self.has(text='请检查网络后重试'),
                            'DeepSeek 重试按钮未响应')

    def steps(self):
        return [
            ('启动DeepSeek', self.launch, 3),
            ('点击对话框，输入什么是AI', lambda: self.send_question(self.QUESTIONS[0]), 1),
            ('浏览搜索结果，上下滑动3次', lambda: self.browse(3, 3, 1), 0),
            ('点击对话框，输入华为终端的主要产品有哪些', lambda: self.send_question(self.QUESTIONS[1]), 1),
            ('浏览搜索结果，上下滑动3次', lambda: self.browse(3, 3, 1), 0),
            ('点击对话框，输入介绍几款市面上主流的手机', lambda: self.send_question(self.QUESTIONS[2]), 1),
            ('浏览搜索结果，上下滑动3次', lambda: self.browse(3, 3, 1), 0),
            ('滑动返回Home页', self.home, 1),
        ]
