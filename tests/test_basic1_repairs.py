"""复现 Basic1 的新版无障碍文本、同名操作表和精选状态差异。"""
import unittest
from unittest.mock import Mock, patch
import xml.etree.ElementTree as ET

with patch('uiautomator2.connect'):
    from Cases.Top48.PerformanceDynamic_xhs_0030 import PerformanceDynamic_xhs_0030
    from Cases.Top48.kuaishou_common import KuaishouDynamicCase
    from Cases.Top48.PerformanceDynamic_xianyu_0010 import PerformanceDynamic_xianyu_0010
    from Cases.Top48.PerformanceDynamic_momo_0010 import PerformanceDynamic_momo_0010
    from Cases.Top48.weixin_common import WeixinDynamicCase, WeixinStepSkipped


class Basic1RepairTests(unittest.TestCase):
    def test_live_retention_cards_are_not_the_live_list(self):
        case = PerformanceDynamic_momo_0010.__new__(PerformanceDynamic_momo_0010)
        case.has = lambda **kw: kw.get('rid') == 'live_center_layout'
        case.current_app = lambda: {'activity': 'com.immomo.molive.gui.activities.live.base.LiveActivity'}
        self.assertFalse(case.live_list())
        case.current_app = lambda: {'activity': 'com.immomo.momo.android.activity.MainTabActivity'}
        self.assertTrue(case.live_list())

    def test_product_wrapper_dedup_does_not_hide_the_card(self):
        case = PerformanceDynamic_xianyu_0010.__new__(PerformanceDynamic_xianyu_0010)
        case.screen_size = lambda: (1220, 2656)
        case.hierarchy = lambda: '''<hierarchy>
          <node package="com.taobao.idlefish" class="android.widget.FrameLayout"
                bounds="[20,700][599,1791]" clickable="false">
            <node package="com.taobao.idlefish" class="android.widget.FrameLayout"
                  bounds="[20,700][599,1791]" clickable="true">
              <node package="com.taobao.idlefish" class="android.widget.TextView"
                    bounds="[33,1600][57,1639]" text="¥" />
            </node>
          </node></hierarchy>'''
        self.assertEqual(len(case.product_cards()), 1)

    def test_search_accessibility_prefix_is_not_a_failed_input(self):
        case = PerformanceDynamic_xhs_0030.__new__(PerformanceDynamic_xhs_0030)
        editor = ET.Element('node', {'class': 'android.widget.EditText', 'text': '搜索, 穿搭图片'})
        button = ET.Element('node', {'text': '搜索', 'bounds': '[1018,163][1116,306]'})
        case.nodes = lambda **kw: [button] if kw else [editor, button]
        case.screen_size = lambda: (1220, 2656)
        case.click_node = Mock()
        case.results_ready = lambda: True
        case.search_header = lambda query: [query]
        def wait(predicate, message, **kw):
            self.assertTrue(predicate(), message)
        case.wait_for = wait
        case.submit_query()
        case.click_node.assert_called_once_with(button)

    @patch('Cases.Top48.weixin_common.time.sleep')
    def test_video_call_chooses_action_sheet_instead_of_background_tool(self, _):
        case = WeixinDynamicCase.__new__(WeixinDynamicCase)
        case.screen = lambda: [
            dict(text='视频通话', x=.55, y=.725, w=.15, h=.025, source='tree'),
            dict(text='视频通话', x=.4, y=.80, w=.2, h=.025, source='screenshot-ocr'),
            dict(text='语音通话', x=.4, y=.87, w=.2, h=.025, source='screenshot-ocr')]
        case._locators = set()
        case.require_test_chat = Mock()
        case.require_delivery = Mock()
        case.pct = Mock()
        case.wait_for = Mock()
        case.invalidate = Mock()
        case.call_warning_reason = lambda: None
        case.dial(video=True)
        self.assertEqual(case.pct.call_count, 1)
        self.assertAlmostEqual(case.pct.call_args.args[1], .8125)

    @patch('Cases.Top48.weixin_common.time.sleep')
    def test_ambiguous_album_is_never_guessed(self, _):
        case = WeixinDynamicCase.__new__(WeixinDynamicCase)
        case.find = lambda *args, **kw: [
            dict(text=case.ALBUM+' (9)', y=.6), dict(text=case.ALBUM+' (9)', y=.7)]
        case.pct = Mock()
        with self.assertRaises(WeixinStepSkipped):
            case.choose_fixture_album()
        case.pct.assert_not_called()

    def test_featured_stream_requires_video_actions_even_with_stale_tab_state(self):
        case = KuaishouDynamicCase.__new__(KuaishouDynamicCase)
        def node(rid):
            return ET.Element('node', {'resource-id': case.PACKAGE+':id/'+rid})
        case.nodes = lambda: [node('featured_left_hamburger'), node('comment_button')]
        self.assertFalse(case.video_ready())
        case.nodes = lambda: [node(rid) for rid in
                             ('featured_left_hamburger', 'comment_button', 'like_button', 'collect_button')]
        self.assertTrue(case.video_ready())


if __name__ == '__main__':
    unittest.main()
