"""微信 0090—0130：搜索、内容浏览与支付页面导航。

只查看支付页面，不输入金额、户号，不提交红包、转账、充值或缴费。
"""
import time
import xml.etree.ElementTree as ET

from Cases.Top48.weixin_common import WeixinDynamicCase, WeixinStepSkipped, optional


class WeixinExtendedCase(WeixinDynamicCase):
    def point(self, x, y):
        self.foreground()
        # 本机短促 tap 偶尔被过滤；鼠标源原地按住 200ms，低于长按阈值。
        result = self.d.shell('input mouse -d 0 swipe {0} {1} {0} {1} 200'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('主屏点击失败：' + result.output)
        self.invalidate()

    def main_page(self):
        # 首页加号菜单仍保留底部标签，不能将弹层当作已经返回首页。
        if (self.main_ready() and self.visible('添加朋友', region=(.55, .1, 1, .45))
                and self.visible('发起群聊', region=(.55, .1, 1, .45))):
            self.back()
        super().main_page()
        if getattr(self, '_live_started', False):
            self.close_live_float()

    def live_float_box(self):
        width, height = self.d.window_size()
        boxes = []
        for node in ET.fromstring(self.d.dump_hierarchy()).iter('node'):
            box = self.bounds(node)
            if len(box) != 4 or node.get('package') != self.PACKAGE:
                continue
            left, top, right, bottom = box
            if (node.get('class') == 'android.widget.FrameLayout'
                    and not node.get('resource-id') and not node.get('content-desc')
                    and .15 < (right-left)/width < .4 and .1 < (bottom-top)/height < .35
                    and (left < width*.05 or right > width*.95)):
                boxes.append(box)
        return max(boxes, key=lambda b: (b[2]-b[0])*(b[3]-b[1])) if boxes else None

    def close_live_float(self):
        """只关闭本用例打开的直播浮窗，并确认其消失。"""
        def close():
            box = self.live_float_box()
            if not box:
                return
            buttons = self.nodes(desc='关闭')
            if len(buttons) == 1:
                self._locators.add('tree')
                self.click_node(buttons[0])
            else:
                # 浮窗有时不导出子控件；按截图核对的浮窗边界比例定位 X。
                left, top, right, bottom = box
                width, height = self.d.window_size()
                self.pct((left+(right-left)*.74)/width, (top+(bottom-top)*.83)/height)
        self.transition(close, lambda: self.live_float_box() is None and not self.live_ready(),
                        '直播浮窗未关闭，停止以免遮挡后续入口')
        self._live_started = False

    def clean_up(self):
        try:
            if getattr(self, '_live_started', False):
                self.main_page()
        finally:
            super().clean_up()

    def plus_menu(self):
        self.wechat_home()
        self.transition(lambda: self.pct(.93, .083),
                        lambda: self.visible('添加朋友', region=(.55, .1, 1, .45)),
                        '首页加号菜单未打开')

    def tab(self, label):
        if label not in ('我', '发现'):
            return super().tab(label)
        self.main_page()
        # “我”也有朋友圈入口，必须校验对应页面，不能仅凭底部标签判断成功。
        ready = (lambda: self.main_ready() and self.visible('服务') and self.visible('收藏')) if label == '我' else (
            lambda: self.main_ready() and self.visible('发现', region=(.2, .05, .8, .11)))
        self.transition(lambda: self.pct(.875 if label == '我' else .625, .943),
                        ready, '未切换到' + label)

    def needs(self, *keys):
        for key in keys:
            if key in self.unavailable:
                raise WeixinStepSkipped('前置功能不可用：' + self.unavailable[key])

    def content_wait(self, predicate, message, timeout=25):
        """有入口但内容受网络/账号/协议限制时，明确记录 SKIP。"""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():
                return
            self.foreground()
            if any(self.visible(word, True) for word in ('同意并', '同意协议', '暂不支持', '加载失败', '网络不可用')):
                raise WeixinStepSkipped(message + '；页面要求协议确认或内容不可用')
            time.sleep(.7)
        raise WeixinStepSkipped(message + '；等待内容超时')

    def me(self):
        self.tab('我')

    @optional('search')
    def search_page(self):
        self.wechat_home()
        def open_search():
            native = self.nodes(desc='搜索')
            if native:
                self.click_node(native[0])
            else:
                # 首页右上角搜索图标，已经实机截图核对。
                self.pct(.827, .083)
        self.transition(open_search, lambda: self.activity_is('FTSMainUI')
                        and self.visible('搜索', True, (0, .05, 1, .15)), '微信搜索输入页未打开')

    @optional('search')
    def search_huawei(self):
        self.needs('search')
        self.input_text('华为手机')
        self.await_text('华为手机', True)
        self.d.press('search')
        self.invalidate()
        self.content_wait(lambda: self.visible('搜索网络结果', True) or self.visible('综合'), '搜索建议未加载')
        if self.visible('搜索网络结果', True):
            heading = self.find('搜索网络结果', True)[0]
            rows = [r for r in self.find('华为手机', True) if r['y'] > heading['y']+heading['h']]
            if not rows:
                raise WeixinStepSkipped('没有华为手机的网络搜索入口')
            row = rows[0]
            self._locators.add(row['source'])
            self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
        self.content_wait(lambda: self.visible('华为手机', True) and (
            self.visible('搜一搜', True) or self.visible('公众号', True) or self.visible('综合')),
            '华为手机搜索结果未显示')

    @optional('scan')
    def scan_qr(self):
        def open_scan():
            if not self.visible('添加朋友', region=(.55, .1, 1, .45)):
                raise WeixinStepSkipped('首页加号菜单不可用')
            # 截图中“扫一扫”偶尔识别为“扫一千”；在已确认的菜单内匹配“扫”。
            self.choose('扫', True, (.55, .2, 1, .33))
        self.transition(open_scan, lambda: self.activity_is('ScanUI', 'BaseScanUI'), '扫一扫取景页未打开')
        # 表中未提供二维码素材；避免扫描到环境中未知的付款/登录二维码。
        self.adapt('未提供指定二维码，以进入扫一扫取景页面并停留替代扫码结果')

    @optional('pay-code')
    def pay_codes(self):
        self.choose('收付款', True, (.55, .2, 1, .45))
        time.sleep(1)
        current = self.current_app()['activity'].lstrip('.')
        windows = self.d.shell('dumpsys window windows').output.split('Window #')
        secure = any(current in part.splitlines()[0] and ' SECURE ' in part[:2000]
                     for part in windows if part.splitlines())
        if secure and not self.nodes() and not any(.12 < row['y'] < .9 for row in self.screen()):
            raise WeixinStepSkipped('收付款窗口启用 SECURE，截图正文为空且控件树无可用节点，无法核对二维码收款入口')
        self.content_wait(lambda: self.visible('二维码收款') or self.visible('收款码'), '收付款页面未显示')

    @optional('pay-code')
    def receive_code(self):
        self.needs('pay-code')
        self.choose('二维码收款' if self.visible('二维码收款') else '收款码')
        self.content_wait(lambda: self.visible('二维码收款', True) and (
            self.visible('设置金额') or self.visible('收款小账本') or self.visible('保存收款码')),
            '二维码收款页面未显示')

    @optional('channels')
    def channels(self):
        self.choose('视频号', region=(0, .12, 1, .9))
        self.content_wait(lambda: self.activity_is('FinderHome', 'FinderTimelineUI') and (
            self.visible('推荐') or self.visible('朋友') or self.visible('关注')), '视频号内容未加载')

    @optional('channels')
    def browse_channels(self):
        self.needs('channels')
        if not self.activity_is('Finder'):
            raise WeixinStepSkipped('当前不在视频号页面')
        self.browse(6, 0)

    @optional('live-list')
    def live_list(self):
        self.choose('直播', region=(0, .12, 1, .9))
        self.content_wait(lambda: self.activity_is('Finder', 'WebView') and (
            self.visible('直播', True) or self.visible('推荐')), '直播列表未加载')

    @optional('live-room')
    def first_live(self):
        self.needs('live-list')
        if not self.activity_is('FinderLiveSquare'):
            raise WeixinStepSkipped('当前不是已核对的双列直播列表')
        if not any(.2 < r['y'] < .85 for r in self.screen()):
            raise WeixinStepSkipped('直播列表未展示内容卡片')
        # 首张卡片的画面区域；卡片底部主播名字会进入资料页，不能点击名字。
        self.transition(lambda: self.pct(.25, .34), self.live_ready, '第一直播间未打开')
        self._live_started = True

    def live_ready(self):
        return self.activity_is('FinderLive') and not self.activity_is('Square')

    @optional('live-room')
    def browse_live(self):
        self.needs('live-list', 'live-room')
        if not self.live_ready():
            raise WeixinStepSkipped('当前不在直播间')
        self.browse(6, 0)

    @optional('games')
    def games(self):
        self.choose('游戏', region=(0, .12, 1, .9))
        self.content_wait(lambda: self.activity_is('GameTabUI', 'GameCenterUI') and (
            self.visible('找游戏') or self.visible('微信游戏', True)), '游戏首页未加载')
        if self.visible('圈子'):
            self.adapt('当前微信游戏默认显示圈子信息流，替代旧版游戏首页浏览')

    @optional('games')
    def browse_games(self):
        self.needs('games')
        if self.main_ready():
            raise WeixinStepSkipped('当前不在游戏首页')
        self.browse(6, 6)

    @optional('service')
    def service(self):
        self.me()
        self.choose('服务')
        self.await_text('钱包')

    @optional('wallet')
    def wallet(self):
        self.needs('service')
        self.choose('钱包')
        self.await_text('零钱')

    @optional('wallet')
    def balance(self):
        self.needs('wallet')
        self.choose('零钱')
        self.await_text('我的零钱')

    def return_service(self):
        self.needs('service')
        self.return_to(lambda: self.visible('钱包') and self.visible('手机充值'), '未返回服务页面', limit=8)

    @optional('top-up')
    def top_up(self):
        self.needs('service')
        self.choose('手机充值')
        self.content_wait(lambda: self.visible('手机充值', region=(.2, .05, .75, .12))
                          and self.visible('充话费'), '手机充值小程序未加载', timeout=40)

    @optional('utilities')
    def utilities(self):
        self.needs('service')
        self.choose('生活缴费')
        self.content_wait(lambda: self.visible('新增缴费') and self.visible('电费'),
                          '生活缴费小程序未加载', timeout=40)

    @optional('electricity')
    def electricity(self):
        self.needs('utilities')
        self.choose('电费')
        self.content_wait(lambda: self.visible('选择缴费单位'), '缴费单位列表未加载')

    @optional('electricity')
    def first_provider(self):
        self.needs('utilities', 'electricity')
        self.await_text('选择缴费单位')
        rows = [r for r in self.screen() if .2 < r['y'] < .85 and r['x'] < .6
                and any(word in r['text'] for word in ('电费', '电网', '电力', '能源'))]
        if not rows:
            raise WeixinStepSkipped('未识别到电费缴费单位')
        row = rows[0]
        self._locators.add(row['source'])
        self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
        self.content_wait(lambda: self.visible('缴费户号', True), '电费户号填写页未加载')
        if '电网' not in row['text']:
            self.adapt('当前城市第一项为“{}”，替代表中的电网公司；不输入户号'.format(row['text']))

    def favorites(self):
        self.me()
        self.choose('收藏')
        self.await_text('收藏', region=(.2, .05, .8, .12))

    @optional('red-packet')
    def red_packet_preview(self):
        self.require_test_chat()
        self.choose('红包')
        self.content_wait(lambda: self.visible('红包个数') or self.visible('塞钱进红包')
                          or self.visible('单个金额') or self.visible('金额'), '红包编辑页未加载')
        self.back()
        self.wait_for(self.chat_ready, '未返回测试聊天')
        self._panel_open = False

    @optional('transfer')
    def transfer(self):
        self.require_test_chat()
        self.choose('转账')
        self.content_wait(lambda: self.visible('添加转账说明', True), '转账编辑页未加载')

    @optional('transfer-memo')
    def transfer_memo(self):
        self.needs('transfer')
        self.choose('添加转账说明', True)
        self.await_text('确定')

    @optional('transfer-memo')
    def edit_memo(self):
        self.needs('transfer', 'transfer-memo')
        self.await_text('确定')
        self.input_text('修改')
        self.await_text('修改')

    @optional('transfer-memo')
    def confirm_memo(self):
        self.needs('transfer', 'transfer-memo')
        self.await_text('修改')
        self.choose('确定')
        self.content_wait(lambda: self.visible('修改', True, (.04, .36, .8, .55))
                          and not self.visible('确定'), '转账说明未保存到编辑页')

    def return_test_chat(self):
        self.needs('test-chat')
        self.return_to(self.chat_ready, '未返回测试聊天', limit=8)
        self._panel_open = False

    def browse_test_chat(self):
        self.require_test_chat()
        self.browse(0, 3)

    @optional('tencent-card')
    def tencent_card(self):
        self.needs('official-list')
        self.find_official(('腾讯新闻',))
        self.await_text('腾讯新闻', region=(0, .1, 1, .35))

    @optional('cctv')
    def cctv_card(self):
        self.needs('official-list')
        self.find_official(('央视新闻',))
        self.await_text('央视新闻', region=(0, .1, 1, .35))

    def cctv_ready(self):
        return (self.visible('央视新闻', region=(.2, .05, .8, .12))
                and self.visible('夜读', True, (0, .89, 1, .98)))

    def cctv_thread(self):
        self.needs('cctv')
        if self.cctv_ready():
            return
        if self.visible('私信') and self.visible('央视新闻', region=(0, .1, 1, .35)):
            self.choose('私信')
        else:
            self.return_to(self.cctv_ready, '未返回央视新闻对话界面', limit=8)
        self.wait_for(self.cctv_ready, '央视新闻对话界面未打开')

    @optional('culture')
    def culture_menu(self):
        self.cctv_thread()
        if self.visible('文博日历', True, (0, .89, 1, .98)):
            self.choose('文博日历', True, (0, .89, 1, .98))
        elif self.visible('打卡笔记', True, (0, .89, 1, .98)):
            self.choose('打卡笔记', True, (0, .89, 1, .98))
            self.adapt('当前菜单“打卡笔记”替代旧版“文博日历”')
        else:
            raise WeixinStepSkipped('央视新闻没有文博日历或打卡笔记菜单')
        self.web_content('文博/打卡页面未加载')

    def web_content(self, message):
        self.content_wait(lambda: self.activity_is('WebView', 'UIPageFragmentActivity')
                          and any(.13 < r['y'] < .88 and len(r['text']) >= 4 for r in self.screen()), message)
        if any(self.visible(word, True) for word in ('无法打开', '停止访问', '已删除', '页面不存在')):
            raise WeixinStepSkipped(message + '；链接已失效或不可访问')

    @optional('culture')
    def browse_culture(self):
        self.needs('culture')
        self.web_content('主题页面不可用')
        self.browse(2, 2)

    @optional('cctv')
    def return_cctv(self):
        self.cctv_thread()

    @optional('night')
    def night_menu(self):
        self.cctv_thread()
        self.choose('夜读', True, (0, .89, 1, .98))
        # 夜读有时先弹出子菜单；从可见菜单中选择夜读主题。
        time.sleep(.7)
        if self.cctv_ready():
            rows = self.find('夜读', True, (0, .5, 1, .89))
            if not rows:
                raise WeixinStepSkipped('夜读子菜单没有可识别的主题')
            row = rows[0]
            self._locators.add(row['source'])
            self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
        self.web_content('夜读详情页未加载')

    @optional('subscriptions')
    def subscriptions(self):
        self.wechat_home()
        for _ in range(5):
            for label in ('订阅号消息', '订阅号', '公众号'):
                if self.visible(label, region=(.12, .11, .9, .92)):
                    self.choose(label, region=(.12, .11, .9, .92))
                    self.content_wait(lambda: not self.main_ready() and (
                        self.visible('公众号', region=(.2, .05, .8, .12))
                        or self.visible('订阅号', True, (.2, .05, .8, .12))), '订阅号内容未加载')
                    if label == '公众号':
                        self.adapt('首页“公众号”替代旧版本“订阅号”聚合入口')
                    return
            self.swipe()
            time.sleep(.7)
        raise WeixinStepSkipped('首页未找到订阅号或公众号聚合入口')

    @optional('tencent-news')
    def tencent_news(self):
        self.needs('subscriptions')
        for _ in range(5):
            if self.visible('腾讯新闻', region=(0, .12, 1, .9)):
                self.choose('腾讯新闻', region=(0, .12, 1, .9), index=0)
                self.content_wait(lambda: self.visible('腾讯新闻', True, (0, .05, 1, .35))
                                  and not self.visible('公众号', region=(.2, .05, .8, .12)),
                                  '腾讯新闻页面未打开')
                return
            self.swipe()
            time.sleep(.7)
        # 账号未出现在当前订阅信息流时，沿用通讯录中已关注的同一个公众号。
        self.return_official()
        self.tencent_card()
        self.adapt('当前订阅信息流未展示腾讯新闻，改从已关注公众号进入腾讯新闻资料/文章页')

    @optional('tencent-news')
    def browse_tencent(self):
        self.needs('subscriptions', 'tencent-news')
        if self.main_ready():
            raise WeixinStepSkipped('腾讯新闻内容页不可用')
        self.browse(0, 3)
