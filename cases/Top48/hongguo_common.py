"""红果免费短剧动态用例的底栏、榜单、评论和搜索公共操作。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class HongguoDynamicCase(DynamicAppCase):
    PACKAGE = 'com.phoenix.read'
    all_app_package_list = [PACKAGE]

    BOTTOM_TAB_ID = 'gbx'
    THEATER_SEARCH_ID = 'k7'
    COMMENT_ID = 'cgr'
    SEARCH_INPUT_ID = 'hrz'
    SEARCH_BUTTON_ID = 'htk'
    SEARCH_RESULT_TITLE_ID = 'ko7'
    FULLSCREEN_ID = 'cvd'

    def bottom_selected(self, name):
        return any(node.get('selected') == 'true'
                   for node in self.nodes(text=name, rid=self.BOTTOM_TAB_ID))

    def switch_bottom(self, name):
        if self.bottom_selected(name):
            return
        self.transition(lambda: self.click(text=name, rid=self.BOTTOM_TAB_ID),
                        lambda: self.bottom_selected(name),
                        '红果免费短剧未切换到底部“{}”页'.format(name))

    def close_pendant(self):
        if self.has(desc='Close Button'):
            self.click(desc='Close Button')
            time.sleep(.5)
        elif not self.nodes():
            # “看短剧奖励待领取”弹窗不进入目标应用控件树，系统返回可安全关闭。
            self.back()
            time.sleep(.7)

    def main_page(self):
        self.return_to(lambda: self.has(text='首页', rid=self.BOTTOM_TAB_ID),
                       '未返回红果免费短剧主界面')
        self.switch_bottom('首页')
        self.close_pendant()

    def launch(self):
        self.start()
        self.main_page()

    def theater_ready(self):
        return self.bottom_selected('剧场') and self.has(rid=self.THEATER_SEARCH_ID)

    def theater(self):
        self.switch_bottom('剧场')
        self.close_pendant()
        self.wait_for(self.theater_ready, '红果剧场页未加载')

    def refresh_theater(self):
        # 表格要求在剧场页再次点击“剧场”；控件文本和资源 ID 均稳定。
        self.click(text='剧场', rid=self.BOTTOM_TAB_ID)
        self.wait_for(self.theater_ready, '再次点击后红果剧场页未就绪')

    def reveal_theater_control(self, text):
        for _ in range(6):
            if self.has(text=text):
                return
            self.swipe(.5, .32, .5, .78, 350)
            time.sleep(.7)
        raise RuntimeError('红果剧场页未找到“{}”'.format(text))

    def rank_ready(self):
        return (self.has(text='推荐榜') and self.has(text='热播榜')
                and self.has(desc='rank_bg'))

    def open_rank(self):
        self.reveal_theater_control('排行榜')
        self.transition(lambda: self.click(text='排行榜'), self.rank_ready,
                        '红果排行榜未打开')

    def select_rank(self, name):
        self.click(text=name)
        self.wait_for(lambda: self.has(desc='rank_bg'),
                      '“{}”内容未加载'.format(name))
        time.sleep(1)

    def rank_to_top(self):
        for _ in range(6):
            if self.has(text='1') and self.has(desc='rank_bg'):
                return
            self.swipe(.5, .32, .5, .82, 350)
            time.sleep(.5)
        raise RuntimeError('排行榜未回到第一名位置')

    def play_first_rank(self):
        self.rank_to_top()
        cards = sorted(self.nodes(desc='rank_bg'),
                       key=lambda node: (self.bounds(node)[1], self.bounds(node)[0]))
        if not cards:
            raise RuntimeError('排行榜没有可播放的短剧')
        self.transition(lambda: self.click_node(cards[0]), self.video_ready,
                        '排行榜第一条短剧未开始播放')

    def video_ready(self):
        return self.has(text='全屏观看', rid=self.FULLSCREEN_ID)

    def return_to_rank(self):
        self.return_to(self.rank_ready, '未返回红果排行榜')

    def return_to_theater(self):
        self.return_to(self.theater_ready, '未返回红果剧场页')
        self.close_pendant()

    def mine(self):
        self.switch_bottom('我的')
        self.close_pendant()
        self.wait_for(lambda: self.bottom_selected('我的') and self.has(desc='历史'),
                      '红果“我的”观看历史未加载')

    def speed_play(self):
        # 推荐视频没有可访问的画面控件；以屏幕比例长按画面中央，再选 2x。
        self.foreground()
        width, height = self.d.window_size()
        # 首页视频在当前布局约占屏幕高度 25%～46%，35% 处可避开顶部字幕和底部控件。
        x, y = round(width * .5), round(height * .35)
        result = self.d.shell(
            'input -d 0 swipe {0} {1} {0} {1} 2200'.format(x, y))
        if result.exit_code:
            raise RuntimeError('长按推荐视频失败：' + result.output)
        self.wait_for(lambda: self.has(text='倍速') and self.has(text='2x'),
                      '长按后未打开倍速面板', timeout=6)
        self.click(text='2x')
        self.back()
        self.wait_for(lambda: self.bottom_selected('首页'),
                      '选择2倍速后未返回推荐视频', timeout=6)

    def comments_ready(self):
        return (self.has(desc='back_unfold')
                and any(node.get('text', '').endswith('条评论') for node in self.nodes()))

    def open_comments(self):
        self.transition(lambda: self.click(rid=self.COMMENT_ID), self.comments_ready,
                        '推荐视频评论面板未打开')

    def close_comments_by_swipe(self):
        # 评论是半屏抽屉；从左缘按比例侧滑退出，避免绑定具体分辨率。
        self.swipe(.02, .58, .82, .58, 450)
        self.wait_for(lambda: self.bottom_selected('首页') and not self.comments_ready(),
                      '侧滑未退出推荐视频评论面板')

    def open_search(self):
        self.transition(lambda: self.click(rid=self.THEATER_SEARCH_ID),
                        lambda: self.has(rid=self.SEARCH_INPUT_ID)
                        and self.has(text='搜索', rid=self.SEARCH_BUTTON_ID),
                        '红果搜索页未打开')

    def search(self, keyword):
        edit = self.d(resourceId=self.PACKAGE + ':id/' + self.SEARCH_INPUT_ID)
        if not edit.wait(timeout=6):
            raise RuntimeError('红果搜索输入框不可用')
        edit.set_text(keyword)
        self.wait_for(lambda: self.has(text=keyword, rid=self.SEARCH_INPUT_ID),
                      '搜索词未写入：' + keyword)
        self.click(text='搜索', rid=self.SEARCH_BUTTON_ID)
        self.wait_for(lambda: bool(self.nodes(rid=self.SEARCH_RESULT_TITLE_ID)),
                      '“{}”没有可见搜索结果'.format(keyword), timeout=20)
        self._search_keyword = keyword

    def play_first_search_result(self):
        # 浏览后先找回与搜索词同名的首条短剧；找不到时才使用当前最上方结果。
        keyword = getattr(self, '_search_keyword', None)
        if keyword:
            for _ in range(5):
                exact = self.nodes(text=keyword, rid=self.SEARCH_RESULT_TITLE_ID)
                if exact:
                    self.transition(lambda: self.click_node(exact[0]), self.video_ready,
                                    '第一条搜索结果未开始播放')
                    return
                self.swipe(.5, .32, .5, .82, 350)
                time.sleep(.5)
        results = sorted(self.nodes(rid=self.SEARCH_RESULT_TITLE_ID),
                         key=lambda node: (self.bounds(node)[1], self.bounds(node)[0]))
        if not results:
            raise RuntimeError('搜索结果页没有可播放短剧')
        self.transition(lambda: self.click_node(results[0]), self.video_ready,
                        '第一条搜索结果未开始播放')

    def watch_portrait(self):
        width, height = self.d.window_size()
        if width >= height or not self.video_ready():
            raise RuntimeError('短剧未处于竖屏播放状态')

    def fullscreen(self):
        self.transition(lambda: self.click(text='全屏观看', rid=self.FULLSCREEN_ID),
                        lambda: self.d.window_size()[0] > self.d.window_size()[1],
                        '短剧未切换至横屏播放')
