"""支付宝动态性能用例共用操作；定位基于实机 UI 层级及 1208×2624 截图。

优先使用 resource-id/text/description。Canvas 没有可用控件时，才在已知页面
按 window_size 换算比例坐标。协议、登录等前置条件失败会中断，避免空跑采集。

0020 的理财、测试聊天及设置操作也在本模块。默认使用“测试账号”和相册前5张；
可通过 ALIPAY_TEST_CONTACT、ALIPAY_TEST_PHOTOS 配置测试收件人和素材。
"""
import logging
import os
import re
import time
import xml.etree.ElementTree as ET

from Cases.CaseBase import Case
from Cases.Top48.main_display import MainDisplayMixin
from Cases.Top48.screen_text import ScreenshotText
from aw_new import SeaOfStarsAW


PACKAGE = 'com.eg.android.AlipayGphone'
TAB_ID = 'com.alipay.android.tablauncher:id/tab_description'
PHOTO_ID = 'com.alipay.android.phone.wallet.beephoto:id/iv_photo'
MINI_TAB_ID = 'com.alipay.multiplatform.phone.xriver_integration:id/ariver_tabbar_item_text'


def bounds(node):
    return tuple(map(int, re.findall(r'\d+', node.get('bounds', ''))))


class AlipayCase(MainDisplayMixin, Case):
    all_app_package_list = [PACKAGE]
    TEST_TIME = 1
    PERMISSIONS = ()

    @property
    def d(self):
        return SeaOfStarsAW.ut_device

    @SeaOfStarsAW.function_log
    def set_up(self):
        if not self.d.app_info(PACKAGE):
            raise RuntimeError('请先安装并登录支付宝')
        if SeaOfStarsAW.is_locked():
            SeaOfStarsAW.unlock_device()
        # 在采集前授权，避免首次权限弹窗混入性能场景。只申请本用例所需权限。
        sdk = int(self.d.shell('getprop ro.build.version.sdk').output.strip())
        for permission in self.PERMISSIONS:
            if permission in ('BLUETOOTH_CONNECT', 'BLUETOOTH_SCAN', 'BLUETOOTH_ADVERTISE') and sdk < 31:
                continue
            if permission == 'READ_MEDIA_IMAGES' and sdk < 33:
                permission = 'READ_EXTERNAL_STORAGE'
            permission = 'android.permission.' + permission
            result = self.d.shell('pm grant {} {}'.format(PACKAGE, permission))
            if result.exit_code or 'Exception' in result.output or 'Error' in result.output:
                raise RuntimeError('权限授权失败 {}: {}'.format(permission, result.output))
        logging.info('支付宝环境准备完成，保留其他应用后台')
        self._screen_text = ScreenshotText()
        self._prepared = True

    def tap(self, text=None, resource_id=None, description=None, timeout=8):
        selector = {}
        if text is not None:
            selector['text'] = text
        if resource_id:
            selector['resourceId'] = resource_id
        if description:
            selector['description'] = description
        obj = self.d(**selector)
        if not obj.wait(timeout=timeout):
            raise RuntimeError('未找到控件 {}；当前页面 {}'.format(selector, self.current_app()))
        obj.click()

    def relative_click(self, x, y):
        if not (0 < x < 1 and 0 < y < 1):
            raise ValueError('坐标必须为屏幕比例，且在 (0, 1) 内')
        if self.current_app()['package'] != PACKAGE:
            raise RuntimeError('比例点击前台不是支付宝，停止操作')
        width, height = self.d.window_size()
        px, py = round(width * x), round(height * y)
        # XRiver Canvas 在本机过滤 u2 短按；向主屏注入 200ms 的单次点击。
        result = self.d.shell('input -d 0 swipe {0} {1} {0} {1} 200'.format(px, py))
        if result.exit_code:
            raise RuntimeError('支付宝主屏点击失败：' + result.output)

    def swipe(self, upward=True):
        width, height = self.d.window_size()
        start, end = (0.78, 0.32) if upward else (0.32, 0.78)
        self.d.swipe(round(width * 0.5), round(height * start),
                     round(width * 0.5), round(height * end), duration=0.4)

    def browse(self, up, down, pause=2):
        self.check_preconditions()
        for upward, count in ((True, up), (False, down)):
            for _ in range(count):
                self.swipe(upward)
                time.sleep(pause)

    def launcher_gesture(self):
        width, height = self.d.window_size()
        self.d.swipe(round(width * 0.5), round(height * 0.995),
                     round(width * 0.5), round(height * 0.62), duration=0.25)
        # 按主屏焦点检查桌面，避免副屏的 launcher 干扰返回判断。
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(), '上滑后未返回Home页')

    def check_preconditions(self):
        if self.d(text='暂不同意').exists or self.d(text='同意并继续').exists:
            raise RuntimeError('请先人工确认当前小程序的用户协议/隐私政策，再运行用例')
        if self.d(text='登录').exists and self.d(text='手机号').exists:
            raise RuntimeError('请先登录测试账号')
        # 森林在内容已渲染后仍保留不可见的“重新加载”节点，以实际内容判断。
        if self.d(text='重新加载').exists and not self.d(text='切换为个人版').exists:
            raise RuntimeError('页面加载失败，请检查手机网络后重跑')

    def is_home(self):
        return self.d(resourceId='com.alipay.android.phone.openplatform.app:id/king_kong_text',
                      text='扫一扫').exists

    def has_tabs(self):
        return self.d(resourceId=TAB_ID).exists

    def return_tab(self, name='首页'):
        for _ in range(10):
            if self.has_tabs():
                self.tab(name)
                if name == '首页':
                    self.wait_for(self.is_home, '未返回支付宝首页')
                return
            if self.current_app()['package'] != PACKAGE:
                raise RuntimeError('返回途中已离开支付宝')
            self.d.press('back')
            time.sleep(0.7)
        raise RuntimeError('未能返回支付宝{}页'.format(name))

    def swipe_back_home(self):
        for _ in range(10):
            if self.has_tabs():
                self.return_tab('首页')
                return
            if self.current_app()['package'] != PACKAGE:
                raise RuntimeError('侧滑返回途中已离开支付宝')
            width, height = self.d.window_size()
            self.d.swipe(round(width * 0.005), round(height * 0.5),
                         round(width * 0.65), round(height * 0.5), duration=0.3)
            time.sleep(0.8)
        raise RuntimeError('侧滑后未返回支付宝首页')

    def tab(self, name):
        if self.d(resourceId='com.alipay.android.tablauncher:id/selected_fl',
                  description=name).exists:
            return
        self.tap(text=name, resource_id=TAB_ID)
        time.sleep(1)
        if name == '理财':
            # 首次理财促销弹窗在层级中是一张无 id 的全屏 ImageView。
            # 只在该已核实结构出现时点击截图中的关闭位置。
            def overlay():
                width, height = self.d.window_size()
                for node in ET.fromstring(self.d.dump_hierarchy()).iter('node'):
                    if node.get('package') == PACKAGE and node.get('class') == 'android.widget.ImageView' and not node.get('resource-id'):
                        box = list(map(int, re.findall(r'\d+', node.get('bounds', ''))))
                        if len(box) == 4 and box[2] - box[0] > width * 0.95 and box[3] - box[1] > height * 0.95:
                            return True
                return False
            for _ in range(2):
                if not overlay():
                    break
                self.relative_click(0.5, 0.835)
                time.sleep(1)
            if overlay():
                raise RuntimeError('理财首次促销弹窗未关闭')

    def launch(self):
        self.d.app_start(PACKAGE, use_monkey=True)
        self.wait_for(lambda: self.current_app()['package'] == PACKAGE,
                      '支付宝未进入主屏前台', timeout=25)
        if not self.d(packageName=PACKAGE).wait(timeout=10):
            raise RuntimeError('支付宝主屏页面未就绪')
        time.sleep(1)
        self.return_tab('首页')
        self.check_preconditions()

    def entry(self, name):
        if not self.is_home():
            raise RuntimeError('打开{}前不在支付宝首页'.format(name))
        # 首页服务和最近消息可能同名，优先锁定服务网格。
        app = self.d(text=name, resourceId='com.alipay.android.phone.openplatform.app:id/app_text')
        for _ in range(2):
            if app.exists:
                app.click()
            else:
                self.tap(text=name, resource_id='com.alipay.android.phone.openplatform.app:id/king_kong_text')
            time.sleep(1)
            if not self.is_home():
                break
        self.wait_for(lambda: not self.is_home(), '点击{}后页面未切换'.format(name))
        time.sleep(2)
        self.dismiss_promotions()
        if name == '蚂蚁森林':
            self.wait_for(lambda: self.d(text='切换为个人版').exists, '蚂蚁森林内容未加载', timeout=20)
        self.check_preconditions()

    def dismiss_promotions(self):
        # XRiver 弹层的层级 bounds 与实际渲染不一致，以下两个关闭按钮已通过截图核实。
        if self.d(text='恭喜获得碰一下券包').exists:
            self.relative_click(0.5, 0.845)
            self.wait_for(lambda: not self.d(text='恭喜获得碰一下券包').exists, '转账活动弹层未关闭')
        if self.d(text='明天继续来领惊喜红包哦～').exists:
            self.relative_click(0.5, 0.73)
            self.wait_for(lambda: not self.d(text='明天继续来领惊喜红包哦～').exists, '闪购活动弹层未关闭')

    def canvas_tap(self, text, ratio, activity):
        if self.d(text=text).exists:
            self.tap(text=text)
        else:
            if activity not in self.current_app()['activity']:
                raise RuntimeError('{}比例定位的页面不匹配'.format(text))
            reader = getattr(self, '_screen_text', None)
            if reader and reader.command:
                matches = [row for row in reader.read(self.d)
                           if row['text'].replace(' ', '') == text.replace(' ', '')]
                if len(matches) > 1:
                    raise RuntimeError('截图中的控件不唯一：' + text)
                if matches:
                    row = matches[0]
                    ratio = (row['x'] + row['w']/2, row['y'] + row['h']/2)
            logging.info('%s 无可访问控件，按主屏截图/比例定位 %s', text, ratio)
            self.relative_click(*ratio)
        time.sleep(2)
        self.check_preconditions()

    def subway(self):
        self.canvas_tap('地铁', (0.8, 0.245), 'CSGAPushActivity')

    def transfer(self):
        if not self.d(text='转账', resourceId='com.alipay.mobile.antui:id/auTitleTextView').exists:
            self.swipe()
            time.sleep(1)
        self.tap(text='转账', resource_id='com.alipay.mobile.antui:id/auTitleTextView')
        self.wait_for(lambda: self.d(text='转到银行卡').exists, '未打开转账页')
        time.sleep(2)
        self.dismiss_promotions()

    def back_to_transfer(self):
        self.d.press('back')
        self.wait_for(lambda: self.d(text='转到银行卡').exists, '未返回转账页')

    def open_bank(self):
        self.tap(text='转到银行卡')
        self.wait_for(lambda: 'TFToCardForm' in self.current_app()['activity'], '未打开转到银行卡页')

    def open_account(self):
        self.tap(text='转到支付宝')
        self.wait_for(lambda: self.d(text='手机号/姓名/支付宝账户', className='android.widget.EditText').exists,
                      '未打开转到支付宝页')

    def open_album(self):
        self.tap(text='相册')
        self.wait_for(lambda: 'PhotoSelectActivity' in self.current_app()['activity'], '未打开相册')

    def preview_first_photo(self):
        photos = self.d(resourceId=PHOTO_ID)
        if not photos.wait(timeout=8):
            raise RuntimeError('相册为空，请预置测试图片')
        photos[0].click()
        self.wait_for(lambda: 'PhotoPreviewActivity' in self.current_app()['activity'], '未进入图片预览')

    def search(self, query):
        obj = self.d(resourceId='com.alipay.mobile.antui:id/search_input_box')
        # 首页“搜索框”外层的空白区域有时不响应；优先点击实际搜索提示文字。
        for _ in range(2):
            hint = self.d(resourceId='com.alipay.android.phone.openplatform.app:id/home_title_search_hint')
            if hint.exists:
                hint.click()
            elif self.is_home():
                self.tap(description='搜索框')
            if obj.wait(timeout=4):
                break
            if not self.is_home():
                break
        if not obj.exists:
            raise RuntimeError('未找到搜索输入框')
        obj.set_text(query)
        self.tap(resource_id='com.alipay.mobile.antui:id/search_confirm')
        self.wait_for(lambda: self.d(resourceId='com.alipay.android.phone.businesscommon.globalsearch:id/search_more').exists,
                      '搜索结果未加载')
        time.sleep(2)

    def open_shansong(self):
        # 搜索框也含“闪送”，排除 EditText，优先点击结果中的 TextView。
        result = self.d(text='闪送', className='android.widget.TextView')
        if result.exists:
            result[0].click()
        else:
            if 'MainSearchActivity' not in self.current_app()['activity']:
                raise RuntimeError('当前不是闪送搜索结果页')
            self.relative_click(0.4, 0.35)
        self.wait_for(lambda: self.d(resourceId=MINI_TAB_ID, text='订单').exists, '未打开闪送小程序')
        time.sleep(2)
        self.check_preconditions()

    def mini_tab(self, name):
        self.check_preconditions()
        self.tap(text=name, resource_id=MINI_TAB_ID)
        time.sleep(1)
        self.check_preconditions()

    def my_entry(self, name):
        # 当前版本“我的”主体为 Canvas；比例来自实机截图，底部 tab 用控件定位。
        ratios = {'支付宝会员': (0.35, 0.251), '账单': (0.3, 0.319),
                  '余额': (0.3, 0.445), '设置': (0.93, 0.092)}
        if not self.has_tabs():
            raise RuntimeError('当前不是支付宝主界面的我的页')
        for _ in range(2):
            self.canvas_tap(name, ratios[name], 'AlipayLogin')
            if not self.has_tabs():
                break
        self.wait_for(lambda: not self.has_tabs(), '点击{}后未离开我的页'.format(name))

    @SeaOfStarsAW.function_log
    def run_case(self):
        # 工程当前 main.py 注释了 set_up 调用，支付宝用例自身保证前置准备执行。
        if not getattr(self, '_prepared', False):
            self.set_up()
        logging.info('用例开始执行!')
        for _ in range(self.TEST_TIME):
            for index, (name, action, stay) in enumerate(self.steps(), 1):
                logging.info('%s、%s', index, name)
                SeaOfStarsAW.start_perfetto_trace()
                failed = False
                try:
                    action()
                    time.sleep(stay)
                except Exception:
                    failed = True
                    logging.exception('步骤 %s、%s 执行失败', index, name)
                    raise
                finally:
                    try:
                        SeaOfStarsAW.stop_and_get_perfetto_trace(
                            self.trace_dir_path, self.__class__.__name__,
                            'step_{}、{}'.format(index, name), '', self.screenshot_dir_path)
                    except Exception:
                        if not failed:
                            raise
                        logging.exception('失败步骤的 trace 导出失败')
        logging.info('用例执行结束!')

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.getLogger().removeHandler(self.fh)
        self.fh.close()
        logging.info('用例结束，保留应用后台')


