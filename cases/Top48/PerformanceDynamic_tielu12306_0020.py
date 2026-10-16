"""12306浏览酒店和会员；用例表1517～1526行。"""
from Cases.Top48.railway_common import RailwayDynamicCase


class PerformanceDynamic_tielu12306_0020(RailwayDynamicCase):
    def steps(self):
        return [
            ('启动铁路12306', self.launch, 2),
            ('上滑2次，浏览首页', self.home_up_twice, 2),
            ('点击酒店住宿，进入酒店住宿页面', self.hotel, 2),
            ('返回铁路12306主界面', self.main_page, 2),
            ('点击出行服务，进入出行服务页面', self.travel_services, 2),
            ('点击订单，进入订单页面', self.orders, 2),
            ('点击铁路会员，进入会员页面', self.membership, 2),
            ('点击首页，进入首页', self.main_page, 2),
            ('下滑2次，浏览首页', self.browse_home_down, 2),
            ('滑动返回Home页', self.home, 2),
        ]
