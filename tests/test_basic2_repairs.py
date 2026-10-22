import unittest
import xml.etree.ElementTree as ET
from types import SimpleNamespace
from unittest.mock import Mock, patch

from PIL import Image, ImageDraw

with patch('uiautomator2.connect'):
    from aw_new import SeaOfStarsAW
    from Cases.Top48.jrtt_common import JrttDynamicCase
    from Cases.Top48.weixin_common import WeixinDynamicCase


class Basic2RepairTests(unittest.TestCase):
    def test_comment_count_button_is_not_an_open_comments_panel(self):
        case = JrttDynamicCase.__new__(JrttDynamicCase)
        case.nodes = lambda: [ET.Element('node', {'content-desc': '评论2827'})]
        self.assertFalse(case.comments_ready())
        for title in ('评论2827', '评论 2827', '2827条评论', '0条评论'):
            case.nodes = lambda: [ET.Element('node', {'text': title})]
            self.assertTrue(case.comments_ready(), title)

    def test_logged_out_bottom_tab_still_allows_video_browsing(self):
        case = JrttDynamicCase.__new__(JrttDynamicCase)
        case.bottom_nodes = lambda name: [name] if name in ('首页', '视频', '未登录') else []
        self.assertTrue(case.bottom_ready())
        case.bottom_nodes = lambda name: [name] if name == '视频' else []
        self.assertFalse(case.bottom_ready())

    @patch('Cases.Top48.jrtt_common.time.sleep')
    def test_comment_scroll_stays_in_body_and_detects_panel_closing(self, _):
        case = JrttDynamicCase.__new__(JrttDynamicCase)
        case.comments_ready = Mock(side_effect=[True, True, False])
        case.swipe = Mock()
        with self.assertRaisesRegex(RuntimeError, '离开了评论面板'):
            case.browse_comments()
        self.assertEqual(case.swipe.call_count, 2)
        for call in case.swipe.call_args_list:
            self.assertGreater(min(call.args[1], call.args[3]), .5)
            self.assertLess(max(call.args[1], call.args[3]), .9)

    def canvas(self, toolbar=True, content=True):
        shot = Image.new('RGB', (1000, 2000), 'black')
        draw = ImageDraw.Draw(shot)
        if content:
            draw.rectangle((0, 400, 999, 1600), fill=(180, 150, 120))
        if toolbar:
            for x in (.59, .695, .805, .92):
                draw.ellipse((x*1000-42, 1888-42, x*1000+42, 1888+42), fill=(71, 71, 71))
        return shot

    def picture_case(self, shot):
        case = WeixinDynamicCase.__new__(WeixinDynamicCase)
        case.activity_is = lambda *names: True
        case.chat_ready = lambda: False
        case._locators = set()
        self.enterContext(patch.object(SeaOfStarsAW, 'ut_device',
                                      SimpleNamespace(screenshot=lambda **kw: shot)))
        return case

    def test_embedded_picture_needs_toolbar_before_accepting_hidden_controls(self):
        shot = self.canvas()
        case = self.picture_case(shot)
        self.assertTrue(case.picture_canvas_ready())
        shot.paste(self.canvas(toolbar=False))
        self.assertTrue(case.picture_canvas_ready())
        case._picture_canvas_verified = False
        self.assertFalse(case.picture_canvas_ready())

    def test_black_loading_screen_is_not_a_picture_even_after_previous_viewer(self):
        case = self.picture_case(self.canvas(toolbar=False, content=False))
        case._picture_canvas_verified = True
        self.assertFalse(case.picture_canvas_ready())

    def test_chat_page_cannot_pass_picture_canvas_check(self):
        case = self.picture_case(self.canvas())
        case.chat_ready = lambda: True
        self.assertFalse(case.picture_canvas_ready())


if __name__ == '__main__':
    unittest.main()
