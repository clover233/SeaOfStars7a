"""抖音创作页、Test 会话和视频分享（表格第 577～609 行）。"""
from Cases.Top48.douyin_common import DouyinDynamicCase


class PerformanceDynamic_douyin_0050(DouyinDynamicCase):
    all_app_package_list = [DouyinDynamicCase.PACKAGE]

    def chat_media(self, action):
        return self.unavailable_chat_media(action)

    def browse_album(self):
        if self.chat_media('相册'):
            self.browse(3, 3)

    def steps(self):
        return [
            ('启动抖音', self.launch, 3),
            ('点击加号进入创作页', self.open_create, 2),
            ('点击相册', lambda: self.create_click('相册'), 2),
            ('返回加号页', self.back_in_create, 1),
            ('点击照片', lambda: self.create_click('照片'), 1),
            ('点击拍照', lambda: self.create_click('拍照'), 2),
            ('点击选择音乐', lambda: self.create_click('选择音乐'), 2),
            ('选择音乐页面上滑6次', lambda: self.browse(6, 0), 0),
            ('返回照片编辑页面', self.back_in_create, 1),
            ('点击下一步', lambda: self.create_click('下一步'), 2),
            ('点击预览', lambda: self.create_click('预览'), 2),
            ('返回抖音首页', self.return_feed, 2),
            ('点击消息页面', self.open_messages, 1),
            ('进入Test聊天界面并向下滑动3次', lambda: (self.open_test_chat(), self.browse(0, 3)), 2),
            ('发送文字华为手机', self.send_chat_text, 2),
            ('发送一个动态表情包', self.send_dynamic_emoji, 2),
            ('点击聊天加号', self.open_chat_media, 1),
            ('点击拍摄', lambda: self.chat_media('拍摄'), 2),
            ('拍摄图片', lambda: self.chat_media('拍摄图片'), 2),
            ('发送图片', lambda: self.chat_media('发送图片'), 2),
            ('点击拍摄', lambda: self.chat_media('拍摄'), 2),
            ('拍摄视频', lambda: self.chat_media('拍摄视频'), 2),
            ('发送视频', lambda: self.chat_media('发送视频'), 2),
            ('点击聊天加号', self.open_chat_media, 1),
            ('点击相册', lambda: self.chat_media('相册'), 1),
            ('相册页面上滑3次、下滑3次', self.browse_album, 0),
            ('点击第一张图片', lambda: self.chat_media('选择第一张图片'), 1),
            ('点击发送', lambda: self.chat_media('发送相册图片'), 2),
            ('返回抖音首页', self.return_feed, 2),
            ('点击分享并选择Test账号', self.share_to_test, 2),
            ('点击发送', self.confirm_share, 2),
            ('返回抖音主界面', self.return_feed, 2),
            ('滑动返回Home页', self.home, 1),
        ]
