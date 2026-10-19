"""微信发布朋友圈；用例表1709～1724行。"""
from Cases.Top48.weixin_common import WeixinDynamicCase


class PerformanceDynamic_weixin_0060(WeixinDynamicCase):
    RECOVERY_CHECKPOINTS = ()

    NEED_IMAGES = True

    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('进入朋友圈', self.moments, 2),
            ('点击右上角的相机图标', self.moments_camera, 2),
            ('点击拍摄', self.camera_from_moments, 2),
            ('返回朋友圈', self.cancel_moments_camera, 2),
            ('点击右上角的相机图标', self.moments_camera, 2),
            ('从相册选择，选择图片3张', self.select_album, 2),
            ('点击预览', self.album_preview, 2),
            ('左滑2次浏览图片', self.preview_slides, 2),
            ('点击右上角完成', self.album_done, 2),
            ('点击所在位置', self.location, 2),
            ('选择具体位置，点击完成', self.select_location, 2),
            ('左滑返回一次', self.leave_draft, 2),
            ('点击不保留', self.discard_draft, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
