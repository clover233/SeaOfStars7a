"""今日头条首页、热榜和推荐文章浏览；Excel 第 929～939 行。"""
from Cases.Top48.jrtt_common import JrttDynamicCase


class PerformanceDynamic_jrtt_0010(JrttDynamicCase):
    def steps(self):
        return [
            ('启动今日头条', self.launch, 3),
            ('主页浏览上滑5次、下滑5次', lambda: self.browse(5, 5), 0),
            ('点击热榜tab', self.hot_list, 2),
            ('热榜上滑2次、下滑2次', lambda: self.browse(2, 2), 0),
            ('点击热榜第一条', self.first_hot_item, 2),
            ('热榜第一条上滑5次、下滑5次', lambda: self.browse(5, 5), 0),
            ('返回热榜页面', self.return_hot, 2),
            ('返回推荐页，点击第一条文章', self.first_recommended_article, 2),
            ('文章页上滑5次、下滑5次', lambda: self.browse(5, 5), 0),
            ('返回今日头条主界面', self.return_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
