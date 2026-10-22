"""豆包动态性能用例的控件定位、提问和媒体选择辅助方法。"""
import logging
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class DoubaoDynamicCase(DynamicAppCase):
    PACKAGE = 'com.larus.nova'

    def point(self, x, y):
        """当前豆包底栏会忽略驻留点击，使用 uiautomator2 普通点击。"""
        self.foreground()
        self.d.click(round(x), round(y))

    def chat_ready(self):
        # action_entrance 仅在语音首页存在，文字对话页改为 input_text。
        return (self.has(rid='chat_root') and self.has(rid='action_entrance')
                or self.has(rid='larus_chat_top_left_create_new_cvs')
                and bool(self.text_editors()))

    def launch(self):
        # Monkey 启动后旧应用有时会重新抢到前台；使用当前安装版本的 launcher。
        output = self.d.shell(['cmd', 'package', 'resolve-activity', '--brief',
                               '-a', 'android.intent.action.MAIN',
                               '-c', 'android.intent.category.LAUNCHER', self.PACKAGE]).output
        components = [line.strip() for line in output.splitlines()
                      if line.strip().startswith(self.PACKAGE + '/')]
        if len(components) != 1:
            raise RuntimeError('无法解析豆包启动入口：' + output)
        result = self.d.shell(['am', 'start', '-W', '--display', '0', '-n', components[0]])
        if result.exit_code or 'Error:' in result.output:
            raise RuntimeError('豆包启动失败：' + result.output)
        # 对话页尚未挂载时不能盲目按返回，否则会直接把刚启动的应用退出。
        self.wait_for(lambda: self.current_package() == self.PACKAGE and self.chat_ready(),
                      '豆包对话页未加载，请确认已登录', timeout=25)

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
        # 输入框本身也包含问题，不能把草稿误认成发送成功，更不能重试发送。
        self.click_node(self.send_button())
        self.wait_for(lambda: any(question in node.get('text', '')
                                 and node.get('class') != 'android.widget.EditText'
                                 for node in self.nodes())
                      and not any(question == n.get('text') for n in self.text_editors()),
                      '豆包未确认问题发送成功，不自动重发')
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

    def camera_capture_active(self):
        app = self.current_app()
        return (app.get('package') == self.PACKAGE
                and app.get('activity', '').endswith('CameraCaptureActivity'))

    def camera_result_ready(self):
        app = self.current_app()
        return (app.get('package') == self.PACKAGE
                and app.get('activity', '').endswith('CameraResultActivity')
                and self.has(rid='markable_preview_image'))

    def camera_photo(self):
        self.launch()
        self.click(desc='相机', rid='action_entrance')
        self.wait_for(lambda: self.camera_capture_active()
                      or self.current_package() != self.PACKAGE
                      or self.has(desc='拍摄') or self.has(desc='拍照'),
                      '豆包相机未打开', timeout=10)
        package = self.current_package()
        shutter = self.external_node(package, ('拍摄', '拍照', '快门', 'shutter'))
        if shutter is None:
            if not self.camera_capture_active():
                logging.warning('SKIP：当前相机页面未暴露可用快门控件')
                self.return_to_doubao('未从相机返回豆包')
                return False
            # 豆包 AI 相机的取景页是自绘画布，当前版本的层级仅暴露外层容器。
            # 严格确认相机 Activity 后按屏幕比例点快门，避免绑定具体分辨率。
            width, height = self.screen_size()
            result = self.d.shell('input -d 0 tap {} {}'.format(
                round(width * .5), round(height * .875)))
            if result.exit_code:
                raise RuntimeError('豆包相机快门点击失败：' + result.output)
        elif package == self.PACKAGE:
            self.click_node(shutter)
        else:
            self.tap_external_node(shutter)
        self.wait_for(lambda: self.camera_result_ready()
                      or self.current_package() != package
                      or self.external_node(self.current_package(),
                                            ('确认', '使用照片', '完成', '✓')) is not None,
                      '拍照后未进入预览页', timeout=10)
        if self.camera_result_ready():
            # 当前版本拍照后直接把照片附加到相机结果页，可继续输入“帮我修图”。
            return True
        confirm = self.external_node(self.current_package(), ('确认', '使用照片', '完成', '✓'))
        if confirm is None:
            logging.warning('SKIP：拍照后未暴露确认控件，返回豆包继续后续步骤')
            self.return_to_doubao('未从相机返回豆包')
            return False
        if self.current_package() == self.PACKAGE:
            self.click_node(confirm)
        else:
            self.tap_external_node(confirm)
        self.return_to_doubao('拍照确认后未返回豆包')
        return True

    def open_media_menu(self):
        self.launch()
        ready = lambda: (self.has(text='从相册选择') or self.has(desc='从相册选择')
                         or self.has(text='相册', rid='layout_menu_item_name'))
        if not self.has(rid='iv_action_menu_entrance'):
            self.media_menu_available = False
            logging.warning('SKIP：当前豆包版本没有更多面板入口')
            return False
        try:
            self.open_control(ready, '豆包更多面板未显示相册入口',
                              rid='iv_action_menu_entrance')
        except RuntimeError:
            self.media_menu_available = False
            logging.warning('SKIP：当前豆包更多面板未显示相册入口')
            return False
        self.media_menu_available = True
        return True

    def album_ready(self):
        return self.current_package() != self.PACKAGE or self.has(rid='media_image_view')

    def choose_from_album(self):
        if not getattr(self, 'media_menu_available', False):
            self.album_open = False
            logging.warning('SKIP：豆包更多面板不可用，跳过相册')
            return False
        if self.has(text='从相册选择'):
            self.click(text='从相册选择')
        elif self.has(desc='从相册选择'):
            self.click(desc='从相册选择')
        elif self.has(text='相册', rid='layout_menu_item_name'):
            self.click(text='相册', rid='layout_menu_item_name')
        else:
            self.album_open = False
            logging.warning('SKIP：豆包更多面板没有相册入口')
            return False
        self.wait_for(self.album_ready, '豆包相册未打开', timeout=10)
        self.album_open = True
        return True

    def open_album(self):
        if self.open_media_menu():
            return self.choose_from_album()
        return False

    def browse_external(self, up=0, down=0, pause=1):
        """在系统相册中使用屏幕比例滑动，避免假定图库分辨率。"""
        package = self.current_package()
        if not getattr(self, 'album_open', False) or not self.album_ready():
            logging.warning('SKIP：未进入豆包相册，跳过图片浏览')
            return False
        width, height = self.screen_size()
        for upward, count in ((True, up), (False, down)):
            for _ in range(count):
                start, end = (.78, .32) if upward else (.32, .78)
                result = self.d.shell('input -d 0 swipe {} {} {} {} 400'.format(
                    round(width * .5), round(height * start),
                    round(width * .5), round(height * end)))
                if result.exit_code:
                    raise RuntimeError('系统相册滑动失败：' + result.output)
                time.sleep(pause)
        return True

    def choose_two_photos(self):
        if not getattr(self, 'album_open', False) or not self.album_ready():
            logging.warning('SKIP：未进入豆包相册，跳过选择图片')
            return False
        package = self.current_package()
        width, height = self.screen_size()
        if package == self.PACKAGE:
            candidates = [node for node in self.nodes(rid='media_item_select_indicator_check_box')
                          if node.get('content-desc', '').startswith('未选中')]
        else:
            candidates = [node for node in self.package_nodes(package)
                          if node.get('class') == 'android.widget.ImageView'
                          and node.get('clickable') == 'true'
                          and self.bounds(node)[0] < width * .95
                          and self.bounds(node)[1] > height * .16
                          and self.bounds(node)[3] < height * .88]
        candidates.sort(key=lambda node: (self.bounds(node)[1], self.bounds(node)[0]))
        if len(candidates) < 2:
            logging.warning('SKIP：相册中未找到两张可选择的图片缩略图')
            return False
        for node in candidates[:2]:
            if package == self.PACKAGE:
                self.click_node(node)
            else:
                self.tap_external_node(node)
            time.sleep(.4)
        done = self.external_node(package, ('完成', '确定', '添加'))
        if done is None:
            attached = self.nodes(rid='file_resource_remove') if package == self.PACKAGE else []
            if len(attached) >= 2:
                logging.info('替代：当前豆包版本选图后自动附加，无“完成”按钮')
                close_nodes = self.nodes(rid='title_close')
                if close_nodes:
                    self.click_node(close_nodes[0])
                    time.sleep(1)
                self.return_to_doubao('从内嵌相册选择后未返回豆包')
                self.album_open = False
                return True
            logging.warning('SKIP：选中两张图片后未找到完成按钮')
            return False
        if package == self.PACKAGE:
            self.click_node(done)
        else:
            self.tap_external_node(done)
        self.return_to_doubao('从相册选择后未返回豆包')
        self.album_open = False
        return True

    def call(self):
        self.launch()
        call_nodes = self.nodes(rid='real_time_call_ic_container') or self.nodes(rid='real_time_call')
        if not call_nodes:
            self.call_available = False
            logging.warning('SKIP：当前豆包版本没有电话入口')
            return False
        self.transition(lambda: self.click_node(call_nodes[0]),
                        self.call_active,
                        '豆包通话界面未打开')
        self.call_available = True
        return True

    def call_active(self):
        return (self.current_package() == self.PACKAGE
                and (self.has(rid='voice_call_hangup')
                     or self.has(desc='挂断') or self.has(text='结束通话')))

    def exit_call(self):
        if not getattr(self, 'call_available', False):
            logging.warning('SKIP：豆包通话未打开，无需退出')
            return False
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
        self.call_available = False
        return True
