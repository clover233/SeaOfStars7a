"""动态性能场景；Excel「新-7.0.2模型测试步骤」第 1625～1632 行。"""
from Cases.Top48.vipshop_common import VipshopDynamicCase


class PerformanceDynamic_weipinhui_0030(VipshopDynamicCase):
    def steps(self):
        return [
            ('启动唯品会', self.launch, 3),
            ('推荐页面向上抛滑3次', lambda: self.fling_up(3), 2),
            ('进入运动页面', lambda: self.group('运动', self.sports), 2),
            ('运动页面向上抛滑3次', lambda: self.within('运动', lambda: self.fling_up(3)), 2),
            ('点击底部分类', lambda: self.group('分类', self.category), 2),
            ('分类页面上滑2次下滑2次', lambda: self.within('分类', lambda: self.browse(2, 2)), 2),
            ('返回唯品会主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 1),
        ]
