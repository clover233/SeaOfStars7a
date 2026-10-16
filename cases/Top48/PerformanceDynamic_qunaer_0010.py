"""去哪儿旅行预订机票和酒店；用例表1315～1333行。"""
from Cases.Top48.travel_shop_common import QunarDynamicCase


class PerformanceDynamic_qunaer_0010(QunarDynamicCase):
    def steps(self):
        return [
            ('启动去哪儿旅行', self.launch, 2),
            ('点击机票，进入机票搜索页面', self.flight_page, 2),
            ('点击搜索，进入机票搜索结果页面', self.flight_search, 2),
            ('点击明天', self.tomorrow, 2),
            ('上滑5次、下滑5次，机票搜索结果页面', self.browse_flights, 2),
            ('上滑到最顶，点击第一个机票方案', self.first_flight, 2),
            ('上滑1次、下滑1次，浏览第一个机票方案', self.browse_flight, 2),
            ('返回去哪儿旅行主界面', self.main_page, 2),
            ('点击酒店，进入酒店页面', self.hotel_page, 2),
            ('点击城市，选择西安', self.xian, 2),
            ('点击酒店订单，进入订单页面', self.hotel_orders, 2),
            ('返回酒店界面', self.return_hotel, 2),
            ('点击开始搜索，进入酒店搜索结果页面', self.hotel_search, 2),
            ('滑动浏览酒店搜索结果，上滑3次，下滑3次', self.browse_hotels, 2),
            ('点击第一条搜索结果，进入酒店详情界面', self.first_hotel, 2),
            ('点击酒店图片，查看酒店图片详情', self.hotel_pictures, 2),
            ('滑动浏览，左滑3次，右滑3次', self.browse_pictures, 2),
            ('返回去哪儿旅行主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
