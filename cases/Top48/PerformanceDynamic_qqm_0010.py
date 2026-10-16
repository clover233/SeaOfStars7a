"""QQ音乐播放和收藏；用例表1280～1307行。"""
from Cases.Top48.tencent_media_common import QqMusicDynamicCase


class PerformanceDynamic_qqm_0010(QqMusicDynamicCase):
    def steps(self):
        return [
            ('启动QQ音乐', self.launch, 2),
            ('点击我的', self.my_page, 2),
            ('点击最近', self.recent, 2),
            ('最近页面，上滑2次，下滑2次', self.browse_recent, 2),
            ('返回我的页', self.my_page, 2),
            ('点击本地', self.local, 2),
            ('返回我的页', self.my_page, 2),
            ('点击首页', self.home_page, 2),
            ('点击搜索框', self.search_page, 2),
            ('输入红旗飘飘并搜索', self.search_song, 2),
            ('点击歌手', self.singers, 2),
            ('点击综合', self.comprehensive, 2),
            ('综合页面，上滑2次，下滑2次', self.browse_results, 2),
            ('点击搜索后的第一个结果进行播放20s', self.first_song, 2),
            ('点击查看播放详情', self.player, 2),
            ('点击暂停播放', self.pause_song, 2),
            ('点击收藏后取消收藏', self.favorite_roundtrip, 2),
            ('切换到歌词界面后返回到播放界面', self.lyrics_roundtrip, 2),
            ('返回到首页', self.home_page, 2),
            ('点击排行榜', self.ranks, 2),
            ('排行榜页面，上滑2次，下滑2次', self.browse_ranks, 2),
            ('点击热歌榜', self.hot_rank, 2),
            ('返回排行榜', self.back_ranks, 2),
            ('切换到新歌榜', self.new_rank, 2),
            ('点击分享', self.rank_share, 2),
            ('点击音乐卡片', self.music_card, 2),
            ('返回QQ音乐主界面', self.home_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
