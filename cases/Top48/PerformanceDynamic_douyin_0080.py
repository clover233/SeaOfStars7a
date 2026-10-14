"""抖音团购、美食商家和套餐浏览（表格第 635～645 行）。"""
from Cases.Top48.douyin_common import DouyinDynamicCase


class PerformanceDynamic_douyin_0080(DouyinDynamicCase):
    all_app_package_list = [DouyinDynamicCase.PACKAGE]

    def steps(self):
        return [
            ('启动抖音', self.launch, 3),
            ('点击团购进入团购页面', self.open_group_buy, 2),
            ('上滑3次、下滑3次浏览团购页面', lambda: self.browse(3, 3), 0),
            ('点击美食进入美食页面', self.open_food, 3),
            ('上滑3次、下滑3次浏览美食页面', lambda: self.browse(3, 3), 0),
            ('点击美食页第一个商家', self.open_first_merchant, 3),
            ('上滑3次、下滑3次浏览商家', lambda: self.browse(3, 3), 0),
            ('点击第一个团购套餐', self.open_first_deal, 2),
            ('点击购买', self.buy_deal, 2),
            ('返回抖音主界面', self.return_feed, 2),
            ('滑动返回Home页', self.home, 1),
        ]
