"""淘宝浏览和关注；用例表1427～1441行。"""
from Cases.Top48.travel_shop_common import TaobaoDynamicCase


class PerformanceDynamic_taobao_0020(TaobaoDynamicCase):
    def steps(self):
        return [
            ('启动淘宝', self.launch, 2),
            ('点击推荐，切换到推荐页面', self.recommend, 2),
            ('点击切换第三个tab图标页面', self.third_tab, 2),
            ('第三个tab图标页面，上滑5次，下滑5次', self.browse_third, 2),
            ('返回淘宝主界面', self.main_page, 2),
            ('推荐页面上滑5次，下滑5次', self.browse_recommend, 2),
            ('点击关注，切换到关注页面', self.following, 2),
            ('关注页面上滑5次，下滑5次', self.browse_following, 2),
            ('点击tab栏逛逛，切换到逛页面', self.explore, 2),
            ('浏览逛逛页面，上滑5次，下滑5次，右滑3次，左滑3次', self.browse_explore, 2),
            ('点击tab栏我的淘宝，切换到我的淘宝页面', self.my_taobao, 2),
            ('点击我的订单，切换到我的订单页面', self.orders, 2),
            ('浏览订单页面，左滑5次，右滑5次', self.browse_orders, 2),
            ('返回淘宝主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
