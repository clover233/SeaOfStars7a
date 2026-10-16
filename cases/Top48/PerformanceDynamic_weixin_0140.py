"""喜茶微信小程序浏览；用例表1818～1824行。"""
from Cases.Top48.weixin_common import WeixinRemainingCase


class PerformanceDynamic_weixin_0140(WeixinRemainingCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('下滑调出最近小程序页面', self.recent_programs, 2),
            ('点击喜茶小程序，切换到喜茶页面', self.heytea, 2),
            ('点击到店取，切换到到店取页面', self.heytea_menu, 2),
            ('到店取页面向下滑动浏览3次，向上滑到顶部', self.browse_heytea, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
