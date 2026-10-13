"""TapTap 找游戏、评价、排行榜、社区和个人主页浏览。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_taptap_0010(DynamicAppCase):
    PACKAGE = 'com.taptap'
    all_app_package_list = [PACKAGE]
    TAB_ID = 'com.taptap.app.middle:id/tab_content'
    SEARCH_ID = 'com.taptap.app.community:id/iv_search'
    INPUT_ID = 'com.taptap.app.community:id/input_box'

    def navigation(self, name):
        height = self.d.window_size()[1]
        return [n for n in self.nodes(text=name) if self.bounds(n)[1] > height * .9]

    def selected(self, name):
        return any(n.get('selected') == 'true' for n in self.navigation(name))

    def switch_tab(self, name):
        def click_tab():
            nodes = self.navigation(name)
            if len(nodes) != 1:
                raise RuntimeError('TapTap 底部入口不可用：' + name)
            self.click_node(nodes[0])
        self.transition(click_tab, lambda: self.selected(name), 'TapTap 未切换到' + name)

    def main_page(self):
        self.return_to(lambda: bool(self.navigation('找游戏')), '未返回 TapTap 导航页')
        self.switch_tab('找游戏')

    def launch(self):
        self.start()
        self.main_page()

    def side_return(self):
        # 表格指定侧滑返回；从屏幕左缘按比例滑入，逐页确认导航恢复。
        for _ in range(6):
            if self.navigation('找游戏'):
                self.switch_tab('找游戏')
                return
            self.swipe(.005, .5, .45, .5, 300)
            time.sleep(1.5)
        raise RuntimeError('侧滑后未返回 TapTap 找游戏页')

    def search(self):
        self.open_control(lambda: self.has(rid=self.INPUT_ID), 'TapTap 搜索框未打开', rid=self.SEARCH_ID)
        self.d(resourceId=self.INPUT_ID, packageName=self.PACKAGE).set_text('王者荣耀')
        self.open_control(lambda: self.has(rid='com.taptap:id/title', text='王者荣耀'),
                          '王者荣耀搜索结果未加载', rid='com.taptap.app.community:id/tvSure')

    def first_result(self):
        results = sorted(self.nodes(rid='com.taptap:id/title'), key=lambda n: self.bounds(n)[1])
        if not results or results[0].get('text') != '王者荣耀':
            raise RuntimeError('首条搜索结果不是王者荣耀，停止打开')
        self.transition(lambda: self.click_node(results[0]),
                        lambda: self.has(text='评价', rid=self.TAB_ID), '游戏详情未打开')

    def reviews(self):
        self.open_control(lambda: self.has(text='全部评价', rid=self.TAB_ID),
                          '游戏评价页未打开', text='评价', rid=self.TAB_ID)

    def profile(self):
        self.open_control(lambda: self.has(rid='com.taptap.app.user:id/tv_user_id'),
                          '个人主页未打开，请确认已登录', text='个人主页')

    def steps(self):
        return [
            ('启动taptap', self.launch, 3),
            ('找游戏页面滑动浏览，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击搜索框，搜索王者荣耀', self.search, 2),
            ('点击查看第一条搜索结果', self.first_result, 2),
            ('点击评价，进入评价页', self.reviews, 2),
            ('浏览评价页，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('侧滑返回到找游戏页面', self.side_return, 2),
            ('点击排行榜，切换到排行榜页面', lambda: self.switch_tab('排行榜'), 3),
            ('点击社区，切换到社区页面', lambda: self.switch_tab('社区'), 3),
            ('浏览社区详情，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击我的游戏，切换到我的界面', lambda: self.switch_tab('我的游戏'), 3),
            ('点击个人主页，查看详情', self.profile, 3),
            ('侧滑返回到taptap首页', self.side_return, 2),
            ('上滑返回home页面', self.home, 1),
        ]
