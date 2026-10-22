import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

with patch('uiautomator2.connect'):
    from aw_new import SeaOfStarsAW
    from Cases.Top48.step_recovery import run_recoverable_case
    from Cases.Top48.weixin_common import WeixinDynamicCase
    from Cases.Top48.PerformanceDynamic_weixin_0010 import PerformanceDynamic_weixin_0010
    from Cases.Top48.PerformanceDynamic_weixin_0060 import PerformanceDynamic_weixin_0060
    from Cases.Top48.PerformanceDynamic_meituxiuxiu_0010 import PerformanceDynamic_meituxiuxiu_0010
    from Cases.Top48.PerformanceDynamic_jrtt_0010 import PerformanceDynamic_jrtt_0010
    from Cases.Top48.PerformanceDynamic_douyinjisu_0010 import PerformanceDynamic_douyinjisu_0010


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        for target in ('start_perfetto_trace', 'stop_and_get_perfetto_trace'):
            mock = self.enterContext(patch.object(SeaOfStarsAW, target))
            setattr(self, target, mock)
        self.enterContext(patch('Cases.Top48.step_recovery.time.sleep'))
        self.case = Mock()
        self.case.TEST_TIME = 1
        self.case._prepared = True
        self.case.PACKAGE = 'app'
        self.case.RECOVERY_CHECKPOINTS = ('checkpoint',)
        self.case.result_dir_path = self.folder.name
        self.state = 'app'
        self.case.current_app.side_effect = lambda: dict(package=self.state, activity='Launcher' if self.state == 'desktop' else 'Activity')
        self.calls = []

        def final_main():
            self.calls.append('main')
        def final_home():
            self.calls.append('home')
            self.state = 'desktop'
        self.main = Mock(side_effect=final_main)
        self.home = Mock(side_effect=final_home)
        self.case.steps.return_value = [('业务', Mock(), 0), ('主页面', self.main, 0), ('Home', self.home, 0)]

    def rows(self):
        return json.loads((Path(self.folder.name) / 'step_results.json').read_text())

    def test_failed_branch_skips_dependencies_and_resumes_at_checkpoint(self):
        failed = Mock(side_effect=RuntimeError('media unavailable'))
        dependent = Mock()
        independent = Mock()
        def checkpoint():
            self.calls.append('checkpoint')
        self.case.steps.return_value = [('图片', failed, 0), ('滑动图片', dependent, 0),
            ('回首页', checkpoint, 0), ('新分支', independent, 0),
            ('主页面', self.main, 0), ('Home', self.home, 0)]
        run_recoverable_case(self.case)
        dependent.assert_not_called()
        independent.assert_called_once()
        self.assertEqual([r['status'] for r in self.rows()], ['SKIP', 'SKIP', 'PASS', 'PASS', 'PASS', 'PASS'])
        self.assertEqual(self.calls, ['checkpoint', 'main', 'home'])
        self.assertIn('_SKIP', self.stop_and_get_perfetto_trace.call_args_list[0].args[2])

    def test_no_checkpoint_skips_remaining_business_but_always_finishes(self):
        self.case.steps.return_value[0][1].side_effect = RuntimeError('failure')
        run_recoverable_case(self.case)
        self.assertEqual(self.calls, ['main', 'home'])
        self.assertEqual(self.rows()[0]['status'], 'SKIP')

    def test_setup_failure_still_runs_final_steps(self):
        self.case._prepared = False
        self.case.set_up.side_effect = RuntimeError('setup failed')
        with self.assertRaisesRegex(RuntimeError, 'setup failed'):
            run_recoverable_case(self.case)
        self.assertEqual(self.calls, ['main', 'home'])

    def test_cleanup_failure_still_returns_home_and_reports_failure(self):
        self.main.side_effect = RuntimeError('no main page')
        with self.assertRaisesRegex(RuntimeError, '返回应用主页失败'):
            run_recoverable_case(self.case)
        self.home.assert_called_once()
        self.assertEqual(self.rows()[-2]['status'], 'FAIL')
        self.case.start.assert_called_once()

    def test_trace_start_failure_cannot_prevent_cleanup(self):
        self.start_perfetto_trace.side_effect = RuntimeError('trace unavailable')
        with self.assertRaisesRegex(RuntimeError, 'trace unavailable'):
            run_recoverable_case(self.case)
        self.assertEqual(self.calls, ['main', 'home'])

    def test_trace_export_failure_does_not_prevent_cleanup(self):
        self.stop_and_get_perfetto_trace.side_effect = RuntimeError('export unavailable')
        with self.assertRaisesRegex(RuntimeError, 'export unavailable'):
            run_recoverable_case(self.case)
        self.assertEqual(self.calls, ['main', 'home'])
        self.assertFalse(self.rows()[-1]['trace_exported'])

    def test_home_gesture_failure_uses_home_key(self):
        self.home.side_effect = RuntimeError('gesture failed')
        self.case.d.press.side_effect = lambda key: setattr(self, 'state', 'desktop')
        run_recoverable_case(self.case)
        self.case.d.press.assert_called_once_with('home')
        self.assertEqual(self.state, 'desktop')

    def test_final_main_relaunches_if_outside_app(self):
        self.state = 'desktop'
        self.case.start.side_effect = lambda: setattr(self, 'state', 'app')
        run_recoverable_case(self.case)
        self.case.start.assert_called_once()
        self.assertEqual(self.calls, ['main', 'home'])

    def test_home_failure_is_reported_as_fail(self):
        self.home.side_effect = RuntimeError('gesture failed')
        self.case.wait_for.side_effect = RuntimeError('desktop unavailable')
        with self.assertRaisesRegex(RuntimeError, 'desktop unavailable'):
            run_recoverable_case(self.case)
        self.assertEqual(self.rows()[-1]['status'], 'FAIL')

    def test_affected_runners_route_to_recovery(self):
        for cls in (PerformanceDynamic_weixin_0010, PerformanceDynamic_weixin_0060,
                    PerformanceDynamic_meituxiuxiu_0010, PerformanceDynamic_jrtt_0010,
                    PerformanceDynamic_douyinjisu_0010):
            case = cls.__new__(cls)
            with patch('Cases.Top48.step_recovery.run_recoverable_case') as runner:
                case.run_case()
            runner.assert_called_once_with(case)

    def test_weixin_main_page_reenters_app_and_refreshes_screen(self):
        case = WeixinDynamicCase.__new__(WeixinDynamicCase)
        case.current_app = Mock(return_value=dict(package='desktop'))
        case.start = Mock()
        case.invalidate = Mock()
        case.main_ready = Mock(return_value=True)
        case.main_page()
        case.start.assert_called_once()
        case.invalidate.assert_called_once()

    def test_only_affected_cases_have_recovery_contract(self):
        for cls in (PerformanceDynamic_weixin_0010, PerformanceDynamic_weixin_0060,
                    PerformanceDynamic_meituxiuxiu_0010, PerformanceDynamic_jrtt_0010,
                    PerformanceDynamic_douyinjisu_0010):
            case = cls.__new__(cls)
            steps = case.steps()
            self.assertIn(steps[-2][1].__name__, ('wechat_home', 'main_page', 'return_home', 'app_home'))
            self.assertEqual(steps[-1][1].__name__, 'home')
            for checkpoint in case.RECOVERY_CHECKPOINTS:
                self.assertIn(checkpoint, [step[1].__name__ for step in steps[:-2]])


if __name__ == '__main__':
    unittest.main()
