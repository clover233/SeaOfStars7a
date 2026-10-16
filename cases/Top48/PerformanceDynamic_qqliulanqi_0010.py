"""QQ浏览器搜索和浏览；用例表1270～1279行。"""
from Cases.Top48.qqbrowser_common import QQBrowserDynamicCase


class PerformanceDynamic_qqliulanqi_0010(QQBrowserDynamicCase):
    def steps(self):
        return [
            ('启动QQ浏览器', self.launch, 3),
            ('点击搜索框', self.open_search, 1),
            ('输入学信网并搜索', self.search, 1),
            ('搜索结果上滑2次下滑2次', self.browse_results, 0),
            ('进入学信网官网', self.official, 1),
            ('官网上滑2次下滑2次', self.browse_site, 0),
            ('点击第一条可见内容', self.first_content, 1),
            ('内容详情上滑2次下滑2次', self.browse_detail, 0),
            ('返回QQ浏览器主界面', self.main_page, 1),
            ('滑动返回Home页', self.home, 1),
        ]
