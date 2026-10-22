# -*- coding: utf-8 -*-

import logging
import time
from Cases.Top48.observed_apps_common import ObservedAppCase

class PerformanceDynamic_xhs_0030(ObservedAppCase):

    PACKAGE = 'com.xingin.xhs'
    COMPONENT = PACKAGE + '/.index.v2.IndexActivityV2'
    QUERY = '穿搭图片'
    all_app_package_list = [PACKAGE]

    def dismiss_ads(self):
        if self.has(text='免流量升级') and self.has(text='稍后再说'):
            self.click(text='稍后再说')
            time.sleep(.5)
        height = self.screen_size()[1]
        skips = [n for n in self.nodes(text='跳过广告', prefix=True)
                 if self.bounds(n)[3] < height * .16]
        if len(skips) == 1:
            self.click_node(skips[0])
            time.sleep(.5)

    def main_ready(self):
        return self.has(desc='首页') and self.has(text='发现')

    def main_page(self):
        self.dismiss_ads()
        self.return_to(self.main_ready, '未返回小红书主界面', limit=6)

    def launch(self):
        self._hot_query = None
        self.start()
        self.main_page()
        def ready():
            self.dismiss_ads()
            return self.main_ready()
        self.wait_for(ready, '小红书首页未加载', timeout=30)

    def search_ready(self):
        return any(n.get('class') == 'android.widget.EditText' for n in self.nodes())

    def results_ready(self):
        return self.has(text='全部') and self.has(text='综合') and not self.search_ready()

    def search_header(self, query):
        height = self.screen_size()[1]
        return [n for n in self.nodes(text=query) if self.bounds(n)[3] < height * .14]

    def open_search(self):
        for _ in range(6):
            self.dismiss_ads()
            if self.search_ready():
                return
            if self.main_ready():
                self.click(desc='搜索')
            elif self.results_ready():
                # 点实际搜索词回到编辑页，不按固定次数返回到发现首页。
                height = self.screen_size()[1]
                titles = [n for n in self.nodes() if n.get('class') == 'android.widget.TextView'
                          and n.get('clickable') == 'true' and n.get('text') not in ('搜索', '')
                          and self.bounds(n)[3] < height * .14]
                if len(titles) != 1:
                    raise RuntimeError('小红书搜索结果顶部词条不唯一')
                self.click_node(titles[0])
            else:
                self.back()
            time.sleep(.5)
        self.wait_for(self.search_ready, '小红书搜索编辑页未打开')

    def set_query(self):
        self.open_search()
        self.d(packageName=self.PACKAGE, className='android.widget.EditText').set_text(self.QUERY)
        self.invalidate()

    def submit_query(self):
        # 新版无障碍文本为“搜索, 穿搭图片”，并非输入失败。
        self.wait_for(lambda: any(n.get('class') == 'android.widget.EditText'
                                  and n.get('text', '').removeprefix('搜索, ') == self.QUERY
                                  for n in self.nodes()), '搜索框中未确认穿搭图片')
        buttons = [n for n in self.nodes(text='搜索') if self.bounds(n)[3] < self.screen_size()[1]*.14]
        if len(buttons) != 1:
            raise RuntimeError('小红书搜索提交入口不唯一')
        self.click_node(buttons[0])
        self.wait_for(lambda: self.results_ready() and bool(self.search_header(self.QUERY)),
                      '小红书搜索结果未加载', timeout=25)

    def return_results(self):
        self.return_to(self.results_ready, '未返回小红书搜索结果页', limit=4)

    def return_search(self):
        self._hot_query = None
        self.open_search()
        self.d(packageName=self.PACKAGE, className='android.widget.EditText').set_text('')
        self.invalidate()
        self.wait_for(lambda: any(self.has(text=label) for label in
                                 ('搜索发现', '小红书热榜', '猜你想搜')),
                      '清空搜索词后搜索发现区域未显示')

    def first_hot(self):
        self.return_search()
        header = next((label for label in ('搜索发现', '小红书热榜', '猜你想搜')
                       if self.has(text=label)), None)
        if header is None:
            raise RuntimeError('当前小红书没有可核验的搜索发现入口')
        top = self.bounds(self.node(text=header))[3]
        width, height = self.screen_size()
        rows = [n for n in self.nodes() if n.get('class') == 'android.widget.TextView'
                and len(n.get('text', '').strip()) >= 2
                and not n.get('text', '').strip().isdigit()
                and top < self.bounds(n)[1] < height * .85
                and self.bounds(n)[0] < width * .5
                and self.bounds(n)[2] < width * .65]
        if not rows:
            raise RuntimeError('搜索发现区域没有可核验的第一条条目')
        first = min(rows, key=lambda n: (self.bounds(n)[1], self.bounds(n)[0]))
        query = first.get('text')
        self.click_node(first)
        self.wait_for(lambda: self.results_ready() and bool(self.search_header(query)),
                      '点击搜索发现首条后结果未加载', timeout=25)
        self._hot_query = query
        if header == '猜你想搜':
            reason = '本版本搜索发现显示“猜你想搜”，浏览当前第一条建议“{}”，替代旧热搜入口'.format(query)
            self.adapt(reason)
            logging.warning('ADAPTED：%s', reason)

    def browse_hot(self):
        if not self._hot_query or not self.results_ready() or not self.search_header(self._hot_query):
            raise RuntimeError('尚未进入当前搜索发现条目的结果页，停止浏览')
        for _ in range(2):
            self.browse(3, 3)

    def repeat_search(self):
        for _ in range(3):
            self.set_query()
            self.submit_query()
            self.open_search()
        self.set_query()

    def first_note(self):
        self.require(text=self.QUERY)
        width, height = self.screen_size()
        cards = [n for n in self.nodes() if n.get('class') == 'android.widget.LinearLayout'
                 and n.get('clickable') == 'true' and self.bounds(n)[0] < width*.5
                 and width*.35 < self.bounds(n)[2]-self.bounds(n)[0] < width*.55
                 and self.bounds(n)[3]-self.bounds(n)[1] > height*.15
                 and height*.2 < self.bounds(n)[1] < height*.8
                 and any(c.get('text') for c in n.iter('node'))]
        if not cards:
            raise RuntimeError('搜索结果没有可核对的首条笔记')
        self.click_node(min(cards, key=lambda n: (self.bounds(n)[1], self.bounds(n)[0])))
        self.wait_for(lambda: self.has(desc='评论框'), '首条笔记详情未打开')

    def note_pictures(self):
        self.require(desc='评论框')
        # 详情浏览后先回到图片区域，以图片语义节点进入大图。
        for _ in range(4):
            images = self.nodes(desc='图片,第', prefix=True)
            if images:
                break
            self.swipe(y1=.32, y2=.78)
        if not images:
            raise RuntimeError('笔记没有可定位的图片')
        self.click_node(images[0])
        # 新版大图覆盖层保留详情旧树；用截图的黑色上下留白确认已进入查看器。
        self.wait_for(self.picture_viewer_ready, '笔记大图未打开')
        for x1, x2 in ((.8, .2), (.2, .8)):
            for _ in range(3):
                self.swipe(x1, .45, x2, .45)
                time.sleep(2)

    def picture_viewer_ready(self):
        shot = self.d.screenshot(display_id=0).convert('RGB')
        width, height = shot.size
        samples = [shot.getpixel((round(width*x), round(height*y)))
                   for x in (.1, .3, .5, .7, .9) for y in (.15, .18, .90, .93)]
        if all(max(pixel) < 25 for pixel in samples):
            return True
        # 长图可能没有留白；截图确认详情的固定评论框、关注和搜索均已隐藏。
        return not any(self.visible(label, True) for label in ('说点什么', '关注', '搜索'))

    def browse_results(self):
        self.wait_for(self.results_ready, '浏览前不在搜索结果页')
        for _ in range(2):
            self.browse(3, 3)

    def steps(self):
        return [
            ('启动小红书', self.launch, 2),
            ('点击右上角搜索', self.open_search, 1),
            ('搜索穿搭图片，返回上一级，重复操作3次', self.repeat_search, 2),
            ('搜索穿搭图片', self.submit_query, 1),
            ('点击左上角第一条消息', self.first_note, 1),
            ('上滑1次，下滑1次浏览笔记详情', lambda: self.browse(1, 1), 0),
            ('点击图片看大图，左滑3次，右滑3次', self.note_pictures, 0),
            ('返回搜索结果页面', self.return_results, 1),
            ('上滑3次，下滑3次浏览搜索结果，重复操作2次', self.browse_results, 0),
            ('返回搜索页面', self.return_search, 1),
            ('点击搜索发现下的第一条热搜', self.first_hot, 1),
            ('上滑3次，下滑3次浏览热搜，重复操作2次', self.browse_hot, 0),
            ('返回小红书主界面', self.main_page, 1),
            ('滑动返回Home页', self.home, 1),
        ]
