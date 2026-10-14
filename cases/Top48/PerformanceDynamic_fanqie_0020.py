"""番茄免费小说听书和榜单浏览场景；步骤对应 Excel 第 673–685 行。"""
from Cases.Top48.fanqie_common import FanqieDynamicCase


class PerformanceDynamic_fanqie_0020(FanqieDynamicCase):
    def back_to_main(self):
        self.switch_bottom('书城')
        self.select_channel('推荐')

    def steps(self):
        return [
            ('启动番茄免费小说', self.launch, 3),
            ('主页浏览，上滑3次，下滑3次', lambda: self.browse(3, 3), 0),
            ('点击听书，进入听书页面', lambda: self.select_channel('听书'), 2),
            ('听书页浏览，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击推荐进入首页（可能需要左滑）', lambda: self.select_channel('推荐'), 2),
            ('点击完本榜，进入完本榜页面', lambda: self.select_rank('完本榜'), 2),
            ('左滑2次，右滑2次，浏览完本榜单', self.browse_rank, 0),
            ('点击巅峰榜，进入巅峰榜页面', lambda: self.select_rank('巅峰榜'), 2),
            ('左滑2次，右滑2次，浏览口碑榜单', self.browse_rank, 0),
            ('点击新书榜，进入新书榜页面', lambda: self.select_rank('新书榜'), 2),
            ('左滑2次，右滑2次，浏览高分榜单', self.browse_rank, 0),
            ('返回番茄免费小说主界面', self.back_to_main, 2),
            ('滑动返回Home页', self.home, 1),
        ]
