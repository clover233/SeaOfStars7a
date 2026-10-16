"""淘宝搜索和购买商品；用例表1410～1426行。"""
from Cases.Top48.travel_shop_common import TaobaoDynamicCase


class PerformanceDynamic_taobao_0010(TaobaoDynamicCase):
    def steps(self):
        return [
            ('启动淘宝', self.launch, 2),
            ('点击搜索框，输入清风卫生纸，搜索清风卫生纸', self.search_tissue, 2),
            ('浏览搜索结果，上滑5次，下滑6次', self.browse_results, 2),
            ('按销量进行筛选，点击第一条商品查看详情', self.sales_first, 2),
            ('浏览商品详情，上滑5次，下滑5次', self.browse_product, 2),
            ('点击查看更多查看宝贝评价', self.reviews, 2),
            ('上滑5次，下滑5次，浏览评价页面', self.browse_reviews, 2),
            ('返回商品详情', self.return_product, 2),
            ('点击屏幕底部客服', self.customer_service, 2),
            ('点击输入框发送文字你好', self.send_hello, 2),
            ('点击+号相册，选择图片，点击发送', self.send_picture, 2),
            ('返回商品详情', self.return_product, 2),
            ('进入店铺浏览，上滑，点击店铺图标，上滑3次，下滑3次', self.shop, 2),
            ('返回商品详情', self.return_product, 2),
            ('加入购物车', self.add_cart, 2),
            ('返回淘宝主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
