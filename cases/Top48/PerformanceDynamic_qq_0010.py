"""QQ浏览动态；用例表1251～1258行。"""
from Cases.Top48.qq_common import QQDynamicCase


class PerformanceDynamic_qq_0010(QQDynamicCase):
    def steps(self):
        return [
            ('启动QQ', self.launch, 3),
            ('点击动态', self.dynamics, 1),
            ('点击空间动态', self.space, 1),
            ('空间动态上滑5次下滑5次', self.browse_space, 0),
            ('查看动态图片', self.space_picture, 1),
            ('图片横向滑动3次', self.space_slides, 1),
            ('返回QQ主界面', self.messages, 1),
            ('滑动返回Home页', self.home, 1),
        ]
