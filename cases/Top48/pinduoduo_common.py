"""拼多多动态性能用例的页面操作。"""
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
        if not self.home_ready():
            self.main_page()
        self.wait_for(self.home_ready, '拼多多首页未加载', timeout=25)

    def search_page_ready(self):
        return self.has(text='搜索') and bool(self.nodes()) and bool(
            self.d(className='android.widget.EditText').count)

    def open_search(self):
        width, height = self.d.window_size()
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
        return self.has(desc='店铺图标') or self.has(text='全部商品')

    def store(self):
        self.transition(lambda: self.click(desc='店铺'), self.store_ready,
                        '拼多多店铺页未打开')

    def main_page(self):
        self.return_to(self.home_ready, '未返回拼多多主界面', limit=7)
