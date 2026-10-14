"""华为商城浏览分类页面；Excel 新-7.0.2模型测试步骤第 832～846 行。"""
from Cases.Top48.hwvmall_common import HwVmallDynamicCase


class PerformanceDynamic_hwvmall_0020(HwVmallDynamicCase):
    def steps(self):
        return [
            ('启动华为商城', self.launch, 3),
            ('点击分类', self.category, 2),
            ('浏览分类上滑5次下滑5次', lambda: self.browse(5, 5), 0),
            ('从分类进入商品详情', self.category_product, 2),
            ('查看商品详情', lambda: self.require(desc='客服'), 2),
            ('浏览商品详情上滑5次下滑5次', lambda: self.browse(5, 5), 0),
            ('商品详情上滑1次', self.swipe, 2),
            ('点击评价', lambda: self.group('评价', self.reveal_reviews), 2),
            ('查看全部评价', lambda: self.within('评价', self.all_reviews), 2),
            ('浏览评价上滑5次下滑5次', lambda: self.within('评价', lambda: self.browse(5, 5)), 0),
            ('返回商品详情', self.return_product, 2),
            ('点击客服', lambda: self.group('客服', self.service), 2),
            ('返回商品详情', self.return_product, 2),
            ('返回华为商城主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
