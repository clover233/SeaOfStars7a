"""王者荣耀启动运行30秒；用例表1548～1549行。"""
from Cases.Top48.game_weather_common import HonorLaunchCase


class PerformanceDynamic_wangzherongyao_0030(HonorLaunchCase):
    def steps(self):
        return [
            ('启动王者荣耀（运行30s）',self.launch_30,0),
            ('滑动返回Home页',self.home,2),
        ]
