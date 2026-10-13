"""高德地图导航至西安北站北进站口。"""
from Cases.Top48.autonavi_common import AutonaviDynamicCase


class PerformanceDynamic_autonavi_0010(AutonaviDynamicCase):
    RESULT = '西安北站(北进站口)'

    def plan_and_navigate(self):
        self.result_route(self.RESULT)
        self.drive()
        self.start_navigation()

    def steps(self):
        return [
            ('启动高德地图', lambda: (self.launch(), self.amap_home()), 3),
            ('点击搜索框，搜索西安北站北进站口',
             lambda: (self.search_page(), self.search('西安北站北进站口', self.RESULT)), 2),
            ('点击路线，点击驾车，点击开始导航', self.plan_and_navigate, 2),
            ('导航界面停留10s', self.navigation_visible, 10),
            ('点击退出，切换到退出导航界面', self.open_exit, 0),
            ('点击退出导航，结束导航', self.confirm_exit, 2),
            ('返回高德地图主界面', self.amap_home, 2),
            ('滑动返回Home页', self.home_gesture, 1),
        ]
