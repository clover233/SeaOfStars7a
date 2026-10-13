"""对应动态性能模型测试用例7.xlsx：哔哩哔哩 0050。"""
from Cases.Top48.bilibili_common import BilibiliDynamicCase


class PerformanceDynamic_bilibili_0050(BilibiliDynamicCase):
    def steps(self):
        return [
            ('启动哔哩哔哩', self.launch, 3),
            ('点击直播进入直播页面', lambda: self.channel('直播'), 1),
            ('上滑5次下滑5次浏览直播页', self.browse, 1),
            ('点击第一个直播进入直播间', self.live_room, 1),
            ('上滑5次下滑5次浏览直播间', self.browse, 1),
            ('观看直播10秒', self.watching_live, 10),
            ('切换横屏观看直播20秒', self.live_fullscreen, 20),
            ('返回哔哩哔哩首页', self.home, 1),
            ('上滑返回桌面', self.launcher_gesture, 1),
        ]
