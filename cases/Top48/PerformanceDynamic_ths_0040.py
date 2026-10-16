"""同花顺浏览自选股票；用例表1490～1495行。"""
from Cases.Top48.ths_common import ThsDynamicCase


class PerformanceDynamic_ths_0040(ThsDynamicCase):
    def steps(self):
        return [
            ('启动同花顺', self.launch, 2),
            ('点击自选', self.watchlist, 2),
            ('上滑2次浏览自选股票', self.watch_up, 2),
            ('下滑2次浏览自选股票', self.watch_down, 2),
            ('返回同花顺主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
