"""微信新闻公众号浏览；用例表1802～1817行。"""
from Cases.Top48.weixin_common import WeixinExtendedCase


class PerformanceDynamic_weixin_0130(WeixinExtendedCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击通讯录', self.contacts, 2),
            ('点击公众号', self.official_list, 2),
            ('点击腾讯新闻的公众号名片', self.tencent_card, 2),
            ('返回公众号界面', self.return_official, 2),
            ('点击央视新闻的公众号名片', self.cctv_card, 2),
            ('点击屏幕底部文博日历查看详情', self.culture_menu, 2),
            ('浏览任意主题（如打卡笔记），上滑2次，下滑2次', self.browse_culture, 2),
            ('返回央视新闻对话界面', self.return_cctv, 2),
            ('点击屏幕底部夜读查看详情', self.night_menu, 2),
            ('返回微信首页', self.wechat_home, 2),
            ('点击订阅号', self.subscriptions, 2),
            ('点击腾讯新闻', self.tencent_news, 2),
            ('腾讯新闻页面下滑3次', self.browse_tencent, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
