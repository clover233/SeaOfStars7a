"""腾讯新闻浏览；用例表1456～1461行。"""
from Cases.Top48.tencent_media_common import TencentNewsDynamicCase


class PerformanceDynamic_tencentnews_0010(TencentNewsDynamicCase):
    def steps(self):
        return [
            ('启动腾讯新闻', self.launch, 2),
            ('首页浏览，上滑5次，下滑5次', self.browse_home, 2),
            ('首页浏览，左滑5次，右滑5次', self.channels, 2),
            ('点击查看首页新闻内容', self.first_news, 2),
            ('新闻页面上滑2次，下滑2次', self.browse_article, 2),
            ('滑动返回Home页', self.home, 2),
        ]
