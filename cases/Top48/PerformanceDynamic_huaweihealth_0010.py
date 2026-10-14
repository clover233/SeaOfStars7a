"""华为运动健康浏览锻炼页面；对应 Excel 第 740～747 行。"""
from Cases.Top48.huaweihealth_common import HuaweiHealthDynamicCase


class PerformanceDynamic_huaweihealth_0010(HuaweiHealthDynamicCase):
    def steps(self):
        return [
            ('启动华为运动健康', self.launch, 3),
            ('切换至运动页面并进入户外跑步计时', self.start_workout, 0),
            ('15秒后长按结束运动', self.wait_and_end_workout, 1),
            ('点击屏幕底部今日', self.today, 2),
            ('点击三叶草查看详情', self.open_clover, 2),
            ('上滑1次，下滑1次，浏览详情页面', lambda: self.browse(1, 1), 0),
            ('返回华为运动健康主界面', self.return_to_main, 2),
            ('滑动返回Home页', self.home, 1),
        ]
