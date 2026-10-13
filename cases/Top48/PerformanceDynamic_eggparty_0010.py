"""Excel 第 664–665 行：仅启动蛋仔派对，然后上滑返回桌面。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_eggparty_0010(DynamicAppCase):
    PACKAGE = 'com.netease.party'
    all_app_package_list = [PACKAGE]

    def home(self):
        # 横屏游戏的防误触会拦截第一次底边手势，需在提示期间再次上滑。
        self.swipe(.5, .995, .5, .62, 250)
        time.sleep(.5)
        if 'launcher' not in self.current_app()['activity'].lower():
            self.swipe(.5, .995, .5, .62, 250)
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(),
                      '游戏底边上滑后未返回桌面', timeout=8)

    def steps(self):
        return [
            ('启动蛋仔派对', self.start, 3),
            ('滑动返回Home页', self.home, 1),
        ]
