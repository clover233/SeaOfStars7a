# -*- coding: utf-8 -*-
"""支付宝浏览主界面功能。

步骤来源：动态性能模型测试用例7.xlsx / 新-7.0.2模型测试步骤。
表中未指定停留时长，浏览每次停留2秒，保留原0010的1/2秒停留。
"""
from Cases.Top48.alipay_common import AlipayCase


class PerformanceDynamic_alipay_0010(AlipayCase):
    PERMISSIONS = ('CAMERA', 'READ_MEDIA_IMAGES', 'ACCESS_COARSE_LOCATION', 'ACCESS_FINE_LOCATION',
                   'BLUETOOTH_CONNECT', 'BLUETOOTH_SCAN', 'BLUETOOTH_ADVERTISE')

    def steps(self):
        return [
            ('启动支付宝', self.launch, 1),
            ('点击出行', lambda: self.entry('出行'), 2),
            ('切换到地铁页', self.subway, 1),
            ('返回支付宝首页', self.return_tab, 1),
            ('点击卡包', lambda: self.entry('卡包'), 2),
            ('返回支付宝首页', self.return_tab, 1),
            ('点击我的', lambda: self.tab('我的'), 2),
            ('返回支付宝首页', self.return_tab, 1),
            ('点击收付款', lambda: self.entry('收付款'), 1),
            ('点击转账按钮', self.transfer, 1),
            ('点击转到银行卡', self.open_bank, 1),
            ('返回转账页', lambda: self.back_to_transfer(), 1),
            ('点击转到支付宝', self.open_account, 1),
            ('返回支付宝首页', self.return_tab, 1),
            ('首页点击扫一扫', lambda: self.entry('扫一扫'), 1),
            ('点击相册按钮', self.open_album, 1),
            ('点击当前页面的第一个图片，预览大图', self.preview_first_photo, 2),
            ('返回支付宝主界面', self.return_tab, 1),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
