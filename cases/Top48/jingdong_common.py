"""京东当前版本的首页、商品、超市、秒送及直播操作。"""
import logging
import time

from Cases.Top48.shopping_common import ShoppingDynamicCase, StepUnavailable


class JingdongDynamicCase(ShoppingDynamicCase):
    PACKAGE = 'com.jingdong.app.mall'
    all_app_package_list = [PACKAGE]

    def main_ready(self):
        return self.activity_has('MainFrameActivity') and self.find_label('首页') is not None

    def bottom(self, label):
        height = self.d.window_size()[1]
        nodes = [n for n in self.nodes() if self.bounds(n)[1] > height*.85
                 and (n.get('text') == label or n.get('content-desc', '').startswith(label))]
        if not nodes:
            raise StepUnavailable('当前版本没有底栏入口：' + label)
        self.click_node(sorted(nodes, key=lambda n: n.get('clickable') != 'true')[0])

    def main_page(self):
        self.return_to(self.main_ready, '未返回京东主界面', limit=12)
        self.bottom('首页')
        time.sleep(1)
        # 底栏首页会恢复上次的“秒送”子页；还需选择顶部“首页”，否则
        # 搜索会进入外卖搜索，手机数码/京东超市等入口也不会出现。
        height = self.d.window_size()[1]
        headers = [n for n in self.nodes(text='首页') if self.bounds(n)[1] < height*.2]
        if headers and headers[0].get('selected') != 'true':
            self.click_node(headers[0])
            time.sleep(1)
        self.return_to(self.main_ready, '首页被活动页遮挡后未能返回', limit=4)
        self.dismiss_popup()

    def phone_channel(self):
        self.main_page()
        self.label('手机数码', '手机', optional=True)
        time.sleep(2)

    def category(self):
        self.main_page()
        # 新版分类入口在首页右上角，底栏已不再提供分类。
        self.label('分类', optional=True)
        self.wait_for(lambda: self.activity_has('NewCategoryActivity'), '京东分类未打开')

    def computer_category(self):
        node = self.find_label('电脑', '电脑办公', '电脑数码')
        if node is None:
            logging.warning('替代：分类页未暴露电脑控件，用搜索“电脑”展示电脑商品')
            self.main_page()
            self.open_search()
            self.query('电脑')
        else:
            self.click_node(node)
            time.sleep(1)

    def first_category(self):
        if self.activity_has('ProductListActivity'):
            self.first_product()
            return
        # 未暴露分类卡片时不给动态布局写死点击位置。
        node = self.find_label('笔记本', '笔记本电脑', '电脑整机')
        if node is None:
            raise StepUnavailable('当前分类页没有可定位的第一类商品')
        self.click_node(node)
        time.sleep(2)

    def open_search(self):
        if not self.activity_has('SearchActivity'):
            node = self.find_label('搜索框', prefix=True)
            if node is not None:
                self.click_node(node)
            else:
                # 首页顶部搜索框未单独暴露；已用主屏截图核对比例。
                self.pct(.45, .115)
            self.wait_for(lambda: self.activity_has('SearchActivity'), '京东搜索页未打开')
        node = self.find_label('搜索框', prefix=True)
        if node is not None:
            self.click_node(node)
        elif self.has(rid='com.jd.lib.omnichannelsearch.feature:id/o3'):
            self.click(rid='com.jd.lib.omnichannelsearch.feature:id/o3')
        else:
            editors = [n for n in self.nodes() if n.get('class') == 'android.widget.EditText']
            if not editors:
                raise RuntimeError('搜索页缺少可输入的搜索框')
            if editors[0].get('focused') != 'true':
                self.click_node(editors[0])
        time.sleep(.5)

    def input_query(self, text):
        self.foreground()
        self.d.send_keys(text, clear=True)

    def query(self, text):
        self.input_query(text)
        self.submit_search()

    def submit_search(self):
        self.label('搜索')
        time.sleep(1)
        self.check_access()
        self.wait_for(lambda: self.activity_has('ProductListActivity', 'SearchResult')
                      or self.find_label('综合排序', prefix=True) is not None,
                      '搜索结果未加载', timeout=20)

    def sales(self):
        self.label('销量', optional=True)

    def product_ready(self):
        return self.activity_has('ProductDetailActivity') and self.find_label('客服') is not None

    def first_product(self):
        width, height = self.d.window_size()
        # 搜索商品无稳定标题 ID。描述含价格的卡片是完整商品入口，过滤购物车
        # 小按钮和顶部店铺广告，取当前屏幕第一条商品。
        cards = [n for n in self.nodes()
                 if '元' in n.get('content-desc', '')
                 and self.bounds(n)[2]-self.bounds(n)[0] > width*.3
                 and self.bounds(n)[3]-self.bounds(n)[1] > height*.09
                 and self.bounds(n)[1] > height*.18]
        if not cards:
            raise RuntimeError('搜索列表未找到带价格的商品卡片')
        self.click_node(min(cards, key=lambda n: self.bounds(n)[1]))
        self.wait_for(self.product_ready, '商品详情未打开', timeout=20)

    def gallery(self):
        # 浏览详情后先回到商品顶部，避免点到详情中的推荐图片。
        node = self.find_label('商品')
        if node is not None:
            self.click_node(node)
            time.sleep(.7)
        for _ in range(5):
            if self.has(desc='商品图片', prefix=True):
                break
            self.swipe(y1=.32, y2=.78)
            time.sleep(.5)
        if self.find_label('图集') is not None:
            self.label('图集')
        self.click(desc='商品图片', prefix=True)
        self.wait_for(lambda: self.has(rid='pd_big_image_id'), '商品大图未打开')

    def browse_gallery(self):
        for left in (True, False):
            for _ in range(3):
                self.swipe(.8 if left else .2, .5, .2 if left else .8, .5)
                time.sleep(2)

    def return_product(self):
        self.return_to(self.product_ready, '未返回京东商品详情', limit=8)

    def reveal_reviews(self):
        self.reveal_label('大家评', '评价', '买家评价')

    def reviews_tab(self):
        self.label('大家评', '评价', '买家评价', optional=True)
        time.sleep(1)

    def all_reviews(self):
        self.label('全部评价', '查看全部评价', '买家评价', optional=True)
        self.wait_for(lambda: self.activity_has('Comment', 'Evaluate')
                      or self.find_label('全部', prefix=True) is not None,
                      '全部评价页未打开')

    def store(self):
        self.return_product()
        self.label('店铺', optional=True)
        self.wait_for(lambda: self.activity_has('Jshop', 'ShopActivity'), '店铺未打开')

    def service(self):
        self.return_product()
        self.label('客服', optional=True)
        self.wait_for(lambda: not self.product_ready(), '客服界面未打开')

    def buy(self):
        self.return_product()
        self.label('立即购买', optional=True)
        self.wait_for(lambda: self.checkout_ready() or self.find_label('确认') is not None,
                      '购买规格/订单确认页未打开')

    def confirm_specs(self):
        if self.checkout_ready():
            raise StepUnavailable('当前版本直接进入订单确认页，没有规格确认按钮')
        self.label('确认', optional=True)
        self.wait_for(self.checkout_ready, '规格确认后未进入订单确认页')

    def checkout_ready(self):
        return self.activity_has('FillOrder', 'Settlement')

    def supermarket(self):
        self.main_page()
        self.label('京东超市', optional=True)
        self.wait_for(lambda: self.find_label('粮油调味') is not None,
                      '京东超市分类未加载', timeout=25)

    def grocery(self):
        self.label('粮油调味', optional=True)
        time.sleep(2)
        if self.find_label('点击收起') is not None:
            self.label('点击收起')
        if not self.activity_has('BabelActivity'):
            logging.warning('替代：超市粮油频道未打开，搜索“食用油”浏览粮油商品')
            self.main_page()
            self.open_search()
            self.query('食用油')

    def add_grocery(self):
        if self.activity_has('ProductListActivity'):
            self.first_product()
        else:
            self.open_first_grocery_product()
        self.label('加入购物车', optional=True)
        time.sleep(1)
        # 只确认加入购物车的规格弹窗，绝不点击支付/提交订单。
        node = self.find_label('确定', '确认')
        if node is not None:
            self.click_node(node)
            time.sleep(1)

    def open_first_grocery_product(self):
        width, height = self.d.window_size()
        images = [n for n in self.nodes() if n.get('class') == 'android.widget.Image'
                  and len(n.get('content-desc', '')) > 5
                  and self.bounds(n)[0] > width*.18
                  and width*.15 < self.bounds(n)[2]-self.bounds(n)[0] < width*.35
                  and height*.25 < self.bounds(n)[1] < height*.8]
        if not images:
            raise StepUnavailable('粮油调味页没有可定位的商品')
        self.click_node(min(images, key=lambda n: self.bounds(n)[1]))
        self.wait_for(self.product_ready, '粮油商品详情未打开')

    def cart(self):
        self.main_page()
        self.bottom('购物车')
        time.sleep(2)

    def checkout(self):
        self.label('去结算', '结算', prefix=True, optional=True)
        self.wait_for(self.checkout_ready, '购物车未进入结算页', timeout=20)

    def grocery_checkout(self):
        if self.product_ready():
            self.label('购物车', prefix=True, optional=True)
            time.sleep(1)
        self.checkout()

    def new_address(self):
        self.label('新建地址', '新增收货地址', '添加收货地址', optional=True)
        time.sleep(1)

    def instant_ready(self):
        return self.has(rid='hourly_go_mvp_address_text_view')

    def instant(self):
        self.main_page()
        node = self.find_label('秒送')
        if node is None:
            # 本版本首页“超市秒送”/“外卖”也可进入秒送聚合页。
            logging.warning('替代：顶部秒送入口不可定位，使用首页“外卖”入口')
            self.label('外卖', '超市秒送', optional=True)
        else:
            self.click_node(node)
        self.wait_for(lambda: self.instant_ready() or self.activity_has('HourlyGo'),
                      '秒送页未打开', timeout=20)

    def food(self):
        if self.activity_has('HourlyGoMulTabActivity'):
            return
        self.label('外卖', optional=True)
        self.wait_for(lambda: self.activity_has('HourlyGoMulTabActivity'), '外卖页未打开')
        self.wait_for(lambda: self.has(rid='hourly_go_new_search_bar'), '外卖列表未加载')

    def first_merchant(self):
        width, height = self.d.window_size()
        cards = [n for n in self.nodes() if '起送' in n.get('content-desc', '')
                 and self.bounds(n)[2]-self.bounds(n)[0] > width*.7
                 and self.bounds(n)[3]-self.bounds(n)[1] > height*.07]
        if not cards:
            raise StepUnavailable('当前地区没有可定位的商家')
        self.click_node(min(cards, key=lambda n: self.bounds(n)[1]))
        self.wait_for(lambda: self.activity_has('HourlyGoLayerActivity', 'MantoLightActivity'),
                      '商家页面未打开', timeout=25)
        time.sleep(2)

    def food_add(self):
        # 当前外卖店铺为小程序，树只有 WebView。动态菜单高度、起送金额不固定，
        # 无可靠控件时跳过加购及其依赖步骤，不猜测“+”坐标。
        self._food_cart_initially_empty = self.find_label('购物车空空如也', '购物车为空') is not None
        self.label('加入购物车', optional=True)
        time.sleep(1)

    def food_cart(self):
        self.label('购物车按钮', '购物车', prefix=True, optional=True)

    def clear_food_cart(self):
        # 此步骤仅在本用例成功加购后执行，并且仅针对该商家购物袋。
        if not getattr(self, '_food_cart_initially_empty', False):
            raise StepUnavailable('无法确认商家购物袋原本为空，保留已有商品')
        if self.checkout_ready():
            self.back()
        self.food_cart()
        self.label('清空购物车', '清空', optional=True)
        self.label('确定', '确认', optional=True)

    def food_search(self):
        self.click(rid='hourly_go_new_search_bar')
        time.sleep(1)
        self.wait_for(lambda: self.find_label('搜索框', prefix=True) is not None
                      or bool(self.d(className='android.widget.EditText').exists),
                      '外卖搜索框未打开')

    def search_medicine(self):
        self.input_query('药店')

    def live_list(self):
        self.main_page()
        self.bottom('逛')
        self.wait_for(lambda: self.find_label('直播') is not None, '逛页面未加载')
        self.label('直播', optional=True)
        self.wait_for(lambda: self.find_label('直播间名称：', prefix=True) is not None,
                      '直播列表没有可观看的直播间', timeout=20)

    def first_live(self):
        self.label('直播间名称：', prefix=True, optional=True)
        self.wait_for(lambda: self.activity_has('VideoLiveRoomActivity'), '直播间未打开')

    def live_input(self):
        self.label('说点什么', '说点什么...', '聊点什么', prefix=True, optional=True)
        self.wait_for(lambda: bool(self.d(className='android.widget.EditText').exists),
                      '直播输入框未打开')

    def live_send(self):
        self.input_query('不错')
        self.label('发送', optional=True)

    def live_bag(self):
        self.label('购物袋', prefix=True, optional=True)
        self.wait_for(lambda: self.find_label('看讲解') is not None,
                      '直播购物袋未打开')

    def mine(self):
        self.main_page()
        self.bottom('我的')
        self.wait_for(lambda: self.find_label('待收货') is not None,
                      '我的页面订单入口未加载')

    def orders(self):
        self.label('全部订单', '我的订单', '全部', optional=True)
        self.wait_for(lambda: not self.activity_has('MainFrameActivity')
                      and self.find_label('待收货') is not None, '全部订单页未打开')
