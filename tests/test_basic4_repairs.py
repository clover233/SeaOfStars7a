import unittest
import xml.etree.ElementTree as ET
from unittest.mock import Mock, patch

with patch('uiautomator2.connect'):
    from Cases.Top48.call_common import CallDynamicCase
    from Cases.Top48.photo_common import PhotoDynamicCase
    from Cases.Top48.PerformanceDynamic_deepseek_0010 import PerformanceDynamic_deepseek_0010
    from Cases.Top48.PerformanceDynamic_douyin_0040 import PerformanceDynamic_douyin_0040
    from Cases.Top48.PerformanceDynamic_dongchedi_0010 import PerformanceDynamic_dongchedi_0010


class PhoneNavigationTests(unittest.TestCase):
    def test_updated_miui_navigation_retains_selected_state(self):
        case = CallDynamicCase.__new__(CallDynamicCase)
        label = ET.Element('node', text='通话', selected='true')
        case.nodes = lambda rid=None, **kw: [label] if rid == 'miuix_navigation_bar_item_label_view' else []
        self.assertTrue(case.tab_selected('通话'))

    @patch('Cases.Top48.call_common.time.sleep')
    def test_ready_navigation_does_not_back_out_of_application(self, _):
        case = CallDynamicCase.__new__(CallDynamicCase)
        case.wait_for = Mock()
        case.tab_nodes = Mock(return_value=[ET.Element('node')])
        case.has = Mock(return_value=False)
        case.phone = Mock()
        case.shell = Mock()
        with patch.object(CallDynamicCase, 'd', new_callable=lambda: property(lambda self: device)):
            device = Mock()
            case.launch()
        case.phone.assert_called_once()
        case.shell.assert_not_called()


class GalleryNavigationTests(unittest.TestCase):
    def test_bottom_tab_excludes_same_label_page_title(self):
        case = PhotoDynamicCase.__new__(PhotoDynamicCase)
        case.screen_size = lambda: (1080, 2400)
        title = ET.Element('node', {'content-desc': '照片', 'clickable': 'false',
                                   'bounds': '[50,200][300,350]'})
        tab = ET.Element('node', {'content-desc': '照片', 'clickable': 'true',
                                 'selected': 'true', 'bounds': '[300,2200][540,2320]'})
        case.nodes = lambda: [title, tab]
        self.assertEqual(case.bottom_tab('照片'), [tab])

    def test_compose_tab_accepts_raw_and_qualified_resource_ids(self):
        case = PhotoDynamicCase.__new__(PhotoDynamicCase)
        for rid in ('segment_1', case.PACKAGE + ':id/segment_1'):
            case.nodes = lambda: [ET.Element('node', {'resource-id': rid, 'selected': 'true'})]
            self.assertTrue(case.picker_tab_selected(1))
            self.assertFalse(case.picker_tab_selected(0))

    def test_slow_video_open_is_not_reclicked_as_a_grid(self):
        case = PhotoDynamicCase.__new__(PhotoDynamicCase)
        case.top = Mock()
        case.has = lambda **kw: kw.get('desc') == '视频'
        case.first_grid_point = Mock(return_value=(.1, .3))
        case.pct = Mock()
        case.viewer = Mock(side_effect=[False, True])
        def wait(predicate, message, timeout):
            self.assertFalse(predicate())
            self.assertTrue(predicate())
        case.wait_for = wait
        case.open_first(home=False)
        case.first_grid_point.assert_called_once()
        case.pct.assert_called_once_with(.1, .3)

    def test_core_package_is_accepted_only_for_gallery_details(self):
        case = PhotoDynamicCase.__new__(PhotoDynamicCase)
        case.current_app = lambda: {'package': 'com.miui.core',
                                    'activity': 'com.miui.gallery.activity.PhotoDetailActivity'}
        case.foreground()
        case.current_app = lambda: {'package': 'com.miui.core', 'activity': 'other.Activity'}
        with self.assertRaises(RuntimeError):
            case.foreground()


class DeepSeekInputTests(unittest.TestCase):
    def test_short_tap_uses_main_screen_ratios(self):
        case = PerformanceDynamic_deepseek_0010.__new__(PerformanceDynamic_deepseek_0010)
        case.foreground = Mock()
        case.screen_size = lambda: (1000, 2000)
        device = Mock()
        with patch.object(PerformanceDynamic_deepseek_0010, 'd', property(lambda self: device)):
            case.point(250, 1600)
        device.click.assert_called_once_with(.25, .8)
        device.shell.assert_not_called()


class DouyinVideoTests(unittest.TestCase):
    def test_nonclickable_work_tiles_are_distinguished_from_shop(self):
        case = PerformanceDynamic_douyin_0040.__new__(PerformanceDynamic_douyin_0040)
        case.screen_size = lambda: (1200, 2600)
        video = ET.Element('node', {'clickable': 'false', 'bounds': '[0,1900][400,2500]'})
        ET.SubElement(video, 'node', {'content-desc': '点赞数48.6万'})
        shop = ET.Element('node', {'clickable': 'true', 'bounds': '[600,1200][1100,1500]'})
        ET.SubElement(shop, 'node', {'text': '进入店铺'})
        case.nodes = lambda **kw: [shop, video]
        self.assertEqual(case.profile_video_candidates(), [video])

    def test_profile_cannot_be_mistaken_for_background_feed(self):
        case = PerformanceDynamic_douyin_0040.__new__(PerformanceDynamic_douyin_0040)
        case.current_app = lambda: {'activity': 'com.ss.android.ugc.aweme.profile.ui.UserProfileActivity'}
        case.nodes = Mock()
        self.assertFalse(case.feed_ready())
        case.nodes.assert_not_called()


class NewsLocatorTests(unittest.TestCase):
    def test_native_filter_label_takes_precedence_over_ocr(self):
        case = PerformanceDynamic_dongchedi_0010.__new__(PerformanceDynamic_dongchedi_0010)
        node = ET.Element('node')
        case.nodes = lambda **kw: [node]
        case.click_node = Mock()
        case.screenshot_rows = Mock()
        case.visual_label('筛选')
        case.click_node.assert_called_once_with(node)
        case.screenshot_rows.assert_not_called()

    @patch('Cases.Top48.PerformanceDynamic_dongchedi_0010.time.sleep')
    def test_icon_merged_with_ocr_label_still_uses_relative_bounds(self, _):
        case = PerformanceDynamic_dongchedi_0010.__new__(PerformanceDynamic_dongchedi_0010)
        case.nodes = lambda **kw: []
        case.screenshot_rows = lambda: [dict(text='7 筛选', x=.8, y=.1, w=.1, h=.04)]
        case.pct = Mock()
        case.visual_label('筛选')
        x, y = case.pct.call_args.args
        self.assertAlmostEqual(x, .85)
        self.assertAlmostEqual(y, .12)


if __name__ == '__main__':
    unittest.main()
