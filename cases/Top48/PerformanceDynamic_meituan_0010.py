"""美团点餐和购物；动态性能模型测试用例7.xlsx 第1041～1057行。"""
from Cases.Top48.meituan_common import MeituanDynamicCase


class PerformanceDynamic_meituan_0010(MeituanDynamicCase):
    def steps(self):
        return [
            ('启动美团', self.launch, 3),
            ('点击外卖', self.delivery, 1),
            ('滑动浏览外卖页面上滑5次下滑5次', lambda: self.browse(5, 5), 0),
            ('点击搜索框', self.search_box, 1),
            ('输入黄焖鸡', lambda: self.enter_query('黄焖鸡'), 1),
            ('点击搜索', self.search, 1),
            ('搜索结果页上滑2次下滑2次', lambda: self.browse(2, 2), 0),
            ('点击第一家商铺', self.shop, 1),
            ('上下各滑动1次浏览商家', lambda: self.browse(1, 1, 1), 0),
            ('点击评价上下各滑动2次', self.comments, 1),
            ('返回进入点菜界面', self.menu, 1),
            ('点击推荐下的第一份食品', self.first_food, 1),
            ('点击加入购物车', self.add_food, 1),
            ('再次点击加入购物车', self.add_again, 1),
            ('点击购物车图标清空购物车', self.clear_cart, 1),
            ('返回美团主界面', self.return_main, 1),
            ('滑动返回Home页', self.home, 1),
        ]
