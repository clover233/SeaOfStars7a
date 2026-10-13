"""备忘录浏览列表；对应模型表第 210—214 行。"""
from Cases.Top48.beiwanglu_common import BeiwangluDynamicCase


class PerformanceDynamic_beiwanglu_0020(BeiwangluDynamicCase):
    def steps(self):
        return [
            ('启动备忘录', self.launch, 3),
            ('上滑2次，下滑2次，查看备忘录列表', self.browse_notes, 1),
            ('点击第一条备忘录查看内容', self.first_note, 3),
            ('返回备忘录主界面', self.notes_home, 1),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
