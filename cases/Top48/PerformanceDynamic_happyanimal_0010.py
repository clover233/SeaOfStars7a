"""开心消消乐启动后停留 15 秒并推入后台。"""
from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_happyanimal_0010(DynamicAppCase):
    PACKAGE = 'com.happyelements.AndroidAnimal'
    all_app_package_list = [PACKAGE]

    def background(self):
        """使用系统 Home 键推后台，避免横屏游戏的坐标和防误触差异。"""
        self.foreground()
        result = self.d.shell('input keyevent 3')
        if result.exit_code:
            raise RuntimeError('开心消消乐推后台失败：' + result.output)
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(),
                      '开心消消乐未进入后台', timeout=8)

    def steps(self):
        return [
            ('启动开心消消乐并停留15秒', self.start, 15),
            ('推后台返回Home页', self.background, 1),
        ]
