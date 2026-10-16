"""验证媒体状态隔离、暂停幂等性及受限播放前置条件，不连接设备。"""
import unittest
from unittest.mock import Mock, PropertyMock, patch
from Cases.Top48.tencent_media_common import (
    TencentObservedCase, QqMusicDynamicCase, TencentNewsDynamicCase, TencentVideoDynamicCase, StepUnavailable,
)


class TencentMediaGuardsTest(unittest.TestCase):
    def setUp(self):
        mocked = patch.object(TencentObservedCase, "d", new_callable=PropertyMock, return_value=Mock())
        mocked.start(); self.addCleanup(mocked.stop)

    def music(self):
        c = object.__new__(QqMusicDynamicCase)
        c.unavailable = {}; c._adaptations = []
        c.dismiss_ads = Mock(); c.native = Mock(); c.go = Mock()
        return c

    def test_media_state_ignores_other_background_players(self):
        c = object.__new__(TencentObservedCase); c.PACKAGE = 'com.tencent.qqmusic'
        c.d.shell.return_value.output = ('package=com.tencent.qqlive\nstate=PlaybackState {state=PLAYING(3), position=50}\n'
                                       'package=com.tencent.qqmusic\nstate=PlaybackState {state=PAUSED(2), position=40}')
        self.assertEqual(c.media_state(), 2)

    def test_absent_media_session_is_not_playing(self):
        c = object.__new__(TencentObservedCase); c.PACKAGE = 'com.tencent.qqmusic'
        c.d.shell.return_value.output = 'package=com.tencent.qqlive\nstate=PlaybackState {state=3}'
        self.assertIsNone(c.media_state())

    def test_media_description_uses_only_target_package(self):
        c = object.__new__(TencentObservedCase); c.PACKAGE = 'com.tencent.qqmusic'
        c.d.shell.return_value.output = ('package=com.tencent.qqlive\nmetadata: size=4, description=其他视频, null\n'
                                       'package=com.tencent.qqmusic\nmetadata: size=21, description=红旗飘飘, 孙楠, 生生世世')
        self.assertEqual(c.media_description(), '红旗飘飘, 孙楠, 生生世世')

    def test_first_song_click_is_not_skipped_for_preexisting_playback(self):
        c = self.music(); c.comprehensive = Mock(); c.has = Mock(return_value=True)
        c.media_state = Mock(return_value=3)
        c.media_description = Mock(return_value='红旗飘飘, 孙楠, 生生世世')
        c.hold_music = Mock()
        c.content_wait = lambda ready, message: self.assertTrue(ready())
        c.first_song()
        c.native.assert_called_once_with(rid='kog', text='红旗飘飘')
        c.hold_music.assert_called_once_with(20)

    def test_label_does_not_click_whole_page_parent(self):
        c = object.__new__(TencentObservedCase); c.PACKAGE = 'com.tencent.qqmusic'
        c._locators = set(); c.d.window_size.return_value = (1000, 2000)
        c.d.dump_hierarchy.return_value = ('<hierarchy><node package="com.tencent.qqmusic" clickable="true" bounds="[0,0][1000,2000]">'
            '<node package="com.tencent.qqmusic" text="乐馆" clickable="false" bounds="[200,200][300,300]"/>'
            '</node></hierarchy>')
        c.find = Mock(return_value=[dict(x=.2,y=.1,w=.1,h=.05)])
        c.choose = Mock(); c.click_node = Mock()
        c.label_node('乐馆')
        c.click_node.assert_not_called(); c.choose.assert_called_once_with('乐馆')

    def test_scrolled_rank_list_does_not_require_header(self):
        c = self.music(); c.main_ready = Mock(return_value=False)
        c.visible = lambda label, *args, **kwargs: label in ('热歌榜', '新歌榜')
        self.assertTrue(c.rank_ready())

    def test_single_rank_detail_is_not_mistaken_for_list(self):
        c = self.music(); c.main_ready = Mock(return_value=False)
        c.visible = lambda label, *args, **kwargs: label == '热歌榜'
        self.assertFalse(c.rank_ready())

    def test_news_column_article_with_comment_icon_is_supported(self):
        c = object.__new__(TencentNewsDynamicCase); c.main_ready = Mock(return_value=False)
        c.has = lambda **kw: kw.get('rid') in ('news_detail_title', 'action_bar_comment')
        c.visible = Mock(return_value=False)
        self.assertTrue(c.article_ready())

    def test_news_detail_activity_alone_does_not_validate_ad(self):
        c = object.__new__(TencentNewsDynamicCase); c.main_ready = Mock(return_value=False)
        c.has = Mock(return_value=False); c.visible = Mock(return_value=False)
        c.activity_is = Mock(return_value=True)
        self.assertFalse(c.article_ready())

    def test_video_home_tab_can_become_back_to_top_after_scroll(self):
        c = object.__new__(TencentVideoDynamicCase)
        c.visible = lambda label, *args, **kwargs: label in ('个人中心', '返回顶部')
        self.assertTrue(c.main_ready())

    def test_pause_does_not_resume_paused_music(self):
        c = self.music(); c.media_state = Mock(return_value=2)
        c.pause(); c.go.assert_not_called(); c.native.assert_not_called()
        self.assertTrue(c._adaptations)

    def test_pause_does_not_click_without_playing_session(self):
        c = self.music(); c.media_state = Mock(return_value=None)
        with self.assertRaises(StepUnavailable): c.pause()
        c.go.assert_not_called()

    def test_favorite_requires_verified_login(self):
        c = self.music(); c.player = Mock(); c._music_logged_in = False
        with self.assertRaises(StepUnavailable): c.favorite_roundtrip()
        c.native.assert_not_called()

    def test_original_favorite_is_preserved(self):
        c = self.music(); c.player = Mock(); c._music_logged_in = True
        c.nodes = Mock(return_value=[{'content-desc': '取消收藏'}])
        with self.assertRaises(StepUnavailable): c.favorite_roundtrip()
        c.native.assert_not_called()

    def test_only_new_favorite_is_restored(self):
        c = self.music(); c.player = Mock(); c._music_logged_in = True
        c.nodes = Mock(side_effect=[[{'content-desc':'收藏'}], [{'content-desc':'取消收藏'}],
                                   [{'content-desc':'取消收藏'}], [{'content-desc':'收藏'}]])
        c.content_wait = lambda ready, message: self.assertTrue(ready())
        c.wait_for = lambda ready, message: self.assertTrue(ready())
        c.favorite_roundtrip()
        self.assertEqual(c.native.call_count, 2)

    def test_failed_video_blocks_player_actions(self):
        c = object.__new__(TencentVideoDynamicCase); c.unavailable = {'video':'VIP限制'}
        c.show_controls = Mock()
        with self.assertRaises(StepUnavailable): c.fullscreen()
        c.show_controls.assert_not_called()

    def test_advertisement_is_not_treated_as_content(self):
        c = object.__new__(TencentVideoDynamicCase); c.unavailable = {}
        c.video_ready = Mock(return_value=True); c.paywall = Mock(return_value=False)
        c.preroll = Mock(return_value=True)
        with self.assertRaises(StepUnavailable): c.require_video()

    def test_film_browse_requires_successful_selection(self):
        c = object.__new__(TencentVideoDynamicCase); c.unavailable = {'film':'没有影视入口'}
        c.browse_checked = Mock()
        with self.assertRaises(StepUnavailable): c.browse_films()
        c.browse_checked.assert_not_called()

if __name__ == '__main__': unittest.main()
