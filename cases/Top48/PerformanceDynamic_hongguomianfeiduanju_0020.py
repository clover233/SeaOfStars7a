"""红果免费短剧推荐视频、评论、搜索和横屏播放；对应 Excel 第 722～739 行。"""
from Cases.Top48.hongguo_common import HongguoDynamicCase


class PerformanceDynamic_hongguomianfeiduanju_0020(HongguoDynamicCase):
    def steps(self):
        return [
            ('启动红果免费短剧', self.launch, 3),
            ('长按首页推荐视频倍速播放', self.speed_play, 1),
            ('点击评论按钮', self.open_comments, 2),
            ('上滑3次，浏览评论', lambda: self.browse(3, 0), 0),
            ('下滑3次，浏览评论', lambda: self.browse(0, 3), 0),
            ('侧滑退出评论', self.close_comments_by_swipe, 1),
            ('点击剧场', self.theater, 2),
            ('再次点击剧场', self.refresh_theater, 1),
            ('点击上方搜索', self.open_search, 1),
            ('搜索仙帝', lambda: self.search('仙帝'), 2),
            ('上滑3次，浏览搜索结果', lambda: self.browse(3, 0), 0),
            ('下滑3次，浏览搜索结果', lambda: self.browse(0, 3), 0),
            ('点击进入第一条搜索结果', self.play_first_search_result, 2),
            ('竖屏观看视频10秒', self.watch_portrait, 10),
            ('切换至横屏观看视频20秒', self.fullscreen, 20),
            ('返回剧场界面', self.return_to_theater, 2),
            ('点击首页', lambda: self.switch_bottom('首页'), 2),
            ('滑动返回Home页', self.home, 1),
        ]
