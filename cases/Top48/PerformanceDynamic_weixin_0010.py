"""微信聊天和互动；用例表1633～1647行。"""
from Cases.Top48.weixin_common import WeixinDynamicCase


class PerformanceDynamic_weixin_0010(WeixinDynamicCase):
    RECOVERY_CHECKPOINTS = ('wechat_home',)

    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击性能图片群，进入群聊界面', self.picture_chat, 2),
            ('点击一张图片，向右滑动3次向左滑动3次浏览图片页面', self.browse_pictures, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('点击性能测试群，进入群聊界面', self.video_chat, 2),
            ('点击一个视频，进入查看视频界面，向右滑动3次向左滑动3次', self.browse_video, 2),
            ('长按视频，进入待转发视频页面', self.video_menu, 2),
            ('点击转发给朋友，进入转发视频界面', self.forward_picker, 2),
            ('点击测试账号，进入确认发送界面', self.forward_recipient, 2),
            ('点击发送，完成发送并进入查看视频界面', self.forward_send, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('点击性能测试语音群，进入群聊界面', self.voice_chat, 2),
            ('点击一个语音进行播放', self.play_voice, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
