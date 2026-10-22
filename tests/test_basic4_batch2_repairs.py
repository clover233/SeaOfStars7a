import unittest
import xml.etree.ElementTree as ET
from unittest.mock import Mock, patch

with patch('uiautomator2.connect'):
    from Cases.Top48.pinduoduo_common import PinduoduoDynamicCase
    from Cases.Top48.bilibili_common import BilibiliDynamicCase
    from Cases.Top48.tencent_media_common import QqMusicDynamicCase
    from Cases.Top48.PerformanceDynamic_wpsoffice_0010 import PerformanceDynamic_wpsoffice_0010
    from Cases.Top48.PerformanceDynamic_didichuxing_0020 import PerformanceDynamic_didichuxing_0020
    from Cases.Top48.weixin_common import WeixinDynamicCase


class StartupRecoveryTests(unittest.TestCase):
    def test_pdd_home_mount_wait_does_not_press_back(self):
        case = PinduoduoDynamicCase.__new__(PinduoduoDynamicCase)
        case.current_app = lambda: {'activity': 'com.xunmeng.pinduoduo.ui.activity.HomeActivity'}
        case.foreground = Mock()
        case.home_ready = Mock(side_effect=[False, True])
        case.wait_for = lambda predicate, *args, **kwargs: self.assertTrue(predicate())
        case.back = Mock()
        case.main_page()
        case.back.assert_not_called()

    def test_brand_hall_requires_its_own_activity_and_content(self):
        case = PinduoduoDynamicCase.__new__(PinduoduoDynamicCase)
        case.current_app = lambda: {'activity': 'com.xunmeng.pinduoduo.activity.NewPageActivity'}
        case.has = lambda **kwargs: kwargs.get('text') in ('商品由第三方商家提供', '该品牌累计热销')
        self.assertTrue(case.store_ready())
        case.current_app = lambda: {'activity': 'com.xunmeng.pinduoduo.activity.GoodsActivity'}
        self.assertFalse(case.store_ready())


class LiveFullscreenTests(unittest.TestCase):
    def test_hidden_chat_input_does_not_reject_landscape_live_player(self):
        case = BilibiliDynamicCase.__new__(BilibiliDynamicCase)
        case.click = Mock()
        case.click_node = Mock()
        case.nodes = lambda **kwargs: [object()] if kwargs else []
        case.landscape = lambda: True
        case.has = lambda rid: rid in ('roomid', 'controller_underlay')
        case.current_app = lambda: {'activity': 'com.bilibili.bililive.room.ui.roomv3.LiveRoomActivityV3'}
        case.wait_for = lambda predicate, *args, **kwargs: self.assertTrue(predicate())
        case.live_fullscreen()

    def test_landscape_non_live_activity_is_rejected(self):
        case = BilibiliDynamicCase.__new__(BilibiliDynamicCase)
        case.click = Mock()
        case.click_node = Mock()
        case.nodes = lambda **kwargs: [object()]
        case.landscape = lambda: True
        case.has = lambda rid: rid in ('roomid', 'controller_underlay')
        case.current_app = lambda: {'activity': 'OtherVideoActivity'}
        def wait(predicate, *args, **kwargs):
            self.assertFalse(predicate())
            raise RuntimeError('not live')
        case.wait_for = wait
        with self.assertRaises(RuntimeError):
            case.live_fullscreen()


class MusicAdTests(unittest.TestCase):
    def test_ad_activity_cannot_match_background_home_navigation(self):
        case = QqMusicDynamicCase.__new__(QqMusicDynamicCase)
        case.activity_is = lambda *names: 'TMECoreActivity' in names
        case.visible = Mock(return_value=True)
        self.assertFalse(case.main_ready())
        case.visible.assert_not_called()


class OwnerMarketingTests(unittest.TestCase):
    def test_both_owner_reward_templates_are_recognized(self):
        detect = PerformanceDynamic_didichuxing_0020.owner_marketing
        self.assertTrue(detect([{'text': '副业跑滴滴'}, {'text': '享新人奖励'}]))
        self.assertTrue(detect([{'text': '劏业跑滴滴'}, {'text': '享新人奖励'}]))
        self.assertTrue(detect([{'text': '成为顺风车车主'}, {'text': '新车王'}, {'text': '奖励'}]))
        self.assertFalse(detect([{'text': '车主服务'}, {'text': '特惠洗车'}, {'text': '成为司机'}]))

    @patch('Cases.Top48.PerformanceDynamic_didichuxing_0020.time.sleep')
    def test_named_ad_close_survives_resource_id_change(self, _):
        case = PerformanceDynamic_didichuxing_0020.__new__(PerformanceDynamic_didichuxing_0020)
        close = ET.Element('node', {'resource-id': case.PACKAGE+':id/close_dialog'})
        case.nodes = Mock(side_effect=[[close], []])
        case.click_node = Mock()
        case.has = Mock(return_value=False)
        case.owner_ready = Mock(return_value=False)
        case.dismiss_ad()
        case.click_node.assert_called_once_with(close)


