"""高德导航在小红书和抖音间切换后继续运行并退出。"""
from Cases.Top48.autonavi_common import AutonaviDynamicCase


class PerformanceDynamic_autonavi_0060(AutonaviDynamicCase):
    all_app_package_list = [AutonaviDynamicCase.AMAP, AutonaviDynamicCase.XHS,
                            AutonaviDynamicCase.DOUYIN]

    def station_search(self):
        self.search('西安北站')

    def station_route(self):
        self.result_route('西安北站')
        self.start_navigation()

    def xhs_home(self):
        self.xhs_tab('首页')

    def xhs_favorites(self):
        self.xhs_tab('收藏')

    def xhs_me(self):
        self.PACKAGE = self.XHS
        self.transition(lambda: self.click_node(text='我', class_name='android.widget.TextView'),
                        lambda: self.has(text='收藏'), '未进入小红书个人页')

    def xhs_messages(self):
        self.PACKAGE = self.XHS
        self.click_node(text='消息', class_name='android.widget.TextView')
        self.wait_for(lambda: not self.has(desc='发现'), '未进入小红书消息页')

    def resume_amap(self):
        self.launch(self.AMAP)
        self.navigation_visible()

    def exit_nav(self):
        self.open_exit()
        self.confirm_exit()

    def steps(self):
        return [
            ('启动高德地图', lambda: (self.launch(), self.amap_home()), 3),
            ('点击搜索框', self.search_page, 1),
            ('输入西安北站并搜索', self.station_search, 2),
            ('点击第一个搜索结果的路线', lambda: self.result_route('西安北站'), 2),
            ('点击开始导航', self.start_navigation, 2),
            ('滑动返回Home页', self.home_gesture, 1),
            ('启动小红书', lambda: self.launch(self.XHS), 3),
            ('浏览首页，上滑5次，下滑5次', lambda: self.scroll_page(up=5, down=5), 1),
            ('点击消息', self.xhs_messages, 2),
            ('点击我', self.xhs_me, 2),
            ('点击收藏', self.xhs_favorites, 2),
            ('浏览收藏页，上滑2次，下滑2次', lambda: self.scroll_page(up=2, down=2), 1),
            ('返回小红书主界面', self.xhs_home, 2),
            ('滑动返回Home页', self.home_gesture, 1),
            ('启动高德地图', self.resume_amap, 2),
            ('滑动返回Home页', self.home_gesture, 1),
            ('启动抖音', lambda: self.launch(self.DOUYIN), 3),
            ('首页观看10s', lambda: self.wait_for(lambda: self.has(text='首页'), '未进入抖音首页'), 10),
            ('浏览首页，上滑5次，下滑5次', lambda: self.scroll_page(up=5, down=5), 1),
            ('点击顶部热点', lambda: self.douyin_tab('热点'), 2),
            ('浏览热点页面，上滑5次，下滑5次', lambda: self.scroll_page(up=5, down=5), 1),
            ('点击推荐', lambda: self.douyin_tab('推荐'), 2),
            ('滑动返回Home页', self.home_gesture, 1),
            ('启动高德地图', self.resume_amap, 2),
            ('退出导航', self.exit_nav, 2),
            ('返回高德地图主界面', self.amap_home, 2),
            ('滑动返回Home页', self.home_gesture, 1),
        ]
