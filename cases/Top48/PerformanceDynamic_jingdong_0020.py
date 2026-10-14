"""京东浏览超市页面；Excel 新-7.0.2模型测试步骤第 859～881 行。"""
from Cases.Top48.jingdong_common import JingdongDynamicCase


class PerformanceDynamic_jingdong_0020(JingdongDynamicCase):
    def steps(self):
        return [
            ('启动京东', self.launch, 3),
            ('进入京东超市', lambda: self.group('超市', self.supermarket), 2),
            ('进入粮油调味', lambda: self.within('超市', lambda: self.group('粮油', self.grocery)), 2),
            ('粮油调味上滑5次下滑5次', lambda: self.within('粮油', lambda: self.browse(5, 5)), 0),
            ('第一个粮油商品加入购物车', lambda: self.within('粮油', lambda: self.group('超市加购', self.add_grocery)), 2),
            ('进入结算页', lambda: self.within('超市加购', lambda: self.group('超市结算', self.grocery_checkout)), 2),
            ('打开新建地址页', lambda: self.within('超市结算', self.new_address), 2),
            ('返回京东主界面', self.main_page, 2),
            ('点击购物车', lambda: self.group('购物车', self.cart), 2),
            ('点击去结算', lambda: self.within('购物车', self.checkout), 2),
            ('返回京东主界面', self.main_page, 2),
            ('进入秒送', lambda: self.group('秒送', self.instant), 2),
            ('秒送上滑5次下滑5次', lambda: self.within('秒送', lambda: self.browse(5, 5)), 0),
            ('进入外卖', lambda: self.within('秒送', lambda: self.group('外卖', self.food)), 2),
            ('外卖上滑3次下滑3次', lambda: self.within('外卖', lambda: self.browse(3, 3)), 0),
            ('进入第一个外卖商家', lambda: self.within('外卖', lambda: self.group('商家', self.first_merchant)), 2),
            ('商家上滑1次下滑1次', lambda: self.within('商家', lambda: self.browse(1, 1)), 0),
            ('第一个商品加入购物车', lambda: self.within('商家', lambda: self.group('外卖加购', self.food_add)), 2),
            ('打开商家购物车', lambda: self.within('外卖加购', lambda: self.group('外卖购物车', self.food_cart)), 2),
            ('外卖购物车进入结算页', lambda: self.within('外卖购物车', self.checkout), 2),
            ('返回购物车清理本用例商品', lambda: self.within('外卖加购', self.clear_food_cart), 2),
            ('返回京东主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
