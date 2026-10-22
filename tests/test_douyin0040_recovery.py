import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

with patch('uiautomator2.connect'):
    from aw_new import SeaOfStarsAW
    from Cases.Top48.douyin_common import DouyinDynamicCase
    from Cases.Top48.PerformanceDynamic_douyin_0040 import PerformanceDynamic_douyin_0040 as Douyin0040


class AuthorRecoveryTests(unittest.TestCase):
    def case(self):
        case = Douyin0040.__new__(Douyin0040)
        case.author_profile_available = True
        case.foreground = Mock()
        case.return_feed = Mock()
        return case

    def test_store_return_skips_branch_and_recovers_home(self):
        case=self.case();case.in_store=Mock(return_value=True);case.back=Mock()
        self.assertFalse(case.back_profile())
        case.return_feed.assert_called_once();case.back.assert_not_called()
        self.assertFalse(case.author_profile_available)
        self.assertIn('店铺',case._step_skip_reason)

    def test_missing_profile_is_bounded_and_disables_later_videos(self):
        case=self.case();case.in_store=Mock(return_value=False)
        case.profile_page=Mock(return_value=False);case.feed_ready=Mock(return_value=False)
        case.dismiss_known_popup=Mock(return_value=False);case.back=Mock()
        self.assertFalse(case.back_profile());self.assertEqual(case.back.call_count,4)
        case.profile_video_candidates=Mock();self.assertFalse(case.play_profile_video(1))
        case.profile_video_candidates.assert_not_called()

    def test_valid_profile_return_remains_successful(self):
        case=self.case();case.in_store=Mock(return_value=False)
        case.profile_page=Mock(side_effect=[False,True]);case.feed_ready=Mock(return_value=False)
        case.dismiss_known_popup=Mock(return_value=False);case.back=Mock()
        self.assertTrue(case.back_profile());case.back.assert_called_once()
        case.return_feed.assert_not_called();self.assertTrue(case.author_profile_available)

    def test_missing_video_skips_without_clicking_other_profile_controls(self):
        case=self.case();case.in_store=Mock(return_value=False);case.profile_page=Mock(return_value=True)
        case.profile_video_candidates=Mock(return_value=[]);case.click_node=Mock()
        self.assertFalse(case.play_profile_video(0));case.click_node.assert_not_called()
        case.return_feed.assert_called_once();self.assertFalse(case.author_profile_available)

    def test_video_candidate_opening_store_is_not_counted_as_playback(self):
        case=self.case();case.in_store=Mock(side_effect=[False,True])
        case.profile_page=Mock(return_value=True);case.profile_video_candidates=Mock(return_value=[{}])
        case.click_node=Mock();case.wait_for=Mock()
        with patch('Cases.Top48.PerformanceDynamic_douyin_0040.time.sleep') as sleep:
            self.assertFalse(case.play_profile_video(0))
        case.wait_for.assert_not_called();sleep.assert_not_called();case.return_feed.assert_called_once()

    def test_home_recovery_failure_still_fails_case(self):
        case=self.case();case.return_feed.side_effect=RuntimeError('home unavailable')
        with self.assertRaisesRegex(RuntimeError,'home unavailable'):
            case.skip_author_branch('missing profile')

    def test_store_background_feed_nodes_do_not_count_as_home(self):
        case=Douyin0040.__new__(Douyin0040);case.foreground=Mock();state=['store']
        case.in_store=lambda:state[0]=='store';case.feed_ready=Mock(return_value=True)
        case.back=Mock(side_effect=lambda:state.__setitem__(0,'feed'))
        with patch.object(DouyinDynamicCase,'return_feed') as normal_return:
            case.return_feed()
        case.back.assert_called_once();normal_return.assert_called_once();self.assertEqual(state[0],'feed')

    def test_failed_search_does_not_open_stale_author_results(self):
        case=self.case();case.search_author=Mock(return_value=False);case.open_searched_author=Mock()
        case._last_skip_reason = 'missing author results'
        with self.assertRaisesRegex(RuntimeError, '重复搜索未进入作者主页'):
            case.repeat_two_search_visits()
        case.open_searched_author.assert_not_called()

    def test_skips_are_exported_and_next_step_still_runs(self):
        case=self.case();case._prepared=True
        with tempfile.TemporaryDirectory() as folder:
            case.result_dir_path=folder;case.trace_dir_path=folder;case.screenshot_dir_path=folder
            next_step=Mock();case.steps=Mock(return_value=[('作者不可用',lambda:case.skip('missing'),0),('返回主页',next_step,0)])
            with patch.object(SeaOfStarsAW,'start_perfetto_trace'),patch.object(SeaOfStarsAW,'stop_and_get_perfetto_trace') as export,patch('Cases.Top48.PerformanceDynamic_douyin_0040.time.sleep'):
                case.run_case()
            rows=json.loads((Path(folder)/'step_results.json').read_text())
            self.assertEqual([r['status'] for r in rows],['SKIP','PASS'])
            self.assertEqual(rows[0]['reason'],'missing');next_step.assert_called_once()
            self.assertIn('_SKIP',export.call_args_list[0].args[2])

    def test_combined_step_with_missing_author_records_partial_coverage(self):
        case=self.case();case._prepared=True
        def combined():
            case.skip('missing author')
            case.return_feed()
        with tempfile.TemporaryDirectory() as folder:
            case.result_dir_path=folder;case.trace_dir_path=folder;case.screenshot_dir_path=folder
            case.steps=Mock(return_value=[('组合浏览',combined,0)])
            with patch.object(SeaOfStarsAW,'start_perfetto_trace'),patch.object(SeaOfStarsAW,'stop_and_get_perfetto_trace'),patch('Cases.Top48.PerformanceDynamic_douyin_0040.time.sleep'):
                case.run_case()
            rows=json.loads((Path(folder)/'step_results.json').read_text())
            self.assertEqual(rows[0]['status'],'ADAPTED')


if __name__=='__main__':unittest.main()
