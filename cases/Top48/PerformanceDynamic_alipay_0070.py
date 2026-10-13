# -*- coding: utf-8 -*-
"""支付宝浏览医疗健康和蚂蚁森林。

步骤来源：动态性能模型测试用例7.xlsx / 新-7.0.2模型测试步骤。
表中未指定停留时长，浏览每次停留2秒，保留原0010的1/2秒停留。
"""
from Cases.Top48.alipay_common import AlipayCase


class PerformanceDynamic_alipay_0070(AlipayCase):
    PERMISSIONS = ('ACCESS_COARSE_LOCATION', 'ACCESS_FINE_LOCATION')

    def steps(self):
        return [
            ('启动支付宝', self.launch, 2),
            ('点击医疗健康', lambda: self.entry('医疗健康'), 2),
            ('返回支付宝首页', self.return_tab, 2),
            ('第二次点击医疗健康', lambda: self.entry('医疗健康'), 2),
            ('上滑1次，浏览医疗健康页面', lambda: self.browse(1, 0), 0),
            ('下滑1次，浏览医疗健康页面', lambda: self.browse(0, 1), 0),
            ('返回支付宝首页', self.return_tab, 2),
            ('点击蚂蚁森林', lambda: self.entry('蚂蚁森林'), 2),
            ('上滑1次，浏览蚂蚁森林页面', lambda: self.browse(1, 0), 0),
            ('下滑1次，浏览蚂蚁森林页面', lambda: self.browse(0, 1), 0),
            ('返回支付宝首页', self.return_tab, 2),
            ('点击淘宝闪购', lambda: self.entry('淘宝闪购'), 2),
            ('上滑3次，下滑3次，浏览淘宝闪购页面', lambda: self.browse(3, 3), 0),
            ('返回支付宝主界面', self.return_tab, 2),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
