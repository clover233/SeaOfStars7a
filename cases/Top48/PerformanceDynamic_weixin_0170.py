"""京东购物微信小程序浏览；用例表1838～1843行。"""
from Cases.Top48.weixin_common import WeixinRemainingCase


class PerformanceDynamic_weixin_0170(WeixinRemainingCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('下滑调出最近小程序页面', self.recent_programs, 2),
            ('点击京东购物小程序，切换到京东购物页面', self.jd, 2),
            ('浏览京东购物首页，上滑3次，下滑3次', self.browse_jd, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
