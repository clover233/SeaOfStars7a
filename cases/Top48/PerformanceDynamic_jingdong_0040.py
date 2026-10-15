"""京东浏览直播页面；Excel 新-7.0.2模型测试步骤第 914～928 行。"""
from Cases.Top48.jingdong_common import JingdongDynamicCase


class PerformanceDynamic_jingdong_0040(JingdongDynamicCase):
    def steps(self):
        return [
            ('启动京东', self.launch, 3),
            ('底部逛进入直播', lambda: self.group('直播列表', self.live_list), 2),
            ('直播列表上滑5次下滑5次', lambda: self.within('直播列表', lambda: self.browse(5, 5)), 0),
            ('进入第一个直播间', lambda: self.within('直播列表', lambda: self.group('直播间', self.first_live)), 2),
            ('打开直播输入框', lambda: self.within('直播间', lambda: self.group('直播输入框', self.live_input)), 2),
            ('输入不错并发送', lambda: self.within('直播输入框', self.live_send), 2),
            ('打开购物袋', lambda: self.within('直播间', lambda: self.group('购物袋', self.live_bag)), 2),
            ('购物袋上滑5次下滑5次', lambda: self.within('购物袋', lambda: self.browse(5, 5)), 0),
            ('返回京东主界面', self.main_page, 2),
            ('点击我的', lambda: self.group('我的', self.mine), 2),
            ('打开全部订单', lambda: self.within('我的', lambda: self.group('订单', self.orders)), 2),
            ('订单上滑2次下滑2次', lambda: self.within('订单', lambda: self.browse(2, 2)), 0),
            ('点击待收货', lambda: self.within('订单', self.receiving_orders), 2),
            ('返回京东主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
