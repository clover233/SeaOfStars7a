"""大众点评美食搜索、首店和评论浏览。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_dazhongdianping_0010(DynamicAppCase):
    PACKAGE = 'com.dianping.v1'
    all_app_package_list = [PACKAGE]

    def on_home(self):
        return self.has(rid='home_tab_home_container')

    def foreground(self):
        current = self.current_app()
        if current['package'] != self.PACKAGE:
            raise RuntimeError('前台不是大众点评：{}'.format(current))
        if 'yoda' in current['activity'].lower():
            raise RuntimeError('大众点评出现验证码，请在设备上手动完成验证后重跑用例')

    def launch(self):
        self.start()
        self.return_to(self.on_home, '未回到大众点评首页')
        for _ in range(6):
            if self.has(rid='tv_category_name', text='美食'):
                return
            self.swipe(y1=.32, y2=.78)
            time.sleep(1)
        self.require(rid='tv_category_name', text='美食')

    def food(self):
        self.open_control(lambda: self.has(desc='searchbox_view'), '未进入美食频道',
                          rid='tv_category_name', text='美食')

    def search_food(self):
        self.open_control(lambda: self.has(rid='search_keyword_edit'), '未进入美食搜索页',
                          desc='searchbox_view')
        self.d(resourceId=self.PACKAGE + ':id/search_keyword_edit').set_text('烧烤')
        self.wait_for(lambda: self.has(rid='search_keyword_edit', text='烧烤'), '烧烤关键词未输入')

    def search(self):
        self.click(rid='search_button')
        self.wait_for(lambda: self.has(rid='search_keyword', text='烧烤') and
                      self.has(desc='SearchPagerListView-全部'), '未加载烧烤商户列表')

    def shop(self):
        self.foreground()
        if self.has(desc='floatingWindow'):
            # 该浮层的“顶部”图标未暴露独立节点；截图核对后按浮层内部比例点选。
            left, top, right, bottom = self.bounds(self.node(desc='floatingWindow'))
            self.point((left + right) / 2, top + (bottom - top) * .8)
            time.sleep(1.5)
        # 筛选栏可能覆盖首条卡片，继续下滑至列表顶部的商户行完整露出。
        for _ in range(6):
            cards = [n for n in self.nodes(desc='gridView_item_wrapper')
                     if any('/人' in c.get('text', '') for c in n.iter('node'))]
            filters = self.nodes(desc='filter_item')
            if cards:
                first = min(cards, key=lambda n: self.bounds(n)[1])
                prices = [c for c in first.iter('node') if '/人' in c.get('text', '')]
                cutoff = max((self.bounds(n)[3] for n in filters), default=0)
                if prices and self.bounds(prices[0])[1] > cutoff:
                    break
            self.swipe(y1=.32, y2=.78)
            time.sleep(1)
        self.transition(self.first_shop,
                        lambda: 'PexusPoiActivity' in self.current_app()['activity'],
                        '未进入首家商铺详情')
        self.wait_for(lambda: self.has(desc='顶部查看全部'), '商铺评价内容未加载', timeout=30)

    def review_area(self):
        self.reveal('未找到商铺评价入口', text='评价')
        self.click(text='评价')
        self.wait_for(lambda: self.has(desc='顶部查看全部'), '评价区未加载')

    def browse_shop(self):
        # 店铺页顶部是可下拉展开的相册，向下浏览的起点放在内容区中部，
        # 避免末次下滑落在封面上而进入相册。
        for _ in range(5):
            self.swipe(y1=.85, y2=.45)
            time.sleep(2)
        for _ in range(5):
            self.swipe(y1=.52, y2=.85)
            time.sleep(2)
        if self.has(text='传照片') and self.has(text='传视频'):
            raise RuntimeError('商铺浏览意外进入相册，未完成店铺页面浏览')

    def all_reviews(self):
        self.click(desc='顶部查看全部')
        self.wait_for(lambda: self.has(desc='全部') and self.has(desc='最新'),
                      '全部评价未加载；如出现验证码请先在设备上完成验证')

    def back_food(self):
        # 评论 -> 商铺 -> 结果 -> 搜索输入页 -> 美食；按页面标志返回。
        self.return_to(lambda: self.has(desc='searchbox_view') and not self.has(rid='search_keyword'),
                       '未返回美食频道', limit=7)

    def app_home(self):
        self.return_to(self.on_home, '未返回大众点评主界面')

    def steps(self):
        return [
            ('启动大众点评', self.launch, 3),
            ('点击美食', self.food, 1),
            ('点击搜索框，输入烧烤', self.search_food, 1),
            ('点击搜索', self.search, 1),
            ('滑动浏览烧烤搜索结果，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击进入第一家商铺', self.shop, 1),
            ('滑动浏览商铺，上滑5次，下滑5次', self.browse_shop, 0),
            ('点击评价', self.review_area, 1),
            ('点击查看全部', self.all_reviews, 1),
            ('滑动浏览评论，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('返回美食页面', self.back_food, 1),
            ('滑动美食页面，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('返回大众点评主界面', self.app_home, 1),
            ('滑动返回Home页', self.home, 1),
        ]
