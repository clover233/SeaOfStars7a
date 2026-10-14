"""豆包动态性能用例的控件定位、提问和媒体选择辅助方法。"""
import logging
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class DoubaoDynamicCase(DynamicAppCase):
    PACKAGE = 'com.larus.nova'

    def chat_ready(self):
        return self.has(rid='chat_root') and self.has(rid='action_entrance')

    def launch(self):
        self.start()
        self.return_to(self.chat_ready, '豆包对话页未加载，请确认已登录')

    def new_chat(self):
        self.require(rid='larus_chat_top_left_create_new_cvs')
        self.click(rid='larus_chat_top_left_create_new_cvs')
        time.sleep(1)
        self.wait_for(self.chat_ready, '豆包新对话页未加载')

    def text_editors(self):
        return [node for node in self.nodes()
                if node.get('class') == 'android.widget.EditText'
                and node.get('enabled') == 'true']

    def open_text_input(self):
        if self.text_editors():
            return True
        # 部分豆包版本的“文本输入”按钮处于灰度状态，点击后仍停留在语音模式。
        # 重试后仍无 EditText 时按表格允许的缺失功能策略跳过本次发送。
        for _ in range(2):
            if not self.has(rid='action_input'):
                break
            self.click(rid='action_input')
            time.sleep(1)
            if self.text_editors():
                return True
        logging.warning('SKIP：当前豆包版本未开放可用的文本输入框')
        return False

    def send_button(self):
        buttons = [node for node in self.nodes()
                   if node.get('content-desc') in ('发送', '发送消息')
                   or node.get('text') in ('发送', '发送消息')]
        return buttons[0] if buttons else None

    def ask(self, question):
        self.enter_text(question)
        self.send_pending()

    def enter_text(self, question):
        self.pending_question = None
        if not self.open_text_input():
            return False
        editor = self.text_editors()[0]
        self.d(resourceId=editor.get('resource-id')).set_text(question)
        self.wait_for(lambda: self.send_button() is not None, '输入问题后未显示豆包发送按钮')
        self.pending_question = question
        return True

    def send_pending(self):
        question = getattr(self, 'pending_question', None)
        if not question:
            logging.warning('SKIP：没有待发送的豆包输入内容')
            return False
        self.transition(lambda: self.click_node(self.send_button()),
                        lambda: any(question in node.get('text', '')
                                    for node in self.nodes()),
                        '豆包未显示已发送的问题')
        # 等待模型生成区结束初始布局，避免随后滑动命中输入区。
        time.sleep(3)
        self.pending_question = None
        return True

    def package_nodes(self, package):
        return self.nodes(package=package)

    def current_package(self):
        return self.current_app()['package']

    def external_node(self, package, words):
        words = tuple(words)
        return next((node for node in self.package_nodes(package)
                     if any(word in node.get('text', '') or word in node.get('content-desc', '')
                            for word in words)), None)

    def tap_external_node(self, node):
        # 外部相机/图库页面不属于豆包，直接按控件 bounds 计算点击中心。
        left, top, right, bottom = self.bounds(node)
        result = self.d.shell('input -d 0 swipe {0} {1} {0} {1} 250'.format(
            round((left + right) / 2), round((top + bottom) / 2)))
        if result.exit_code:
            raise RuntimeError('外部页面控件点击失败：' + result.output)

    def return_to_doubao(self, message, limit=6):
        for _ in range(limit):
            if self.current_package() == self.PACKAGE and self.chat_ready():
                return
            self.d.shell('input -d 0 keyevent 4')
            time.sleep(1)
        self.wait_for(lambda: self.current_package() == self.PACKAGE and self.chat_ready(), message, timeout=5)

    def camera_photo(self):
        self.launch()
        self.click(desc='相机', rid='action_entrance')
        self.wait_for(lambda: self.current_package() != self.PACKAGE
                      or self.has(desc='拍摄') or self.has(desc='拍照'),
                      '豆包相机未打开', timeout=10)
        package = self.current_package()
        if package == self.PACKAGE:
            shutter = self.external_node(package, ('拍摄', '拍照', '快门'))
        else:
            shutter = self.external_node(package, ('拍摄', '拍照', '快门', 'shutter'))
        if shutter is None:
            logging.warning('SKIP：当前相机页面未暴露可用快门控件')
            self.return_to_doubao('未从相机返回豆包')
            return False
        self.tap_external_node(shutter)
        time.sleep(1)
        confirm = self.external_node(self.current_package(), ('确认', '使用照片', '完成', '✓'))
        if confirm is None:
            logging.warning('SKIP：拍照后未暴露确认控件，返回豆包继续后续步骤')
            self.return_to_doubao('未从相机返回豆包')
            return False
        self.tap_external_node(confirm)
        self.return_to_doubao('拍照确认后未返回豆包')
        return True

    def open_media_menu(self):
        self.launch()
        self.open_control(lambda: self.has(text='从相册选择') or self.has(desc='从相册选择'),
                          '豆包更多面板未显示从相册选择', rid='iv_action_menu_entrance')

    def choose_from_album(self):
        if not (self.has(text='从相册选择') or self.has(desc='从相册选择')):
            raise RuntimeError('豆包更多面板没有从相册选择入口')
        if self.has(text='从相册选择'):
            self.click(text='从相册选择')
        else:
            self.click(desc='从相册选择')
        self.wait_for(lambda: self.current_package() != self.PACKAGE,
                      '系统相册未打开', timeout=10)

    def open_album(self):
        self.open_media_menu()
        self.choose_from_album()

    def browse_external(self, up=0, down=0, pause=1):
        """在系统相册中使用屏幕比例滑动，避免假定图库分辨率。"""
        package = self.current_package()
        if package == self.PACKAGE:
            raise RuntimeError('未进入外部相册，不能浏览图片')
        width, height = self.d.window_size()
        for upward, count in ((True, up), (False, down)):
            for _ in range(count):
                start, end = (.78, .32) if upward else (.32, .78)
                result = self.d.shell('input -d 0 swipe {} {} {} {} 400'.format(
                    round(width * .5), round(height * start),
                    round(width * .5), round(height * end)))
                if result.exit_code:
                    raise RuntimeError('系统相册滑动失败：' + result.output)
                time.sleep(pause)

    def choose_two_photos(self):
        package = self.current_package()
        if package == self.PACKAGE:
            raise RuntimeError('未进入系统相册，停止选择图片')
        width, height = self.d.window_size()
        candidates = [node for node in self.package_nodes(package)
                      if node.get('class') == 'android.widget.ImageView'
                      and node.get('clickable') == 'true'
                      and self.bounds(node)[0] < width * .95
                      and self.bounds(node)[1] > height * .16
                      and self.bounds(node)[3] < height * .88]
        candidates.sort(key=lambda node: (self.bounds(node)[1], self.bounds(node)[0]))
        if len(candidates) < 2:
            raise RuntimeError('相册中未找到两张可选择的图片缩略图')
        for node in candidates[:2]:
            self.tap_external_node(node)
            time.sleep(.4)
        done = self.external_node(package, ('完成', '确定', '添加'))
        if done is None:
            raise RuntimeError('选中两张图片后未找到完成按钮')
        self.tap_external_node(done)
        self.return_to_doubao('从相册选择后未返回豆包')

    def call(self):
        self.launch()
        self.open_control(lambda: self.current_package() != self.PACKAGE
                          or self.has(desc='挂断') or self.has(text='结束通话'),
                          '豆包通话界面未打开', rid='real_time_call_ic_container')

    def exit_call(self):
        package = self.current_package()
        end = self.external_node(package, ('挂断', '结束通话', '退出通话'))
        if end is not None:
            if package == self.PACKAGE:
                self.click_node(end)
            else:
                self.tap_external_node(end)
        else:
            self.d.shell('input -d 0 keyevent 4')
        self.return_to_doubao('退出通话后未返回豆包')
