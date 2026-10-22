"""云闪付浏览场景，适配新版优惠页“生活”分类。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_cloudflashpay_0010(DynamicAppCase):
    PACKAGE = 'com.unionpay'
    all_app_package_list = [PACKAGE]
    PERMISSIONS = ('CAMERA',)

    def on_home(self):
        return self.has(rid='firstItem') and self.has(rid='thirdItem')

    def app_home(self):
        self.return_to(lambda: self.has(rid='tv_tab_name', text='首页'), '未返回云闪付主界面')
        self.open_control(lambda: any(n.get('selected') == 'true' for n in
                                      self.nodes(rid='tv_tab_name', text='首页')),
                          '未切换回云闪付首页', rid='tv_tab_name', text='首页')
        for _ in range(8):
            if self.on_home():
                return
            self.swipe(y1=.32, y2=.78)
            time.sleep(1)
        self.wait_for(self.on_home, '未恢复云闪付首页顶部')

    def launch(self):
        self.start()
        self.app_home()

    def pay(self):
        self.app_home()
        self.click(rid='firstItem')
        self.wait_for(lambda: self.has(rid='tv_title', text='收付款')
                      or self.has(rid='btn_next') and self.has(rid='btn_register'),
                      '未进入收付款页')
        if self.has(rid='btn_next') and self.has(rid='btn_register'):
            raise RuntimeError('云闪付收付款需要登录测试账号；当前为手机号登录页')
        # 用例表要求“收付款，并返回”，扫一扫从首页独立进入。
        self.app_home()

    def scan(self):
        if self.has(rid='tv_upper_skid', text='扫一扫'):
            self.open_control(lambda: self.has(rid='tv_scan_help_tip'),
                              '未进入扫一扫页，请检查相机权限', rid='tv_upper_skid')
        else:
            # 部分版本/账户的收付款页不提供扫码入口。
            if not self.on_home():
                self.app_home()
            self.open_control(lambda: self.has(rid='tv_scan_help_tip'),
                              '未进入扫一扫页，请检查相机权限', rid='thirdItem')

    def rescan(self):
        self.app_home()
        self.scan()

    def offer(self):
        self.app_home()
        self.open_control(lambda: self.has(rid='recommend_label'), '未进入优惠页',
                          rid='tv_tab_name', text='优惠')

    def life(self):
        if self.has(text='惠生活'):
            self.click(text='惠生活')
            self.wait_for(lambda: not self.has(rid='recommend_label'), '未打开惠生活')
        else:
            self.reveal('未找到优惠生活分类', rid='tv_recommend_classify_title', text='生活')
            self.select_category('生活')
            self.wait_for(lambda: self.has(rid='ticket_name'), '生活优惠未加载')

    def select_category(self, label):
        self.open_control(lambda: any(n.get('selected') == 'true' for n in
                                      self.nodes(rid='tv_recommend_classify_title', text=label)),
                          '优惠分类未切换至{}'.format(label),
                          rid='tv_recommend_classify_title', text=label)

    def food(self):
        # 生活为页内分类时不按返回，否则会离开优惠页。
        if not self.has(rid='tv_tab_name', text='优惠'):
            self.back()
        self.reveal('未返回优惠页的美食分类', rid='tv_recommend_classify_title', text='美食')
        self.select_category('美食')
        self.wait_for(lambda: self.has(rid='ticket_name'), '美食优惠未加载')

    def steps(self):
        return [
            ('启动云闪付', self.launch, 3),
            ('主页浏览，上下各滑动1次，循环5次', lambda: self.alternating(5), 0),
            ('点击收付款', self.pay, 1),
            ('点击扫一扫', self.scan, 1),
            ('返回云闪付首页，点击扫一扫', self.rescan, 1),
            ('点击优惠', self.offer, 1),
            ('浏览优惠页，上下各滑动1次，循环5次', lambda: self.alternating(5), 0),
            ('点击惠生活', self.life, 1),
            ('浏览惠生活，上下各滑动1次', lambda: self.browse(1, 1), 0),
            ('返回优惠页，点击美食', self.food, 1),
            ('返回云闪付主界面', self.app_home, 1),
            ('滑动返回Home页', self.home, 1),
        ]
