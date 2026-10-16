"""瑞幸微信小程序浏览；用例表1725～1733行。"""
from Cases.Top48.weixin_common import WeixinDynamicCase


class PerformanceDynamic_weixin_0070(WeixinDynamicCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('下滑调出最近小程序页面', self.recent_minis, 2),
            ('点击瑞幸小程序，切换到瑞幸咖啡页面', self.luckin, 2),
            ('点击菜单，切换到菜单页', self.luckin_menu, 2),
            ('点击人气top', self.luckin_top, 2),
            ('点击第一个商品', self.luckin_product, 2),
            ('点击加入购物车', self.luckin_cart, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
