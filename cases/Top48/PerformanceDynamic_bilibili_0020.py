"""对应动态性能模型测试用例7.xlsx：哔哩哔哩 0020。"""
from Cases.Top48.bilibili_common import BilibiliDynamicCase


class PerformanceDynamic_bilibili_0020(BilibiliDynamicCase):
    def steps(self):
        return [
            ('启动哔哩哔哩', self.launch, 3),
            ('点击推荐', lambda: self.channel('推荐'), 1),
            ('浏览推荐，上滑5次下滑5次', self.browse, 1),
            ('点击热门', lambda: self.channel('热门'), 1),
            ('点击第一个视频播放', self.video, 1),
            ('点击视频UP主', self.up_page, 1),
            ('浏览UP主，上滑5次下滑5次', self.browse, 1),
            ('点击UP主第一个视频播放', self.up_video, 1),
            ('点击视频下的评论', self.comments, 1),
            ('浏览评论，上滑5次下滑5次', self.browse, 1),
            ('返回哔哩哔哩主界面', self.home, 1),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
