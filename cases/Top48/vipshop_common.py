"""唯品会当前版本的搜索、商品和分类；定位来自 weditor 与实机控件树。"""
import re
import time

from Cases.Top48.shopping_common import StepUnavailable
from Cases.Top48.weibo_vip_common import WeiboVipDynamicCase


class VipshopDynamicCase(WeiboVipDynamicCase):
    PACKAGE = 'com.achievo.vipshop'
    all_app_package_list = [PACKAGE]

    def main_ready(self):
        return self.activity_has('LodingActivity', 'MainActivity') and self.has(rid='tv_title', text='首页')

    def main_page(self):
        self.return_to(self.main_ready, '未返回唯品会主界面', limit=12)
        self.bottom('首页')
        self.wait_for(lambda: self.has(rid='index_searchbar_layout'), '唯品会首页未加载')
        self.dismiss_popup()

    def launch(self):
        self._added_title = None
        self._product_title = None
        self.start()
        self.main_page()

    def bottom(self, label):
        height = self.d.window_size()[1]
        nodes = [n for n in self.nodes(rid='tv_title', text=label) if self.bounds(n)[1] > height*.88]
        if not nodes:
            raise StepUnavailable('当前页面没有唯品会底栏：' + label)
        self.click_node(nodes[0])

    def await_page(self, ready, message, optional=False):
        def check():
            if self.activity_has('Login', 'login', 'Passport'):
                self.back()
                raise StepUnavailable('唯品会要求登录：' + message)
            return ready()
        try:
            self.wait_for(check, message, timeout=18)
        except RuntimeError:
            if optional:
                raise StepUnavailable(message)
            raise

    def search_tissue(self):
        self.main_page()
        # 占位词会轮播，点击稳定的整个搜索栏，避开右侧拍照按钮。
        self.transition(lambda: self.click(rid='index_searchbar_layout'),
                        lambda: self.has(rid='search_text_view'), '搜索输入框未打开')
        self.d(resourceId=self.PACKAGE+':id/search_text_view').set_text('清风卫生纸')
        self.wait_for(lambda: self.has(rid='search_text_view', text='清风卫生纸'), '搜索词输入失败')
        self.click(rid='tv_search')
        self.await_page(lambda: self.activity_has('TabSearchProductListActivity'), '清风卫生纸搜索结果未打开')
        self.await_page(lambda: bool(self.product_cards()), '没有可定位的清风商品')

    def product_cards(self):
        width, height = self.d.window_size()
        return sorted([n for n in self.nodes() if n.get('content-desc', '').startswith('清风 ')
                       and re.search(r'\d.*元$', n.get('content-desc', ''))
                       and self.bounds(n)[2]-self.bounds(n)[0] > width*.3
                       and height*.15 < self.bounds(n)[1] < height*.8],
                      key=lambda n: (self.bounds(n)[1], self.bounds(n)[0]))

    def product_ready(self):
        return self.activity_has('ProductDetailActivity') and self.has(desc='加入购物车按钮')

    def first_product(self):
        cards = self.product_cards()
        if not cards:
            raise StepUnavailable('当前搜索结果没有清风商品')
        # 点击卡片的商品标题，避开图片上的“直播中”入口。
        titles = [n for n in cards[0].iter('node') if '清风' in n.get('text', '') and len(n.get('text', '')) > 12]
        if not titles:
            raise StepUnavailable('第一条商品未暴露可核对的标题')
        self._product_title = titles[0].get('text').strip()
        self.transition(lambda: self.click_node(titles[0]), self.product_ready, '商品详情未打开')

    def return_product(self):
        self.return_to(self.product_ready, '未返回商品详情', limit=8)

    def browse_shop(self):
        node = None
        for _ in range(7):
            node = self.find_label('进店逛逛', '进入店铺', '进店', '店铺')
            if node is not None:
                break
            self.swipe()
            time.sleep(.7)
        if node is None:
            raise StepUnavailable('商品没有可定位的店铺入口')
        before = self.current_app()['activity']
        self.click_node(node)
        self.await_page(lambda: self.current_app()['activity'] != before or self.find_label('店铺首页', '全部商品') is not None,
                        '店铺页面未打开', optional=True)
        self.browse(3, 3)

    def cart_ready(self):
        return self.activity_has('ShopCart', 'ShoppingCart', 'CartActivity', 'ShopBag') or self.find_label('购物袋', '购物车') is not None and self.find_label('结算', prefix=True) is not None

    def open_cart(self):
        if self.cart_ready():
            return
        node = self.find_label('购物车', '购物袋', prefix=True)
        if node is not None:
            self.click_node(node)
        else:
            self.main_page()
            self.bottom('购物车')
        self.await_page(self.cart_ready, '购物车未打开', optional=True)

    def return_cart(self):
        self.return_to(self.cart_ready, '未返回购物车', limit=6)

    @staticmethod
    def normalize_title(text):
        return re.sub(r'\s+', '', text)

    def added_rows(self):
        title = self.normalize_title(self._product_title or '')
        if not title:
            return []
        return [n for n in self.nodes() if self.normalize_title(n.get('text', '')) == title]

    def add_to_cart(self):
        if not self._product_title:
            raise StepUnavailable('未确认本次商品身份')
        badges = self.nodes(rid='bag_Num')
        if any(n.get('text', '').isdigit() and int(n.get('text')) > 0 for n in badges):
            raise StepUnavailable('原购物车已有商品，保留原数量；跳过加购及后续结算、删除')
        # 加购前检查原购物车，只清理本次新增商品。
        self.open_cart()
        self.await_page(lambda: self.find_label('结算', prefix=True) is not None,
                        '购物车未暴露可核实的商品和结算控件，跳过加购', optional=True)
        existing = self.added_rows()
        self._cart_had_products = any('清风' in n.get('text', '') for n in self.nodes())
        self.return_product()
        if existing:
            raise StepUnavailable('该商品原已在购物车，保留原数量')
        self.label('加入购物车按钮', '加入购物车', '加入购物袋')
        time.sleep(1)
        self.await_page(lambda: self.product_ready() or self.find_label('确定', '确认') is not None,
                        '加购或规格选择未打开', optional=True)
        confirm = self.find_label('确定', '确认')
        if confirm is not None:
            self.click_node(confirm)
        # 不重复点击加购；以购物车中的完整商品标题核实新增结果。
        self.open_cart()
        self.await_page(lambda: bool(self.added_rows()), '未在购物车确认新增商品', optional=True)
        self._added_title = self._product_title

    def checkout(self):
        if not self._added_title or not self.cart_ready():
            raise StepUnavailable('没有本次新增商品或不在购物车页')
        if self._cart_had_products:
            raise StepUnavailable('原购物车含其他清风商品，跳过混合结算')
        self.label('结算', prefix=True, optional=True)
        self.await_page(lambda: self.find_label('确认订单', '提交订单', '订单确认') is not None,
                        '未进入订单确认页', optional=True)
        # 表格仅要求点击结算，停留确认页，不点击提交订单/付款。

    def hold_added_product(self):
        if not self._added_title or self._added_title != self._product_title:
            raise StepUnavailable('本次用例没有已核实的新增商品')
        self.return_cart()
        rows = self.added_rows()
        if len(rows) != 1:
            raise StepUnavailable('无法唯一定位本次新增商品')
        l, t, r, b = self.bounds(rows[0])
        x, y = round((l+r)/2), round((t+b)/2)
        self.foreground()
        result = self.d.shell('input -d 0 swipe {0} {1} {0} {1} 900'.format(x, y))
        if result.exit_code:
            raise RuntimeError('长按商品失败：' + result.output)
        self.await_page(lambda: self.find_label('删除') is not None, '当前版本不支持长按删除', optional=True)

    def delete_added_product(self):
        if not self._added_title or self._added_title != self._product_title:
            raise StepUnavailable('没有本次新增商品可删除')
        self.label('删除')
        time.sleep(.5)
        node = self.find_label('确认删除', '确定删除')
        if node is not None:
            self.click_node(node)
        self.await_page(lambda: not self.added_rows(), '删除后仍存在本次新增商品')
        self._added_title = None

    def fling_up(self, count=3):
        for _ in range(count):
            self.swipe(.5, .8, .5, .25, duration=120)
            time.sleep(2)

    def sports(self):
        # 推荐页抛滑后导航通常吸顶；先按控件寻找，必要时回顶部。
        for _ in range(7):
            node = self.find_label('运动')
            if node is not None:
                self.click_node(node)
                self.await_page(lambda: self.has(rid='tab_text', text='运动'), '运动频道未打开', optional=True)
                return
            self.swipe(y1=.3, y2=.8, duration=150)
        raise StepUnavailable('当前版本没有运动频道')

    def category(self):
        self.bottom('分类')
        self.await_page(lambda: self.activity_has('Category') or self.find_label('推荐分类', '为你推荐') is not None,
                        '分类页面未打开', optional=True)

    def browse(self, up=5, down=5, pause=2):
        if self.activity_has('Category'):
            # 分类页左侧为分类菜单，滑右侧商品区。
            for y1, y2, count in ((.78, .32, up), (.32, .78, down)):
                for _ in range(count):
                    self.swipe(.7, y1, .7, y2)
                    time.sleep(pause)
        else:
            super().browse(up, down, pause)
