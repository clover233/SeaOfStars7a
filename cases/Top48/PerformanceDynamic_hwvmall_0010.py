"""华为商城浏览商品页面；Excel 新-7.0.2模型测试步骤第 818～831 行。"""
from Cases.Top48.hwvmall_common import HwVmallDynamicCase


class PerformanceDynamic_hwvmall_0010(HwVmallDynamicCase):
    def steps(self):
        return [
            ('启动华为商城', self.launch, 3),
            ('点击第一个轮播图进入详情', lambda: self.group('轮播图1', lambda: self.open_banner(1)), 2),
            ('浏览第一个轮播图上滑3次下滑3次', lambda: self.within('轮播图1', lambda: self.browse(3, 3)), 0),
            ('点击第二个轮播图进入详情', lambda: self.group('轮播图2', lambda: self.open_banner(2)), 2),
            ('浏览第二个轮播图上滑3次下滑3次', lambda: self.within('轮播图2', lambda: self.browse(3, 3)), 0),
            ('点击第三个轮播图进入详情', lambda: self.group('轮播图3', lambda: self.open_banner(3)), 2),
            ('浏览第三个轮播图上滑3次下滑3次', lambda: self.within('轮播图3', lambda: self.browse(3, 3)), 0),
            ('点击搜索框搜索p60', self.search_p60, 2),
            ('浏览搜索结果上滑5次下滑5次', lambda: self.browse(5, 5), 0),
            ('进入商品详情', self.first_product, 2),
            ('浏览商品详情上滑6次下滑6次', lambda: self.browse(6, 6), 0),
            ('返回华为商城主界面', self.main_page, 2),
            ('首页上滑6次下滑6次', lambda: self.browse(6, 6), 0),
            ('滑动返回Home页', self.home, 2),
        ]
