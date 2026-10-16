"""动态性能场景；Excel「新-7.0.2模型测试步骤」第 1558～1576 行。"""
from Cases.Top48.weibo_common import WeiboDynamicCase


class PerformanceDynamic_weibo_0020(WeiboDynamicCase):
    def steps(self):
        return [
            ('启动微博', self.launch, 3),
            ('点击首页', self.main_page, 1),
            ('点击推荐', lambda: self.feed_tab('推荐'), 1),
            ('推荐页面上滑5次下滑6次', lambda: self.browse(5, 6), 2),
            ('点击关注', lambda: self.group('关注', self.following), 1),
            ('关注页面上滑5次下滑5次', lambda: self.within('关注', lambda: self.browse(5, 5)), 2),
            ('打开第一个直播博主', lambda: self.group('直播', lambda: self.within('关注', self.first_live)), 2),
            ('直播页面上滑5次下滑5次', lambda: self.within('直播', lambda: self.browse(5, 5)), 2),
            ('返回关注界面', lambda: self.within('关注', self.return_following), 1),
            ('长按底部视频tab', lambda: self.group('切换菜单', lambda: self.tab_menu('视频')), 1),
            ('点击超话（新版使用首页左上入口）', lambda: self.group('超话', self.super_topic), 2),
            ('超话页面上滑3次下滑3次', lambda: self.within('超话', lambda: self.browse(3, 3)), 2),
            ('点击第一条超话', lambda: self.group('超话详情', lambda: self.within('超话', self.first_super_topic)), 2),
            ('超话内容上滑3次下滑3次', lambda: self.within('超话详情', lambda: self.browse(3, 3)), 2),
            ('返回超话界面', lambda: self.within('超话', self.return_super_topic), 1),
            ('长按底部超话tab', lambda: self.group('恢复菜单', lambda: self.within('超话', lambda: self.tab_menu('超话'))), 1),
            ('切换回视频', lambda: self.within('恢复菜单', lambda: self.bottom_from_menu('视频')), 1),
            ('返回微博主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 1),
        ]
