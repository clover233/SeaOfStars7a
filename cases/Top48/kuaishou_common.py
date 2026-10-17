"""快手 14.8.40 主屏定位；按 Excel 947～969 行逐步采集性能。"""
import logging
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class KuaishouDynamicCase(DynamicAppCase):
    PACKAGE = 'com.smile.gifmaker'
    all_app_package_list = [PACKAGE]

    def point(self, x, y):
        # 主屏 input 注入；180ms 可触发点击，避免 350ms 拉起评论快捷表情。
        self.foreground()
        result = self.d.shell('input -d 0 swipe {0} {1} {0} {1} 180'.format(
            round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('快手点击失败：' + result.output)

    def bottom_selected(self, name):
        return any(n.get('selected') == 'true' for n in self.nodes(desc=name)
                   if self.bounds(n)[1] > self.d.window_size()[1] * .88)

    def menu_ready(self):
        # 关闭抽屉后快手仍把移出屏幕的旧节点标为 visible；不能仅判断存在。
        width = self.d.window_size()[0]
        return any(self.bounds(n)[2] >= width * .78
                   for n in self.nodes(desc='sideBarScroller'))

    def main_ready(self):
        self.dismiss_widget_prompt()
        return (not self.menu_ready() and self.has(desc='首页')
                and self.has(desc='精选') and self.has(desc='侧边栏'))

    def dismiss_widget_prompt(self):
        labels = ' '.join(n.get('text', '') + n.get('content-desc', '') for n in self.nodes())
        if '快手商城' in labels and '小组件' in labels and '去添加' in labels:
            self.back()
            return True
        return False

    def switch_bottom(self, name):
        def ready():
            self.dismiss_widget_prompt()
            return self.bottom_selected(name)
        def select():
            self.foreground()
            left, top, right, bottom = self.bounds(self.node(desc=name))
            # 当前版本底栏中心点击会被忽略；实机核对下半部短按可切换。
            # 仍以可见节点为锚点，并用 selected 状态确认导航结果。
            result = self.d.shell('input mouse -d 0 tap {} {}'.format(
                round((left + right) / 2), round(top + (bottom - top) * .7)))
            if result.exit_code:
                raise RuntimeError('快手底栏点击失败：' + result.output)
        self.transition(select,
                        ready, '未切换到快手' + name)

    def return_home(self):
        # 直播间先关闭，避免系统返回触发挽留推荐；其余页面有限次返回。
        if self.has(rid='live_close'):
            self.click(rid='live_close')
            time.sleep(1)
        self.return_to(self.main_ready, '未返回快手主界面', limit=8)
        self.switch_bottom('首页')

    def launch(self):
        self.start()
        self.return_home()

    def video_ready(self):
        return self.bottom_selected('精选') and self.has(rid='comment_button')

    def featured_videos(self):
        self.switch_bottom('精选')
        self.wait_for(self.video_ready, '精选视频未加载', timeout=20)
        for _ in range(3):
            self.swipe(duration=1000)
            self.wait_for(self.video_ready, '切换后精选视频控件未加载')
            time.sleep(10)

    def comments_ready(self):
        return self.has(rid='tabs_panel_close')

    def open_comments(self):
        self.require(rid='comment_button')
        self.transition(lambda: self.click(rid='comment_button'),
                        self.comments_ready, '评论面板未打开')

    def browse_comments(self):
        self.require(rid='tabs_panel_close')
        # 手势限制在面板内部，避免在上半屏切换背景视频。
        for start, end in ((.86, .55), (.55, .86)):
            for _ in range(2):
                self.swipe(y1=start, y2=end)
                time.sleep(2)
        self.click(rid='tabs_panel_close')
        self.wait_for(lambda: not self.comments_ready() and self.video_ready(),
                      '关闭评论后未返回精选视频')

    def activate_video_action(self, rid, inactive, active):
        self.wait_for(self.video_ready, '视频交互前精选页未就绪')
        node = self.node(rid=rid)
        desc = node.get('content-desc', '')
        if desc.startswith(active):
            logging.info('%s 已处于目标状态，保留现有状态', rid)
            return
        if not desc.startswith(inactive):
            raise RuntimeError('无法识别视频交互状态：' + desc)
        # 点赞/收藏只点击一次，不能用导航重试逻辑误取消。
        self.click_node(node)
        self.wait_for(lambda: self.has(rid=rid, desc=active, prefix=True),
                      rid + '点击后未生效')

    def like(self):
        self.activate_video_action('like_button', '未点赞', '已点赞')

    def collect(self):
        self.activate_video_action('collect_button', '未收藏', '已收藏')

    def search_ready(self):
        return self.has(rid='editor') and self.has(text='搜索发现')

    def open_search(self):
        self.return_home()
        self.transition(lambda: self.click(desc='查找'), self.search_ready, '搜索页未打开')

    def search_phone(self):
        self.require(rid='editor')
        self.d(resourceId=self.PACKAGE + ':id/editor').set_text('华为手机')
        self.click(rid='right_tv', text='搜索')
        self.wait_for(lambda: self.has(rid='search_result_text', text='华为手机'),
                      '未进入华为手机搜索结果', timeout=20)

    def browse_results(self):
        self.require(rid='search_result_text', text='华为手机')
        self.browse(3, 3)

    def return_search(self):
        self.return_to(self.search_ready, '未返回搜索界面')

    def rank_ready(self):
        return any(n.get('selected') == 'true' for n in self.nodes(text='直播榜'))

    def live_rank(self):
        self.require(text='直播榜')
        self.transition(lambda: self.click(text='直播榜'), self.rank_ready, '直播榜未打开')
        self.wait_for(lambda: self.has(rid='left_text', text='1'), '直播榜未出现第一名')

    def live_ready(self):
        return self.has(rid='live_close') and self.has(rid='live_name_text')

    def first_live(self):
        if not self.rank_ready():
            raise RuntimeError('进入直播前不在直播榜')
        self.click(rid='left_text', text='1')
        self.wait_for(self.live_ready, '第一名直播间未打开', timeout=25)

    def next_live(self):
        self.wait_for(self.live_ready, '切换直播前未进入直播间')
        previous = self.node(rid='live_name_text').get('text')
        self.swipe()
        self.wait_for(lambda: self.live_ready()
                      and self.node(rid='live_name_text').get('text') != previous,
                      '上滑后未切换到下一直播间', timeout=25)

    def open_menu(self):
        self.require(desc='侧边栏')
        self.transition(lambda: self.click(desc='侧边栏'),
                        self.menu_ready, '侧边栏未完全展开')

    def shop_ready(self):
        return self.has(text='我的订单') and self.has(text='退款售后')

    def open_shop(self):
        self.wait_for(self.menu_ready, '进入小店前侧边栏未完全展开')
        self.transition(lambda: self.click(desc='快手小店'), self.shop_ready,
                        '快手小店未打开')
        self.wait_for(lambda: bool(self.product_titles()), '小店推荐商品未加载', timeout=25)

    def product_titles(self):
        # 推荐商品名称含零宽字符；匹配当前可见卡片，不写死商品名称。
        height = self.d.window_size()[1]
        return sorted([n for n in self.nodes() if '\u200b' in n.get('text', '')
                       and height * .2 < self.bounds(n)[1] < height * .87],
                      key=lambda n: (self.bounds(n)[1], self.bounds(n)[0]))

    def browse_shop(self):
        if not self.shop_ready():
            raise RuntimeError('浏览前未进入快手小店')
        self.browse(3, 3)

    def product_ready(self):
        return self.has(text='进店') and self.has(text='客服') and self.has(text='购物车')

    def first_product(self):
        self.wait_for(lambda: bool(self.product_titles()), '未找到小店第一件可见商品')
        self.click_node(self.product_titles()[0])
        self.wait_for(self.product_ready, '第一件商品详情未打开', timeout=25)

    def cart_count(self):
        # 购物车文字的同级节点为角标；用于验证加购，避免把关闭面板当成成功。
        for node in self.nodes():
            children = list(node)
            if any(c.get('text') == '购物车' for c in children):
                values = [c.get('text', '') for c in node.iter('node')
                          if c.get('text', '').isdigit()]
                if values:
                    return int(values[0])
        return 0

    def add_to_cart(self):
        if not self.product_ready():
            raise RuntimeError('加购前未进入商品详情')
        previous = self.cart_count()
        buttons = self.nodes(text='加入购物袋') or self.nodes(text='加入购物车')
        if buttons:
            self.click_node(buttons[0])
        else:
            # 当前详情的加购图标没有 id/描述。截图与 hierarchy 核对后，
            # 从底栏无文本可点击节点中选择“购物车”和购买按钮之间的独立图标。
            width, height = self.d.window_size()
            icons = [n for n in self.nodes() if n.get('clickable') == 'true'
                     and not any(c.get('text') for c in n.iter('node'))
                     and .30 < self.bounds(n)[0] / width < .45
                     and .44 < self.bounds(n)[2] / width < .52
                     and self.bounds(n)[1] > height * .90]
            if len(icons) != 1:
                logging.warning('跳过加入购物袋：当前商品没有可确认的加购入口')
                return
            self.click_node(icons[0])
        self.wait_for(lambda: self.has(desc='merchant_sku_panel_count_input')
                      or (self.product_ready() and self.cart_count() > previous),
                      '点击加购后规格面板未加载', timeout=20)
        if self.has(desc='merchant_sku_panel_count_input'):
            headers = self.nodes(text='包装规格')
            counters = self.nodes(desc='merchant_sku_panel_count_input')
            options = []
            if headers:
                top = self.bounds(headers[0])[3]
                bottom = self.bounds(counters[0])[1]
                options = sorted([
                    n for n in self.nodes() if n.get('clickable') == 'true'
                    and n.get('enabled') == 'true'
                    and top <= self.bounds(n)[1] < self.bounds(n)[3] <= bottom
                    and any('¥' in c.get('text', '') for c in n.iter('node'))],
                    key=lambda n: (self.bounds(n)[1], self.bounds(n)[0]))
            if not options:
                logging.warning('跳过加入购物袋：首件商品需要未适配的规格选择')
                self.back()
                return
            # 首个低价规格容易达到限购数；按用户要求优先选下面一个规格。
            # 若面板仍未关闭且角标未增加，再尝试其余规格，不重复提交同一规格。
            ordered = options[1:] + options[:1]
            for option in ordered:
                label = next((c.get('text') for c in option.iter('node')
                              if c.get('text') and '¥' not in c.get('text')
                              and '购买' not in c.get('text')), '规格')
                logging.info('尝试加购规格：%s', label)
                def selected():
                    return any(label in n.get('text', '')
                               for n in self.nodes(text='已选：', prefix=True))
                if not selected():
                    self.click_node(option)
                self.wait_for(selected, '商品规格选择未生效')
                self.click(text='加入购物车')
                deadline = time.monotonic() + 5
                while time.monotonic() < deadline:
                    if self.product_ready() and self.cart_count() > previous:
                        logging.info('加购成功，购物车角标 %s -> %s', previous, self.cart_count())
                        return
                    time.sleep(.4)
                if not self.has(desc='merchant_sku_panel_count_input'):
                    raise RuntimeError('加购后未出现可确认的购物车数量变化')
                logging.warning('当前规格未完成加购（可能已达限购数量），尝试下一个规格')
            logging.warning('跳过加入购物袋：可见规格均未完成加购，请检查限购提示')
            self.back()
            return
        self.wait_for(lambda: self.product_ready() and self.cart_count() > previous,
                      '加购后购物车角标未增加', timeout=15)
