"""抖音动态性能用例的语义定位、版本兼容和比例手势。"""
import logging
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class DouyinDynamicCase(DynamicAppCase):
    PACKAGE = 'com.ss.android.ugc.aweme'
    QUERY = '华为p70'
    AUTHOR = '华为终端'
    COMMENT = '我是评论ABC'

    def point(self, x, y):
        """抖音底栏会忽略驻留 250ms 的伪点击，使用 uiautomator2 普通点击。"""
        self.foreground()
        self.d.click(round(x), round(y))

    def contains_nodes(self, text=None, desc=None, rid=None):
        def normalized(value):
            return value.replace('\u200b', '').replace('\ufeff', '')

        result = []
        for node in self.nodes(rid=rid):
            if text is not None and normalized(text) not in normalized(node.get('text', '')):
                continue
            if desc is not None and normalized(desc) not in normalized(node.get('content-desc', '')):
                continue
            result.append(node)
        return result

    def first_contains(self, text=None, desc=None, rid=None):
        nodes = self.contains_nodes(text=text, desc=desc, rid=rid)
        if not nodes:
            return None
        return sorted(nodes, key=lambda node: (self.bounds(node)[1], self.bounds(node)[0]))[0]

    def first_any(self, *queries):
        for query in queries:
            node = self.first_contains(**query)
            if node is not None:
                return node
        return None

    def click_contains(self, text=None, desc=None, rid=None):
        node = self.first_contains(text=text, desc=desc, rid=rid)
        if node is None:
            raise RuntimeError('未找到包含指定内容的控件：text={!r}, desc={!r}, rid={!r}'.format(
                text, desc, rid))
        self.click_node(node)

    def skip(self, message):
        logging.warning('SKIP：%s', message)
        return False

    def bottom_tab(self, name):
        nodes = self.nodes(text=name, rid='0py')
        if not nodes:
            nodes = self.contains_nodes(desc=name + '，按钮')
        if not nodes:
            raise RuntimeError('抖音底栏没有“{}”入口'.format(name))
        self.click_node(nodes[0])
        time.sleep(1)

    def top_tabs(self, name):
        return [node for node in self.nodes()
                if name in node.get('content-desc', '')
                and '按钮' in node.get('content-desc', '')
                and self.bounds(node)[1] < self.d.window_size()[1] * .14]

    def top_selected(self, name):
        return any('已选中' in node.get('content-desc', '') for node in self.top_tabs(name))

    def reveal_top_tab(self, name):
        directions = ((.83, .25), (.25, .83), (.25, .83), (.83, .25))
        for start, end in directions:
            if self.top_tabs(name):
                return True
            self.swipe(start, .08, end, .08, 350)
            time.sleep(.6)
        return bool(self.top_tabs(name))

    def switch_top(self, name, substitutes=()):
        if name == '推荐':
            shortcut = self.first_contains(desc='返回推荐页')
            if shortcut is not None:
                self.click_node(shortcut)
                time.sleep(2)
                return self.wait_feed(5)
        target = name
        if not self.reveal_top_tab(target):
            for candidate in substitutes:
                if self.reveal_top_tab(candidate):
                    logging.info('替代：当前抖音版本无“%s”，使用“%s”', name, candidate)
                    target = candidate
                    break
            else:
                return self.skip('当前抖音版本无“{}”频道'.format(name))
        if not self.top_selected(target):
            self.click_node(self.top_tabs(target)[0])
            time.sleep(2)
        return True

    def feed_ready(self):
        nodes = self.nodes()
        selected = any('已选中' in node.get('content-desc', '')
                       and '推荐' in node.get('content-desc', '')
                       for node in nodes)
        video_controls = any(
            node.get('resource-id', '').endswith((':id/user_avatar', ':id/comment_container'))
            or '评论' in node.get('content-desc', '')
            for node in nodes)
        return selected and video_controls

    def dismiss_known_popup(self):
        nodes = self.nodes()

        def first_node(predicate):
            return next((node for node in nodes if predicate(node)), None)

        node = first_node(lambda item: item.get('text') == '取消'
                          and item.get('resource-id', '').endswith(':id/b4y'))
        if node is not None:
            self.click_node(node)
            time.sleep(1)
            return True
        node = first_node(lambda item: item.get('text') == '不感兴趣')
        if node is not None:
            self.click_node(node)
            time.sleep(1)
            return True
        if first_node(lambda item: item.get('resource-id', '').endswith(':id/iv_close')) is not None:
            # “完善账号安全设置”在此版本只响应系统返回键。
            self.back()
            return True
        node = first_node(lambda item: item.get('resource-id', '').endswith(':id/c=-'))
        if node is not None:
            self.click_node(node)
            time.sleep(1)
            return True
        close_nodes = [node for node in nodes if '关闭' in node.get('content-desc', '')]
        close_nodes = [node for node in close_nodes
                       if (self.bounds(node)[2] - self.bounds(node)[0]) < self.d.window_size()[0] * .25]
        if close_nodes:
            self.click_node(min(close_nodes, key=lambda node: self.bounds(node)[1]))
            time.sleep(1)
            return True
        return False

    def return_feed(self):
        for _ in range(12):
            if self.feed_ready():
                return
            # 聊天、商品、作者等二级页可能仍把底部导航保留在无障碍树中；
            # 优先处理当前页真正可见的返回按钮，避免点击被上层页面拦截。
            if any(node.get('content-desc') == '返回' for node in self.nodes()):
                self.back()
                continue
            self.dismiss_known_popup()
            home_nodes = self.nodes(text='首页', rid='0py')
            if home_nodes:
                self.click_node(home_nodes[0])
                time.sleep(2)
                if self.feed_ready():
                    return
                shortcut = self.first_contains(desc='返回推荐页')
                if shortcut is not None:
                    self.click_node(shortcut)
                    time.sleep(2)
                    if self.feed_ready():
                        return
                recommend = self.top_tabs('推荐')
                if recommend:
                    self.click_node(recommend[0])
                    time.sleep(2)
                    if self.feed_ready():
                        return
                continue
            self.back()
        self.wait_for(self.feed_ready, '未返回抖音推荐页', timeout=5)

    def wait_feed(self, timeout=8):
        try:
            self.wait_for(self.feed_ready, '抖音推荐页未加载', timeout=timeout)
            return True
        except RuntimeError:
            return False

    def launch(self):
        self.start()
        try:
            # 冷/热启动后视频画面先出现，Accessibility 树通常稍晚才挂载底栏。
            self.wait_for(lambda: bool(self.nodes(text='首页', rid='0py')),
                          '抖音底栏尚未加载', timeout=12)
        except RuntimeError:
            # 可能恢复在二级页，交给统一返回逻辑逐层回退。
            pass
        self.return_feed()

    # 推荐视频和评论
    def browse_videos(self, count=3):
        for _ in range(count):
            self.swipe(.5, .78, .5, .26, 350)
            time.sleep(2)

    def open_comments(self):
        node = self.first_any(
            {'rid': 'comment_container'}, {'rid': 'e3z'}, {'rid': 'e9l'}, {'desc': '评论'})
        if node is None:
            raise RuntimeError('当前视频没有评论入口')

        def ready():
            nodes = self.nodes()
            return (any(item.get('resource-id', '').endswith(':id/e19') for item in nodes)
                    and any('评论' in item.get('text', '') for item in nodes))

        self.transition(lambda: self.click_node(node), ready, '评论面板未打开')

    def browse_comments(self):
        self.swipe(.5, .78, .5, .48, 350)
        time.sleep(1)

    def focus_comment(self):
        self.require(rid='e19')
        self.click(rid='e19')

    def type_comment(self):
        self.require(rid='e19')
        self.d(resourceId=self.PACKAGE + ':id/e19').set_text(self.COMMENT)
        self.wait_for(lambda: self.has(text='发送', rid='e6h'), '评论发送按钮未出现')

    def send_comment(self):
        self.click(text='发送', rid='e6h')
        time.sleep(2)

    # 直播和小黄车
    def open_live_hall(self):
        self.return_feed()
        if not self.switch_top('直播'):
            return False
        self.wait_for(lambda: self.top_selected('直播') and self.has(rid='qbc'),
                      '直播频道未加载')
        return True

    def enter_live_room(self):
        if not self.has(rid='qbc'):
            self.live_room_open = False
            return self.skip('直播频道没有可进入的直播间')
        self.click(rid='qbc')
        time.sleep(2)
        if self.has(rid='c=-'):
            self.click(rid='c=-')
            time.sleep(1)
            self.click(rid='qbc')
        self.wait_for(lambda: self.has(rid='h7l') or bool(self.contains_nodes(desc='关闭 按钮')),
                      '直播间未打开')
        self.live_room_open = True
        return True

    def browse_live_rooms(self, count=3):
        if not self.has(rid='h7l'):
            return self.skip('未进入直播间，跳过直播间切换')
        self.browse(count, 0, pause=2)
        return True

    def open_live_cart(self):
        if not getattr(self, 'live_room_open', False):
            self.live_cart_open = False
            return self.skip('未进入直播间，跳过小黄车入口')
        words = ('小黄车', '购物车', '购物袋', '商品')
        candidates = []
        for node in self.nodes():
            value = node.get('text', '') + node.get('content-desc', '')
            if any(word in value for word in words):
                left, top, right, bottom = self.bounds(node)
                if top > self.d.window_size()[1] * .2 and right - left < self.d.window_size()[0] * .7:
                    candidates.append(node)
        if not candidates:
            self.live_cart_open = False
            return self.skip('当前直播间未展示小黄车，跳过商品面板')
        self.click_node(sorted(candidates, key=lambda node: self.bounds(node)[1], reverse=True)[0])
        time.sleep(2)
        self.live_cart_open = True
        return True

    def browse_live_cart(self):
        if not getattr(self, 'live_cart_open', False):
            return self.skip('小黄车未打开，跳过商品列表滑动')
        self.browse(5, 5, pause=1)
        return True

    # 商城
    def open_mall(self):
        self.return_feed()
        if not self.switch_top('商城'):
            return False
        self.wait_for(lambda: self.top_selected('商城') and bool(self.contains_nodes(desc='购物车')),
                      '抖音商城未加载')
        return True

    def open_mall_search(self):
        node = self.first_contains(desc='搜索 按钮')
        if node is None:
            raise RuntimeError('商城搜索框不可用')
        self.transition(lambda: self.click_node(node), lambda: self.has(rid='yy6'),
                        '商城搜索页未打开')

    def search_product(self):
        self.d(resourceId=self.PACKAGE + ':id/yy6').set_text(self.QUERY)
        self.transition(
            lambda: self.click(rid='yzs'),
            lambda: self.has(text='全部', rid='x7p') and bool(self.contains_nodes(desc='华为')),
            '华为 P70 搜索结果未加载',
        )

    def open_first_product(self):
        if not self.contains_nodes(desc='华为'):
            self.product_open = False
            return self.skip('商城搜索结果没有华为商品')
        # 搜索结果商品图是自绘列表；在已核验结果页内按屏幕比例点击首项图片区。
        self.transition(lambda: self.pct(.18, .27), self.product_ready,
                        '首个商品详情未打开')
        self.product_open = True
        return True

    def product_ready(self):
        return bool(self.contains_nodes(desc='购物车')) and bool(self.contains_nodes(desc='进店'))

    def add_to_cart(self):
        if not self.product_ready():
            return self.skip('未在商品详情页，跳过加入购物车')
        add = self.first_any({'text': '加入购物车'}, {'desc': '加入购物车'})
        if add is not None:
            self.click_node(add)
        else:
            # 新版将加购图标绘制在详情页底部中间，控件树不暴露文字。
            logging.info('替代：按商品详情底栏比例点击加购图标')
            self.pct(.40, .95)
        time.sleep(2)
        for label in ('确定', '加入购物车'):
            node = self.first_any({'text': label}, {'desc': label})
            if node is not None:
                self.click_node(node)
                time.sleep(2)
                break
        self.added_to_cart = bool(self.contains_nodes(text='已加入')
                                  or self.contains_nodes(desc='已加入'))
        if not self.added_to_cart:
            logging.warning('SKIP：当前商品要求未暴露的规格选择，未确认新增购物车条目')
        return self.added_to_cart

    def open_cart(self):
        cart = self.first_contains(desc='购物车')
        if cart is None:
            return self.skip('当前页面没有购物车入口')
        self.click_node(cart)
        time.sleep(3)
        self.cart_open = bool(self.contains_nodes(text='管理') or self.contains_nodes(desc='管理'))
        if not self.cart_open:
            logging.warning('SKIP：购物车页面未公开稳定管理控件')
        return self.cart_open

    def product_action(self, label):
        self.return_to(self.product_ready, '未返回商品详情页')
        node = self.first_any({'text': label}, {'desc': label})
        if node is None:
            return self.skip('商品详情没有“{}”入口'.format(label))
        self.click_node(node)
        time.sleep(2)
        return True

    def cart_manage(self):
        if not getattr(self, 'added_to_cart', False):
            return self.skip('本轮未确认新增购物车条目，不管理既有商品')
        if not getattr(self, 'cart_open', False) and not self.open_cart():
            return False
        manage = self.first_any({'text': '管理'}, {'desc': '管理'})
        if manage is None:
            return self.skip('购物车没有管理按钮')
        self.click_node(manage)
        time.sleep(1)
        self.cart_managing = True
        return True

    def cart_delete(self):
        if not getattr(self, 'cart_managing', False):
            return self.skip('未进入购物车管理状态，不删除既有商品')
        delete = self.first_any({'text': '删除'}, {'desc': '删除'})
        if delete is None:
            return self.skip('购物车没有删除按钮')
        self.click_node(delete)
        time.sleep(1)
        confirm = self.first_any({'text': '删除'}, {'text': '确定'})
        if confirm is not None:
            self.click_node(confirm)
        return True

    # 作者主页和搜索
    def open_current_author(self):
        self.return_feed()
        avatars = self.nodes(rid='user_avatar')
        if not avatars:
            self.author_profile_available = False
            return self.skip('当前视频未暴露作者头像')
        self.click_node(avatars[0])
        time.sleep(3)
        self.author_profile_available = self.profile_page()
        if not self.author_profile_available:
            return self.skip('作者主页未公开稳定的作品控件')
        return True

    def profile_page(self):
        return bool(self.contains_nodes(text='关注')) and (
            bool(self.contains_nodes(text='作品')) or bool(self.contains_nodes(desc='作品')))

    def open_me(self):
        self.bottom_tab('我')
        time.sleep(2)
        self.dismiss_known_popup()
        self.wait_for(lambda: bool(self.contains_nodes(text='我的钱包'))
                      and bool(self.contains_nodes(desc='收藏,按钮')),
                      '抖音个人页未加载')

    def open_following(self):
        self.open_me()
        nodes = self.nodes(text='关注')
        if not nodes:
            return self.skip('个人页没有关注入口')
        self.click_node(nodes[0])
        time.sleep(3)
        return True

    def open_followed_author(self):
        node = self.first_any({'text': self.AUTHOR}, {'desc': self.AUTHOR})
        if node is None:
            self.author_profile_available = False
            return self.skip('关注列表没有“{}”，保留关注列表浏览'.format(self.AUTHOR))
        self.click_node(node)
        time.sleep(3)
        self.author_profile_available = self.profile_page()
        if not self.author_profile_available:
            return self.skip('“{}”主页未公开稳定的作品控件'.format(self.AUTHOR))
        return True

    def profile_video_candidates(self):
        width, height = self.d.window_size()
        result = []
        for node in self.nodes():
            left, top, right, bottom = self.bounds(node)
            if (node.get('clickable') == 'true' and top > height * .42
                    and bottom < height * .94 and right - left < width * .55
                    and bottom - top > height * .08):
                result.append(node)
        return sorted(result, key=lambda node: (self.bounds(node)[1], self.bounds(node)[0]))

    def play_profile_video(self, index):
        if not getattr(self, 'author_profile_available', False):
            return self.skip('未进入作者主页，跳过第 {} 个作品'.format(index + 1))
        videos = self.profile_video_candidates()
        if len(videos) <= index:
            return self.skip('作者主页没有第 {} 个可播放作品'.format(index + 1))
        self.click_node(videos[index])
        time.sleep(15)
        return True

    def search_author(self):
        self.return_feed()
        search = self.first_contains(desc='搜索')
        if search is None:
            return self.skip('推荐页没有搜索入口')
        self.click_node(search)
        self.wait_for(lambda: any(node.get('class') == 'android.widget.EditText'
                                  for node in self.nodes()), '抖音搜索框未打开')
        editors = [node for node in self.nodes() if node.get('class') == 'android.widget.EditText']
        editor = editors[0]
        editor_id = editor.get('resource-id')
        if editor_id:
            self.d(resourceId=editor_id).set_text(self.AUTHOR)
        else:
            self.click_node(editor)
            self.d.send_keys(self.AUTHOR, clear=True)
        button = self.first_any({'text': '搜索'}, {'desc': '搜索'})
        if button is not None:
            self.click_node(button)
        time.sleep(4)
        user_tabs = self.nodes(text='用户', rid='android:id/text1')
        if not user_tabs:
            self.author_results_open = False
            return self.skip('搜索结果没有“用户”分类')
        self.transition(
            lambda: self.click_node(user_tabs[0]),
            lambda: bool(self.contains_nodes(desc='关注按钮')),
            '作者用户搜索结果未加载',
        )
        self.author_results_open = True
        return True

    def open_searched_author(self):
        if not getattr(self, 'author_results_open', False):
            self.author_profile_available = False
            return self.skip('未进入作者用户搜索结果')
        follow_nodes = (self.contains_nodes(desc='已关注按钮')
                        or self.contains_nodes(desc='关注按钮'))
        if not follow_nodes:
            self.author_profile_available = False
            return self.skip('用户搜索结果没有可打开的作者')
        first = min(follow_nodes, key=lambda node: self.bounds(node)[1])
        width, _ = self.d.window_size()
        _, top, _, bottom = self.bounds(first)
        # 用户卡片仅公开右侧关注按钮；按该按钮的纵向中心点击同卡片左侧作者区域。
        self.point(width * .25, (top + bottom) / 2)
        time.sleep(3)
        self.author_profile_available = self.profile_page()
        if not self.author_profile_available:
            return self.skip('搜索结果作者主页未公开稳定的作品控件')
        return True

    # 消息和创作
    def open_messages(self):
        self.return_feed()
        self.bottom_tab('消息')
        self.wait_for(lambda: self.has(text='消息', rid='tv_title') and self.has(rid='0b9'),
                      '抖音消息页未加载')

    def open_test_chat(self):
        self.open_messages()
        cards = [node for node in self.nodes(rid='0b9')
                 if any(child.get('text') == 'Test' for child in node.iter('node'))]
        if not cards:
            return self.skip('消息页没有 Test 会话')
        self.click_node(cards[0])
        self.wait_for(lambda: self.has(rid='msg_et'), 'Test 聊天页未打开')
        return True

    def send_chat_text(self, message='华为手机'):
        if not self.has(rid='msg_et'):
            return self.skip('未进入 Test 聊天页，跳过文字消息')
        self.d(resourceId=self.PACKAGE + ':id/msg_et').set_text(message)
        time.sleep(1)
        send = self.first_any({'text': '发送'}, {'desc': '发送'})
        if send is None:
            return self.skip('输入文字后没有发送按钮')
        self.click_node(send)
        time.sleep(1)
        return True

    def send_dynamic_emoji(self):
        if not self.has(rid='msg_et'):
            return self.skip('未进入 Test 聊天页，跳过动态表情')
        chip = self.first_contains(text='早上好')
        if chip is None:
            return self.skip('当前聊天页没有动态表情快捷项')
        logging.info('替代：发送当前版本提供的“早上好”动态表情快捷项')
        self.click_node(chip)
        time.sleep(1)
        return True

    def open_chat_media(self):
        if not self.has(rid='msg_et'):
            return self.skip('未进入 Test 聊天页，跳过聊天媒体面板')
        more = self.first_contains(desc='更多面板', rid='mxo')
        if more is not None:
            self.click_node(more)
            time.sleep(1)
        if not (self.contains_nodes(text='拍摄') or self.contains_nodes(text='相册')):
            self.chat_media_available = False
            return self.skip('当前抖音聊天“+”仅提供一起玩，没有拍摄或相册入口')
        self.chat_media_available = True
        return True

    def unavailable_chat_media(self, action):
        if not getattr(self, 'chat_media_available', False):
            return self.skip('当前版本聊天页无“{}”功能'.format(action))
        aliases = {
            '拍摄': ('拍摄',),
            '拍摄图片': ('拍照', '拍摄照片'),
            '发送图片': ('发送',),
            '拍摄视频': ('录像', '录制视频'),
            '发送视频': ('发送',),
            '相册': ('相册',),
            '发送相册图片': ('发送',),
        }
        labels = aliases.get(action)
        if not labels:
            return self.skip('“{}”页面是自绘控件，未找到稳定语义定位'.format(action))
        node = None
        for label in labels:
            node = self.first_any({'text': label}, {'desc': label})
            if node is not None:
                break
        if node is None:
            return self.skip('当前聊天媒体流程没有“{}”控件'.format(action))
        self.click_node(node)
        time.sleep(2)
        return True

    def open_create(self):
        self.return_feed()
        create = self.first_contains(desc='拍摄，按钮')
        if create is None:
            return self.skip('底栏没有创作入口')
        self.click_node(create)
        time.sleep(4)
        self.create_available = bool(self.contains_nodes(text='相册')
                                     or self.contains_nodes(text='照片'))
        if not self.create_available:
            logging.warning('SKIP：创作页未公开照片/相册控件')
        return self.create_available

    def back_in_create(self):
        if self.feed_ready():
            return self.skip('创作子页面未打开，无需返回')
        if self.current_app()['package'] != self.PACKAGE:
            return self.skip('当前不在抖音创作流程，跳过返回')
        self.back()
        return True

    def create_click(self, label):
        if not getattr(self, 'create_available', False):
            return self.skip('创作页不可用，跳过“{}”'.format(label))
        node = self.first_any({'text': label}, {'desc': label})
        if node is None:
            return self.skip('当前创作页没有“{}”'.format(label))
        self.click_node(node)
        time.sleep(2)
        return True

    def share_to_test(self):
        self.return_feed()
        share = self.nodes(rid='share_container') or self.nodes(rid='zzr')
        if not share:
            return self.skip('当前视频没有分享入口')
        self.click_node(share[0])
        time.sleep(2)
        target = self.first_any({'text': 'Test'}, {'desc': 'Test'})
        if target is None:
            self.share_target_selected = False
            return self.skip('分享面板没有 Test 联系人')
        self.click_node(target)
        time.sleep(1)
        self.share_target_selected = True
        return True

    def confirm_share(self):
        if not getattr(self, 'share_target_selected', False):
            return self.skip('未选择 Test 联系人，跳过分享发送')
        send = self.first_any({'text': '发送'}, {'desc': '发送'})
        if send is None:
            return self.skip('分享面板没有发送按钮')
        self.click_node(send)
        time.sleep(1)
        return True

    # 个人收藏/喜欢和钱包
    def open_profile_tab(self, name):
        self.open_me()
        tabs = [node for node in self.nodes()
                if name in (node.get('content-desc', '') + node.get('text', ''))
                and ('按钮' in node.get('content-desc', '') or node.get('resource-id') == 'android:id/text1')]
        if not tabs:
            return self.skip('个人页没有“{}”标签'.format(name))
        self.click_node(tabs[0])
        time.sleep(2)
        return True

    def open_first_profile_work(self, category):
        videos = self.profile_video_candidates()
        if not videos:
            return self.skip('“{}”页面没有可播放作品'.format(category))
        self.click_node(videos[0])
        time.sleep(2)
        return True

    def open_wallet(self):
        self.open_me()
        wallet = self.first_contains(text='我的钱包')
        if wallet is None:
            return self.skip('个人页没有“我的钱包”')
        self.click_node(wallet)
        time.sleep(3)
        return True

    # 长视频/经验/热点
    def cycle_channels(self):
        for _ in range(3):
            for name in ('关注', '团购', '推荐'):
                self.switch_top(name)

    # 团购
    def open_group_buy(self):
        self.return_feed()
        if not self.switch_top('团购'):
            return False
        time.sleep(2)
        for _ in range(3):
            if not self.dismiss_known_popup():
                break
        return True

    def open_food(self):
        node = self.first_any({'desc': '附近美食'}, {'text': '附近美食'})
        if node is None:
            self.food_open = False
            return self.skip('团购页没有附近美食入口')
        self.click_node(node)
        time.sleep(4)
        for _ in range(2):
            if not self.dismiss_known_popup():
                break
        self.food_open = True
        return True

    def open_first_merchant(self):
        # 美食列表由自绘卡片组成。价格符号可从控件树读取，以首个价格行
        # 向上偏移 10% 屏高定位对应商家标题，兼容地址栏高度和首屏卡片变化。
        if not getattr(self, 'food_open', False):
            self.merchant_open = False
            return self.skip('未进入美食页，跳过商家卡片')
        if self.contains_nodes(desc='立即抢购'):
            self.merchant_open = True
            return True
        width, height = self.d.window_size()
        prices = [node for node in self.nodes(desc='¥')
                  if self.bounds(node)[1] > height * .2]
        if not prices:
            self.merchant_open = False
            return self.skip('美食页未公开首个商家的价格锚点')
        first_price_top = min(self.bounds(node)[1] for node in prices)
        target_y = max(height * .23, first_price_top - height * .10)
        for _ in range(2):
            self.point(width * .45, target_y)
            time.sleep(3)
            if self.contains_nodes(desc='立即抢购'):
                self.merchant_open = True
                break
        else:
            self.merchant_open = False
        if not self.merchant_open:
            return self.skip('首个商家页没有公开团购套餐')
        return True

    def open_first_deal(self):
        if not getattr(self, 'merchant_open', False):
            self.deal_open = False
            return self.skip('未进入商家页，跳过团购套餐')
        deals = self.contains_nodes(desc='立即抢购')
        if not deals:
            self.deal_open = False
            return self.skip('商家页没有团购套餐')
        self.click_node(deals[0])
        time.sleep(2)
        self.deal_open = True
        return True

    def buy_deal(self):
        if not getattr(self, 'deal_open', False):
            return self.skip('未进入套餐页，跳过购买入口')
        buy = self.first_any(
            {'text': '购买'}, {'desc': '购买'},
            {'text': '立即抢购'}, {'desc': '立即抢购'})
        if buy is None:
            return self.skip('套餐页没有购买入口')
        self.click_node(buy)
        time.sleep(2)
        return True
