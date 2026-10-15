"""快手浏览直播和购物；动态性能模型测试用例7.xlsx 第954～969行。"""
from Cases.Top48.kuaishou_common import KuaishouDynamicCase


class PerformanceDynamic_kuaishou_0020(KuaishouDynamicCase):
    def steps(self):
        return [
            ('启动快手', self.launch, 5),
            ('点击首页右上角搜索图标', self.open_search, 1),
            ('搜索华为手机', self.search_phone, 2),
            ('上滑3次下滑3次浏览搜索结果', self.browse_results, 2),
            ('返回搜索界面', self.return_search, 1),
            ('点击直播榜', self.live_rank, 1),
            ('点击排名第一的直播账号观看15s', self.first_live, 15),
            ('上滑查看下一个直播观看15s', self.next_live, 15),
            ('返回快手主界面', self.return_home, 2),
            ('点击左上角三横线', self.open_menu, 1),
            ('点击快手小店', self.open_shop, 2),
            ('上滑3次下滑3次浏览小店推荐', self.browse_shop, 2),
            ('点击第一个商品', self.first_product, 2),
            ('点击加入购物袋', self.add_to_cart, 2),
            ('返回快手主界面', self.return_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
