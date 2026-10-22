"""抖音商城搜索、商品、购物车和团购浏览（表格第 535～556 行）。"""
from Cases.Top48.douyin_common import DouyinDynamicCase


class PerformanceDynamic_douyin_0030(DouyinDynamicCase):
    all_app_package_list = [DouyinDynamicCase.PACKAGE]

    def browse_cart_page(self):
        if self.open_cart():
            self.browse(3, 0)
            return True
        return False

    def return_product(self):
        self.return_to(self.product_ready, '未返回商品详情页')

    def cart_from_mall(self):
        if self.open_mall():
            return self.open_cart()
        return False

    def enter_store(self):
        self.store_open = bool(self.product_action('进店'))
        return self.store_open

    def browse_store(self):
        if not getattr(self, 'store_open', False):
            return self.skip('进店入口不可用，跳过依赖店铺页面的滑动')
        self.browse(3, 0)
        return True

    def group_buy(self):
        self.group_buy_open = bool(self.open_group_buy())
        return self.group_buy_open

    def browse_group_buy(self):
        if not getattr(self, 'group_buy_open', False):
            return self.skip('团购入口不可用，跳过依赖团购页面的滑动')
        self.browse(3, 3)
        return True

    def steps(self):
        return [
            ('启动抖音', self.launch, 3),
            ('点击商城，切换至商城页面', self.open_mall, 2),
            ('上滑3次浏览推荐商品', lambda: self.browse(3, 0), 0),
            ('下滑3次浏览推荐商品', lambda: self.browse(0, 3), 0),
            ('搜索华为p70', lambda: (self.open_mall_search(), self.search_product()), 3),
            ('上滑3次浏览搜索结果', lambda: self.browse(3, 0), 0),
            ('下滑3次浏览搜索结果', lambda: self.browse(0, 3), 0),
            ('点击第一个商品进入详情页', self.open_first_product, 3),
            ('点击加入购物车', self.add_to_cart, 2),
            ('上滑3次浏览购物车界面', self.browse_cart_page, 0),
            ('点击左下角客服', lambda: self.product_action('客服'), 2),
            ('返回商品详情界面', self.return_product, 2),
            ('点击左下角进店', self.enter_store, 2),
            ('上滑3次浏览店铺界面', self.browse_store, 0),
            ('返回抖音主界面', self.return_feed, 2),
            ('点击商城首页右上角购物车', self.cart_from_mall, 2),
            ('点击管理按钮', self.cart_manage, 1),
            ('点击删除', self.cart_delete, 2),
            ('返回抖音商城界面', self.open_mall, 2),
            ('点击团购进入团购界面', self.group_buy, 2),
            ('上滑3次、下滑3次浏览团购界面', self.browse_group_buy, 0),
            ('滑动返回Home页', self.home, 1),
        ]
