"""微信发送通话；用例表1678～1694行。"""
from Cases.Top48.weixin_common import WeixinDynamicCase


class PerformanceDynamic_weixin_0040(WeixinDynamicCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击测试账号，进入好友聊天页面', self.test_chat, 2),
            ('点击输入框，进入消息编辑界面', self.edit_message, 2),
            ('输入哈哈哈，点击发送', self.send_text, 2),
            ('点击语音按钮，发送语音给好友', self.send_voice, 2),
            ('点击表情包按钮，进入表情框界面', self.emoji_panel, 2),
            ('点击选择前三个表情，点击发送', self.send_emoji, 2),
            ('点击加号按钮，进入更多功能页面', self.chat_more, 2),
            ('点击视频通话，进入选择通话界面', self.call_picker, 2),
            ('点击视频通话，进入视频通话界面', self.video_call, 2),
            ('点击挂断按钮，好友聊天页面', self.hang_up, 2),
            ('点击加号按钮，进入更多功能页面', self.chat_more, 2),
            ('点击视频通话，进入选择通话界面', self.call_picker, 2),
            ('点击语音通话，进入语音通话界面', self.voice_call, 2),
            ('点击挂断按钮，好友聊天页面', self.hang_up, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
