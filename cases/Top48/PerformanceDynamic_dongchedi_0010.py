"""懂车帝推荐、车型图集和热榜浏览（表格第 475～491 行）。"""
import logging
import re
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_dongchedi_0010(DynamicAppCase):
    PACKAGE = 'com.ss.android.auto'
    all_app_package_list = [PACKAGE]
    QUERY = '奥迪A8'
    DEFAULT_FEED = '独家'

    def main_ready(self):
        return self.has(text='首页', rid='bs6') and self.has(rid='q')

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
        self.open_control(lambda: self.has(rid='evk'), '懂车帝搜索页未打开', rid='q')

    def search(self):
        self.d(resourceId=self.PACKAGE + ':id/evk').set_text(self.QUERY)
        self.open_control(lambda: self.has(text=self.QUERY, rid='rca'),
                          '奥迪A8搜索结果未加载', text='搜索', rid='rc0')

    def first_car_result(self):
        self.require(text=self.QUERY, rid='rca')
        # 当前结果页由自绘卡片构成，没有稳定的车型项 id；仅在已核验查询页后按比例点首车卡。
        self.transition(lambda: self.pct(.15, .23),
                        lambda: self.has(text=self.QUERY, rid='f9o'),
                        '首条奥迪A8车型结果未打开')

    def gallery(self):
        self.require(text=self.QUERY, rid='f9o')
        if not self.tab_selected('图集'):
            self.click(text='图集', rid='tv_tab')
            time.sleep(1)
        self.wait_for(
            lambda: self.tab_selected('图集') or self.has(rid='d26'),
            '车型图集标签未切换',
        )

    def viewer_ready(self):
        return any(re.fullmatch(r'\d+\s*/\s*\d+', node.get('text', ''))
                   for node in self.nodes())

    def open_first_photo(self):
        photos = sorted(self.nodes(rid='bnv'), key=lambda node: (self.bounds(node)[1], self.bounds(node)[0]))
        if photos:
            opener = lambda: self.click_node(photos[0])
        elif self.has(rid='d26'):
            # 新版图集以顶部大图替代“全部车型”缩略图列表。
            logging.info('替代：新版懂车帝点击图集顶部大图进入图片查看器')
            opener = lambda: self.click(rid='d26')
        else:
            raise RuntimeError('车型图集中没有可打开的图片')
        self.transition(opener, self.viewer_ready,
                        '第一张车型图片未打开')

    def browse_photos(self):
        self.require(text='外观', rid='e53')
        for _ in range(3):
            self.swipe(.82, .50, .18, .50, 350)
        for _ in range(3):
            self.swipe(.18, .50, .82, .50, 350)

    def return_search_page(self):
        self.return_to(lambda: self.has(rid='evk') and self.has(text='热榜'),
                       '未返回懂车帝搜索页')

    def first_hot_news(self):
        width, height = self.d.window_size()
        titles = [node for node in self.nodes(rid='tv_title')
                  if node.get('text', '').strip()
                  and self.bounds(node)[0] < width * .25
                  and self.bounds(node)[1] > height * .18]
        if not titles:
            raise RuntimeError('懂车帝热榜没有可打开的新闻')
        first = min(titles, key=lambda node: self.bounds(node)[1])
        self.open_control(lambda: self.has(rid='rca'), '热榜第一条未打开',
                          text=first.get('text'), rid='tv_title')
        # 新版热榜先展示该新闻的搜索结果页，页面未暴露稳定文章节点，保留结果页浏览。
        logging.info('替代：新版懂车帝热榜第一条进入新闻搜索结果页，浏览该结果页')

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
                lambda: self.tab_selected('图集') or self.has(rid='d26'),
                '未返回图片界面',
            ), 2),
            ('返回搜索界面', self.return_search_page, 2),
            ('点击热榜下第一条新闻', self.first_hot_news, 2),
            ('新闻页上滑2次、下滑2次', lambda: self.browse(2, 2), 0),
            ('返回懂车帝主界面', self.back_main, 2),
            ('滑动返回Home页', self.home, 1),
        ]
