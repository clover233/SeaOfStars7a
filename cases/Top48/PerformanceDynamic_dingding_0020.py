"""钉钉发起单人语音会议并切换今日头条浏览（表格第 450～474 行）。"""
import logging
import time

from Cases.Top48.dingding_common import DingTalkDynamicCase, ToutiaoDynamicFlow


class PerformanceDynamic_dingding_0020(DingTalkDynamicCase):
    NEWS_PACKAGE = ToutiaoDynamicFlow.PACKAGE
    all_app_package_list = [DingTalkDynamicCase.PACKAGE, NEWS_PACKAGE]

    def __init__(self, result_path):
        super().__init__(result_path)
        self.news = object.__new__(ToutiaoDynamicFlow)
        self.meeting_title = None

    def more_options(self):
        self.return_to(self.navigation_ready, '未返回钉钉底部导航')
        self.open_control(lambda: self.has(rid='home_fern_grid_more_edit'),
                          '钉钉更多选项未展开', text='更多')

    def meeting_page(self):
        # 设备上的新版钉钉将“会议”置于底栏，更多选项中已无此入口。
        self.more_options()
        logging.info('替代：新版钉钉“会议”位于底栏，关闭更多面板后进入会议页')
        self.back()
        self.conference_page()

    def live_meeting(self):
        return self.has(text='结束', rid='tv') and self.has(rid='conf_duration_text')

    def create_voice_meeting(self):
        self.meeting_page()
        self.open_control(lambda: self.has(text='语音会议', rid='tv_content'),
                          '发起会议选项未打开', text='发起会议', rid='item_text')
        self.open_control(lambda: self.has(rid='edit_conf_title') and self.has(text='进入会议', rid='tv'),
                          '语音会议准备页未打开', text='语音会议', rid='tv_content')
        self.meeting_title = '动态性能测试_{}'.format(int(time.time()))
        self.d(resourceId=self.PACKAGE + ':id/edit_conf_title').set_text(self.meeting_title)
        self.open_control(self.live_meeting, '未进入语音会议', text='进入会议', rid='tv')

    def leave_to_home_with_meeting(self):
        if not self.live_meeting():
            raise RuntimeError('会议未处于进行中，停止离开应用')
        self.home()

    def news_home(self):
        self.news.launch()

    def news_hot(self):
        self.news.hot_list()

    def news_hot_first(self):
        self.news.first_hot_item()

    def news_discover(self):
        self.news.switch_channel('发现')

    def news_recommended_first(self):
        self.news.first_recommended_article()

    def news_return_home(self):
        self.news.return_to(self.news.home_ready, '未返回今日头条主界面')

    def news_leave_home(self):
        self.news.home()

    def resume_own_meeting(self):
        self.start()
        if self.live_meeting():
            logging.info('钉钉恢复后已自动回到进行中的会议')
            return
        self.conference_page()
        if not self.meeting_title or not self.has(text=self.meeting_title):
            raise RuntimeError('今天列表中没有本用例创建的会议：{}'.format(self.meeting_title))
        self.click(text=self.meeting_title)
        self.wait_for(lambda: self.has(text='入会') or self.live_meeting(), '会议详情未打开')
        if not self.live_meeting():
            self.open_control(self.live_meeting, '未重新进入本用例创建的会议', text='入会')

    def wait_one_minute(self):
        # 表格要求保持会议一分钟，按秒等待以保留异常中断时的日志线索。
        for second in range(60):
            if not self.live_meeting():
                raise RuntimeError('等待过程中会议已意外结束（{} 秒）'.format(second))
            time.sleep(1)

    def end_own_meeting(self):
        if not self.live_meeting():
            return
        self.click(text='结束', rid='tv')
        time.sleep(1)
        # 单人会议通常直接结束；若版本展示“全员结束会议”确认，按页面控件确认。
        if self.has(text='全员结束会议'):
            self.click(text='全员结束会议')
            time.sleep(.8)
        if self.has(text='结束会议'):
            self.click(text='结束会议')
        self.wait_for(lambda: not self.live_meeting(), '会议未结束', timeout=10)

    def ding_home(self):
        self.return_to(self.navigation_ready, '未返回钉钉主界面')

    def clean_up(self):
        # 如中途失败，只结束本用例创建的正在进行的会议，避免遗留通话状态。
        try:
            if self.current_app()['package'] == self.PACKAGE:
                self.end_own_meeting()
        except Exception:
            logging.exception('清理阶段未能结束测试会议')
        super().clean_up()

    def steps(self):
        return [
            ('启动钉钉', self.launch, 3),
            ('点击更多，拉起更多选项', self.more_options, 2),
            ('点击会议，切换到会议详情页面', self.meeting_page, 2),
            ('点击发起会议，选择语音会议', self.create_voice_meeting, 2),
            ('点击进入会议按钮，进入会议详情', lambda: self.require(rid='conf_duration_text'), 2),
            ('滑动返回Home页', self.leave_to_home_with_meeting, 2),
            ('启动今日头条', self.news_home, 3),
            ('主页浏览，上滑5次，下滑5次', lambda: self.news.browse(5, 5), 0),
            ('点击热榜tab', self.news_hot, 2),
            ('热榜浏览，上滑5次，下滑5次', lambda: self.news.browse(5, 5), 0),
            ('点击热榜第一条', self.news_hot_first, 2),
            ('热榜第一条上滑5次、下滑5次', lambda: self.news.browse(5, 5), 0),
            ('返回今日头条主界面', self.news_return_home, 2),
            ('点击发现tab', self.news_discover, 2),
            ('发现页浏览，上滑5次、下滑5次', lambda: self.news.browse(5, 5), 0),
            ('返回推荐页，点击第一条文章', self.news_recommended_first, 2),
            ('第一条文章上滑5次、下滑5次', lambda: self.news.browse(5, 5), 0),
            ('返回今日头条主界面', self.news_return_home, 2),
            ('滑动返回Home页', self.news_leave_home, 2),
            ('启动钉钉', self.resume_own_meeting, 3),
            ('点击今天列表下的第一个会议信息，点击入会', self.resume_own_meeting, 2),
            ('等待1min', self.wait_one_minute, 0),
            ('点击结束并结束全员会议', self.end_own_meeting, 2),
            ('返回钉钉主界面', self.ding_home, 2),
            ('滑动返回Home页', self.home, 1),
        ]
