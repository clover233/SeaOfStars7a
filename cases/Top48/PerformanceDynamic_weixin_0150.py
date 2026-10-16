"""美团微信小程序浏览；用例表1825～1830行。"""
from Cases.Top48.weixin_common import WeixinRemainingCase


class PerformanceDynamic_weixin_0150(WeixinRemainingCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('下滑调出最近小程序页面', self.recent_programs, 2),
            ('点击美团小程序，切换到美团页面', self.meituan, 2),
            ('浏览美团首页，上滑3次，下滑3次', self.browse_meituan, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
