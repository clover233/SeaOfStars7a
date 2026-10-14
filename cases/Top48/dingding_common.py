"""钉钉与今日头条动态性能用例的可复用页面操作。"""
import logging

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
        self.switch_tab('会议')
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
        return self.has(desc='返回') and (self.has(desc='更多操作') or self.has(desc='more'))

    def search_page(self):
        self.open_control(lambda: self.has(rid='cx'),
                          '今日头条搜索页未打开', rid='kic')

    def hot_list(self):
        self.return_to(self.home_ready, '未返回今日头条首页')
        self.transition(lambda: self.click(desc='热榜'),
                        lambda: self.channel_selected('热榜'),
                        '今日头条未切换到热榜频道')
        # 热榜主体为自绘卡片，内容加载后会暴露“焦点关注”语义；该控件用于避免点到骨架屏。
        self.wait_for(lambda: self.has(desc='焦点关注'), '今日头条热榜内容未加载', timeout=20)

    def first_hot_item(self):
        if not self.channel_selected('热榜') or not self.has(desc='焦点关注'):
            raise RuntimeError('热榜首条点击前页面未完成加载')
        # 热榜新闻卡片由自绘层承载，没有稳定控件 id。以已选中热榜和加载完成作前置，
        # 再按屏幕比例点击第一张新闻卡的标题区，避开顶部专题与 AI 摘要区域。
        self.transition(lambda: self.pct(.28, .50), self.article_ready,
                        '热榜第一条文章未打开')

    def channel_selected(self, name):
        return any(node.get('selected') == 'true' for node in self.nodes(desc=name))

    def switch_channel(self, name):
        self.return_to(self.home_ready, '未返回今日头条首页')
        self.transition(lambda: self.click(desc=name),
                        lambda: self.channel_selected(name),
                        '今日头条未切换到{}频道'.format(name))

    def first_recommended_article(self):
        self.switch_channel('推荐')
        height = self.d.window_size()[1]
        cards = [node for node in self.nodes()
                 if node.get('content-desc', '').endswith('文章')
                 and self.bounds(node)[1] > height * .14
                 and self.bounds(node)[1] < height * .80]
        if not cards:
            raise RuntimeError('推荐页没有可打开的文章卡片')
        card = min(cards, key=lambda node: self.bounds(node)[1])
        self.transition(lambda: self.click_node(card), self.article_ready,
                        '推荐第一篇文章未打开')
