"""支付导航的前置条件与页面识别回归，不连接实机。"""
import unittest
from unittest.mock import Mock

from Cases.Top48.weixin_common import WeixinStepSkipped
from Cases.Top48.weixin_extended import WeixinExtendedCase


class WeixinExtendedGuardsTest(unittest.TestCase):
    def case(self):
        case = object.__new__(WeixinExtendedCase)
        case.unavailable = {}
        return case

    def test_transfer_stops_before_click_if_chat_is_unverified(self):
        case = self.case()
        case.require_test_chat = Mock(side_effect=WeixinStepSkipped('会话不符'))
        case.choose = Mock()
        with self.assertRaises(WeixinStepSkipped):
            case.transfer()
        case.choose.assert_not_called()

    def test_missing_transfer_skips_memo_input(self):
        case = self.case()
        case.unavailable['transfer'] = '没有转账入口'
        case.input_text = Mock()
        with self.assertRaises(WeixinStepSkipped):
            case.edit_memo()
        case.input_text.assert_not_called()

    def test_memo_confirm_clicks_only_dialog_confirm(self):
        case = self.case()
        case.await_text = Mock()
        case.choose = Mock()
        case.content_wait = Mock()
        case.confirm_memo()
        case.choose.assert_called_once_with('确定')

    def test_live_square_is_not_a_live_room(self):
        case = self.case()
        case.activity_is = lambda name: name.lower() in 'finderlivesquarenewentranceui'
        self.assertFalse(case.live_ready())
        case.activity_is = lambda name: name.lower() in 'finderlivevisitorui'
        self.assertTrue(case.live_ready())


if __name__ == '__main__':
    unittest.main()
