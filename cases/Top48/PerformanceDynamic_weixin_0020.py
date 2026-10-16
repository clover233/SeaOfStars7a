"""微信添加朋友和朋友圈；用例表1648～1661行。"""
from Cases.Top48.weixin_common import WeixinDynamicCase


class PerformanceDynamic_weixin_0020(WeixinDynamicCase):
    NEED_IMAGES = True

    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击右上角+号', self.plus_menu, 2),
            ('点击右上角+号，切换到添加朋友页面', self.add_friend, 2),
            ('点击搜索框，输入好友账号点击查询', self.friend_query, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('点击发现，切换到发现页面', self.discover, 2),
            ('点击朋友圈，切换到朋友圈页面', self.moments, 2),
            ('浏览朋友圈上滑3次，下滑3次', self.browse_moments, 2),
            ('在第一条朋友圈评论真不错', self.comment, 2),
            ('点击右上角相机按钮', self.moments_camera, 2),
            ('点击拍摄，切换到拍照页面后，返回上一页', self.camera_and_back, 2),
            ('9宫格选择9张照片', self.nine_photos, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
