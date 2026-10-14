"""抖音推荐视频与评论浏览（表格第 516～525 行）。"""
from Cases.Top48.douyin_common import DouyinDynamicCase


class PerformanceDynamic_douyin_0010(DouyinDynamicCase):
    all_app_package_list = [DouyinDynamicCase.PACKAGE]

    def steps(self):
        return [
            ('启动抖音', self.launch, 3),
            ('浏览推荐视频3次', lambda: self.browse_videos(3), 0),
            ('点击评论按钮，评论区上滑1次', lambda: (self.open_comments(), self.browse_comments()), 1),
            ('关闭评论并浏览推荐视频3次', lambda: (self.back(), self.browse_videos(3)), 0),
            ('点击评论按钮，评论区上滑1次', lambda: (self.open_comments(), self.browse_comments()), 1),
            ('点击评论输入框', self.focus_comment, 1),
            ('输入我是评论ABC', self.type_comment, 1),
            ('点击发送', self.send_comment, 2),
            ('返回抖音主界面', self.return_feed, 2),
            ('滑动返回Home页', self.home, 1),
        ]
