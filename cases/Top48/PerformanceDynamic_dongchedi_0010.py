"""懂车帝推荐、车型图集和热榜浏览（表格第 475～491 行）。"""
import json
import logging
from pathlib import Path
import subprocess
import tempfile
import re
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_dongchedi_0010(DynamicAppCase):
    PACKAGE = 'com.ss.android.auto'
    all_app_package_list = [PACKAGE]
    PERMISSIONS = ('ACCESS_COARSE_LOCATION', 'ACCESS_FINE_LOCATION')
    QUERY = '奥迪A8'
    DEFAULT_FEED = '独家'

    def set_up(self):
        super().set_up()
        from Cases.Top48.weixin_common import WeixinDynamicCase
        self._ocr_command = None
        self._locators = set()
        WeixinDynamicCase.prepare_ocr(self)

    def screenshot_rows(self):
        if not self._ocr_command:
            raise RuntimeError('新闻搜索结果为自绘页面，需要本地 OCR')
        with tempfile.TemporaryDirectory(prefix='dongchedi-screen-') as folder:
            path = str(Path(folder) / 'screen.png')
            self.d.screenshot(path, display_id=0)
            result = subprocess.run(self._ocr_command + [path], check=True,
                                    capture_output=True, text=True, timeout=30)
        self._locators.add('screenshot-ocr-relative')
        return json.loads(result.stdout)

    def visual_label(self, label):
        # 优先控件属性；自绘筛选面板没有节点时才使用截图文字的比例边界。
        nodes = self.nodes(text=label) or self.nodes(desc=label)
        if nodes:
            self.click_node(nodes[0])
            return
        rows = [r for r in self.screenshot_rows() if label in r['text'] and len(r['text'].strip()) <= len(label) + 3]
        if len(rows) != 1:
            raise RuntimeError('截图文字不存在或不唯一：' + label)
        row = rows[0]
        self.pct(row['x'] + row['w']/2, row['y'] + row['h']/2)
        time.sleep(.7)

    def main_ready(self):
        height = self.screen_size()[1]
        return (any(self.bounds(n)[1] > height * .9 for n in self.nodes(text='首页'))
                and self.has(rid='q'))

    def feed_tabs(self, name):
        return self.nodes(text=name, rid='tv_tag')

    def tab_selected(self, name):
        return any(node.get('selected') == 'true' for node in self.feed_tabs(name))

    def launch(self):
        self.start()
        self.return_to(self.main_ready, '懂车帝首页未加载')
        self.switch_feed('推荐')

    def switch_feed(self, name):
        if name == '推荐' and not self.feed_tabs(name):
            # 当前版本首页以“独家”作为默认资讯流，不再提供“推荐”标签。
            logging.info('替代：新版懂车帝无“推荐”标签，使用默认“%s”资讯流', self.DEFAULT_FEED)
            self._adaptation = '新版无推荐标签，使用默认“{}”资讯流'.format(self.DEFAULT_FEED)
            name = self.DEFAULT_FEED
        tabs = self.feed_tabs(name)
        if len(tabs) != 1:
            raise RuntimeError('懂车帝频道不可用：{}（{} 个）'.format(name, len(tabs)))
        if any(node.get('selected') == 'true' for node in self.nodes(rid='tv_tag')):
            self.transition(lambda: self.click_node(tabs[0]), lambda: self.tab_selected(name),
                            '懂车帝未切换到{}频道'.format(name))
        else:
            # 此版本未公开标签 selected 状态，仍按唯一标签控件点击并等待页面刷新。
            self.click_node(tabs[0])
            time.sleep(1)

    def search_page(self):
        self.return_to(self.main_ready, '未返回懂车帝首页')
        self.open_control(self.search_ready, '懂车帝搜索页未打开', rid='q')

    def search_ready(self):
        return any(n.get('class') in ('android.widget.AutoCompleteTextView',
                                      'android.widget.EditText') for n in self.nodes())

    def search(self):
        editors = [n for n in self.nodes() if n.get('class') in (
            'android.widget.AutoCompleteTextView', 'android.widget.EditText')]
        if len(editors) != 1:
            raise RuntimeError('懂车帝搜索输入框不唯一')
        self.d(packageName=self.PACKAGE, className=editors[0].get('class')).set_text(self.QUERY)
        self.click(text='搜索')
        self.wait_for(self.results_ready, '奥迪A8搜索结果未加载', timeout=30)

    def results_ready(self):
        height = self.screen_size()[1]
        return (any(self.bounds(n)[1] > height * .15 for n in self.nodes(text=self.QUERY))
                and self.has(desc='参数配置'))

    def car_ready(self):
        return self.has(text=self.QUERY) and self.has(text='图集', rid='tv_tab')

    def first_car_result(self):
        self.wait_for(self.results_ready, '奥迪A8车型结果未加载', timeout=30)
        height = self.screen_size()[1]
        title = next(n for n in self.nodes(text=self.QUERY) if self.bounds(n)[1] > height * .15)
        self.transition(lambda: self.click_node(title), self.car_ready,
                        '首条奥迪A8车型结果未打开')

    def gallery(self):
        self.wait_for(self.car_ready, '奥迪A8车型详情未打开')
        # 第一次选中顶部图集封面，第二次进入“全部车型”图集列表。
        self.transition(lambda: self.click(text='图集', rid='tv_tab'),
                        self.gallery_ready, '车型图集列表未打开')

    def gallery_ready(self):
        return self.has(text='全部车型', rid='tv_title') and self.has(text='外观')

    def viewer_ready(self):
        return any(re.fullmatch(r'\d+\s*/\s*\d+', node.get('text', ''))
                   for node in self.nodes())

    def open_first_photo(self):
        photos = sorted(self.nodes(rid='bnv'), key=lambda node: (self.bounds(node)[1], self.bounds(node)[0]))
        if not photos:
            width, height = self.screen_size()
            photos = sorted([n for n in self.nodes()
                             if n.get('class') == 'android.widget.ImageView'
                             and n.get('clickable') == 'true'
                             and .2 < (self.bounds(n)[2] - self.bounds(n)[0]) / width < .4
                             and (self.bounds(n)[3] - self.bounds(n)[1]) > height * .05],
                            key=lambda n: (self.bounds(n)[1], self.bounds(n)[0]))
        if photos:
            opener = lambda: self.click_node(photos[0])
        else:
            heroes = self.nodes(rid='d26')
        if not photos and heroes:
            # 新版图集以顶部大图替代“全部车型”缩略图列表。
            logging.info('替代：新版懂车帝点击图集顶部大图进入图片查看器')
            opener = lambda: self.click_node(heroes[0])
        elif not photos and self.gallery_ready():
            # 当前版本的车型缩略图网格完全自绘；只在已核验图集页内按比例点首图。
            logging.info('替代：按图集页比例点击第一张车型缩略图')
            opener = lambda: self.pct(.16, .55)
        elif not photos:
            raise RuntimeError('车型图集中没有可打开的图片')
        self.transition(opener, self.viewer_ready,
                        '第一张车型图片未打开')

    def browse_photos(self):
        self.wait_for(self.viewer_ready, '图片浏览前未进入大图页')
        for _ in range(3):
            self.swipe(.82, .50, .18, .50, 350)
        for _ in range(3):
            self.swipe(.18, .50, .82, .50, 350)

    def return_search_page(self):
        self.return_to(lambda: self.search_ready() and self.has(text='热榜'),
                       '未返回懂车帝搜索页')

    def first_hot_news(self):
        width, height = self.screen_size()
        titles = [node for node in self.nodes(rid='tv_title')
                  if node.get('text', '').strip()
                  and self.bounds(node)[0] < width * .25
                  and self.bounds(node)[1] > height * .18]
        if not titles:
            raise RuntimeError('懂车帝热榜没有可打开的新闻')
        first = min(titles, key=lambda node: self.bounds(node)[1])
        title = first.get('text')
        def result_opened():
            return (not self.search_ready() and any(self.bounds(n)[1] < height * .13
                    for n in self.nodes(text=title)))
        self.open_control(result_opened, '热榜第一条未打开',
                          text=first.get('text'), rid='tv_title')
        # 热榜先进入混合搜索结果，首卡可能为视频；通过本版筛选入口保留图文正文浏览。
        self.wait_for(lambda: any('筛选' in r['text'] for r in self.screenshot_rows()),
                      '热榜主题搜索结果未加载', timeout=25)
        self.visual_label('筛选')
        self.wait_for(lambda: any(r['text'] == '内容形式' for r in self.screenshot_rows()),
                      '新闻筛选面板未打开')
        self.visual_label('专业内容')
        self.visual_label('图文')
        self.visual_label('确定')
        time.sleep(2)
        rows = self.screenshot_rows()
        candidates = sorted([r for r in rows if len(r['text'].strip()) >= 10
                             and r['w'] > .2 and .20 < r['y'] < .84],
                            key=lambda r: (r['y'], r['x']))
        for row in candidates[:8]:
            self.pct(row['x'] + row['w']/2, row['y'] + row['h']/2)
            time.sleep(1)
            if 'NewDetailActivity' in self.current_app()['activity']:
                self.wait_for(self.news_ready, '新闻正文内容未加载', timeout=20)
                self._adaptation = '新版热榜进入混合搜索，经专业内容/图文筛选打开同主题首个可用新闻正文'
                logging.info('适配：%s；正文标题：%s', self._adaptation, row['text'])
                return
            if 'SearchActivity' not in self.current_app()['activity']:
                self.back()
                self.wait_for(result_opened, '未返回热榜主题结果页')
        raise RuntimeError('热榜主题图文结果中未找到可浏览的新闻正文')

    def news_ready(self):
        return ('NewDetailActivity' in self.current_app()['activity']
                and any(n.get('class') == 'android.webkit.WebView' for n in self.nodes())
                and self.has(text='说点什么', prefix=True))

    def browse_news(self):
        self.wait_for(self.news_ready, '新闻浏览前未进入正文页')
        self.browse(2, 2)
        self.wait_for(self.news_ready, '滑动后离开了新闻正文页')

    def back_main(self):
        self.return_to(self.main_ready, '未返回懂车帝主界面')
        self.switch_feed('推荐')

    def steps(self):
        return [
            ('启动懂车帝', self.launch, 3),
            ('推荐页上滑5次、下滑5次', lambda: self.browse(5, 5), 0),
            ('点击关注', lambda: self.switch_feed('关注'), 2),
            ('关注页上滑2次、下滑2次', lambda: self.browse(2, 2), 0),
            ('点击推荐，返回推荐页面', lambda: self.switch_feed('推荐'), 2),
            ('点击搜索框', self.search_page, 2),
            ('输入奥迪A8，点击搜索', self.search, 2),
            ('点击第一个搜索结果', self.first_car_result, 2),
            ('点击图片', self.gallery, 2),
            ('点击查看第一张图片', self.open_first_photo, 2),
            ('图片页左滑3次、右滑3次', self.browse_photos, 0),
            ('返回图片界面', lambda: self.return_to(
                self.gallery_ready,
                '未返回图片界面',
            ), 2),
            ('返回搜索界面', self.return_search_page, 2),
            ('点击热榜下第一条新闻', self.first_hot_news, 2),
            ('新闻页上滑2次、下滑2次', self.browse_news, 0),
            ('返回懂车帝主界面', self.back_main, 2),
            ('滑动返回Home页', self.home, 1),
        ]
