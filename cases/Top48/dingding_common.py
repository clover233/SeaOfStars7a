"""钉钉与今日头条动态性能用例的可复用页面操作。"""
import logging
import re

from Cases.Top48.screen_text import ScreenshotText

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class DingTalkDynamicCase(DynamicAppCase):
    PACKAGE = 'com.alibaba.android.rimet'

    def bottom_tabs(self, name):
        height = self.d.window_size()[1]
        return [node for node in self.nodes(text=name)
                if self.bounds(node)[1] > height * .78
                and (node.get('resource-id', '').endswith('home_bottom_tab_text')
                     or node.get('resource-id', '').endswith('home_bottom_tab_text_highlight'))]

    def tab_selected(self, name):
        return any(node.get('resource-id', '').endswith('home_bottom_tab_text_highlight')
                   or node.get('selected') == 'true'
                   for node in self.bottom_tabs(name))

    def navigation_ready(self):
        return bool(self.bottom_tabs('消息')) and bool(self.bottom_tabs('更多'))

    def launch(self):
        self.start()
        self.return_to(self.navigation_ready, '钉钉底部导航未加载，请确认已登录')

    def switch_tab(self, name):
        def tap_tab():
            nodes = self.bottom_tabs(name)
            if len(nodes) != 1:
                raise RuntimeError('钉钉底部入口不可用：{}（{} 个）'.format(name, len(nodes)))
            self.click_node(nodes[0])

        self.transition(tap_tab, lambda: self.tab_selected(name), '钉钉未切换到{}页'.format(name))

    def messages_page(self):
        self.return_to(self.navigation_ready, '未返回钉钉底部导航')
        self.switch_tab('消息')

    def conference_page(self):
        self.return_to(self.navigation_ready, '未返回钉钉底部导航')
        if self.bottom_tabs('会议'):
            self.switch_tab('会议')
        else:
            # 当前版本将会议收在底栏“更多”面板中。
            self.open_control(lambda: self.has(text='会议', rid='app_name'),
                              '更多面板没有会议入口', text='更多', rid='home_bottom_tab_text')
            self.open_control(lambda: self.has(text='发起会议', rid='item_text'),
                              '钉钉会议页未加载', text='会议', rid='app_name')
        self.wait_for(lambda: self.has(text='发起会议', rid='item_text'),
                      '钉钉会议页未加载')


class ToutiaoDynamicFlow(DynamicAppCase):
    """只承载今日头条的页面定位，实例无需 Case 初始化。"""
    PACKAGE = 'com.ss.android.article.news'

    def point(self, x, y):
        # 当前测试机上的头条会过滤过短按压；节点中心点击仍由 bounds 决定。
        self.foreground()
        result = self.d.shell('input -d 0 swipe {0} {1} {0} {1} 450'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('今日头条点击失败：' + result.output)

    def home_ready(self):
        return self.has(rid='kic') and self.has(desc='推荐')

    def launch(self):
        self.start()
        self.return_to(self.home_ready, '今日头条首页未加载')

    def article_ready(self):
        # 图文和视频热榜详情的右上角语义不同，均有返回和更多操作控件。
        if self.has(desc='返回') and (self.has(desc='更多操作') or self.has(desc='more')):
            return True
        # 新版信息流文章的返回箭头没有无障碍描述，核对文章Activity、作者和正文。
        return (self.current_app().get('activity', '').endswith('ArticleInflowActivity')
                and self.has(desc='更多操作') and self.has(rid='n07')
                and any(len(node.get('content-desc', '')) > 80 for node in self.nodes()))

    def search_page(self):
        self.open_control(lambda: self.has(rid='cx'),
                          '今日头条搜索页未打开', rid='kic')

    def hot_list(self):
        self.return_to(self.home_ready, '未返回今日头条首页')
        self.transition(lambda: self.click(desc='热榜'),
                        lambda: self.channel_selected('热榜'),
                        '今日头条未切换到热榜频道')
        # 新版热榜正文为自绘层，“焦点关注”节点已移除；用截图核对榜单与排名。
        self.wait_for(lambda: self.has(desc='焦点关注') or bool(self.first_rank_rows()),
                      '今日头条热榜内容未加载', timeout=20)

    def first_rank_rows(self):
        rows = ScreenshotText().read(self.d)
        if not any('头条热榜' in r['text'] for r in rows):
            return []
        return [r for r in rows if .24 < r['y'] < .85 and len(r['text']) > 8
                and re.match(r'^[1①](?:\s|[^0-9])', r['text'])]

    def first_hot_item(self):
        if not self.channel_selected('热榜'):
            raise RuntimeError('热榜首条点击前页面未完成加载')
        # 先恢复榜单顶部；仅点击截图中排名1的标题，避免固定位置误中其它排名。
        for _ in range(8):
            rows = self.first_rank_rows()
            if rows:
                break
            self.swipe(y1=.32, y2=.78)
        if not rows:
            raise RuntimeError('热榜没有可核对的排名1标题')
        row = min(rows, key=lambda r: r['y'])
        self.pct(row['x'] + row['w']/2, row['y'] + row['h']/2)
        # 新版榜单首条进入话题聚合页，仍是该排名的详情；与推荐文章详情分开核验。
        self.wait_for(lambda: self.article_ready() or self.hot_topic_ready(),
                      '热榜第一条详情未打开', timeout=30)

    def hot_topic_ready(self):
        return (self.current_app().get('activity', '').endswith('SearchActivity')
                and self.has(text='完整榜单') and self.has(rid='cx')
                and self.has(text='参与讨论', prefix=True))

    def channel_selected(self, name):
        return any(node.get('selected') == 'true' for node in self.nodes(desc=name))

    def switch_channel(self, name):
        self.return_to(self.home_ready, '未返回今日头条首页')
        self.transition(lambda: self.click(desc=name),
                        lambda: self.channel_selected(name),
                        '今日头条未切换到{}频道'.format(name))

    def first_recommended_article(self):
        self.switch_channel('推荐')
        height = self.screen_size()[1]
        def visible_articles():
            return [node for node in self.nodes()
                    if node.get('content-desc', '').endswith('文章')
                    and height * .14 < self.bounds(node)[1] < height * .80
                    and self.bounds(node)[3] - self.bounds(node)[1] > height * .03]
        self.wait_for(lambda: bool(visible_articles()) or self.has(desc='播放视频'),
                      '推荐内容未加载', timeout=30)
        # 推荐流可能先显示视频，按业务要求继续找到首篇图文文章。
        for _ in range(10):
            if visible_articles():
                break
            self.swipe(y1=.8, y2=.35)
        if not visible_articles():
            raise RuntimeError('推荐页没有可打开的文章卡片')
        card = min(visible_articles(), key=lambda node: self.bounds(node)[1])
        self.click_node(card)
        self.wait_for(self.article_ready, '推荐第一篇文章未打开', timeout=30)
