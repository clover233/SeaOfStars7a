"""对应动态性能模型测试用例7.xlsx：哔哩哔哩 0040。"""
from Cases.Top48.bilibili_common import BilibiliDynamicCase


class PerformanceDynamic_bilibili_0040(BilibiliDynamicCase):
    def steps(self):
        return [
            ('启动哔哩哔哩', self.launch, 3),
            ('点击搜索框', self.search_box, 1),
            ('输入华为终端并搜索', self.search_huawei, 1),
            ('上滑5次浏览搜索结果', lambda: self.browse(up=5, down=0), 1),
            ('下滑5次浏览搜索结果', lambda: self.browse(up=0, down=5), 1),
            ('点击一个视频播放', self.video, 1),
            ('观看10秒视频', self.playing_video, 10),
            ('点击UP头像进入主页', self.up_page, 1),
            ('上滑5次浏览UP主页', lambda: self.browse(up=5, down=0), 1),
            ('下滑5次浏览UP主页', lambda: self.browse(up=0, down=5), 1),
            ('返回哔哩哔哩主界面', self.home, 1),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
