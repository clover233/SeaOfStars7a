"""华为商城：2026-10-14 通过 weditor dump、控件树及截图核对。"""
import logging
import re
import time

from Cases.Top48.shopping_common import ShoppingDynamicCase, StepUnavailable


class HwVmallDynamicCase(ShoppingDynamicCase):
    PACKAGE = 'com.vmall.client'
    all_app_package_list = [PACKAGE]

    def main_ready(self):
        return self.has(rid='home_tab')

    def product_ready(self):
        return (self.activity_has('RnProductDetailActivity', 'ProductDetailActivity')
                and self.has(desc='客服'))

    def main_page(self):
        self.return_to(self.main_ready, '未返回华为商城主界面', limit=12)
        self.click(rid='home_tab')
        time.sleep(1)
        self.dismiss_popup()

    def open_banner(self, number):
        self.main_page()
        # 首页搜索框和轮播图合并为一个无标识 ViewGroup。比例由实机截图核对。
        for _ in range(number - 1):
            self.swipe(.82, .38, .18, .38)
            time.sleep(.5)
        self.pct(.5, .38)
        time.sleep(2)
        if self.main_ready():
            raise StepUnavailable('首页轮播图未提供可进入的活动，跳过该轮播图')

    def open_search(self):
        self.main_page()
        self.pct(.45, .15)
        self.wait_for(lambda: self.has(rid='vui_searchbar_input'), '华为商城搜索框未打开')

    def search_p60(self):
        self.open_search()
        self.d(resourceId='vui_searchbar_input').set_text('p60')
        self.label('搜索')
        self.wait_for(lambda: bool(self.product_cards()), 'p60 搜索商品未加载', timeout=25)

    def product_cards(self):
        return [n for n in self.nodes()
                if re.fullmatch(r'\d+-searchProduct', n.get('resource-id', ''))]

    def first_product(self):
        cards = self.product_cards()
        if not cards:
            raise RuntimeError('搜索结果中没有可浏览的商品')
        self.click_node(min(cards, key=lambda n: self.bounds(n)[1]))
        self.wait_for(self.product_ready, '商品详情未打开')

    def category(self):
        self.main_page()
        self.click(rid='category_tab')
        time.sleep(2)

    def category_product(self):
        node = self.find_label('华为手机', '手机')
        if node is not None:
            self.click_node(node)
            time.sleep(2)
        cards = [n for n in self.nodes()
                 if re.fullmatch(r'\d+-searchProduct', n.get('resource-id', ''))]
        if not cards:
            logging.warning('替代：分类无可定位商品卡片，通过搜索“p60”进入商品详情')
            self.search_p60()
        self.first_product()

    def reveal_reviews(self):
        self.click_node(self.reveal_label('查看全部评价'))
        self.wait_for(lambda: self.activity_has('ProductCommentActivity'), '商品评价未打开')

    def all_reviews(self):
        if not self.activity_has('ProductCommentActivity'):
            self.reveal_reviews()
        if self.find_label('全部') is not None:
            self.label('全部')

    def service(self):
        self.label('客服', optional=True)
        self.wait_for(lambda: not self.product_ready(), '客服界面未打开')

    def return_product(self):
        self.return_to(self.product_ready, '未返回商品详情', limit=6)
