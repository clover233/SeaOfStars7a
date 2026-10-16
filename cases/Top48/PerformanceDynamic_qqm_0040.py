"""QQ音乐播放；用例表1308～1311行。"""
from Cases.Top48.tencent_media_common import QqMusicDynamicCase


class PerformanceDynamic_qqm_0040(QqMusicDynamicCase):
    def steps(self):
        return [
            ('启动QQ音乐', self.launch, 2),
            ('浏览首页，上滑2次，下滑2次', self.browse_home, 2),
            ('点击一个音乐卡片进行播放', self.home_music, 2),
            ('滑动返回Home页', self.home, 2),
        ]
