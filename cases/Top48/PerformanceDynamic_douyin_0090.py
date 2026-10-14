"""抖音直播间小黄车浏览（表格第 646～652 行）。"""
from Cases.Top48.douyin_common import DouyinDynamicCase


class PerformanceDynamic_douyin_0090(DouyinDynamicCase):
    all_app_package_list = [DouyinDynamicCase.PACKAGE]

    def steps(self):
        return [
            ('启动抖音', self.launch, 3),
            ('点击直播栏进入直播页面', self.open_live_hall, 2),
            ('点击第一个直播间', self.enter_live_room, 3),
            ('点击小黄车进入商品页', self.open_live_cart, 2),
            ('小黄车页面上滑5次、下滑5次', self.browse_live_cart, 0),
            ('返回抖音主界面', self.return_feed, 2),
            ('滑动返回Home页', self.home, 1),
        ]
