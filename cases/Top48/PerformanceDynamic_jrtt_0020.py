"""今日头条视频和评论浏览；Excel 第 940～946 行。"""
from Cases.Top48.jrtt_common import JrttDynamicCase


class PerformanceDynamic_jrtt_0020(JrttDynamicCase):
    def steps(self):
        return [
            ('启动今日头条', self.launch, 3),
            ('点击视频', self.video_page, 2),
            ('滑动浏览视频上滑5次、下滑5次', lambda: self.browse(5, 5), 0),
            ('点击评论按钮', self.open_comments, 2),
            ('滑动浏览评论上滑2次、下滑2次', self.browse_comments, 0),
            ('返回今日头条主界面', self.return_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
