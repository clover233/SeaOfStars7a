"""微信服务和支付；用例表1774～1788行。"""
from Cases.Top48.weixin_extended import WeixinExtendedCase


class PerformanceDynamic_weixin_0110(WeixinExtendedCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击我', self.me, 2),
            ('点击服务', self.service, 2),
            ('点击钱包', self.wallet, 2),
            ('点击零钱', self.balance, 2),
            ('返回服务页面', self.return_service, 2),
            ('点击手机充值', self.top_up, 2),
            ('返回服务页面', self.return_service, 2),
            ('点击生活缴费', self.utilities, 2),
            ('点击电费', self.electricity, 2),
            ('点击第一个电网公司', self.first_provider, 2),
            ('返回我页面', self.me, 2),
            ('点击收藏', self.favorites, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
