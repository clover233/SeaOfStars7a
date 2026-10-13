"""高德地图浏览西安北站的公交地铁路线。"""
from Cases.Top48.autonavi_common import AutonaviDynamicCase


class PerformanceDynamic_autonavi_0030(AutonaviDynamicCase):
    def transit_page(self):
        self.result_route('西安北站')
        self.transition(lambda: self.click_node(desc='公共交通'),
                        lambda: any('公共交通' in n.get('content-desc', '') and
                                    '已选中' in n.get('content-desc', '')
                                    for n in self.nodes()), '未切换到公交地铁路线')

    def first_route(self):
        # 公共交通列表随出发城市变化，选择当前列表中的首条路线卡片。
        candidates = []
        for node in self.nodes():
            if node.get('class') != 'android.view.ViewGroup' or not node.get('content-desc', '').startswith('约'):
                continue
            _, top, _, bottom = self.bounds(node)
            if 600 <= top < 2100 and bottom - top > 50:
                candidates.append((top, node))
        if not candidates:
            raise RuntimeError('公交地铁列表没有可选择的路线')
        self.node_click(min(candidates, key=lambda item: item[0])[1])
        self.scroll_page(up=1, down=1)

    def steps(self):
        return [
            ('启动高德地图', lambda: (self.launch(), self.amap_home()), 3),
            ('搜索西安北站', lambda: (self.search_page(), self.search('西安北站')), 2),
            ('切换到公交地铁页面', self.transit_page, 3),
            ('上滑1次，下滑1次浏览公交地铁页面',
             lambda: self.scroll_page(up=1, down=1), 1),
            ('点击第一条路线，上滑1次，下滑1次', self.first_route, 1),
            ('返回高德地图主界面', self.amap_home, 2),
            ('滑动返回Home页', self.home_gesture, 1),
        ]
