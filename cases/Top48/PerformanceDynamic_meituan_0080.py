"""美团美食团购；动态性能模型测试用例7.xlsx 第1058～1067行。"""
from Cases.Top48.meituan_common import MeituanDynamicCase


class PerformanceDynamic_meituan_0080(MeituanDynamicCase):
    def steps(self):
        return [
            ('启动美团', self.launch, 3),
            ('点击美食团购', self.food, 1),
            ('上滑5次浏览美食团购页面', lambda: self.browse(5, 0), 0),
            ('下滑5次浏览美食团购页面', lambda: self.browse(0, 5), 0),
            ('点击美食餐厅下方第一个商家', self.local_shop, 1),
            ('上滑3次浏览商家页面', lambda: self.browse(3, 0), 0),
            ('下滑3次浏览商家页面', lambda: self.browse(0, 3), 0),
            ('点击第一个团购商品', self.group_product, 1),
            ('返回美团主界面', self.return_main, 1),
            ('滑动返回Home页', self.home, 1),
        ]
