"""华为运动健康浏览设备页面；对应 Excel 第 748～753 行。"""
from Cases.Top48.huaweihealth_common import HuaweiHealthDynamicCase


class PerformanceDynamic_huaweihealth_0020(HuaweiHealthDynamicCase):
    def steps(self):
        return [
            ('启动华为运动健康', self.launch, 3),
            ('点击设备，进入设备界面', self.device, 2),
            ('点击右上角更多图标，进入更多功能页面', self.open_more, 1),
            ('进入扫一扫页面后返回，重复3次', self.scan_three_times, 0),
            ('返回华为运动健康主界面', self.return_to_main, 2),
            ('滑动返回Home页', self.home, 1),
        ]
