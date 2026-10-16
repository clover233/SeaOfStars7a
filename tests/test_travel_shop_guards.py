"""不连接设备：客服授权、重复发送与前置状态隔离。"""
import os
import unittest
from unittest.mock import Mock, PropertyMock, patch
from Cases.Top48.travel_shop_common import TravelShopCase, TaobaoDynamicCase, SodaMusicDynamicCase, QunarDynamicCase, StepUnavailable

class TravelShopGuardsTest(unittest.TestCase):
    def setUp(self):
        p=patch.object(TravelShopCase,'d',new_callable=PropertyMock,return_value=Mock());p.start();self.addCleanup(p.stop)

    def customer(self):
        c=object.__new__(TaobaoDynamicCase);c.unavailable={};c._verified_product=True
        c._customer_header='清风官方旗舰店';c.chat_header=Mock(return_value=c._customer_header)
        c.chat_ready=Mock(return_value=True);c.input_text=Mock();c.entry=Mock()
        return c

    def test_customer_requires_explicit_runtime_opt_in(self):
        c=self.customer()
        with patch.dict(os.environ,{c.SEND_ENV:'0'}),self.assertRaises(StepUnavailable):c.send_hello()
        c.input_text.assert_not_called();c.entry.assert_not_called()

    def test_changed_customer_cannot_receive_message(self):
        c=self.customer();c.chat_header.return_value='其他店铺'
        with patch.dict(os.environ,{c.SEND_ENV:'1'}),self.assertRaises(StepUnavailable):c.send_hello()
        c.input_text.assert_not_called()

    def test_unverified_product_cannot_receive_message(self):
        c=self.customer();c._verified_product=False
        with patch.dict(os.environ,{c.SEND_ENV:'1'}),self.assertRaises(StepUnavailable):c.send_hello()
        c.input_text.assert_not_called()

    def test_hello_is_not_retried_after_send_attempt(self):
        c=self.customer();c._hello_attempted=True
        with patch.dict(os.environ,{c.SEND_ENV:'1'}),self.assertRaises(StepUnavailable):c.send_hello()
        c.input_text.assert_not_called()

    def test_picture_is_not_retried_after_send_attempt(self):
        c=self.customer();c._picture_attempted=True;c.native=Mock()
        with patch.dict(os.environ,{c.SEND_ENV:'1'}),self.assertRaises(StepUnavailable):c.send_picture()
        c.native.assert_not_called()

    def test_missing_search_prevents_product_click(self):
        c=self.customer();c.unavailable={'search':'未登录'};c.click_node=Mock()
        with self.assertRaises(StepUnavailable):c.sales_first()
        c.click_node.assert_not_called()

    def test_input_without_edit_field_does_not_broadcast(self):
        c=object.__new__(TravelShopCase);c.nodes=Mock(return_value=[])
        with self.assertRaises(StepUnavailable):c.input_text('西安')
        c.d.shell.assert_not_called()

    def test_music_main_page_does_not_toggle_playback(self):
        c=object.__new__(SodaMusicDynamicCase);c.dismiss_ads=Mock();c.return_to=Mock();c.native=Mock()
        c.main_page();c.native.assert_not_called()

    def test_already_playing_music_waits_then_pauses_only(self):
        c=object.__new__(SodaMusicDynamicCase);c.unavailable={};c.main_page=Mock()
        c.media_state=Mock(return_value=3);c.play_control=Mock();c.content_wait=Mock()
        with patch('Cases.Top48.travel_shop_common.time.sleep') as sleep:c.play_pause()
        sleep.assert_called_once_with(15);c.play_control.assert_called_once_with(True)

    def test_flight_failure_prevents_booking(self):
        c=object.__new__(QunarDynamicCase);c.unavailable={'flight_detail':'没有航班'};c.entry=Mock()
        with self.assertRaises(StepUnavailable):c.booking()
        c.entry.assert_not_called()

if __name__=='__main__':unittest.main()
