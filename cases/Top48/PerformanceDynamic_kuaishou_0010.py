"""快手浏览推荐视频；动态性能模型测试用例7.xlsx 第947～953行。"""
from Cases.Top48.kuaishou_common import KuaishouDynamicCase


class PerformanceDynamic_kuaishou_0010(KuaishouDynamicCase):
    def steps(self):
        return [
            ('启动快手', self.launch, 5),
            ('精选页面上滑切换视频播放10s重复3次', self.featured_videos, 0),
            ('点击评论拉起评论页', self.open_comments, 2),
            ('评论页上滑2次下滑2次返回视频页', self.browse_comments, 2),
            ('点击赞', self.like, 2),
            ('点击收藏', self.collect, 2),
            ('滑动返回Home页', self.home, 2),
        ]
