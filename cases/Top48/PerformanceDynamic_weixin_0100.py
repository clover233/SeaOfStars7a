"""微信视频号和直播；用例表1760～1773行。"""
from Cases.Top48.weixin_extended import WeixinExtendedCase


class PerformanceDynamic_weixin_0100(WeixinExtendedCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击发现', self.discover, 2),
            ('点击视频号', self.channels, 2),
            ('上滑6次浏览视频号', self.browse_channels, 2),
            ('返回发现页面', self.discover, 2),
            ('点击直播', self.live_list, 2),
            ('点击第一个直播', self.first_live, 2),
            ('上滑切换直播间6次', self.browse_live, 2),
            ('返回发现页', self.discover, 2),
            ('点击游戏', self.games, 2),
            ('首页上滑6次，下滑6次浏览', self.browse_games, 2),
            ('返回微信发现页', self.discover, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
