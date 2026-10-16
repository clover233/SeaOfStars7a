"""微信转账；用例表1789～1801行。"""
from Cases.Top48.weixin_common import WeixinExtendedCase


class PerformanceDynamic_weixin_0120(WeixinExtendedCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('点击测试账号，进入好友聊天页面', self.test_chat, 2),
            ('点击加号，进入更多功能页面', self.chat_more, 2),
            ('点击红包，进入红包页面后，返回上一页面', self.red_packet_preview, 2),
            ('点击加号，进入更多功能页面', self.chat_more, 2),
            ('点击转账，进入转账页面', self.transfer, 2),
            ('点击添加转账说明，进入添加说明页面', self.transfer_memo, 2),
            ('输入修改', self.edit_memo, 2),
            ('点击确定，进入转账页面', self.confirm_memo, 2),
            ('返回好友聊天页面', self.return_test_chat, 2),
            ('下滑3次浏览好友聊天页面', self.browse_test_chat, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
