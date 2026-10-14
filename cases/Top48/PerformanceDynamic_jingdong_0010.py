"""京东浏览推荐页面；Excel 新-7.0.2模型测试步骤第 847～858 行。"""
from Cases.Top48.jingdong_common import JingdongDynamicCase


class PerformanceDynamic_jingdong_0010(JingdongDynamicCase):
    def steps(self):
        return [
            ('启动京东', self.launch, 3),
            ('首页浏览上滑5次下滑5次', lambda: self.browse(5, 5), 0),
            ('点击手机数码', lambda: self.group('手机数码', self.phone_channel), 2),
            ('手机数码浏览上滑5次下滑5次', lambda: self.within('手机数码', lambda: self.browse(5, 5)), 0),
            ('点击分类（新版首页右上入口）', lambda: self.group('分类', self.category), 2),
            ('分类浏览上滑2次下滑2次', lambda: self.within('分类', lambda: self.browse(2, 2)), 0),
            ('点击电脑分类', lambda: self.group('电脑', self.computer_category), 2),
            ('电脑页面浏览上滑2次下滑2次', lambda: self.within('电脑', lambda: self.browse(2, 2)), 0),
            ('点击第一类商品', lambda: self.group('分类商品', self.first_category), 2),
            ('商品页浏览上滑5次下滑5次', lambda: self.within('分类商品', lambda: self.browse(5, 5)), 0),
            ('返回京东主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
