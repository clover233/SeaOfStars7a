"""蜜雪冰城微信小程序浏览；用例表1831～1837行。"""
from Cases.Top48.weixin_common import WeixinRemainingCase


class PerformanceDynamic_weixin_0160(WeixinRemainingCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('下滑调出最近小程序页面', self.recent_programs, 2),
            ('点击蜜雪冰城小程序，切换到蜜雪冰城页面', self.mixue, 2),
            ('点击点餐，切换到点餐页面', self.mixue_menu, 2),
            ('浏览点餐页面，上滑3次，下滑3次', self.browse_mixue, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
