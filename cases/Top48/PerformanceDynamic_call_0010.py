"""浏览联系人并搜索atest；对应模型表第301—309行。"""
from Cases.Top48.call_common import CallDynamicCase


class PerformanceDynamic_call_0010(CallDynamicCase):
    def steps(self):
        return [
            ('启动电话', self.launch, 3),
            ('点击屏幕底部联系人', self.contacts, 1),
            ('联系人页面上滑2次下滑2次', lambda: self.browse(up=2, down=2), 1),
            ('点击搜索框', self.search_box, 1),
            ('输入atest，点击第一条搜索记录进入详情', self.search_contact, 1),
            ('返回联系人界面', self.return_contacts, 1),
            ('联系人页面上滑5次下滑5次', self.browse, 1),
            ('返回电话主界面', self.phone, 1),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
