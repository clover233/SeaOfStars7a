"""支付宝动态性能用例共用操作；定位基于实机 UI 层级及 1208×2624 截图。

优先使用 resource-id/text/description。Canvas 没有可用控件时，才在已知页面
按 window_size 换算比例坐标。协议、登录等前置条件失败会中断，避免空跑采集。
"""
import logging
import re
import time
import xml.etree.ElementTree as ET

from Cases.CaseBase import Case
from aw_new import SeaOfStarsAW


PACKAGE = 'com.eg.android.AlipayGphone'
TAB_ID = 'com.alipay.android.tablauncher:id/tab_description'
PHOTO_ID = 'com.alipay.android.phone.wallet.beephoto:id/iv_photo'
MINI_TAB_ID = 'com.alipay.multiplatform.phone.xriver_integration:id/ariver_tabbar_item_text'


class AlipayCase(Case):
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
            if permission == 'READ_MEDIA_IMAGES' and sdk < 33:
                permission = 'READ_EXTERNAL_STORAGE'
            permission = 'android.permission.' + permission
            result = self.d.shell('pm grant {} {}'.format(PACKAGE, permission))
            if result.exit_code or 'Exception' in result.output or 'Error' in result.output:
                raise RuntimeError('权限授权失败 {}: {}'.format(permission, result.output))
        logging.info('支付宝环境准备完成，保留其他应用后台')
        self._prepared = True

    def wait_for(self, predicate, message, timeout=12):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(0.4)
        raise RuntimeError('{}；当前页面 {}'.format(message, self.d.app_current()))

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
            raise RuntimeError('未找到控件 {}；当前页面 {}'.format(selector, self.d.app_current()))
        obj.click()

    def relative_click(self, x, y):
        if not (0 < x < 1 and 0 < y < 1):
            raise ValueError('坐标必须为屏幕比例，且在 (0, 1) 内')
        if self.d.app_current()['package'] != PACKAGE:
            raise RuntimeError('比例点击前台不是支付宝，停止操作')
        width, height = self.d.window_size()
        self.d.click(round(width * x), round(height * y))

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
        # 适配不同厂商桌面包名；app_current 在桌面返回 launcher activity。
        self.wait_for(lambda: 'launcher' in self.d.app_current()['activity'].lower(), '上滑后未返回Home页')

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
            if self.d.app_current()['package'] != PACKAGE:
                raise RuntimeError('返回途中已离开支付宝')
            self.d.press('back')
            time.sleep(0.7)
        raise RuntimeError('未能返回支付宝{}页'.format(name))

    def swipe_back_home(self):
        for _ in range(10):
            if self.has_tabs():
                self.return_tab('首页')
                return
            if self.d.app_current()['package'] != PACKAGE:
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
        time.sleep(2)
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
            self.relative_click(0.5, 0.816)
            self.wait_for(lambda: not self.d(text='恭喜获得碰一下券包').exists, '转账活动弹层未关闭')
        if self.d(text='明天继续来领惊喜红包哦～').exists:
            self.relative_click(0.5, 0.73)
            self.wait_for(lambda: not self.d(text='明天继续来领惊喜红包哦～').exists, '闪购活动弹层未关闭')

    def canvas_tap(self, text, ratio, activity):
        if self.d(text=text).exists:
            self.tap(text=text)
        else:
            if activity not in self.d.app_current()['activity']:
                raise RuntimeError('{}比例定位的页面不匹配'.format(text))
            logging.info('%s 无可访问控件，使用屏幕比例 %s', text, ratio)
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
        self.wait_for(lambda: 'TFToCardForm' in self.d.app_current()['activity'], '未打开转到银行卡页')

    def open_account(self):
        self.tap(text='转到支付宝')
        self.wait_for(lambda: self.d(text='手机号/姓名/支付宝账户', className='android.widget.EditText').exists,
                      '未打开转到支付宝页')

    def open_album(self):
        self.tap(text='相册')
        self.wait_for(lambda: 'PhotoSelectActivity' in self.d.app_current()['activity'], '未打开相册')

    def preview_first_photo(self):
        photos = self.d(resourceId=PHOTO_ID)
        if not photos.wait(timeout=8):
            raise RuntimeError('相册为空，请预置测试图片')
        photos[0].click()
        self.wait_for(lambda: 'PhotoPreviewActivity' in self.d.app_current()['activity'], '未进入图片预览')

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
            if 'MainSearchActivity' not in self.d.app_current()['activity']:
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
