"""高德地图浏览地图和打车车型，不发起叫车。"""
from Cases.Top48.autonavi_common import AutonaviDynamicCase


class PerformanceDynamic_autonavi_0050(AutonaviDynamicCase):
    def click_point(self, x, y):
        # 打车 WebView 实机核对使用主屏触屏驻留点击，坐标来自控件 bounds。
        self.foreground()
        result = self.d.shell('input touchscreen -d 0 swipe {0} {1} {0} {1} 250'.format(
            round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('主屏点击失败：' + result.output)

    def taxi_tab(self):
        self.transition(lambda: self.click_node(text='打车', rid=self.PREFIX + 'tab_name_v2'),
                        lambda: self.has(text='你要去哪儿'), '未进入打车标签页')

    def taxi_destination(self):
        self.transition(lambda: self.click_node(text='你要去哪儿'),
                        lambda: self.has(text='请输入终点'), '未进入目的地搜索')

    def taxi_search(self):
        self.click_node(text='请输入终点', class_name='android.widget.EditText')
        self.d.send_keys('西安钟楼')
        self.wait_for(lambda: self.has(text='售票处'), '未找到西安钟楼售票处')

    def ticket_office(self):
        self.transition(lambda: self.click_node(text='售票处'),
                        lambda: self.has(text='在这下车'), '未出现下车点列表')

    def dropoff(self):
        self.transition(lambda: self.click_node(text='在这下车'),
                        lambda: self.has(text='立即打车'), '未出现车型列表')

    def browse_models(self):
        if not self.has(text='立即打车'):
            raise RuntimeError('当前不是车型列表')
        self.scroll_page(up=3, down=3, x=.7, upper=.53, lower=.81)
        if not self.has(text='立即打车'):
            raise RuntimeError('车型列表浏览后页面异常')

    def back_to_taxi(self):
        self.d.press('back')
        self.wait_for(lambda: self.has(text='你要去哪儿'), '未返回打车标签页')

    def back_to_map(self):
        self.click_node(text='首页', rid=self.PREFIX + 'tab_name_v2')
        self.wait_for(lambda: self.has(rid=self.PREFIX + 'txt_hotword'), '未回到高德首页')

    def steps(self):
        return [
            ('启动高德地图', lambda: (self.launch(), self.amap_home()), 3),
            ('地图界面上滑1次浏览', lambda: self.map_swipe('up'), 3),
            ('地图界面下滑1次浏览', lambda: self.map_swipe('down'), 3),
            ('地图界面左滑1次浏览', lambda: self.map_swipe('left'), 3),
            ('地图界面右滑1次浏览', lambda: self.map_swipe('right'), 3),
            ('双指捏合放大，缩小当前位置地图', self.map_pinch, 3),
            ('点击下方打车tab页', self.taxi_tab, 2),
            ('点击目的地', self.taxi_destination, 1),
            ('输入西安钟楼，搜索', self.taxi_search, 2),
            ('选择售票处', self.ticket_office, 2),
            ('选择下车点', self.dropoff, 2),
            ('上滑3次，下滑3次，浏览车型', self.browse_models, 1),
            ('滑动返回打车tab页', self.back_to_taxi, 1),
            ('点击回到高德首页', self.back_to_map, 2),
            ('滑动返回桌面', self.home_gesture, 1),
        ]
