"""腾讯视频浏览和播放；用例表1462～1475行。"""
from Cases.Top48.tencent_media_common import TencentVideoDynamicCase


class PerformanceDynamic_tencentvideo_0010(TencentVideoDynamicCase):
    def steps(self):
        return [
            ('启动腾讯视频', self.launch, 2),
            ('首页浏览，上滑2次，下滑2次', self.browse_home, 2),
            ('点击首页第一个推荐视频播放30s', self.first_video, 2),
            ('切换到全屏模式', self.fullscreen, 10),
            ('退出全屏模式', self.exit_fullscreen, 2),
            ('浏览屏幕底部推荐视频，上滑3次，下滑3次', self.browse_recommendations, 2),
            ('返回腾讯视频主界面', self.main_page, 2),
            ('点击搜索框', self.search_page, 2),
            ('输入斗破苍穹并搜索', self.search_drama, 2),
            ('上滑3次，下滑3次浏览搜索结果', self.browse_results, 2),
            ('点击影视，切换到影视界面', self.film_tab, 2),
            ('上滑1次，下滑1次，浏览影视搜索结果', self.browse_films, 2),
            ('返回腾讯视频主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
