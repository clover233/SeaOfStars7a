"""美团多任务操作；动态性能模型测试用例7.xlsx 第1068～1093行，按要求删除原13～18步。"""
from Cases.Top48.meituan_common import MeituanDynamicCase


class PerformanceDynamic_meituan_0090(MeituanDynamicCase):
    def steps(self):
        return [
            ('启动美团', self.launch, 3),
            ('首页滑动浏览上滑5次', lambda: self.browse(5, 0), 0),
            ('首页滑动浏览下滑5次', lambda: self.browse(0, 5), 0),
            ('点击美食团购', self.food, 1),
            ('美食团购页面上滑2次下滑2次', lambda: self.browse(2, 2), 0),
            ('返回美团首页', self.return_main, 1),
            ('点击休闲玩乐', self.leisure, 1),
            ('点击第一条结果', self.local_shop, 1),
            ('休闲场所详情上滑2次下滑2次', lambda: self.browse(2, 2), 0),
            ('返回美团首页', self.return_main, 1),
            ('点击外卖', self.delivery, 1),
            ('点击搜索框', self.search_box, 1),
            ('返回到外卖界面', self.return_delivery, 1),
            ('点击我的', self.mine, 1),
            ('点击我的地址', self.addresses, 1),
            ('点击第一个收货地址', self.first_address, 1),
            ('点击保存地址', self.save_address, 1),
            ('点击新增收货地址', self.new_address, 1),
            ('返回美团主界面', self.return_main, 1),
            ('滑动返回Home页', self.home, 1),
        ]
