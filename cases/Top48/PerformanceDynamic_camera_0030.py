"""对应动态性能模型测试用例7.xlsx：相机 0030。"""
from Cases.Top48.camera_common import CameraDynamicCase


class PerformanceDynamic_camera_0030(CameraDynamicCase):
    def steps(self):
        return [
            ('启动相机', self.launch, 3),
            ('设置4X变焦', lambda: self.zoom(4), 1),
            ('点击屏幕中间对焦并拍照5次', self.five_photos, 1),
            ('点击左下角缩略图查看图片', self.gallery, 1),
            ('左滑8次查看其它照片', self.browse_photos, 1),
            ('返回相机拍照界面', self.return_preview, 1),
            ('后置切换前置', lambda: self.switch_camera('前置'), 1),
            ('前置切换后置', lambda: self.switch_camera('后置'), 1),
            ('切换到录像模式', lambda: self.mode('录像'), 1),
            ('录像设置4X、1080P60FPS', lambda: self.video_config(4, 60), 1),
            ('开始录像', self.start_recording, 0),
            ('录制达到10秒后结束录像', self.stop_after_ten, 1),
            ('恢复1X、1080P30FPS', lambda: self.video_config(1, 30), 1),
            ('点击左下角查看视频', self.gallery, 1),
            ('点击播放视频', self.play_video, 3),
            ('返回相机录像界面', self.return_preview, 1),
            ('右滑进入拍照界面', self.swipe_photo_mode, 1),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
