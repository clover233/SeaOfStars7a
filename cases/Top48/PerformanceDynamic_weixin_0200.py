"""微信收藏、我的浏览；用例表1866～1876行。"""
from Cases.Top48.weixin_common import WeixinRemainingCase


class PerformanceDynamic_weixin_0200(WeixinRemainingCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击我，切换到我页面', self.me, 2),
            ('点收藏，切换到收藏页面', self.favorites_page, 2),
            ('收藏页面上滑3次，下滑3次', self.browse_favorites, 2),
            ('点击第一条收藏，进入到详情页', self.first_favorite, 2),
            ('返回微信我页面', self.me, 2),
            ('点击设置，切换到设置页面', self.settings, 2),
            ('点击通用，切换到通用页面', self.general, 2),
            ('点击存储空间，切换到存储空间页面', self.storage, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
