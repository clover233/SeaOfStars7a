"""微信通讯录和推荐；用例表1662～1677行。"""
from Cases.Top48.weixin_common import WeixinDynamicCase


class PerformanceDynamic_weixin_0030(WeixinDynamicCase):
    NEED_IMAGES = True
    # 旧设备有两个同名“微信性能素材”目录；使用本轮唯一生成的测试相册。
    ALBUM = '微信回归素材7'

    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击通讯录', self.contacts, 2),
            ('通讯录页面，上滑3次，下滑3次', self.browse_contacts, 2),
            ('进入好友xxxx的详情界面', self.friend_profile, 2),
            ('点击头像，并返回', self.friend_avatar, 2),
            ('点击好友的朋友圈', self.friend_moments, 2),
            ('浏览图片，横向滑动6次', self.friend_pictures, 2),
            ('返回好友xxxx的详情界面', self.return_profile, 2),
            ('把她推荐给好友', self.recommend_friend, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('点击右上角+号', self.plus_menu, 2),
            ('点击扫一扫', self.scan, 2),
            ('点击相册', self.scan_album, 2),
            ('选择一张图片', self.scan_picture, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
