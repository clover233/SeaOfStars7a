"""爱奇艺频道浏览与“大话天仙”搜索播放；Excel 第 1238～1250 行。"""
from Cases.Top48.qiyi_common import QiyiDynamicCase


class PerformanceDynamic_qiyi_0030(QiyiDynamicCase):
    def steps(self):
        return [
            ('启动爱奇艺', self.launch, 2),
            ('主页上滑5次、下滑5次', lambda: self.browse(5, 5), 0),
            ('点击电视剧tab', self.tv, 2),
            ('电视剧页上滑3次、下滑3次', lambda: self.browse(3, 3), 0),
            ('点击电影tab', self.movie, 2),
            ('电影页上滑3次、下滑3次', lambda: self.browse(3, 3), 0),
            ('返回推荐页并点击搜索', self.open_search, 1),
            ('输入“大话天仙”', self.input_movie, 1),
            ('搜索“大话天仙”，重复2次', self.search_twice, 2),
            ('播放“大话天仙”并观看30秒', self.play_movie, 30),
            ('播放页上滑5次、下滑5次', lambda: self.browse(5, 5), 0),
            ('返回爱奇艺主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
