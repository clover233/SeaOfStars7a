"""同花顺管理自选股票；用例表1496～1505行。"""
from Cases.Top48.ths_common import ThsDynamicCase


class PerformanceDynamic_ths_0050(ThsDynamicCase):
    def steps(self):
        return [
            ('启动同花顺', self.launch, 2),
            ('点击自选', self.watchlist, 2),
            ('点击搜索按钮', self.stock_search, 2),
            ('输入格力电器', self.stock_query, 2),
            ('点击格力电器股票', self.stock_detail, 2),
            ('点击加自选', self.add_watch, 2),
            ('上滑3次浏览格力电器股票', self.browse_stock, 2),
            ('点击删自选', self.remove_watch, 2),
            ('返回同花顺主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
