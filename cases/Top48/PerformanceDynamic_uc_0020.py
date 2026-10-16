"""UC浏览器搜索和浏览；用例表1539～1547行。"""
from Cases.Top48.uc_common import UcDynamicCase


class PerformanceDynamic_uc_0020(UcDynamicCase):
    def steps(self):
        return [
            ('启动UC浏览器', self.launch, 2),
            ('点击搜索框', self.search_page, 2),
            ('输入大话天仙，进行搜索', self.movie_search, 2),
            ('上下各滑动5次浏览搜索结果', self.browse_search, 2),
            ('返回搜索页面', self.return_search, 2),
            ('点击第一条搜索发现', self.first_discovery, 2),
            ('上下滑动各5次浏览详情', self.browse_discovery, 2),
            ('返回UC浏览器主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
