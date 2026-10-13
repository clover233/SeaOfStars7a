"""高德地图浏览美食并导航至首条商户。"""
from Cases.Top48.autonavi_common import AutonaviDynamicCase


class PerformanceDynamic_autonavi_0040(AutonaviDynamicCase):
    def food_page(self):
        self.transition(lambda: self.click_node(text='美食', first=True),
                        lambda: self.has(desc='搜索框，美食'), '未进入美食列表')

    def food_detail(self):
        self.first_visible_result(800, 300, exclude=('搜索框', '返回'))
        self.wait_for(lambda: self.has(text='路线'), '未进入美食详情')

    def route(self):
        self.transition(lambda: self.click_node(text='路线'),
                        lambda: any(n.get('content-desc', '').startswith('终点，')
                                    for n in self.nodes()), '美食路线未规划')
        self.drive()

    def finish_to_results(self):
        self.confirm_exit()
        for _ in range(4):
            if self.has(desc='搜索框，美食'):
                return
            self.d.press('back')
        self.wait_for(lambda: self.has(desc='搜索框，美食'), '未返回美食搜索结果')

    def steps(self):
        return [
            ('启动高德地图', lambda: (self.launch(), self.amap_home()), 3),
            ('点击搜索框', self.search_page, 1),
            ('点击美食', self.food_page, 3),
            ('上滑3次浏览美食', lambda: self.scroll_page(up=3, down=0), 1),
            ('下滑3次浏览美食', lambda: self.scroll_page(up=0, down=3), 1),
            ('点击第一条搜索结果', self.food_detail, 2),
            ('点击路线', self.route, 2),
            ('点击开始导航', self.start_navigation, 2),
            ('点击退出按钮', self.open_exit, 0),
            ('点击退出导航到搜索结果页面', self.finish_to_results, 2),
            ('返回高德地图主界面', self.amap_home, 2),
            ('滑动返回Home页', self.home_gesture, 1),
        ]
