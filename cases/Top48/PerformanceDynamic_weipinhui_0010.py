"""动态性能场景；Excel「新-7.0.2模型测试步骤」第 1610～1624 行。"""
from Cases.Top48.vipshop_common import VipshopDynamicCase


class PerformanceDynamic_weipinhui_0010(VipshopDynamicCase):
    def steps(self):
        return [
            ('启动唯品会', self.launch, 3),
            ('搜索清风卫生纸', self.search_tissue, 2),
            ('搜索结果上滑2次下滑3次', lambda: self.browse(2, 3), 2),
            ('查看第一条商品', lambda: self.group('商品', self.first_product), 2),
            ('商品详情上滑2次下滑3次', lambda: self.within('商品', lambda: self.browse(2, 3)), 2),
            ('进入店铺上滑3次下滑3次', lambda: self.group('店铺', lambda: self.within('商品', self.browse_shop)), 2),
            ('返回商品详情', lambda: self.within('商品', self.return_product), 2),
            ('加入购物车', lambda: self.group('本次加购', lambda: self.within('商品', self.add_to_cart)), 2),
            ('点击购物车', lambda: self.group('购物车', self.open_cart), 2),
            ('点击结算查看确认页', lambda: self.group('结算', lambda: self.within('本次加购', self.checkout)), 2),
            ('返回购物车界面', lambda: self.within('购物车', self.return_cart), 1),
            ('长按本次加购商品', lambda: self.group('删除菜单', lambda: self.within('本次加购', self.hold_added_product)), 1),
            ('删除本次加购商品', lambda: self.within('删除菜单', self.delete_added_product), 1),
            ('返回唯品会主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 1),
        ]
