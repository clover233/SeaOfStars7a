"""今日头条动态性能用例的可复用页面操作。"""
import re
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class JrttDynamicCase(DynamicAppCase):
    """适配今日头条 18.7.0 的首页、热榜和视频页面。"""

    PACKAGE = 'com.ss.android.article.news'

    def point(self, x, y):
        # 当前测试机上的头条会过滤较短的按压；450ms 能稳定触发且未达到长按菜单阈值。
        self.foreground()
        result = self.d.shell(
            'input -d 0 swipe {0} {1} {0} {1} 450'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('今日头条点击失败：' + result.output)

    def bottom_nodes(self, name):
        height = self.screen_size()[1]
        return [node for node in self.nodes(text=name, rid='tp')
                if self.bounds(node)[1] > height * .88]

    def bottom_selected(self, name):
        return any(node.get('selected') == 'true' for node in self.bottom_nodes(name))

    def bottom_ready(self):
        # 未登录版本将“我的”直接显示为“未登录”，不影响新闻和视频浏览。
        return (all(self.bottom_nodes(name) for name in ('首页', '视频'))
                and any(self.bottom_nodes(name) for name in ('我的', '未登录')))

    def switch_bottom(self, name):
        def tap_tab():
            nodes = self.bottom_nodes(name)
            if len(nodes) != 1:
                raise RuntimeError('今日头条底部入口不可用：{}（{} 个）'.format(name, len(nodes)))
            self.click_node(nodes[0])

        self.transition(tap_tab, lambda: self.bottom_selected(name),
                        '今日头条未切换到底部{}页'.format(name))

    def channel_selected(self, name):
        return any(node.get('selected') == 'true' for node in self.nodes(desc=name))

    def home_ready(self):
        return (self.bottom_selected('首页')
                and self.has(rid='kic')
                and self.has(desc='推荐'))

    def comments_ready(self):
        # 新版标题为“评论2540”，旧版为“2540条评论”；面板已打开时不能再点原入口。
        return any(re.fullmatch(r'(?:评论\s*\d+|\d+\s*条评论)',
                                node.get('text', ''))
                   for node in self.nodes())

    def main_page(self):
        if self.comments_ready():
            self.back()
        self.return_to(self.bottom_ready, '未返回今日头条底部导航')
        self.switch_bottom('首页')
        self.wait_for(self.home_ready, '今日头条首页未加载')

    def launch(self):
        self.start()
        self.main_page()

    def switch_channel(self, name):
        self.main_page()
        self.transition(lambda: self.click(desc=name),
                        lambda: self.channel_selected(name),
                        '今日头条未切换到{}频道'.format(name))

    def hot_ready(self):
        # 当前版本热榜列表为自绘层；“实时更新”是加载完成后可访问树中的稳定锚点。
        return self.channel_selected('热榜') and self.has(desc='实时更新')

    def hot_list(self):
        self.switch_channel('热榜')
        self.wait_for(self.hot_ready, '今日头条热榜内容未加载', timeout=20)

    def article_ready(self):
        if not self.has(desc='返回'):
            return False
        return (self.has(desc='更多操作')
                or self.has(desc='more')
                or any(node.get('content-desc', '').startswith('更多面板')
                       for node in self.nodes()))

    def first_hot_item(self):
        if not self.hot_ready():
            raise RuntimeError('热榜第一条点击前页面未完成加载')
        # weditor 的 hierarchy dump 显示热榜正文是自绘层，没有可点击节点。
        # 先用已选中频道和加载锚点约束页面，再按分辨率比例点击首个编号榜单项。
        self.transition(lambda: self.pct(.50, .325), self.article_ready,
                        '热榜第一条文章未打开')

    def return_hot(self):
        self.back()
        self.wait_for(self.hot_ready, '未返回今日头条热榜页')

    def recommended_cards(self):
        height = self.d.window_size()[1]
        cards = [node for node in self.nodes(rid='bos')
                 if node.get('content-desc', '').endswith('文章')
                 and height * .14 < self.bounds(node)[1] < height * .80]
        if not cards:
            # 不同推荐卡模板可能不带固定 id，保留内容描述作为语义后备定位。
            cards = [node for node in self.nodes()
                     if node.get('content-desc', '').endswith('文章')
                     and height * .14 < self.bounds(node)[1] < height * .80]
        return cards

    def first_recommended_article(self):
        self.switch_channel('推荐')
        self.wait_for(lambda: bool(self.recommended_cards()),
                      '推荐页没有可打开的文章卡片', timeout=20)
        cards = self.recommended_cards()
        card = min(cards, key=lambda node: self.bounds(node)[1])
        self.transition(lambda: self.click_node(card), self.article_ready,
                        '推荐第一篇文章未打开')

    def return_home(self):
        if self.comments_ready():
            self.back()
        self.return_to(self.bottom_ready, '未返回今日头条底部导航')
        self.switch_bottom('首页')
        self.wait_for(self.home_ready, '未返回今日头条主界面')

    def video_ready(self):
        return (self.bottom_selected('视频')
                and self.has(rid='gys')
                and (self.has(desc='暂停') or self.has(desc='播放')))

    def video_page(self):
        self.main_page()
        self.switch_bottom('视频')
        self.wait_for(self.video_ready, '今日头条视频页未加载', timeout=20)

    def open_comments(self):
        self.wait_for(self.video_ready, '评论打开前视频页未加载')
        nodes = self.nodes(rid='gys')
        if len(nodes) != 1:
            raise RuntimeError('视频评论入口不可用（{} 个）'.format(len(nodes)))
        self.transition(lambda: self.click_node(nodes[0]), self.comments_ready,
                        '今日头条视频评论面板未打开')

    def browse_comments(self):
        if not self.comments_ready():
            raise RuntimeError('评论浏览前评论面板未打开')
        # 半屏评论的标题/拖动区在约 1/3 屏处，不能从通用 .32 起手下拉。
        for start, end in ((.82, .56), (.56, .82)):
            for _ in range(2):
                self.swipe(.5, start, .5, end, 400)
                time.sleep(2)
                if not self.comments_ready():
                    raise RuntimeError('滑动评论时离开了评论面板')
