"""照片实发的会话、素材与数量保护，无实机操作。"""
import unittest
from unittest.mock import Mock

from Cases.Top48.weixin_common import WeixinStepSkipped
from Cases.Top48.weixin_remaining import WeixinRemainingCase


class PhotoDeliveryGuardsTest(unittest.TestCase):
    def case(self):
        c = object.__new__(WeixinRemainingCase)
        c.unavailable = {}
        c._chat = c.TEST_CONTACT
        c._verified_chat = c.TEST_CONTACT
        c._album_origin_verified = True
        c._album_selected = 3
        c.visible = Mock(return_value=True)
        c.choose = Mock()
        c.require_delivery = Mock()
        c.chat_ready = Mock(return_value=True)
        c.wait_for = lambda predicate, message: self.assertTrue(predicate(), message)
        return c

    def test_wrong_receiver_cannot_send(self):
        c = self.case()
        c._chat = '测试账号'
        with self.assertRaises(RuntimeError):
            c.send_chat_photos()
        c.choose.assert_not_called()

    def test_unverified_album_cannot_send(self):
        c = self.case()
        c._album_origin_verified = False
        with self.assertRaises(WeixinStepSkipped):
            c.send_chat_photos()
        c.choose.assert_not_called()

    def test_wrong_count_cannot_send(self):
        c = self.case()
        c._album_selected = 1
        with self.assertRaises(RuntimeError):
            c.send_chat_photos()
        c.choose.assert_not_called()

    def test_send_once_and_check_returned_chat(self):
        c = self.case()
        c.send_chat_photos()
        c.choose.assert_called_once_with('发送3', True, region=(.65, .85, 1, 1))
        c.chat_ready.assert_called_once_with(c.TEST_CONTACT)
        self.assertFalse(c._album_origin_verified)
        self.assertEqual(c._album_selected, 0)


if __name__ == '__main__':
    unittest.main()
