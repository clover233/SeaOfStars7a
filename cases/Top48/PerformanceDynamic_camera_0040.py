"""对应动态性能模型测试用例7.xlsx：相机 0040。"""
from Cases.Top48.camera_common import CameraDynamicCase


class PerformanceDynamic_camera_0040(CameraDynamicCase):
    def steps(self):
        return [
            ('启动相机', self.launch, 3),
            ('点击尝试AI唤起小爱同学', self.open_ai, 1),
            ('输入并发送我要拍夕阳应该怎么拍', self.ask_ai, 1),
            ('等待10秒后退出AI', self.close_ai, 1),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
