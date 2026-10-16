"""UC 当前版本新闻频道、搜索及搜索发现浏览。"""
import re
import time

from Cases.Top48.observed_apps_common import ObservedAppCase, StepUnavailable, optional


class UcDynamicCase(ObservedAppCase):
    PACKAGE = 'com.UCMobile'
    all_app_package_list = [PACKAGE]
    COMPONENT = PACKAGE + '/.main.UCMobile'

    def dismiss_ads(self):
        super().dismiss_ads()
        if self.visible('退出UC', True) and self.visible('取消'):
            self.choose('取消')
            self.wait_for(lambda: not self.visible('退出UC', True), 'UC退出提示未关闭')
        if self.visible('开启消息通知') and self.visible('前往开启'):
            # 当前通知引导弹窗右上 X，已用截图核对；关闭，不开启通知权限。
            if self.visible('X', region=(.7, .28, .95, .45)):
                self.choose('X', region=(.7, .28, .95, .45))
            else:
                self.pct(.842, .355)
            self.wait_for(lambda: not self.visible('开启消息通知'), 'UC通知引导未关闭')

    def main_ready(self):
        if self.has(desc='菜单') and self.has(desc='网盘') and self.has(desc='小说'):
            height = self.d.window_size()[1]
            if any(.12 < (self.bounds(n)[1]+self.bounds(n)[3])/2/height < .17
                   and n.get('text') for n in self.nodes()):
                return True
        # 横滑到末尾会出现漫剧/有声等新频道，不能只按初始几个名称判断首页。
        channels = [r for r in self.screen() if .12 < r['y']+r['h']/2 < .17
                    and r['x'] < .85 and 2 <= len(r['text']) <= 8]
        return (len(channels) >= 2
                and self.visible('菜单', region=(0, .88, 1, 1)))

    def main_page(self):
        for _ in range(10):
            self.dismiss_ads()
            if self.main_ready():
                return
            self.back()
        raise RuntimeError('未返回UC浏览器首页频道栏')

    def selected_channel(self, label):
        return any(n.get('selected') == 'true' for n in self.nodes(text=label))

    def channel(self, label):
        self.main_page()
        height = self.d.window_size()[1]
        for _ in range(6):
            nodes = [n for n in self.nodes(text=label) if self.bounds(n)[1] < height*.23]
            if nodes or self.visible(label, region=(0, .1, 1, .23)):
                break
            self.swipe(.2, .145, .8, .145, 400)
            time.sleep(.5)
        if nodes:
            self._locators.add('tree')
            self.click_node(nodes[0])
        elif self.visible(label, region=(0, .1, 1, .23)):
            self.choose(label, region=(0, .1, 1, .23))
        else:
            raise StepUnavailable('当前频道栏没有可唯一定位的“{}”'.format(label))
        time.sleep(1)
        self.dismiss_ads()
        self.content_wait(self.main_ready, label + '频道未显示')
        if not self.selected_channel(label):
            self.adapt('已点击“{}”频道，当前控件不导出选中状态，保留截图核对'.format(label))

    def swipe_channels(self, left=True):
        self.main_page()
        for _ in range(5):
            self.swipe(.8 if left else .2, .145, .2 if left else .8, .145, 400)
            time.sleep(1)
        self.adapt('当前小说等频道会进入独立页面，改为横滑顶部频道栏五次浏览入口，保留当前信息流')

    def channels_left(self):
        self.swipe_channels(True)

    def channels_right(self):
        self.swipe_channels(False)

    def browse_feed(self):
        if not self.main_ready():
            raise StepUnavailable('当前不在UC首页信息流')
        self.browse(5, 5)

    @optional('sports')
    def sports(self):
        self.channel('体育')

    @optional('sports')
    def browse_sports(self):
        self.needs('sports')
        self.browse_feed()

    def recommend(self):
        self.channel('推荐')

    @optional('news')
    def first_news(self):
        self.recommend()
        rows = [r for r in self.screen() if .2 < r['y'] < .85 and len(r['text']) >= 10
                and not any(s in r['text'] for s in ('广告', '立即下载', '去领取', '会员', '热度', '开启', '小说', '短剧'))]
        if not rows:
            raise StepUnavailable('推荐信息流没有可核对的首条新闻标题')
        row = rows[0]
        self._locators.add(row['source'])
        self._news_title = row['text']
        self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
        self.content_wait(self.article_ready, '新闻正文未打开')

    def article_ready(self):
        return not self.main_ready() and (self.visible('说点什么', True)
            or self.visible('评论', True, (0, .88, 1, 1))
            or self.visible('收藏', region=(.6, .88, .9, 1)))

    @optional('news')
    def browse_news(self):
        self.needs('news')
        if not self.article_ready():
            raise StepUnavailable('新闻正文不可用')
        self.browse(5, 5)

    def search_ready(self):
        return any(n.get('class') == 'android.widget.EditText' for n in self.nodes()) and (
            self.has(rid='cancel', text='搜索') or self.has(rid='search_rec_item_text')
            or self.visible('搜索发现', True) or self.visible('热搜榜', True))

    @optional('search')
    def search_page(self):
        self.main_page()
        # 首页搜索热词会动态变化，以原生输入/搜索栏节点优先。
        nodes = [n for n in self.nodes() if self.bounds(n)[1] < self.d.window_size()[1]*.13
                 and ('search' in n.get('resource-id', '').lower() or n.get('content-desc') in ('搜索', '搜索框'))]
        action = (lambda: self.click_node(nodes[0])) if nodes else (lambda: self.pct(.48, .093))
        self.go(action, self.search_ready, 'UC搜索编辑页未打开')

    @optional('search-results')
    def movie_search(self):
        self.needs('search')
        fields = [n for n in self.nodes() if n.get('class') == 'android.widget.EditText']
        if len(fields) != 1:
            raise StepUnavailable('搜索输入框不唯一')
        self.click_node(fields[0])
        self.input_text('大话天仙')
        if self.has(rid='cancel', text='搜索'):
            self._locators.add('tree')
            self.click(rid='cancel', text='搜索')
        else:
            self.choose('搜索', region=(.7, .04, 1, .17), index=0)
        self.content_wait(lambda: self.visible('大话天仙', True) and any(self.visible(s, True) for s in (
            '综合', '全部', '网页', '视频', '资讯', '图片', '相关搜索', 'UC搜索')), '大话天仙搜索结果未加载')

    @optional('search-results')
    def browse_search(self):
        self.needs('search-results')
        if not self.visible('大话天仙', True):
            raise StepUnavailable('当前不是大话天仙搜索结果')
        self.browse(5, 5)

    @optional('search')
    def return_search(self):
        self.needs('search')
        self.dismiss_system_prompt()
        self.main_page()
        self.search_page()
        self.adapt('当前从首页重新打开搜索编辑页，替代旧版从结果页直接返回编辑页')

    @optional('discovery')
    def first_discovery(self):
        self.needs('search')
        if not self.search_ready():
            raise StepUnavailable('搜索编辑页未打开')
        headings = self.find('搜索发现', True)
        if not headings:
            headings = self.find('资讯热搜榜', True) or self.find('热搜榜', True)
            if headings:
                self.adapt('当前“资讯热搜榜”替代旧版“搜索发现”栏目')
        if not headings:
            raise StepUnavailable('当前搜索页没有搜索发现栏目')
        top = headings[0]['y'] + headings[0]['h']
        rows = [r for r in self.screen() if top < r['y'] < .85 and len(r['text']) >= 4
                and not re.fullmatch(r'[\d\W]+', r['text'])
                and not any(s in r['text'] for s in ('关闭', '广告', '更多', '历史', '删除', '清空'))]
        if not rows:
            raise StepUnavailable('搜索发现没有可定位的第一条词条')
        row = rows[0]
        self._discovery = row['text']
        self._locators.add(row['source'])
        self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
        self.content_wait(lambda: not self.search_ready(), '搜索发现详情未打开')

    @optional('discovery')
    def browse_discovery(self):
        self.needs('discovery')
        if self.search_ready() or self.main_ready():
            raise StepUnavailable('搜索发现详情不可用')
        self.browse(5, 5)
