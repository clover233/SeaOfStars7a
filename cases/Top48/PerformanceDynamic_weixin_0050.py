"""微信科技类公众号浏览；用例表1695～1708行。"""
from Cases.Top48.weixin_common import WeixinDynamicCase


class PerformanceDynamic_weixin_0050(WeixinDynamicCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击通讯录', self.contacts, 2),
            ('点击公众号', self.official_list, 2),
            ('点击华为手机（或者华为）的公众号名片，点击右上角人头像', self.huawei, 2),
            ('浏览公众号', self.browse_official, 2),
            ('点击第一个文章', self.first_article, 2),
            ('浏览搜索结果', self.browse_article, 2),
            ('返回测试公众号界面', self.return_official, 2),
            ('点击HarmonyOS的公众号名片', self.harmony, 2),
            ('点击屏幕底部HMOS后点击官网直达', self.harmony_site, 2),
            ('上滑2次，下滑2次浏览文章', self.browse_harmony, 2),
            ('返回测试公众号界面', self.return_official, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
