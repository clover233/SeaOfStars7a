"""滴滴订单、钱包、出行入口、目的地搜索和车主服务浏览。"""
import logging
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_didichuxing_0020(DynamicAppCase):
    PACKAGE = 'com.sdu.didi.psnger'
    all_app_package_list = [PACKAGE]
    DESTINATION = '大雁塔北广场南停车场'

    def dismiss_ad(self):
        if self.has(desc='关闭弹窗', rid='popClose'):
            self.click(desc='关闭弹窗', rid='popClose')
            time.sleep(.8)

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
            return
        self.open_control(ready, name + '页面未加载', text=name, rid='entrance_name')
        time.sleep(3)
        self.home_page()

    def search_page(self):
        self.open_control(lambda: self.has(rid='way_point_edit_search_address'),
                          '目的地搜索框未打开', rid='end_click_view')

    def search(self):
        self.foreground()
        self.d(resourceId=self.PACKAGE + ':id/way_point_edit_search_address').set_text(self.DESTINATION)
        self.wait_for(lambda: self.has(rid='content_title', text=self.DESTINATION, prefix=True),
                      '目的地搜索未返回匹配结果', timeout=30)
        # 只收起键盘，保留搜索结果页；不选择目的地或发起叫车。
        if self.d.shell('dumpsys input_method').output.find('mInputShown=true') >= 0:
            self.back()
        self.require(rid='way_point_edit_search_address')

    def owner(self):
        self.home_page()
        self.open_control(self.owner_ready, '车主服务未加载', text='车主', rid='tab_name')

    def wash(self):
        if not self.has(text='特惠洗车'):
            logging.warning('SKIP：当前车主页无特惠洗车入口')
            return
        self.open_control(lambda: self.has(text='门店洗车'), '洗车商户列表未加载', text='特惠洗车')
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
            return
        self.open_control(lambda: self.has(text='搜索品牌、车系'), '看车选车内容未加载', text='看车选车')
        self.browse(5, 5)

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
            ('点击打车后返回首页', lambda: self.service('打车', lambda: self.has(rid='to_poi_bg_view')), 1),
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
