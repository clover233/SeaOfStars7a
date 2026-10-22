import unittest
from unittest.mock import Mock, patch
import xml.etree.ElementTree as ET
from pathlib import Path
import tempfile
from types import SimpleNamespace

with patch('uiautomator2.connect'):
    from Cases.Top48.main_display import MainDisplayMixin
    from Cases.Top48.doubao_common import DoubaoDynamicCase
    from Cases.Top48.douyin_common import DouyinDynamicCase
    from Cases.Top48.hongguo_common import HongguoDynamicCase
    from Cases.Top48.qq_common import QQDynamicCase, QQStepSkipped
    from Cases.Top48.PerformanceDynamic_douyin_0030 import PerformanceDynamic_douyin_0030
    from Cases.Top48.weixin_common import WeixinExtendedCase
    from Cases.Top48.shopping_common import ShoppingDynamicCase, AccountBlocked


class FailureRepairTests(unittest.TestCase):
    def test_main_screen_dimensions_ignore_landscape_secondary_screen(self):
        case = Mock()
        case.d.shell.return_value.output = (
            'Display: mDisplayId=1\n  init=400x900 cur=900x400\n'
            'Display: mDisplayId=0\n  init=1220x2656 cur=1220x2656\n')
        self.assertEqual(MainDisplayMixin.screen_size(case), (1220, 2656))
        case.d.screenshot.assert_not_called()

    def test_dimensions_follow_main_screen_rotation(self):
        case = Mock()
        case.d.shell.return_value.output = 'Display: mDisplayId=0\n init=1220x2656 cur=2656x1220\n'
        self.assertEqual(MainDisplayMixin.screen_size(case), (2656, 1220))

    def test_text_chat_does_not_require_voice_home_button(self):
        case = DoubaoDynamicCase.__new__(DoubaoDynamicCase)
        case.has = lambda **kw: kw.get('rid') == 'larus_chat_top_left_create_new_cvs'
        case.text_editors = lambda: [ET.Element('node', {'class': 'android.widget.EditText'})]
        self.assertTrue(case.chat_ready())
        case.text_editors = lambda: []
        self.assertFalse(case.chat_ready())

    def test_draft_is_not_evidence_that_ai_question_was_sent(self):
        case = DoubaoDynamicCase.__new__(DoubaoDynamicCase)
        case.pending_question = '什么是AI'
        draft = ET.Element('node', {'text': '什么是AI', 'class': 'android.widget.EditText'})
        case.nodes = lambda: [draft]
        case.text_editors = lambda: [draft]
        case.send_button = Mock(return_value='send')
        case.click_node = Mock()
        def wait(predicate, message):
            self.assertFalse(predicate())
            raise RuntimeError(message)
        case.wait_for = wait
        with self.assertRaisesRegex(RuntimeError, '不自动重发'):
            case.send_pending()
        case.click_node.assert_called_once_with('send')

    def test_new_comment_title_is_ready_and_does_not_reclick_hidden_button(self):
        case = HongguoDynamicCase.__new__(HongguoDynamicCase)
        case.has = lambda **kw: kw.get('desc') == 'back_unfold'
        case.nodes = lambda: [ET.Element('node', {'text':'评论 3353'})]
        self.assertTrue(case.comments_ready())
        case.nodes = lambda: [ET.Element('node', {'text':'评论'})]
        self.assertTrue(case.comments_ready())
        case.has = lambda **kw: kw.get('rid') == 'iup' and kw.get('text') in ('评论', '剧评')
        self.assertTrue(case.comments_ready())

    def test_product_activity_is_required_when_bottom_semantics_are_missing(self):
        case = DouyinDynamicCase.__new__(DouyinDynamicCase)
        case.nodes = lambda: [ET.Element('node', {'text': x}) for x in ('店铺','购物车','客服')]
        case.current_app = lambda: dict(package=case.PACKAGE, activity='ProductDetailV2Activity')
        self.assertTrue(case.product_ready())
        case.nodes = lambda: [ET.Element('node', {'text':'加入购物车'})]
        self.assertFalse(case.product_ready())
        case.current_app = lambda: dict(package='other.app', activity='ProductDetailV2Activity')
        self.assertFalse(case.product_ready())

    @patch('Cases.Top48.qq_common.time.sleep')
    def test_expired_media_is_a_skip_instead_of_a_navigation_failure(self, _):
        case = QQDynamicCase.__new__(QQDynamicCase)
        case.picture_ready = Mock(side_effect=[True, False])
        case.swipe = Mock()
        case.expired_picture = lambda: True
        with self.assertRaisesRegex(QQStepSkipped, '已过期'):
            case.slide_pictures(right=4, left=4)
        case.swipe.assert_called_once()

    def test_store_browsing_does_not_run_on_product_page_when_entry_is_missing(self):
        case = PerformanceDynamic_douyin_0030.__new__(PerformanceDynamic_douyin_0030)
        case.browse = Mock()
        self.assertFalse(case.browse_store())
        case.browse.assert_not_called()
        self.assertIn('进店入口不可用', case._last_skip_reason)

    def test_missing_cart_cannot_be_reported_as_successful_cart_browsing(self):
        case = PerformanceDynamic_douyin_0030.__new__(PerformanceDynamic_douyin_0030)
        case.open_cart = lambda: False
        case.browse = Mock()
        self.assertFalse(case.browse_cart_page())
        case.browse.assert_not_called()

    def test_memo_ocr_fallback_is_anchored_to_the_memo_dialog(self):
        case = WeixinExtendedCase.__new__(WeixinExtendedCase)
        case.visible = lambda *args, **kw: False
        case.find = lambda *args, **kw: [dict(y=.68, h=.025)]
        case.visible_crop = Mock(return_value=True)
        self.assertTrue(case.memo_input_ready())
        label, region = case.visible_crop.call_args.args
        self.assertEqual(label, '修改')
        self.assertAlmostEqual(region[1], .72)
        case.find = lambda *args, **kw: []
        case.visible_crop.reset_mock()
        self.assertFalse(case.memo_input_ready())
        case.visible_crop.assert_not_called()

    def test_jd_security_verification_blocks_dependent_business_steps(self):
        case = ShoppingDynamicCase.__new__(ShoppingDynamicCase)
        case.activity_has = lambda *names: 'JDRiskHandleActivity' in names
        with self.assertRaises(AccountBlocked) as raised:
            case.check_access()
        self.assertTrue(raised.exception.blocks_case)

    def test_rerun_initializes_groups_and_skips_account_dependencies_but_returns_home(self):
        from tools import rerun_failed as runner
        dependent = Mock()
        instances = []
        class FakeCase:
            def __init__(self, folder):
                self.result_dir_path = str(Path(folder)/'fake')
                Path(self.result_dir_path).mkdir()
                self.d = Mock()
                self.d.shell.return_value = SimpleNamespace(exit_code=0, output='')
                self.d.current_ime.return_value = 'test.ime'
                self.set_up = Mock()
                self.clean_up = Mock()
                instances.append(self)
            def blocked(self):
                raise AccountBlocked('需要验证')
            def home(self):
                self.returned_home = True
            def dependent_action(self):
                dependent()
            def steps(self):
                return [('启动', lambda: ShoppingDynamicCase.group(self, 'live', lambda: None), 0),
                        ('账号入口', self.blocked, 0), ('依赖业务', self.dependent_action, 0), ('Home', self.home, 0)]
        module = SimpleNamespace(PerformanceDynamic_fake=FakeCase)
        with tempfile.TemporaryDirectory() as folder, \
                patch.object(runner, 'evidence', return_value={}), \
                patch.object(runner.time, 'sleep'), \
                patch.object(runner.importlib, 'import_module', return_value=module):
            result = runner.run_one('PerformanceDynamic_fake', Path(folder), False)
        self.assertEqual(result['status'], 'COMPLETED_WITH_SKIPS')
        self.assertEqual([r['status'] for r in result['steps']], ['PASS','SKIP','SKIP','PASS'])
        self.assertTrue(instances[0]._groups['live'])
        self.assertTrue(instances[0].returned_home)
        dependent.assert_not_called()


if __name__ == '__main__':
    unittest.main()
