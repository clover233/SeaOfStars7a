"""抖音推荐、关注和搜索作者主页浏览（表格第 557～576 行）。"""
from Cases.Top48.douyin_common import DouyinDynamicCase


class PerformanceDynamic_douyin_0040(DouyinDynamicCase):
    all_app_package_list = [DouyinDynamicCase.PACKAGE]

    def repeat_recommended_author(self):
        self.return_feed()
        self.browse_videos(5)
        self.open_current_author()
        self.return_feed()

    def back_profile(self):
        if not getattr(self, 'author_profile_available', False):
            return self.skip('未进入作者主页，跳过返回作者主页')
        if not self.profile_page():
            self.back()
        self.wait_for(self.profile_page, '未返回作者主页')

    def browse_author(self, up, down):
        if not getattr(self, 'author_profile_available', False):
            return self.skip('未进入作者主页，跳过作品列表浏览')
        self.browse(up, down)
        return True

    def repeat_two_search_visits(self):
        self.return_feed()
        for _ in range(2):
            self.search_author()
            if self.open_searched_author():
                self.browse(3, 3)
            self.return_feed()

    def steps(self):
        return [
            ('启动抖音', self.launch, 3),
            ('推荐页面上滑切换视频5次', lambda: self.browse_videos(5), 0),
            ('点击当前视频作者头像进入主页', self.open_current_author, 2),
            ('返回主界面并重复浏览推荐作者1次', self.repeat_recommended_author, 2),
            ('点击我，切换到我页面', self.open_me, 2),
            ('点击关注，切换到关注页面', self.open_following, 2),
            ('点击华为终端头像查看博主主页', self.open_followed_author, 2),
            ('博主主页上滑5次、下滑5次', lambda: self.browse_author(5, 5), 0),
            ('播放博主第1个视频15秒', lambda: self.play_profile_video(0), 0),
            ('返回博主主页', self.back_profile, 1),
            ('播放博主第2个视频15秒', lambda: self.play_profile_video(1), 0),
            ('返回博主主页', self.back_profile, 1),
            ('播放博主第3个视频15秒', lambda: self.play_profile_video(2), 0),
            ('返回博主主页', self.back_profile, 1),
            ('返回抖音主界面', self.return_feed, 2),
            ('搜索华为终端', self.search_author, 3),
            ('点击搜索结果作者头像进入主页', self.open_searched_author, 2),
            ('作者主页上滑3次、下滑3次', lambda: self.browse_author(3, 3), 0),
            ('返回主界面并将搜索浏览循环补足3次', self.repeat_two_search_visits, 2),
            ('滑动返回Home页', self.home, 1),
        ]
