"""汽水音乐搜索和播放；用例表1384～1395行。"""
from Cases.Top48.travel_shop_common import SodaMusicDynamicCase


class PerformanceDynamic_sodamusic_0010(SodaMusicDynamicCase):
    def steps(self):
        return [
            ('启动汽水音乐', self.launch, 2),
            ('点击右上角搜索', self.search_page, 2),
            ('搜索国歌', self.search_anthem, 2),
            ('上滑2次，下滑2次浏览国歌', self.browse_search, 2),
            ('返回首页', self.main_page, 2),
            ('点击下方播放按钮（如果播放中15s后直接暂停），播放15S后暂停', self.play_pause, 2),
            ('点击右下角我的', self.my_page, 2),
            ('点击我喜欢的音乐', self.favorites, 2),
            ('返回首页', self.main_page, 2),
            ('点击右上角三横线', self.header_menu, 2),
            ('返回汽水音乐主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
