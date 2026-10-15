"""七猫频道、分类与搜索浏览；Excel 第 1222～1237 行。"""
from Cases.Top48.qimao_common import QimaoDynamicCase


class PerformanceDynamic_qimao_0020(QimaoDynamicCase):
    def steps(self):
        return [
            ('启动七猫免费小说', self.launch, 2),
            ('主页上滑3次、下滑3次', lambda: self.browse(3, 3), 0),
            ('点击小说', lambda: self.channel('小说'), 2),
            ('小说页上滑2次、下滑2次', lambda: self.browse(2, 2), 0),
            ('点击短剧', lambda: self.channel('短剧'), 2),
            ('短剧页上滑2次、下滑2次', lambda: self.browse(2, 2), 0),
            ('点击分类', self.category, 2),
            ('点击现代言情', self.modern_romance, 2),
            ('现代言情上滑2次、下滑2次', lambda: self.browse(2, 2), 0),
            ('点击最高评分', self.highest_rating, 2),
            ('评分结果上滑2次、下滑2次', lambda: self.browse(2, 2), 0),
            ('返回七猫主界面', self.return_main, 2),
            ('点击搜索框', self.open_search, 1),
            ('输入“长生”并搜索', self.search_changsheng, 2),
            ('返回七猫主界面', self.return_main, 2),
            ('滑动返回Home页', self.home, 2),
        ]
