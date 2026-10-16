"""微信拍摄和录像；用例表1734～1747行。"""
from Cases.Top48.weixin_common import WeixinDynamicCase


class PerformanceDynamic_weixin_0080(WeixinDynamicCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击测试账号，进入好友聊天页面', self.test_chat, 2),
            ('点击加号按钮，进入更多功能页面', self.chat_more, 2),
            ('点击拍摄，进入拍照界面', self.chat_camera, 2),
            ('点击拍照按钮，进入拍照完成界面', self.photo, 2),
            ('点击对号后点击发送，进入好友聊天页面', self.send_capture, 2),
            ('点击加号按钮，进入更多功能页面', self.chat_more, 2),
            ('点击拍摄，进入拍照界面', self.chat_camera, 2),
            ('点击录像，进入录像界面', self.video_mode, 2),
            ('点击开始录像按钮，进入开始录像界面', self.start_recording, 3),
            ('点击停止录像按钮，进入待发送录像界面', self.stop_recording, 2),
            ('点击对号，进入好友聊天页面', self.send_capture, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
