"""抖音收藏、喜欢和钱包浏览（表格第 622～634 行）。"""
from Cases.Top48.douyin_common import DouyinDynamicCase


class PerformanceDynamic_douyin_0070(DouyinDynamicCase):
    all_app_package_list = [DouyinDynamicCase.PACKAGE]

    def back_me(self):
        self.return_to(lambda: bool(self.contains_nodes(text='我的钱包')),
                       '未返回抖音个人页')

    def steps(self):
        return [
            ('启动抖音', self.launch, 3),
            ('点击我', self.open_me, 2),
            ('点击收藏', lambda: self.open_profile_tab('收藏'), 2),
            ('点击第一个收藏作品', lambda: self.open_first_profile_work('收藏'), 2),
            ('上滑3次浏览收藏作品', lambda: self.browse(3, 0), 0),
            ('返回我的页面', self.back_me, 2),
            ('点击喜欢', lambda: self.open_profile_tab('喜欢'), 2),
            ('点击第一个喜欢作品', lambda: self.open_first_profile_work('喜欢'), 2),
            ('上滑3次浏览喜欢作品', lambda: self.browse(3, 0), 0),
            ('返回我的页面', self.back_me, 2),
            ('点击我的钱包', self.open_wallet, 2),
            ('返回抖音主界面', self.return_feed, 2),
            ('滑动返回Home页', self.home, 1),
        ]
