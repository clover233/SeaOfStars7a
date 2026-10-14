"""京东浏览搜索页面；Excel 新-7.0.2模型测试步骤第 882～913 行。"""
from Cases.Top48.jingdong_common import JingdongDynamicCase


class PerformanceDynamic_jingdong_0030(JingdongDynamicCase):
    def steps(self):
        return [
            ('启动京东', self.launch, 3),
            ('点击搜索框', self.open_search, 2),
            ('搜索华为手机', lambda: self.query('华为手机'), 2),
            ('搜索结果上滑5次下滑5次', lambda: self.browse(5, 5), 0),
            ('点击销量', self.sales, 2),
            ('进入第一个商品详情', self.first_product, 2),
            ('商品详情上滑5次下滑5次', lambda: self.browse(5, 5), 0),
            ('打开商品图片', lambda: self.group('大图', self.gallery), 2),
            ('图片左滑3次右滑3次', lambda: self.within('大图', self.browse_gallery), 0),
            ('返回商品详情', self.return_product, 2),
            ('上滑至评价', lambda: self.group('评价入口', self.reveal_reviews), 2),
            ('点击评价（新版大家评）', lambda: self.within('评价入口', self.reviews_tab), 2),
            ('进入全部评价', lambda: self.within('评价入口', lambda: self.group('全部评价', self.all_reviews)), 2),
            ('全部评价上滑3次下滑3次', lambda: self.within('全部评价', lambda: self.browse(3, 3)), 0),
            ('进入店铺', lambda: self.group('店铺', self.store), 2),
            ('店铺上滑3次下滑3次', lambda: self.within('店铺', lambda: self.browse(3, 3)), 0),
            ('返回商品详情', self.return_product, 2),
            ('进入客服', lambda: self.group('客服', self.service), 2),
            ('返回商品详情', self.return_product, 2),
            ('点击立即购买', lambda: self.group('购买', self.buy), 2),
            ('确认商品规格', lambda: self.within('购买', self.confirm_specs), 2),
            ('返回京东主界面', self.main_page, 2),
            ('进入秒送', lambda: self.group('秒送', self.instant), 2),
            ('进入外卖', lambda: self.within('秒送', lambda: self.group('外卖', self.food)), 2),
            ('打开外卖搜索框', lambda: self.within('外卖', lambda: self.group('药店搜索框', self.food_search)), 2),
            ('输入药店', lambda: self.within('药店搜索框', self.search_medicine), 2),
            ('搜索药店', lambda: self.within('药店搜索框', lambda: self.group('药店结果', self.submit_search)), 2),
            ('药店搜索结果上滑3次下滑3次', lambda: self.within('药店结果', lambda: self.browse(3, 3)), 0),
            ('进入第一个药店', lambda: self.within('药店结果', lambda: self.group('药店', self.first_merchant)), 2),
            ('药店上滑3次下滑3次', lambda: self.within('药店', lambda: self.browse(3, 3)), 0),
            ('返回京东主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
