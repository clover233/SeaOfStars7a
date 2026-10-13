"""对应动态性能模型测试用例7.xlsx：相机 0020。"""
from Cases.Top48.camera_common import CameraDynamicCase


class PerformanceDynamic_camera_0020(CameraDynamicCase):
    def steps(self):
        return [
            ('启动相机', self.launch, 3),
            ('点击广角W并拍照', lambda: self.zoom_photo(.7), 1),
            ('点击1X并拍照', lambda: self.zoom_photo(1), 1),
            ('点击2X并拍照', lambda: self.zoom_photo(2), 1),
            ('点击10X并拍照', lambda: self.zoom_photo(10), 1),
            ('点击箭头拉起设置菜单', self.open_menu, 1),
            ('点击设置', self.settings, 1),
            ('设置页面上滑1次下滑1次，重复3次', self.browse_settings, 1),
            ('点击照片比例（MIUI画幅）', self.photo_ratio, 1),
            ('取消照片比例选择', self.cancel_ratio, 1),
            ('点击照片格式', self.photo_format, 1),
            ('取消照片格式选择', self.cancel_format, 1),
            ('点击声控拍照', self.voice_shutter, 1),
            ('取消声控拍照弹框', self.cancel_voice, 1),
            ('侧滑返回预览框', self.side_to_preview, 1),
            ('点击小艺视觉（没有则跳过）', self.visual, 1),
            ('小艺视觉点击拍照', self.visual_photo, 1),
            ('侧滑返回扫一扫', self.visual_back, 1),
            ('点击左侧图库（没有则跳过）', self.visual_gallery, 1),
            ('图库上滑3次下滑3次', self.browse_visual_gallery, 1),
            ('侧滑返回扫一扫', self.visual_gallery_back, 1),
            ('返回相机主界面', self.return_preview, 1),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
