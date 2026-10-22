"""豆包拍照修图、相册选图合成视频和实时通话（表格第 500～515 行）。"""
import logging
import time

from Cases.Top48.doubao_common import DoubaoDynamicCase


class PerformanceDynamic_doubao_0020(DoubaoDynamicCase):
    all_app_package_list = [DoubaoDynamicCase.PACKAGE]
    # 拍照和实时通话在采集前准备权限，避免系统弹窗被当成相机页面。
    PERMISSIONS = ('CAMERA', 'RECORD_AUDIO', 'READ_MEDIA_IMAGES')
    TEST_ALBUM = '动态性能素材'

    def set_up(self):
        super().set_up()
        from Cases.Top48.fixture_images import prepare_images
        prepare_images(self.d, self.TEST_ALBUM, 5)

    def photo_for_retouch(self):
        return self.camera_photo()

    def retouch(self):
        return self.enter_text('帮我修图')

    def photo_for_video(self):
        if self.camera_photo() is False:
            return False
        # 新版确认照片停在独立结果页，发送图片后才回到带“+”的对话页。
        if self.camera_result_ready():
            button = self.send_button()
            if button is None:
                raise RuntimeError('拍照结果页没有确认发送入口')
            self.click_node(button)
            self.wait_for(lambda: not self.camera_result_ready() and self.chat_ready(),
                          '确认照片后未返回豆包对话页', timeout=25)

    def choose_album_photos(self):
        return self.choose_two_photos()

    def choose_two_photos(self):
        if not getattr(self, 'album_open', False):
            raise RuntimeError('选择测试图片前未打开相册')
        self.open_control(lambda: self.has(text=self.TEST_ALBUM, rid='item_folder_name'),
                          '豆包相册列表未打开', rid='title_folder_entrance')
        self.click(text=self.TEST_ALBUM, rid='item_folder_name')
        self.wait_for(lambda: self.has(text=self.TEST_ALBUM, rid='title_folder_entrance'),
                      '未进入专用测试相册')
        return super().choose_two_photos()

    def make_video(self):
        return self.enter_text('合成视频')

    def wait_in_call(self):
        if not getattr(self, 'call_available', False):
            logging.warning('SKIP：豆包通话未打开，跳过停留15秒')
            return False
        # 表格指定停留 15 秒，逐秒确认界面没有意外退出。
        for second in range(15):
            if not self.call_active():
                raise RuntimeError('豆包通话在第 {} 秒前已退出'.format(second))
            time.sleep(1)

    def steps(self):
        return [
            ('启动豆包', self.launch, 3),
            ('点击拍照，进行拍摄并确认', self.photo_for_retouch, 2),
            ('输入帮我修图', self.retouch, 2),
            ('点击发送', self.send_pending, 2),
            ('点击拍照，进行拍摄并确认', self.photo_for_video, 2),
            ('点击加号', self.open_media_menu, 2),
            ('选择从相册选择', self.choose_from_album, 2),
            ('上滑3次浏览所有图片', lambda: self.browse_external(3, 0, pause=1), 0),
            ('下滑3次浏览所有图片', lambda: self.browse_external(0, 3, pause=1), 0),
            ('选择2张照片后点完成', self.choose_two_photos, 2),
            ('在输入框输入合成视频', self.make_video, 2),
            ('点击发送', self.send_pending, 2),
            ('点击右上角电话图标', self.call, 2),
            ('在与豆包通话界面停留15s', self.wait_in_call, 0),
            ('退出通话界面', self.exit_call, 2),
            ('滑动返回Home页', self.home, 1),
        ]
