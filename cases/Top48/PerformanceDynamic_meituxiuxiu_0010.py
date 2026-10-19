"""美图秀秀图片编辑和相机拍照；Excel 第 1094～1112 行。"""
from Cases.Top48.meituxiuxiu_common import MeituXiuxiuDynamicCase


class PerformanceDynamic_meituxiuxiu_0010(MeituXiuxiuDynamicCase):
    RECOVERY_CHECKPOINTS = ('main_page',)

    def steps(self):
        return [
            ('启动美图秀秀', self.launch, 2),
            ('点击导入图片，切换到图片页面', self.import_page, 2),
            ('选择第一张图片，点击滤镜', self.first_image_and_filter, 2),
            ('选中第一种滤镜格式并确认', self.first_filter, 2),
            ('点击调色，将亮度设置为100%并确认', self.brightness_100, 2),
            ('点击保存', self.save, 2),
            ('点击再修一张，切换到图片页面', self.edit_another, 2),
            ('返回美图秀秀主界面', self.main_page, 2),
            ('点击相机', self.camera, 2),
            ('点击滤镜', self.camera_filter, 2),
            ('切换一次滤镜', self.switch_camera_filter, 2),
            ('点击右下角箭头收起滤镜弹框', self.collapse_camera_filter, 2),
            ('点击快门进行拍照', self.shutter, 2),
            ('点击编辑', self.edit_photo, 2),
            ('点击调色，将亮度设置为100%并确认', self.brightness_100, 2),
            ('点击保存', self.save, 2),
            ('点击再修一张，切换到图片页面', self.edit_another, 2),
            ('返回美图秀秀主界面', self.main_page, 2),
            ('滑动桌面', self.home, 2),
        ]
