"""豆包拍照修图、相册选图合成视频和实时通话（表格第 500～515 行）。"""
import time

from Cases.Top48.doubao_common import DoubaoDynamicCase


class PerformanceDynamic_doubao_0020(DoubaoDynamicCase):
    all_app_package_list = [DoubaoDynamicCase.PACKAGE]

    def photo_for_retouch(self):
        self.camera_photo()

    def retouch(self):
        self.enter_text('帮我修图')

    def photo_for_video(self):
        self.camera_photo()

    def choose_album_photos(self):
        self.choose_two_photos()

    def make_video(self):
        self.enter_text('合成视频')

    def wait_in_call(self):
        # 表格指定停留 15 秒，逐秒确认界面没有意外退出。
        for second in range(15):
            package = self.current_package()
            if package == self.PACKAGE and not (self.has(desc='挂断') or self.has(text='结束通话')):
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
