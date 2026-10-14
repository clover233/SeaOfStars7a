"""抖音直播频道、直播间与小黄车浏览（表格第 526～534 行）。"""
from Cases.Top48.douyin_common import DouyinDynamicCase


class PerformanceDynamic_douyin_0020(DouyinDynamicCase):
    all_app_package_list = [DouyinDynamicCase.PACKAGE]

    def steps(self):
        return [
            ('启动抖音', self.launch, 3),
            ('点击直播栏，进入直播页面', self.open_live_hall, 2),
            ('上滑3次浏览直播页面', lambda: self.browse(3, 0), 0),
            ('点击进入直播间', self.enter_live_room, 3),
            ('上滑3次浏览直播间页面', lambda: self.browse_live_rooms(3), 0),
            ('点击直播间小黄车', self.open_live_cart, 2),
            ('小黄车页面上滑5次、下滑5次', self.browse_live_cart, 0),
            ('返回抖音主界面', self.return_feed, 2),
            ('滑动返回Home页', self.home, 1),
        ]
