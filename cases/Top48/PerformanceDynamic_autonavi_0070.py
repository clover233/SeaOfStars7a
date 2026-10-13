"""开始西安北站导航后返回桌面，导航留在后台供 0080 接续。"""
from Cases.Top48.autonavi_common import AutonaviDynamicCase


class PerformanceDynamic_autonavi_0070(AutonaviDynamicCase):
    def station_search(self):
        self.search('西安北站')

    def station_route(self):
        self.result_route('西安北站')
        self.drive()

    def steps(self):
        return [
            ('启动高德地图', lambda: (self.launch(), self.amap_home()), 3),
            ('点击搜索框', self.search_page, 1),
            ('输入西安北站并搜索', self.station_search, 2),
            ('点击第一个搜索结果的路线', self.station_route, 2),
            ('点击开始导航', self.start_navigation, 2),
            ('滑动返回Home页', self.home_gesture, 1),
        ]
