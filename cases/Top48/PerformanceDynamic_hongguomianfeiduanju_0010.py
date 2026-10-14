"""红果免费短剧推荐、剧场榜单和观看历史浏览；对应 Excel 第 701～721 行。"""
from Cases.Top48.hongguo_common import HongguoDynamicCase


class PerformanceDynamic_hongguomianfeiduanju_0010(HongguoDynamicCase):
    def steps(self):
        return [
            ('启动红果免费短剧', self.launch, 3),
            ('向上抛滑5次，浏览首页', lambda: self.browse(5, 0), 0),
            ('向下抛滑5次，浏览首页', lambda: self.browse(0, 5), 0),
            ('点击剧场按钮，进入剧场页面', self.theater, 2),
            ('向上滑动5次，浏览找剧页面', lambda: self.browse(5, 0), 0),
            ('向下滑动5次，浏览找剧页面', lambda: self.browse(0, 5), 0),
            ('点击排行榜，进入红果推荐榜', self.open_rank, 2),
            ('向上滑动5次，浏览红果推荐榜', lambda: self.browse(5, 0), 0),
            ('向下滑动5次，浏览红果推荐榜', lambda: self.browse(0, 5), 0),
            ('点击推荐榜第一的短剧，观看视频15秒', self.play_first_rank, 15),
            ('返回红果推荐榜', self.return_to_rank, 2),
            ('点击热播榜', lambda: self.select_rank('热播榜'), 2),
            ('向上滑动5次，浏览热播榜', lambda: self.browse(5, 0), 0),
            ('向下滑动5次，浏览热播榜', lambda: self.browse(0, 5), 0),
            ('点击热播榜第一的短剧，观看视频15秒', self.play_first_rank, 15),
            ('返回剧场界面', self.return_to_theater, 2),
            ('点击我的，进入我的界面', self.mine, 2),
            ('上滑一次，浏览观看历史', lambda: self.browse(1, 0), 0),
            ('下滑一次，浏览观看历史', lambda: self.browse(0, 1), 0),
            ('点击首页', lambda: self.switch_bottom('首页'), 2),
            ('滑动返回Home页', self.home, 1),
        ]