class WpsNavigationTests(unittest.TestCase):
    def test_auto_hidden_toolbar_does_not_hide_document_identity(self):
        case = PerformanceDynamic_wpsoffice_0010.__new__(PerformanceDynamic_wpsoffice_0010)
        case.current_app = lambda: {'activity': 'cn.wps.moffice.writer.multiactivity.Writer1'}
        case.has = lambda **kw: kw.get('rid') == 'writer_layout'
        self.assertTrue(case.document_ready())

    def test_blank_writer_frame_does_not_count_as_readable_document(self):
        case = PerformanceDynamic_wpsoffice_0010.__new__(PerformanceDynamic_wpsoffice_0010)
        case.document_ready = lambda: True
        case._locators = set()
        case.body_rows = lambda: []
        self.assertFalse(case.readable_document())
        case.body_rows = lambda: [{'text': 'body paragraph'}]*3
        self.assertTrue(case.readable_document())

    def test_navigation_requires_selected_resource_id_not_page_title(self):
        case = PerformanceDynamic_wpsoffice_0010.__new__(PerformanceDynamic_wpsoffice_0010)
        case.nodes = lambda **kw: [ET.Element('node', selected='false')]
        self.assertFalse(case.tab_selected('首页'))
        case.nodes = lambda **kw: [ET.Element('node', selected='true')]
        self.assertTrue(case.tab_selected('首页'))

    @patch('Cases.Top48.PerformanceDynamic_wpsoffice_0010.time.sleep')
    def test_offer_close_that_also_exits_payment_does_not_press_back_again(self, _):
        case = PerformanceDynamic_wpsoffice_0010.__new__(PerformanceDynamic_wpsoffice_0010)
        case.navigation_ready = Mock(side_effect=[False, True])
        close = ET.Element('node')
        case.member_offer_closes = lambda: [close]
        case.click_node = Mock()
        case.back = Mock()
        case._locators = set()
        case.return_navigation()
        case.click_node.assert_called_once_with(close)
        case.back.assert_not_called()

    def test_unnamed_payment_button_is_not_offer_close(self):
        case = PerformanceDynamic_wpsoffice_0010.__new__(PerformanceDynamic_wpsoffice_0010)
        case.has = lambda **kw: True
        case.screen_size = lambda: (1000, 2000)
        close = ET.Element('node', {'class': 'android.view.View', 'clickable': 'true',
                                   'bounds': '[450,1450][550,1550]'})
        pay = ET.Element('node', {'class': 'android.view.View', 'clickable': 'true',
                                 'bounds': '[200,1200][800,1350]'})
        case.nodes = lambda: [pay, close]
        self.assertEqual(case.member_offer_closes(), [close])


class LuckinPromptTests(unittest.TestCase):
    def test_ocr_title_missing_de_is_still_closed_with_ratios(self):
        case = WeixinDynamicCase.__new__(WeixinDynamicCase)
        case.visible = lambda *a, **kw: False
        case.find = lambda label, *a, **kw: [dict(text='距你最近门店，是否前往', y=.60, h=.03)]
        case.nodes = lambda **kw: []
        case._locators = set()
        case.invalidate = Mock()
        case.wait_for = lambda predicate, *a, **kw: self.assertTrue(predicate())
        device = Mock()
        with patch.object(WeixinDynamicCase, 'd', property(lambda self: device)):
            case.dismiss_luckin_prompts()
        x, y = device.click.call_args.args
        self.assertAlmostEqual(x, .897)
        self.assertTrue(0 < y < 1)

    def test_non_single_quantity_blocks_add_to_cart(self):
        case = WeixinDynamicCase.__new__(WeixinDynamicCase)
        case.unavailable = {}
        case.visible = lambda *a, **kw: False
        case.choose = Mock()
        with self.assertRaises(RuntimeError):
            case.luckin_cart()
        case.choose.assert_not_called()


if __name__ == '__main__':
    unittest.main()
