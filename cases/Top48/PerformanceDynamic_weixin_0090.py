"""微信搜索和支付；用例表1748～1759行。"""
from Cases.Top48.weixin_common import WeixinExtendedCase


class PerformanceDynamic_weixin_0090(WeixinExtendedCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击搜索，切换到搜索页面', self.search_page, 2),
            ('搜索华为手机', self.search_huawei, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('点击右上角+号', self.plus_menu, 2),
            ('点击扫一扫，扫描二维码', self.scan_qr, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('点击右上角+号', self.plus_menu, 2),
            ('点击收付款，切换到收付款页面', self.pay_codes, 2),
            ('点击二维码收款', self.receive_code, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
