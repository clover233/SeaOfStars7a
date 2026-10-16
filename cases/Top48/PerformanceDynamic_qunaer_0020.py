"""去哪儿旅行预订火车票；用例表1334～1347行。"""
from Cases.Top48.travel_shop_common import QunarDynamicCase


class PerformanceDynamic_qunaer_0020(QunarDynamicCase):
    def steps(self):
        return [
            ('启动去哪儿旅行', self.launch, 2),
            ('点击机票，切换到机票页', self.flight_page, 2),
            ('点击搜索，查看搜索结果', self.flight_search, 2),
            ('点击搜索结果第一条查看详情', self.first_flight, 2),
            ('点击预订，切换到订票页面', self.booking, 2),
            ('滑动浏览订票页面，上滑2次，下滑2次', self.browse_booking, 2),
            ('侧滑3次返回机票页', self.return_flight, 2),
            ('点击值机选座，切换到选座页', self.checkin, 2),
            ('值机选座页上滑1次、下滑1次', self.browse_checkin, 2),
            ('侧滑返回去哪儿旅行主页', self.main_page, 2),
            ('点击火车高铁，进入搜索页面', self.train_page, 2),
            ('点击搜索，进入车次选择页面', self.train_search, 2),
            ('返回去哪儿旅行主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
