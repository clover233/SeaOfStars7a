# -*- coding: utf-8 -*-
"""支付宝-闪送。

步骤来源：动态性能模型测试用例7.xlsx / 新-7.0.2模型测试步骤。
表中未指定停留时长，浏览每次停留2秒，保留原0010的1/2秒停留。
"""
from Cases.Top48.alipay_common import AlipayCase


class PerformanceDynamic_alipay_0030(AlipayCase):
    PERMISSIONS = ('ACCESS_COARSE_LOCATION', 'ACCESS_FINE_LOCATION')

    def steps(self):
        return [
            ('启动支付宝', self.launch, 2),
            ('点击搜索框，输入【闪送】并确定', lambda: self.search('闪送'), 2),
            ('上滑1次，下滑1次，查看闪送搜索结果', lambda: self.browse(1, 1), 0),
            ('点击第一个搜索结果进入闪送小程序', self.open_shansong, 2),
            ('上滑1次，下滑1次，浏览小程序信息', lambda: self.browse(1, 1), 0),
            ('点击订单，切换到订单页面', lambda: self.mini_tab('订单'), 2),
            ('点击我的，切换到我的信息界面', lambda: self.mini_tab('我的'), 2),
            ('点击首页，返回小程序首页', lambda: self.mini_tab('首页'), 2),
            ('侧滑返回支付宝首页', self.swipe_back_home, 2),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
