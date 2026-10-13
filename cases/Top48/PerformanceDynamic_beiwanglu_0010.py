"""备忘录新建笔记及待办；对应模型表第 200—209 行。"""
from Cases.Top48.beiwanglu_common import BeiwangluDynamicCase


class PerformanceDynamic_beiwanglu_0010(BeiwangluDynamicCase):
    def steps(self):
        return [
            ('启动备忘录', self.launch, 3),
            ('点击新建笔记图标', self.new_note, 1),
            ('输入动态并点击保存', self.write_note, 1),
            ('返回备忘录首页', self.notes_home, 1),
            ('点击待办，切换到待办页', self.todos, 1),
            ('点击新建按钮，拉起输入法', self.new_todo, 1),
            ('26键盘输入test，点击键盘回车', self.type_todo, 1),
            ('点击保存按钮', self.save_todo, 1),
            ('返回备忘录主界面', self.notes_home, 1),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
