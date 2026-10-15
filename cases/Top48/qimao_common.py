"""七猫免费小说动态性能用例的页面操作。"""
import logging
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class QimaoDynamicCase(DynamicAppCase):
    PACKAGE = 'com.kmxs.reader'

    def point(self, x, y):
        self.foreground()
        # 七猫 8.8 的底栏会过滤普通短点击；450ms 可稳定触发且不会弹出长按菜单。
        self.d.long_click(round(x), round(y), duration=.45)

    def swipe(self, x1=.5, y1=.78, x2=.5, y2=.32, duration=400):
        self.foreground()
        width, height = self.d.window_size()
        result = self.d.shell('input swipe {} {} {} {} {}'.format(
            round(width*x1), round(height*y1), round(width*x2), round(height*y2), duration))
        if result.exit_code:
            raise RuntimeError('七猫滑动失败：' + result.output)

    def back(self):
        self.foreground()
        for rid in ('top_back_bg', 'read_title_left_arrow', 'back_click_area'):
            controls = self.nodes(rid=rid)
            if controls:
                left, top, right, bottom = self.bounds(controls[0])
                self.d.click((left + right) // 2, (top + bottom) // 2)
                time.sleep(.8)
                return
        result = self.d.shell('input keyevent 4')
        if result.exit_code:
            raise RuntimeError('七猫返回失败：' + result.output)
        time.sleep(.8)

    def dismiss_popups(self):
        for rid in ('iv_close', 'close_red_packet'):
            controls = self.nodes(rid=rid)
            if controls:
                self.click_node(controls[0])
                time.sleep(.8)

    def home_activity(self):
        try:
            return self.current_app()['activity'].endswith('HomeActivity')
        except RuntimeError:
            return False

    def home_shell_ready(self):
        return self.home_activity() and all(
            self.has(text=name, rid='km_ui_navigation_tab_text')
            for name in ('书架', '书城', '分类', '我的'))

    def container_for_text(self, name):
        candidates = [node for node in self.nodes()
                      if node.get('clickable') == 'true'
                      and any(child.get('text') == name for child in node.iter('node'))]
        if candidates:
            return min(candidates, key=lambda node: (
                (self.bounds(node)[2] - self.bounds(node)[0])
                * (self.bounds(node)[3] - self.bounds(node)[1])))
        return self.node(text=name)

    def semantic_click(self, name):
        self.click_node(self.container_for_text(name))

    def book_city_ready(self):
        return self.home_shell_ready() and self.has(rid='cover_view')

    def main_page(self):
        try:
            self.return_to(self.home_shell_ready, '未返回七猫主界面', limit=5)
        except RuntimeError:
            # 阅读器部分版本吞掉系统返回键，显式回到同应用首页作为兼容后备。
            self.d.app_start(self.PACKAGE, '.home.ui.HomeActivity')
            self.wait_for(self.home_shell_ready, '七猫主界面未加载', timeout=20)
        self.dismiss_popups()
        if self.has(text='书城', rid='km_ui_navigation_tab_text'):
            self.semantic_click('书城')
            time.sleep(2)

    def launch(self):
        self.start()
        # app_start 可能恢复上次的阅读器/搜索页，先尝试回到应用首页。
        if not self.home_shell_ready():
            self.main_page()
        self.wait_for(self.home_shell_ready, '七猫主界面未加载', timeout=30)
        self.dismiss_popups()
        self.main_page()

    def bookshelf(self):
        self.dismiss_popups()
        self.semantic_click('书架')
        time.sleep(3)

    def reading_ready(self):
        current = self.current_app()
        return current['package'] == self.PACKAGE and not current['activity'].endswith('HomeActivity')

    def open_kuangbiao(self):
        all_nodes = self.nodes()
        titles = [node for node in all_nodes
                  if '狂飙' in node.get('text', '')]
        if not titles:
            titles = [node for node in all_nodes
                      if any(key in node.get('resource-id', '')
                             for key in ('book_name', 'book_title', 'tv_book_name'))]
        if not titles:
            logging.warning('书架中没有“狂飙”或其他可读书籍，按用例约定跳过阅读')
            self._reading_skipped = True
            return
        target = titles[0]
        containers = [node for node in all_nodes
                      if node.get('clickable') == 'true' and target in list(node.iter('node'))]
        if containers:
            target = min(containers, key=lambda node: (
                self.bounds(node)[2] - self.bounds(node)[0])
                * (self.bounds(node)[3] - self.bounds(node)[1]))
        left, top, right, bottom = self.bounds(target)
        self.transition(lambda: self.d.click((left + right) // 2, (top + bottom) // 2),
                        self.reading_ready,
                        '七猫书籍未打开')
        guide = self.nodes(rid='read_guide_layout')
        if guide:
            left, top, right, bottom = self.bounds(guide[0])
            self.d.click((left + right) // 2, (top + bottom) // 2)
            time.sleep(1)
        if any(node.get('text', '').startswith('左滑开始阅读') for node in self.nodes()):
            width, height = self.d.window_size()
            self.d.swipe(round(width * .82), round(height * .50),
                         round(width * .18), round(height * .50), duration=.35)
            time.sleep(2)

    def turn_pages(self):
        if getattr(self, '_reading_skipped', False):
            return
        width, height = self.d.window_size()
        for _ in range(5):
            self.d.click(round(width * .82), round(height * .50))
            time.sleep(1)
        for _ in range(5):
            self.d.click(round(width * .18), round(height * .50))
            time.sleep(1)

    def channel(self, name):
        if not self.has(text=name, rid='title_tv'):
            logging.warning('七猫当前版本没有“%s”频道，跳过切换', name)
            return
        self.semantic_click(name)
        time.sleep(3)

    def category(self):
        self.semantic_click('分类')
        time.sleep(3)

    def modern_romance(self):
        if self.has(text='现代言情'):
            self.semantic_click('现代言情')
            time.sleep(2)
        else:
            logging.warning('七猫当前分类页没有“现代言情”，跳过该筛选')

    def highest_rating(self):
        label = '最高评分' if self.has(text='最高评分') else '好评榜'
        if self.has(text=label):
            self.semantic_click(label)
            time.sleep(2)
        else:
            logging.warning('七猫当前页面没有评分排序，跳过该筛选')

    def open_search(self):
        self.main_page()
        # 书城热搜框中部会直接打开推荐书；借用书架页固定的放大镜入口进入同一搜索页。
        self.bookshelf()
        controls = self.nodes(rid='tb_nav_search')
        if not controls:
            raise RuntimeError('七猫搜索框不可用')
        left, top, right, bottom = self.bounds(controls[0])
        self.d.click((left + right) // 2, (top + bottom) // 2)
        self.wait_for(lambda: bool(self.d(className='android.widget.EditText').count),
                      '七猫搜索页未打开')

    def search_changsheng(self):
        edit = self.d(className='android.widget.EditText')
        edit.set_text('长生')
        if self.has(desc='搜索'):
            self.click(desc='搜索')
        elif self.has(text='搜索'):
            self.semantic_click('搜索')
        else:
            self.d.press('enter')
        self.wait_for(lambda: (self.has(desc='综合', prefix=True)
                               and any(node.get('content-desc', '').startswith('长生\n')
                                       for node in self.nodes())),
                      '七猫“长生”搜索结果未加载', timeout=20)

    def return_main(self):
        self.main_page()
