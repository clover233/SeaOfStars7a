"""拼多多动态性能用例的页面操作。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PinduoduoDynamicCase(DynamicAppCase):
    PACKAGE = 'com.xunmeng.pinduoduo'

    def point(self, x, y):
        self.foreground()
        result = self.d.shell(
            'input -d 0 swipe {0} {1} {0} {1} 200'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('拼多多点击失败：' + result.output)

    def home_ready(self):
        return self.has(desc='首页') and self.has(desc='搜索')

    def launch(self):
        self.start()
        self.main_page()

    def search_page_ready(self):
        return self.has(text='搜索') and bool(self.nodes()) and bool(
            self.d(className='android.widget.EditText').count)

    def open_search(self):
        width, height = self.screen_size()
        candidates = [node for node in self.nodes()
                      if node.get('clickable') == 'true'
                      and self.bounds(node)[1] < height * .14
                      and self.bounds(node)[2] - self.bounds(node)[0] > width * .65
                      and any(child.get('content-desc') == '搜索'
                              for child in node.iter('node'))]
        if not candidates:
            candidates = self.nodes(desc='搜索')
        target = min(candidates, key=lambda node: self.bounds(node)[1])
        self.transition(lambda: self.click_node(target), self.search_page_ready,
                        '拼多多搜索页未打开')

    def results_ready(self):
        return self.has(text='综合') and self.has(text='销量') and self.has(rid='tv_title')

    def search_phone(self):
        edit = self.d(className='android.widget.EditText')
        if not edit.exists:
            raise RuntimeError('拼多多搜索页没有输入框')
        edit.set_text('华为手机')
        buttons = [node for node in self.nodes(text='搜索')
                   if node.get('clickable') == 'true']
        if not buttons:
            raise RuntimeError('拼多多搜索按钮不可用')
        self.transition(lambda: self.click_node(buttons[-1]), self.results_ready,
                        '华为手机搜索结果未加载')

    def product_ready(self):
        return self.has(desc='店铺') and self.has(desc='客服')

    def first_product(self):
        cards = [node for node in self.nodes()
                 if node.get('clickable') == 'true'
                 and any(child.get('resource-id', '').endswith('/tv_title')
                         for child in node.iter('node'))]
        if not cards:
            titles = self.nodes(rid='tv_title')
            if not titles:
                raise RuntimeError('拼多多搜索结果没有商品')
            target = titles[0]
        else:
            target = min(cards, key=lambda node: self.bounds(node)[1])
        self.transition(lambda: self.click_node(target), self.product_ready,
                        '拼多多第一件商品未打开')

    def store_ready(self):
        return (self.has(desc='店铺图标') or self.has(text='全部商品')
                or self.brand_store_ready())

    def brand_store_ready(self):
        return (self.current_app()['activity'].endswith('.NewPageActivity')
                and self.has(text='商品由第三方商家提供')
                and self.has(text='该品牌累计热销', prefix=True))

    def store(self):
        self.transition(lambda: self.click(desc='店铺'), self.store_ready,
                        '拼多多店铺页未打开')
        if self.brand_store_ready():
            self._adaptation = '该商品的店铺入口进入品牌馆，保留品牌商品列表浏览'

    def main_page(self):
        for _ in range(7):
            current = self.current_app()
            self.foreground()
            if self.home_ready():
                return
            if current['activity'].endswith('.LoginActivity'):
                # 首次启动的登录营销页有明确“跳过”；Back 会退出应用。
                skips = self.nodes(text='跳过')
                if skips:
                    self.click_node(skips[0])
                self.wait_for(lambda: self.home_ready() or
                              not self.current_app()['activity'].endswith('.LoginActivity'),
                              '未退出拼多多登录引导', timeout=25)
            elif current['activity'].endswith('.HomeActivity'):
                # HomeActivity 先恢复，再异步挂载搜索栏和底部导航。
                self.wait_for(self.home_ready, '拼多多首页未加载', timeout=30)
                return
            else:
                self.back()
            time.sleep(.8)
        raise RuntimeError('未返回拼多多主界面')

    def home(self):
        self.foreground()
        # 从手势条内部起滑；屏幕最底部会被本机系统输入区过滤。
        self.swipe(.5, .985, .5, .62, 300)
        time.sleep(.8)
        if 'launcher' not in self.current_app()['activity'].lower():
            self.d.shell('input -d 0 keyevent 3')
            self._adaptation = '系统未响应上滑手势，使用主屏 Home 键返回桌面'
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(),
                      '未返回桌面')
