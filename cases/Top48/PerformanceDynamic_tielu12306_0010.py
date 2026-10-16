"""12306浏览车票信息；用例表1506～1516行。"""
from Cases.Top48.railway_common import RailwayDynamicCase


class PerformanceDynamic_tielu12306_0010(RailwayDynamicCase):
    def steps(self):
        return [
            ('启动铁路12306', self.launch, 2),
            ('向上抛滑1次，浏览首页', self.browse_home_up, 2),
            ('向下抛滑2次，浏览首页', self.browse_home_down, 2),
            ('点击首页的查询车票', self.tickets, 2),
            ('向上抛滑2次，浏览信息', self.results_up, 2),
            ('向下抛滑3次，浏览信息', self.results_down, 2),
            ('点击耗时最短', self.shortest, 2),
            ('点击发时最早', self.earliest, 2),
            ('点击价格最低', self.cheapest, 2),
            ('返回铁路12306主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
