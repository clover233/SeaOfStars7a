# -*- coding: utf-8 -*-
"""支付宝浏览理财和消息页面。

步骤来源：动态性能模型测试用例7.xlsx / 新-7.0.2模型测试步骤。
表中未指定停留时长，浏览每次停留2秒，保留原0010的1/2秒停留。
"""
from Cases.Top48.alipay_common import AlipayMessageCase


class PerformanceDynamic_alipay_0020(AlipayMessageCase):
    PERMISSIONS = ('CAMERA', 'READ_MEDIA_IMAGES')

    def steps(self):
        return [
            ('启动支付宝', self.launch, 2),
            ('首页点击tab切换理财', lambda: self.tab('理财'), 2),
            ('上滑2次，下滑2次浏览理财', lambda: self.browse(2, 2), 0),
            ('点击稳健理财', self.open_steady, 2),
            ('上滑2次，下滑2次浏览稳健理财', lambda: self.browse(2, 2), 0),
            ('点击稳健理财页热销的第一个理财产品', self.open_first_product, 2),
            ('上滑2次，下滑2次浏览产品', lambda: self.browse(2, 2), 0),
            ('返回理财页', lambda: self.return_tab('理财'), 2),
            ('理财页点击tab切换消息', lambda: self.tab('消息'), 2),
            ('点击测试账号进入聊天对话框', self.open_test_chat, 2),
            ('上滑5次，下滑5次查看聊天记录', lambda: self.browse(5, 5), 0),
            ('点击输入框，发送动态性能测试', self.send_test_message, 2),
            ('点击图片', self.chat_album, 2),
            ('选择5张图片，点击完成', self.send_test_photos, 2),
            ('返回消息页', lambda: self.return_tab('消息'), 2),
            ('点击右上角+号', self.message_plus, 2),
            ('点击扫一扫', lambda: self.tap(text='扫一扫'), 2),
            ('点击相册', self.open_album, 2),
            ('返回消息页', lambda: self.return_tab('消息'), 2),
            ('点击我的', lambda: self.tab('我的'), 2),
            ('点击支付宝会员', lambda: self.my_entry('支付宝会员'), 2),
            ('上滑5次，下滑5次浏览会员页', lambda: self.browse(5, 5), 0),
            ('返回我的页', lambda: self.return_tab('我的'), 2),
            ('点击账单', lambda: self.my_entry('账单'), 2),
            ('返回我的页', lambda: self.return_tab('我的'), 2),
            ('点击余额', lambda: self.my_entry('余额'), 2),
            ('返回我的页', lambda: self.return_tab('我的'), 2),
            ('点击设置', lambda: self.my_entry('设置'), 2),
            ('点击新消息通知', lambda: self.settings_entry('新消息通知'), 2),
            ('返回设置页', self.back_to_settings, 2),
            ('点击通用', lambda: self.settings_entry('通用'), 2),
            ('返回我的页', lambda: self.return_tab('我的'), 2),
            ('返回支付宝主界面', self.return_tab, 2),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
