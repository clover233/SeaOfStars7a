"""UC浏览器浏览新闻；用例表1527～1538行。"""
from Cases.Top48.uc_common import UcDynamicCase


class PerformanceDynamic_uc_0010(UcDynamicCase):
    def steps(self):
        return [
            ('启动UC浏览器', self.launch, 2),
            ('左滑5次切换顶部tab栏', self.channels_left, 2),
            ('上滑5次，下滑5次浏览当前页面', self.browse_feed, 2),
            ('右滑5次切换顶部tab栏', self.channels_right, 2),
            ('点击体育，切换到体育页', self.sports, 2),
            ('体育页浏览上滑5次，下滑5次', self.browse_sports, 2),
            ('点击推荐，切换到推荐页', self.recommend, 2),
            ('点击推荐下的第一条新闻', self.first_news, 2),
            ('浏览新闻内容，上下各滑动5次', self.browse_news, 2),
            ('返回首UC浏览器主界面', self.main_page, 2),
            ('浏览首页，上下各滑动5次', self.browse_feed, 2),
            ('滑动返回Home页', self.home, 2),
        ]
