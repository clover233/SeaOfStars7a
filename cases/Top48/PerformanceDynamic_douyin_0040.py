"""抖音推荐、关注和搜索作者主页浏览（表格第 557～576 行）。"""
import json
import logging
from pathlib import Path
import time

from Cases.Top48.douyin_common import DouyinDynamicCase
from aw_new import SeaOfStarsAW


class PerformanceDynamic_douyin_0040(DouyinDynamicCase):
    all_app_package_list = [DouyinDynamicCase.PACKAGE]

    def skip(self, message):
        self._step_skip_reason = message
        return super().skip(message)

    def in_store(self):
        return 'ECStoreActivity' in self.current_app()['activity']

    def return_feed(self):
        for _ in range(4):
            self.foreground()
            # 店铺背后可能仍导出推荐页节点，先退出真实店铺窗口再核验主页。
            if self.in_store():
                self.back()
                continue
            super().return_feed()
            if not self.in_store() and self.feed_ready():
                return
        raise RuntimeError('未退出店铺并返回抖音推荐主页')

    def skip_author_branch(self, reason):
        self.author_profile_available = False
        # 推荐主页仍是必须确认的恢复点；返回失败不能当作 SKIP 吞掉。
        self.return_feed()
        return self.skip(reason + '；已返回抖音推荐主页')

    def repeat_recommended_author(self):
        self.return_feed()
        self.browse_videos(5)
        if not self.open_current_author():
            raise RuntimeError('重复推荐浏览未进入作者主页：' + self._last_skip_reason)
        self.return_feed()

    def back_profile(self):
        if not getattr(self, 'author_profile_available', False):
            return self.skip_author_branch('作者主页不可用，跳过返回作者主页')
        for _ in range(4):
            self.foreground()
            if self.in_store():
                return self.skip_author_branch('当前进入了店铺页，停止本段作者作品浏览')
            if self.profile_page():
                return True
            if self.feed_ready():
                return self.skip_author_branch('已回到推荐页，未找到作者主页')
            if not self.dismiss_known_popup():
                self.back()
        if not self.in_store() and self.profile_page():
            return True
        return self.skip_author_branch('有限返回后未找到作者主页')

    def feed_ready(self):
        # 作者/搜索页背后的推荐节点不能作为已返回首页的依据。
        return (self.current_app()['activity'].endswith(('.MainActivity', '.SplashActivity'))
                and super().feed_ready())

    def profile_video_candidates(self):
        width, height = self.screen_size()
        # 作品 FrameLayout 不公开 clickable；以格子内“点赞数”语义节点确认作品，
        # 排除同页店铺、系列合集和直播入口，不再按固定纵向位置过滤。
        videos = []
        for node in self.nodes(rid='container'):
            left, top, right, bottom = self.bounds(node)
            if (.2 < (right-left)/width < .5 and bottom-top > height*.08
                    and any(c.get('content-desc', '').startswith('点赞数')
                            for c in node.iter('node'))):
                videos.append(node)
        return sorted(videos, key=lambda node: (self.bounds(node)[1], self.bounds(node)[0]))

    def author_video_ready(self):
        self.foreground()
        if self.in_store():
            return False
        width = self.screen_size()[0]
        return any((n.get('resource-id', '').endswith(':id/comment_container')
                    or n.get('content-desc', '').startswith('评论'))
                   and self.bounds(n)[0] > width * .6 for n in self.nodes())

    def play_profile_video(self, index):
        if (not getattr(self, 'author_profile_available', False)
                or self.in_store() or not self.profile_page()):
            return self.skip_author_branch('作者主页不可用，跳过第{}个作品'.format(index + 1))
        videos = self.profile_video_candidates()
        if len(videos) <= index:
            return self.skip_author_branch('没有第{}个可确认的作者作品'.format(index + 1))
        self.click_node(videos[index])
        if self.in_store():
            return self.skip_author_branch('作品入口打开了店铺，跳过本段作者作品')
        try:
            self.wait_for(self.author_video_ready, '作者作品播放页未就绪', timeout=6)
        except RuntimeError:
            self.foreground()
            return self.skip_author_branch('未确认进入作者作品播放页')
        time.sleep(15)
        return True

    def browse_author(self, up, down):
        if (not getattr(self, 'author_profile_available', False)
                or self.in_store() or not self.profile_page()):
            return self.skip_author_branch('未进入作者主页，跳过作品列表浏览')
        self.browse(up, down)
        return True

    def repeat_two_search_visits(self):
        self.return_feed()
        for _ in range(2):
            if not self.search_author() or not self.open_searched_author():
                raise RuntimeError('重复搜索未进入作者主页：' + self._last_skip_reason)
            self.browse(3, 3)
            self.return_feed()

    @SeaOfStarsAW.function_log
    def run_case(self):
        if not getattr(self, '_prepared', False):
            self.set_up()
        records = []
        path = Path(self.result_dir_path) / 'step_results.json'
        for run in range(self.TEST_TIME):
            for number, (name, action, stay) in enumerate(self.steps(), 1):
                row = dict(run=run + 1, step=number, name=name, status='PASS')
                self._step_skip_reason = None
                logging.info('%s、%s', number, name)
                SeaOfStarsAW.start_perfetto_trace()
                try:
                    if action() is False:
                        row.update(status='SKIP', reason=self._step_skip_reason or '当前场景不可用')
                    elif self._step_skip_reason:
                        row.update(status='ADAPTED', reason='部分操作跳过：' + self._step_skip_reason)
                    time.sleep(stay)
                except Exception as error:
                    row.update(status='FAIL', reason=str(error))
                    raise
                finally:
                    records.append(row)
                    try:
                        SeaOfStarsAW.stop_and_get_perfetto_trace(
                            self.trace_dir_path, self.__class__.__name__,
                            'step_{}、{}_{}'.format(number, name, row['status']), '', self.screenshot_dir_path)
                    except Exception as error:
                        if row['status'] != 'FAIL':
                            row.update(status='FAIL', reason='trace导出失败：' + str(error))
                            raise
                        logging.exception('失败步骤的trace导出失败')
                    finally:
                        path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')

    def steps(self):
        return [
            ('启动抖音', self.launch, 3),
            ('推荐页面上滑切换视频5次', lambda: self.browse_videos(5), 0),
            ('点击当前视频作者头像进入主页', self.open_current_author, 2),
            ('返回主界面并重复浏览推荐作者1次', self.repeat_recommended_author, 2),
            ('点击我，切换到我页面', self.open_me, 2),
            ('点击关注，切换到关注页面', self.open_following, 2),
            ('点击华为终端头像查看博主主页', self.open_followed_author, 2),
            ('博主主页上滑5次、下滑5次', lambda: self.browse_author(5, 5), 0),
            ('播放博主第1个视频15秒', lambda: self.play_profile_video(0), 0),
            ('返回博主主页', self.back_profile, 1),
            ('播放博主第2个视频15秒', lambda: self.play_profile_video(1), 0),
            ('返回博主主页', self.back_profile, 1),
            ('播放博主第3个视频15秒', lambda: self.play_profile_video(2), 0),
            ('返回博主主页', self.back_profile, 1),
            ('返回抖音主界面', self.return_feed, 2),
            ('搜索华为终端', self.search_author, 3),
            ('点击搜索结果作者头像进入主页', self.open_searched_author, 2),
            ('作者主页上滑3次、下滑3次', lambda: self.browse_author(3, 3), 0),
            ('返回主界面并将搜索浏览循环补足3次', self.repeat_two_search_visits, 2),
            ('滑动返回Home页', self.home, 1),
        ]
