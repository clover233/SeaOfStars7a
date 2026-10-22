"""闲鱼搜索和分享商品；Excel 第 1965～1974 行。"""
import time

from Cases.Top48.shopping_common import VisualShoppingDynamicCase


class PerformanceDynamic_xianyu_0010(VisualShoppingDynamicCase):
    PACKAGE = 'com.taobao.idlefish'
    all_app_package_list = [PACKAGE]
    QUERY = '华为mate60'

    def point(self, x, y):
        # Flutter 搜索提交忽略同点长按注入；使用属性节点的实时边界短按。
        self.foreground()
        self.d.click(round(x), round(y))
        self.invalidate()

    def main_ready(self):
        return self.has(rid='search_bar_layout') and self.has(desc='已选中，首页')

    def main_page(self):
        self.return_to(self.main_ready, '未返回闲鱼首页', limit=6)

    def launch(self):
        self.start()
        def ready():
            if self.has(rid='splash_ad_close'):
                self.click(rid='splash_ad_close')
            return self.main_ready()
        self.wait_for(lambda: ready() or not self.has(rid='splash_ad_close'),
                      '闲鱼启动广告未结束', timeout=30)
        self.main_page()

    def search_ready(self):
        return any(n.get('class') == 'android.widget.EditText' for n in self.nodes())

    def open_search(self):
        self.main_page()
        self.transition(lambda: self.click(rid='search_bar_layout'), self.search_ready, '闲鱼搜索页未打开')

    def results_ready(self):
        return self.has(rid='keyword_text', text=self.QUERY) and self.has(text='综合')

    def search_phone(self):
        self.wait_for(self.search_ready, '搜索前未打开输入页')
        self.d(packageName=self.PACKAGE, className='android.widget.EditText').set_text(self.QUERY)
        self.click(desc='搜索')
        self.wait_for(self.results_ready, '华为mate60 搜索结果未加载', timeout=25)

    def first_product(self):
        self.wait_for(self.results_ready, '进入商品前不在搜索结果页')
        if self.has(rid='scroll_to_top'):
            self.click(rid='scroll_to_top')
        self.wait_for(lambda: bool(self.product_cards()), '闲鱼搜索结果没有可核验的商品卡片')
        cards = self.product_cards()
        self.click_node(min(cards, key=lambda n: (self.bounds(n)[1], self.bounds(n)[0])))
        self.wait_for(self.product_ready, '首个商品详情未打开')

    def product_cards(self):
        width, height = self.screen_size()
        # 同边界外层先被公共去重保留，clickable 可能是 false；价格子节点和卡片尺寸仍可定位。
        return [n for n in self.nodes() if n.get('class') == 'android.widget.FrameLayout'
                and any(c.get('text') == '¥' for c in n.iter('node'))
                and width*.3 < self.bounds(n)[2] - self.bounds(n)[0] < width*.55
                and self.bounds(n)[3] - self.bounds(n)[1] > height*.12
                and height*.18 < self.bounds(n)[1] < height*.85]

    def product_ready(self):
        return self.has(rid='share_appbar') and self.has(rid='detail_right_button')

    def share_product(self):
        self.wait_for(self.product_ready, '分享前不在商品详情页')
        self.click(rid='share_appbar', desc='分享按钮')
        self.wait_for(lambda: self.has(desc='复制链接') or self.has(text='复制链接'), '商品分享面板未打开')
        time.sleep(4)
        self.back()
        self.wait_for(self.product_ready, '取消分享后未返回商品详情')

    def steps(self):
        return [
            ('启动闲鱼', self.launch, 2),
            ('首页浏览，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击搜索框，进入搜索页面', self.open_search, 1),
            ('搜索华为mate60', self.search_phone, 2),
            ('搜索结果浏览，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击第一个商品，进入商品详情页', self.first_product, 2),
            ('商品详情页浏览，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击分享，等待4s后返回', self.share_product, 0),
            ('返回闲鱼主界面', self.main_page, 1),
            ('滑动返回Home页', self.home, 2),
        ]
