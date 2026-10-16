"""微信选择照片发送；用例表1854～1865行。"""
from Cases.Top48.weixin_common import WeixinRemainingCase


class PerformanceDynamic_weixin_0190(WeixinRemainingCase):
    NEED_IMAGES = True

    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击测试账号，进入好友聊天页面', self.test_chat, 2),
            ('点击加号按钮，进入更多功能页面', self.chat_more, 2),
            ('点击照片，进入照片页面', self.chat_album, 2),
            ('浏览照片页面，上滑3次，下滑3次', self.browse_chat_album, 2),
            ('点击选择多张图片', self.select_chat_photos, 2),
            ('点击发送，进入好友聊天页面', self.send_chat_photos, 2),
            ('点击加号按钮，进入更多功能页面', self.chat_more, 2),
            ('点击照片，进入照片页面', self.chat_album, 2),
            ('点击第一张图片大图，进入大图界面', self.first_chat_photo, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
