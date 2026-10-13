"""输入并删除10086、浏览通话记录；对应模型表第310—315行。"""
from Cases.Top48.call_common import CallDynamicCase


class PerformanceDynamic_call_0020(CallDynamicCase):
    def steps(self):
        return [
            ('启动电话', self.launch, 3),
            ('点击电话，查看所有通话', self.phone, 1),
            ('输入号码10086后，删除键删除号码', self.number_and_delete, 1),
            ('点击拨号键盘上方空白处', self.hide_keypad_by_blank, 1),
            ('上滑5次下滑5次浏览拨打历史记录', self.browse, 1),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
