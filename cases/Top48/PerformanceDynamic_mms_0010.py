"""系统信息通知浏览；Excel 第 1123～1128 行。"""
from Cases.Top48.mms_common import MmsDynamicCase


class PerformanceDynamic_mms_0010(MmsDynamicCase):
    def steps(self):
        return [
            ('启动信息', self.launch, 2),
            ('点击通知信息，进入通知信息页面', self.notifications, 2),
            ('浏览通知信息，上滑5次、下滑5次', lambda: self.browse(5, 5), 0),
            ('打开通知信息查看，重复操作2次', self.view_two_messages, 2),
            ('返回信息主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
