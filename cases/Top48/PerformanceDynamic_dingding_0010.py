"""钉钉消息页、群消息和群设置页浏览（表格第 441～449 行）。"""
from Cases.Top48.dingding_common import DingTalkDynamicCase


class PerformanceDynamic_dingding_0010(DingTalkDynamicCase):
    all_app_package_list = [DingTalkDynamicCase.PACKAGE]
    GROUP_NAME = '欢迎试用钉钉群'

    def group_ready(self):
        return self.has(text=self.GROUP_NAME, rid='tv_title') and self.has(rid='rich_edit_text')

    def open_trial_group(self):
        self.messages_page()
        self.open_control(self.group_ready, '未打开欢迎试用钉钉群',
                          text=self.GROUP_NAME, rid='session_title')

    def group_member_is_self_only(self):
        return any(node.get('text') == '1位成员'
                   for node in self.nodes(rid='tv_group_member_count'))

    def send_greeting(self):
        self.require(text=self.GROUP_NAME, rid='tv_title')
        # 仅允许在已核验的单人成员群中发送，避免把测试消息投递给其他会话。
        if not self.group_member_is_self_only():
            raise RuntimeError('欢迎试用钉钉群成员数不是 1，停止发送测试消息')
        editor = self.d(resourceId=self.PACKAGE + ':id/rich_edit_text')
        editor.set_text('你好')
        self.wait_for(lambda: self.has(text='发送'), '输入消息后未显示发送按钮')
        before = len(self.nodes(text='你好', rid='tv_dup_text'))
        self.transition(lambda: self.click(text='发送'),
                        lambda: len(self.nodes(text='你好', rid='tv_dup_text')) > before
                        or not self.has(text='你好', rid='rich_edit_text'),
                        '群消息发送后未得到界面反馈')

    def group_info(self):
        self.open_control(lambda: self.has(text='群设置')
                          and self.has(text=self.GROUP_NAME, rid='tv_header_conversation_title'),
                          '群聊信息页未打开', desc='群聊信息')

    def messages_home(self):
        self.return_to(self.navigation_ready, '未返回钉钉主界面')
        self.switch_tab('消息')

    def steps(self):
        return [
            ('启动钉钉', self.launch, 3),
            ('点击消息图标，切换到消息页', self.messages_page, 2),
            ('点击欢迎试用钉钉群', self.open_trial_group, 2),
            ('群消息页面上滑2次、下滑2次', lambda: self.browse(2, 2), 0),
            ('输入你好并发送', self.send_greeting, 2),
            ('点击右上角更多，切换到更多页面', self.group_info, 2),
            ('更多页面上滑1次、下滑1次', lambda: self.browse(1, 1), 0),
            ('返回钉钉主界面', self.messages_home, 2),
            ('滑动返回Home页', self.home, 1),
        ]
