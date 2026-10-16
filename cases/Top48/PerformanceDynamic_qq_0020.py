"""QQ浏览消息；用例表1259～1269行。实发目标已确认为“多媒体消息”。"""
from Cases.Top48.qq_common import QQDynamicCase


class PerformanceDynamic_qq_0020(QQDynamicCase):
    NEED_TEST_IMAGE = True

    def steps(self):
        return [
            ('启动QQ', self.launch, 3),
            ('进入测试图片群', self.picture_chat, 1),
            ('群消息上滑2次下滑2次', self.browse_chat, 0),
            ('群聊大图右滑4次左滑4次', self.chat_pictures, 1),
            ('侧滑返回消息列表', self.side_to_messages, 1),
            ('进入多媒体消息群', self.multimedia_chat, 1),
            ('发送文字你好，动态', self.send_text, 1),
            ('发送表情', self.send_emoji, 1),
            ('发送专用测试图片', self.send_image, 1),
            ('侧滑返回消息页', self.side_to_messages, 1),
            ('滑动返回Home页', self.home, 1),
        ]
