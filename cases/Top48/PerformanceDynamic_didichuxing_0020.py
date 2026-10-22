"""滴滴订单、钱包、出行入口、目的地搜索和车主服务浏览。"""
import logging
import json
from pathlib import Path
import subprocess
import tempfile
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_didichuxing_0020(DynamicAppCase):
    PACKAGE = 'com.sdu.didi.psnger'
    all_app_package_list = [PACKAGE]
    DESTINATION = '大雁塔北广场南停车场'

    def set_up(self):
        super().set_up()
        from Cases.Top48.weixin_common import WeixinDynamicCase
        self._ocr_command = None
        self._locators = set()
        WeixinDynamicCase.prepare_ocr(self)

    def screenshot_rows(self):
        if not self._ocr_command:
            raise RuntimeError('车主营销弹窗未导出控件，需要本地 OCR 核验')
        with tempfile.TemporaryDirectory(prefix='didi-screen-') as folder:
            shot = str(Path(folder)/'screen.png')
            self.d.screenshot(shot, display_id=0)
            result = subprocess.run(self._ocr_command + [shot], check=True,
                                    capture_output=True, text=True, timeout=30)
        return json.loads(result.stdout)

    @staticmethod
    def owner_marketing(rows):
        labels = ''.join(row['text'] for row in rows)
        # “副”在原失败截图中被OCR识别为“劏”，采用保留完整品牌词的稳定片段。
        return any(title in labels for title in ('跑滴滴', '成为顺风车车主')) and '奖励' in labels

    def dismiss_ad(self):
        for _ in range(3):
            closes = self.nodes(desc='关闭弹窗')
            if len(closes) != 1:
                break
            # 新版广告由popClose改为close_dialog，明确的关闭描述保持不变。
            self.click_node(closes[0])
            time.sleep(.8)
        # 车主频道另有延迟出现的代驾新客券，关闭叉号未导出节点。
        if (self.has(text='恭喜你获得') and self.has(text='开心收下')
                and self.has(text='代驾 · 新客券')):
            self.pct(.5, .827)
            time.sleep(.8)
        if self.owner_ready() and self.owner_marketing(self.screenshot_rows()):
            # 实机树只导出背景和无属性的全屏 FrameLayout；两版车主奖励图
            # 的关闭 X 均在截图下方此比例，不点击“去领取/领取发单”。
            self._locators.add('screenshot-ocr-relative')
            self.pct(.5, .84)
            self.wait_for(lambda: not self.owner_marketing(self.screenshot_rows()),
                          '滴滴车主奖励弹窗未关闭', timeout=8)

    def open_control(self, ready, message, **selector):
        # 新人礼也会在服务页切换时异步出现；等待目标页期间同样处理遮罩。
        def current_ready():
            self.dismiss_ad()
            return ready()
        def tap_control():
            self.dismiss_ad()
            self.click(**selector)
        self.transition(tap_control, current_ready, message)

    def home_ready(self):
        return self.has(rid='end_click_view') and self.has(text='首页', rid='tab_text')

    def my_ready(self):
        return self.has(text='我的钱包') and self.has(text='全部订单')

    def owner_ready(self):
        return self.has(text='车主服务', rid='ch_tab_name') and self.has(text='特惠洗车')

    def return_page(self, ready, message):
        # H5 返回和键盘收起是异步的，每次返回后观察页面，避免连续返回越过目标页。
        for _ in range(6):
            self.dismiss_ad()
            if ready():
                return
            self.back()
            deadline = time.monotonic() + 3
            while time.monotonic() < deadline:
                self.dismiss_ad()
                if ready():
                    return
                time.sleep(.4)
        self.wait_for(ready, message, timeout=5)

    def home_page(self):
        self.return_page(lambda: self.has(text='首页', rid='tab_text'), '未返回滴滴底部导航')
        self.dismiss_ad()
        if self.my_ready():
            self.open_control(lambda: self.has(text='出行', rid='tab_name'),
                              '未离开我的页面', text='首页', rid='tab_text')
        # 首页保留上次“车主”频道，显式切回“出行”。
        if not self.home_ready():
            self.open_control(self.home_ready, '滴滴出行首页未加载', text='出行', rid='tab_name')
        self.dismiss_ad()

    def launch(self):
        self.start()
        self.home_page()

    def my_page(self):
        self.open_control(self.my_ready, '滴滴我的页面未加载，请确认已登录', text='我的', rid='tab_text')

    def wallet(self):
        self.open_control(lambda: self.has(text='资产概览') and self.has(text='支付设置'),
                          '我的钱包未加载', text='我的钱包')

    def return_my(self):
        self.return_page(self.my_ready, '未返回滴滴我的界面')

    def orders(self):
        self.open_control(lambda: self.has(text='订单') and self.has(text='筛选'),
                          '订单页未加载', text='全部订单')
        time.sleep(2)
        self.return_my()

    def settings(self):
        self.open_control(lambda: self.has(text='账号安全') and self.has(text='通用'),
                          '设置页未加载', text='设置')
        time.sleep(2)
        self.return_my()

    def service(self, name, ready):
        self.dismiss_ad()
        self.require(rid='end_click_view')
        if not self.has(text=name, rid='entrance_name'):
            logging.warning('SKIP：当前首页没有%s入口', name)
            return False
        self.open_control(ready, name + '页面未加载', text=name, rid='entrance_name')
        time.sleep(3)
        self.home_page()

    def search_page(self):
        self.open_control(lambda: self.has(rid='way_point_edit_search_address'),
                          '目的地搜索框未打开', rid='end_click_view')

    def search(self):
        self.foreground()
        self.d(resourceId=self.PACKAGE + ':id/way_point_edit_search_address').set_text(self.DESTINATION)
        retries = []
        def results_ready():
            if self.has(rid='content_title', text=self.DESTINATION, prefix=True):
                return True
            if (len(retries) < 2 and (not retries or time.monotonic() - retries[-1] > 5)
                    and self.has(text='网络加载异常')
                    and self.has(rid='poi_select_scene_prompt_error_retry_btn')):
                self.click(rid='poi_select_scene_prompt_error_retry_btn')
                retries.append(time.monotonic())
            return False
        self.wait_for(results_ready, '目的地搜索未返回匹配结果', timeout=60)
        # 只收起键盘，保留搜索结果页；不选择目的地或发起叫车。
        if self.d.shell('dumpsys input_method').output.find('mInputShown=true') >= 0:
            self.back()
        self.require(rid='way_point_edit_search_address')

    def owner(self):
        self.home_page()
        self.open_control(self.owner_ready, '车主服务未加载', text='车主', rid='tab_name')

    def wash(self):
        self.dismiss_ad()
        if not self.has(text='特惠洗车'):
            logging.warning('SKIP：当前车主页无特惠洗车入口')
            return False
        self.click(text='特惠洗车')
        last_click = [time.monotonic()]
        # 首次进入会加载洗车授权页，不能在 H5 加载时重复点击原页面入口。
        def wash_ready():
            self.dismiss_ad()
            if (self.current_app().get('activity', '').endswith('MainActivity')
                    and self.owner_ready() and time.monotonic() - last_click[0] > 3):
                self.click(text='特惠洗车')
                last_click[0] = time.monotonic()
                return False
            if any('洗车服务' in node.get('text', '') and '授权协议' in node.get('text', '')
                   for node in self.nodes()) and self.has(text='同意'):
                self.click(text='同意')
            if self.has(text='门店洗车') and self.has(text='排序/筛选'):
                return True
            if self.current_app()['activity'].endswith('WebActivity'):
                # 当前 H5 商户列表整页未导出文字节点，截图同时核对导航与商户内容。
                rows = self.screenshot_rows()
                labels = ''.join(row['text'] for row in rows)
                ready = ('门店洗车' in labels and '筛选' in labels
                         and sum('营业时间' in row['text'] for row in rows) >= 2)
                if ready:
                    self._locators.add('screenshot-ocr-relative')
                return ready
            return False
        self.wait_for(wash_ready, '洗车商户列表未加载', timeout=60)
        self.browse(5, 5)
        self.return_page(self.owner_ready, '未返回车主服务页')

    def cars(self):
        self.require(text='特惠洗车')
        if not self.has(text='看车选车'):
            # 新版入口移至“更多 → 全部服务”。
            self.open_control(lambda: self.has(text='全部服务'), '车主全部服务未打开', text='更多')
        if not self.has(text='看车选车'):
            logging.warning('SKIP：全部服务中未提供看车选车入口')
            self.return_page(self.owner_ready, '未返回车主服务页')
            return False
        self.click(text='看车选车')
        self.wait_for(lambda: self.has(text='搜索品牌、车系') and self.has(text='条件选车'),
                      '看车选车内容未加载', timeout=60)
        self.browse(5, 5)

    def home(self):
        self.foreground()
        self.swipe(.5, .985, .5, .62, 300)
        time.sleep(.8)
        if 'launcher' not in self.current_app()['activity'].lower():
            self.d.shell('input -d 0 keyevent 3')
            self._adaptation = '系统未响应上滑手势，使用主屏Home键返回桌面'
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(), '未返回桌面')

    def steps(self):
        return [
            ('启动滴滴出行', self.launch, 3),
            ('点击我的', self.my_page, 2),
            ('点击钱包', self.wallet, 3),
            ('返回我的界面', self.return_my, 2),
            ('点击订单后返回我的界面', self.orders, 1),
            ('点击设置后返回我的界面', self.settings, 1),
            ('点击底部首页图标，回到首页', self.home_page, 2),
            ('点击城际拼车后返回首页', lambda: self.service('城际拼车', lambda: self.has(rid='book_btn')), 1),
            ('点击顺风车后返回首页', lambda: self.service('顺风车', lambda: self.has(rid='sfc_title_arrow')), 1),
            ('点击打车后返回首页', lambda: self.service('打车', lambda: self.has(rid='to_poi_bg_view')
             or self.has(text='输入目的地') and not self.has(rid='end_click_view')), 1),
            ('点击青桔骑行后返回首页', lambda: self.service('青桔骑行', lambda: self.has(text='扫码用车')), 1),
            ('点击搜索框', self.search_page, 1),
            ('输入大雁塔北广场南停车场', self.search, 2),
            ('浏览搜索结果，上滑2次，下滑2次', lambda: self.browse(2, 2), 0),
            ('返回滴滴出行首页', self.home_page, 2),
            ('点击车主', self.owner, 3),
            ('点击特惠洗车并浏览，上滑5次，下滑5次', self.wash, 1),
            ('点击看车选车并浏览，上滑5次，下滑5次', self.cars, 1),
            ('返回滴滴出行主界面', self.home_page, 2),
            ('滑动返回Home页', self.home, 1),
        ]
