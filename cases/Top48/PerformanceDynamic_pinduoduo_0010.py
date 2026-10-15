"""拼多多搜索华为手机并浏览商品、店铺；Excel 第 1196～1206 行。"""
from Cases.Top48.pinduoduo_common import PinduoduoDynamicCase


class PerformanceDynamic_pinduoduo_0010(PinduoduoDynamicCase):
    def steps(self):
        return [
            ('启动拼多多', self.launch, 2),
            ('主页上滑3次、下滑3次', lambda: self.browse(3, 3), 0),
            ('点击搜索框', self.open_search, 1),
            ('输入华为手机并搜索', self.search_phone, 2),
            ('搜索结果上滑3次、下滑3次', lambda: self.browse(3, 3), 0),
            ('点击第一个商品', self.first_product, 2),
            ('商品详情上滑2次、下滑2次', lambda: self.browse(2, 2), 0),
            ('点击左下角店铺', self.store, 2),
            ('店铺页上滑2次、下滑2次', lambda: self.browse(2, 2), 0),
            ('返回拼多多主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
