"""铁路 12306 只读查询、结果排序与服务页面。"""
from Cases.Top48.observed_apps_common import ObservedAppCase, StepUnavailable, optional


class RailwayDynamicCase(ObservedAppCase):
    PACKAGE = 'com.MobileTicket'
    all_app_package_list = [PACKAGE]
    COMPONENT = PACKAGE + '/.ui.activity.WelcomeGuideActivity'

    def main_ready(self):
        return self.visible('出行服务', region=(0, .87, 1, .99)) and self.visible('铁路会员', region=(0, .87, 1, .99))

    def main_page(self):
        self.return_to(self.main_ready, '未返回铁路12306主界面', limit=10)
        self.go(lambda: self.bottom_node('首页'), lambda: self.main_ready() and self.visible('查询车票'),
                '铁路12306首页未显示')

    def browse_home_up(self):
        self.main_page()
        self.browse(1, 0)

    def browse_home_down(self):
        self.browse(0, 2)

    def home_up_twice(self):
        self.main_page()
        self.browse(2, 0)

    @optional('tickets')
    def tickets(self):
        self.main_page()
        self.choose('查询车票')
        self.content_wait(self.results_ready, '车票结果未加载，可能当前查询条件、网络或页面不可用', timeout=35)

    def results_ready(self):
        return not self.visible('查询车票') and any(self.visible(s, True) for s in (
            '耗时最短', '发时最早', '价格最低', '出发时间', '历时', '无票', '暂无余票'))

    @optional('tickets')
    def results_up(self):
        self.needs('tickets')
        if not self.results_ready():
            raise StepUnavailable('当前不是车票结果页')
        self.browse(2, 0)

    @optional('tickets')
    def results_down(self):
        self.needs('tickets')
        if not self.results_ready():
            raise StepUnavailable('当前不是车票结果页')
        self.browse(0, 3)

    def sort_results(self, label, aliases=()):
        self.needs('tickets')
        if not self.results_ready():
            raise StepUnavailable('当前不是车票结果页，不能排序')
        for text in (label,) + aliases:
            if self.visible(text, True):
                self.choose(text, True, index=0)
                self.content_wait(self.results_ready, '排序后车票列表未显示')
                self.adapt('已点击“{}”排序入口；排序方向未导出，保留截图核对'.format(text))
                return
        raise StepUnavailable('当前版本没有“{}”或对应排序入口'.format(label))

    def shortest(self):
        self.sort_results('耗时最短', ('历时',))

    def earliest(self):
        self.sort_results('发时最早', ('出发时间',))

    def cheapest(self):
        self.sort_results('价格最低', ('票价',))

    @optional('hotel')
    def hotel(self):
        # 表中先滑动首页；定位酒店时可回到顶部或继续滚动寻找入口。
        for _ in range(5):
            if self.visible('酒店住宿'):
                break
            self.swipe(y1=.3, y2=.8)
        self.choose('酒店住宿')
        self.content_wait(lambda: not self.main_ready() and any(self.visible(s, True) for s in (
            '酒店', '入住', '离店', '目的地')), '酒店住宿页面未加载', timeout=35)

    def rail_tab(self, label):
        self.return_to(self.main_ready, '未返回铁路12306底部导航', limit=8)
        self.bottom_node(label)
        self.content_wait(lambda: self.visible(label, True, (0, .04, 1, .2)) or (
            self.visible('登录', True) and self.visible('注册', True)), label + '页面未加载')
        if self.visible('登录', True) and not self.visible(label, True, (0, .04, 1, .2)):
            self.adapt(label + '需要登录，验证到登录入口，不输入账号')

    def travel_services(self):
        self.rail_tab('出行服务')

    def orders(self):
        self.rail_tab('订单')

    def membership(self):
        self.rail_tab('铁路会员')
