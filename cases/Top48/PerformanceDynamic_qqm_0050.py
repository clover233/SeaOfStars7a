"""QQ音乐暂停和退出；用例表1312～1314行。"""
from Cases.Top48.tencent_media_common import QqMusicDynamicCase


class PerformanceDynamic_qqm_0050(QqMusicDynamicCase):
    def steps(self):
        return [
            ('启动QQ音乐', self.launch, 2),
            ('QQ音乐首页，点击底部暂停按钮', self.pause, 2),
            ('滑动返回Home页', self.home, 2),
        ]
