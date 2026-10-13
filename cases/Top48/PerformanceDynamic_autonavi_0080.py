"""接续 0070 的后台导航，退出后返回高德首页和桌面。"""
from Cases.Top48.autonavi_common import AutonaviDynamicCase


class PerformanceDynamic_autonavi_0080(AutonaviDynamicCase):
    def resume_navigation(self):
        self.launch()
        self.navigation_visible()

    def exit_to_home(self):
        self.open_exit()
        self.confirm_exit()
        self.amap_home()

    def steps(self):
        return [
            ('启动高德地图', self.resume_navigation, 2),
            ('进入导航页面后退出后台导航返回首页', self.exit_to_home, 2),
            ('滑动返回Home页', self.home_gesture, 1),
        ]