class AlipayMessageCase(AlipayCase):
    def set_up(self):
        self.contact = os.environ.get('ALIPAY_TEST_CONTACT', '测试账号').strip()
        raw_photos = os.environ.get('ALIPAY_TEST_PHOTOS', '1,2,3,4,5')
        try:
            self.photo_numbers = [int(value) for value in raw_photos.split(',')]
        except ValueError:
            self.photo_numbers = []
        if not self.contact or len(self.photo_numbers) != 5 or len(set(self.photo_numbers)) != 5 or min(self.photo_numbers) < 1:
            raise RuntimeError('0020 前置条件：配置 ALIPAY_TEST_CONTACT=准确联系人名，'
                               'ALIPAY_TEST_PHOTOS=五张允许发送的照片序号（如 1,2,3,4,5）')
        super().set_up()

    def open_steady(self):
        target = self.d(text='稳健理财', resourceId='com.alipay.android.widget.fortunehome:id/title')
        for _ in range(4):
            if target.exists:
                break
            self.swipe(False)
            time.sleep(1)
        self.tap(text='稳健理财', resource_id='com.alipay.android.widget.fortunehome:id/title')
        self.wait_for(lambda: self.d(text='稳健理财', resourceId='com.alipay.multiplatform.phone.xriver_integration:id/textView_title').exists,
                      '未打开稳健理财页')
        time.sleep(3)
        # 弹层背后的“其他产品”也会进入控件树，必须按截图确认遮罩。
        self.close_steady_intro()
        self.wait_for(lambda: self.d(text='其他产品').exists, '稳健理财内容未加载或首次介绍未关闭')

    def close_steady_intro(self):
        reader = getattr(self, '_screen_text', None)
        if reader is None:
            reader = self._screen_text = ScreenshotText()
        if not reader.command:
            raise RuntimeError('稳健理财需核实首次活动遮罩，请配置 ANDROID_OCR_COMMAND')
        def covered():
            texts = [row['text'].replace(' ', '') for row in reader.read(self.d)]
            return any('去看看' in text for text in texts) and any('攒钱多点米' in text for text in texts)
        for _ in range(3):
            if not covered():
                return
            # 当前“攒钱多点米”介绍页的关闭叉号；不点击活动主按钮。
            self.relative_click(.5, .717)
            time.sleep(.8)
        self.wait_for(lambda: not covered(), '稳健理财活动遮罩未关闭')

    def open_first_product(self):
        # 当前版本的热销区叫“大家都在买/一周热门榜”。从卡片容器读取产品名，
        # 避免推荐变化后仍点击旧名称，也排除屏幕右侧预加载的其他榜单。
        for _ in range(8):
            root = ET.fromstring(self.d.dump_hierarchy())
            for section in root.iter('node'):
                if section.get('class') == 'android.view.View' and section.get('text') in ('一周热门榜', '热销'):
                    candidates = [node for node in section.iter('node')
                                  if node.get('class') == 'android.widget.TextView' and node.get('text')]
                    # 实机容器的第一个文本为榜单说明，第二个为第一名产品名称。
                    if len(candidates) > 1:
                        product = candidates[1]
                        box = bounds(product)
                        width, height = self.d.window_size()
                        if len(box) == 4 and box[0] < width * 0.5 and height * 0.14 < box[1] < height * 0.85:
                            logging.info('打开热销第一款产品：%s', product.get('text'))
                            self.tap(text=product.get('text'))
                            self.wait_for(lambda: not self.d(text='稳健理财', resourceId='com.alipay.multiplatform.phone.xriver_integration:id/textView_title').exists,
                                          '点击后未进入理财产品页')
                            return
            self.swipe()
            time.sleep(1)
        raise RuntimeError('未找到热销/一周热门榜第一款理财产品，请检查当前版本布局')

    def message_plus(self):
        if not self.has_tabs():
            raise RuntimeError('点击消息+号前不在消息页')
        self.canvas_tap('+', (0.94, 0.085), 'AlipayLogin')
        self.wait_for(lambda: self.d(text='扫一扫').exists, '消息+号菜单未打开')

    def open_test_chat(self):
        if not self.has_tabs():
            raise RuntimeError('查找测试联系人前不在消息页')
        # 消息列表为 Canvas；通讯录暴露真实好友 id，避免误点全局搜索建议。
        self.canvas_tap('通讯录', (0.825, 0.085), 'AlipayLogin')
        self.wait_for(lambda: 'ContactMainPageActivity' in self.current_app()['activity'],
                      '未进入通讯录')
        result = self.d(text=self.contact, resourceId='com.alipay.mobile.socialcontactsdk:id/list_item_title')
        for _ in range(10):
            if result.exists:
                break
            self.swipe()
            time.sleep(0.5)
        if not result.exists or result.count != 1:
            raise RuntimeError('测试联系人未找到或不唯一：{}'.format(self.contact))
        result.click()
        self.wait_for(lambda: 'CSGAPushActivity' in self.current_app()['activity'],
                      '未进入已匹配测试账号的资料页')
        time.sleep(1)
        self.canvas_tap('发消息', (0.5, 0.94), 'CSGAPushActivity')
        self.wait_for(self.is_test_chat, '未进入指定测试联系人的聊天页')

    def is_test_chat(self):
        current = self.current_app()
        if current['package'] != PACKAGE or 'PersonalChatMsgActivity' not in current['activity']:
            return False
        return self.d(text=self.contact, resourceId='com.alipay.mobile.antui:id/title_text').exists

    def send_test_message(self):
        if not self.is_test_chat():
            raise RuntimeError('收件人校验失败，停止发送')
        edit = self.d(resourceId='com.alipay.mobile.chatapp:id/chat_msg_edit')
        if not edit.wait(timeout=8) or edit.count != 1:
            raise RuntimeError('未找到唯一的聊天输入框，请先完成测试账号聊天预置')
        edit.set_text('动态性能测试')
        self.tap(resource_id='com.alipay.mobile.chatapp:id/sendBtn', description='发送')
        self.wait_for(lambda: self.d(text='动态性能测试', resourceId='com.alipay.mobile.chatapp:id/chat_msg_text').exists,
                      '消息发送后未出现在聊天记录中')

    def chat_album(self):
        if not self.is_test_chat():
            raise RuntimeError('打开聊天图片前收件人校验失败')
        if not self.d(text='图片').exists:
            more = self.d(resourceId='com.alipay.mobile.chatapp:id/chat_stage_control_btn')
            if not more.exists:
                raise RuntimeError('未找到聊天更多按钮，请用测试账号核实当前版本聊天定位')
            more.click()
        self.tap(text='图片')
        self.wait_for(lambda: 'PhotoSelectActivity' in self.current_app()['activity'], '未打开聊天相册')

    def send_test_photos(self):
        if 'PhotoSelectActivity' not in self.current_app()['activity']:
            raise RuntimeError('当前不是聊天相册')
        initial = ET.fromstring(self.d.dump_hierarchy())
        if any(node.get('checked') == 'true' for node in initial.iter('node')):
            raise RuntimeError('相册已有勾选图片，请清空选择后重跑')
        selected = set()
        photo_order = {}
        for _ in range(15):
            root = ET.fromstring(self.d.dump_hierarchy())
            parents = {child: parent for parent in root.iter() for child in parent}
            for photo in root.iter('node'):
                if photo.get('resource-id') != PHOTO_ID:
                    continue
                match = re.match(r'照片(\d+)[，,]', photo.get('content-desc', ''))
                if not match:
                    continue
                # 相册编号混合视频和照片；按照片出现顺序计数，跳过视频。
                media_number = int(match.group(1))
                if media_number not in photo_order:
                    photo_order[media_number] = len(photo_order) + 1
                number = photo_order[media_number]
                if number not in self.photo_numbers or number in selected:
                    continue
                cell = parents[photo]
                checks = []
                for _ in range(3):
                    checks = [node for node in cell.iter('node') if node.get('checkable') == 'true']
                    if checks:
                        break
                    if cell not in parents:
                        break
                    cell = parents[cell]
                if len(checks) != 1:
                    raise RuntimeError('照片{}未暴露唯一勾选框，停止以避免误发'.format(number))
                checkbox = checks[0]
                if checkbox.get('checked') != 'true':
                    x1, y1, x2, y2 = bounds(checkbox)
                    self.d.click((x1 + x2) // 2, (y1 + y2) // 2)
                    time.sleep(0.3)
                selected.add(number)
            if len(selected) == 5:
                break
            self.swipe()
            time.sleep(0.5)
        if len(selected) != 5:
            raise RuntimeError('相册中未找到全部五张指定测试图片')
        root = ET.fromstring(self.d.dump_hierarchy())
        checked = [node for node in root.iter('node') if node.get('checked') == 'true']
        finish = self.d(resourceId='com.alipay.android.phone.wallet.beephoto:id/bt_finish')
        # 屏幕外勾选框可能不在层级中，完成按钮计数也可核实总选择数量。
        if not finish.exists or not (len(checked) == 5 or re.search(r'[（(]5(?:/\d+)?[）)]', finish.info.get('text', ''))):
            raise RuntimeError('无法确认恰好选择5张图片，停止发送')
        finish.click()
        self.wait_for(self.is_test_chat, '完成图片选择后未返回指定聊天页')

    def settings_entry(self, name):
        title_id = 'com.alipay.mobile.antui:id/title_text'
        if not self.d(text='设置', resourceId=title_id).exists:
            raise RuntimeError('当前不是设置页')
        ratios = {'新消息通知': (0.35, 0.412), '通用': (0.35, 0.594)}
        for _ in range(2):
            self.canvas_tap(name, ratios[name], 'CSPushActivity')
            if not self.d(text='设置', resourceId=title_id).exists:
                break
        self.wait_for(lambda: self.d(text=name, resourceId='com.alipay.multiplatform.phone.xriver_integration:id/textView_title').exists
                      or self.d(text=name, resourceId=title_id).exists, '未打开{}页'.format(name))

    def back_to_settings(self):
        self.d.press('back')
        self.wait_for(lambda: self.d(text='设置', resourceId='com.alipay.mobile.antui:id/title_text').exists,
                      '未返回设置页')
