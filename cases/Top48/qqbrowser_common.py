"""QQ浏览器20.6.7：原生搜索入口及学信网公开网页浏览。"""
import time
from urllib.parse import urlsplit

from Cases.Top48.qq_common import QQDynamicBase, QQStepSkipped
from Cases.Top48.screen_text import ScreenshotText


class QQBrowserDynamicCase(QQDynamicBase):
    PACKAGE = 'com.tencent.mtt'
    all_app_package_list = [PACKAGE]
    OFFICIAL_URL = 'https://www.chsi.com.cn/'

    def set_up(self):
        super().set_up()
        self._original_ime = self.d.current_ime()
        # Android 17 的默认 clearInputText 不兼容，采集前准备广播输入法。
        self.d.set_input_ime(True)

    def clean_up(self):
        try:
            original = getattr(self, '_original_ime', None)
            if original and self.d.current_ime() != original:
                self.d.shell(['ime', 'set', original])
        finally:
            super().clean_up()

    @staticmethod
    def label(node):
        return node.get('text') or node.get('content-desc') or ''

    def main_ready(self):
        # 新版多窗口入口已移到底栏，取消旧版右上角 resource-id。
        return (self.has(desc='搜索栏') and (self.has(rid='right_top_multi_window')
                or self.has(text='首页') and self.has(text='多窗口')))

    def main_page(self):
        for _ in range(8):
            if self.main_ready():
                return
            if self.has(desc='首页') or self.has(text='首页'):
                self.choose('首页')
                time.sleep(1)
            else:
                self.back()
        self.wait_for(self.main_ready, '未返回 QQ 浏览器主界面')

    def launch(self):
        self._site_reason = None
        self._detail_reason = None
        self._detail_open = False
        self._site_address = None
        self.start()
        # 已安装版本有开屏广告，等待结束或仅点击命名“跳过”控件。
        for _ in range(8):
            if self.has(text='跳过'):
                self.click(text='跳过')
            if self.main_ready():
                return
            time.sleep(1)
        self.main_page()

    def search_edit_ready(self):
        return self.has(rid='search_frame_input_right', text='搜索') or self.has(rid='search_frame_input_center_search')

    def open_search(self):
        self.main_page()
        self.click(desc='搜索栏')
        self.wait_for(lambda:self.search_edit_ready() or self.has(rid='white_tv_title'),
                      '浏览器搜索入口未打开')
        # 本版点搜索栏可能先搜索热词；再点顶部词条进入自绘输入页。
        if not self.search_edit_ready():
            self.click(rid='white_tv_title')
        self.wait_for(self.search_edit_ready, '搜索编辑页未打开')

    def search(self):
        if not self.search_edit_ready():
            raise RuntimeError('不在搜索编辑页')
        # 搜索框为自绘控件，没有 android.widget.EditText 节点；通过当前焦点输入。
        self.d.send_keys('学信网', clear=True)
        self.wait_for(lambda:any('学信网' in self.label(n) for n in self.nodes()), '搜索词未显示')
        if self.has(rid='search_frame_input_right', text='搜索'):
            self.click(rid='search_frame_input_right', text='搜索')
        else:
            self.click(rid='search_frame_input_center_search')
        self.wait_for(self.results_ready,
                      '未进入学信网搜索结果', timeout=25)
        time.sleep(2)

    def results_ready(self):
        return (self.has(rid='white_tv_title', text='学信网')
                or self.has(text='学信网') and self.has(desc='全部') and self.has(desc='资讯'))

    def browse_results(self):
        if not self.results_ready():
            raise RuntimeError('浏览前未进入学信网搜索结果')
        self.browse(2, 2)

    def dismiss_default_prompt(self):
        labels = [self.label(n) for n in self.nodes()]
        if any('QQ浏览器设为默认浏览器' in text for text in labels) and '下次再说' in labels:
            self.choose('下次再说')
            time.sleep(.5)
            return True
        return False

    @staticmethod
    def official_address(address):
        try:
            url = urlsplit(address if '://' in address else 'https://' + address)
            host = (url.hostname or '').lower()
            return (url.scheme in ('https', 'http') and not url.username and not url.password
                    and (host == 'chsi.com.cn' or host.endswith('.chsi.com.cn')))
        except ValueError:
            return False

    def site_ready(self):
        self.dismiss_default_prompt()
        # 核对原生地址栏；搜索摘要出现官网域名不能代表已进入官网。
        return (not self.results_ready()
                and bool(self.nodes(rid='third_web_search_title'))
                and (any(self.official_address(n.get('text', ''))
                         for n in self.nodes(rid='third_web_search_title'))
                     or bool(getattr(self, '_site_address', None))))

    def verify_address(self):
        # 新版地址栏显示网页标题，点开后首条原生语义才显示当前网址。
        # 只核验顶部当前网址，不能拿下方搜索建议中的官方域名代替。
        titles = self.nodes(rid='third_web_search_title')
        if not titles:
            raise RuntimeError('当前页面没有浏览器地址栏')
        title = titles[0].get('text', '')
        if self.official_address(title):
            self._site_address = title
            return title
        self.dismiss_default_prompt()
        self.transition(lambda: self.click(rid='third_web_search_title'),
                        self.search_edit_ready, '地址编辑页未打开')
        height = self.screen_size()[1]
        def addresses():
            self.dismiss_default_prompt()
            return [self.label(n) for n in self.nodes()
                    if height * .13 < self.bounds(n)[1] < height * .23
                    and self.label(n).startswith(('https://', 'http://'))]
        try:
            self.wait_for(lambda: bool(addresses()), '当前网页网址未显示', timeout=10)
            current = addresses()[0]
            if not self.official_address(current):
                raise RuntimeError('当前网页不是学信网官方域名：' + current)
            self._site_address = current
            return current
        finally:
            self.back()

    def official(self):
        if not self.results_ready():
            raise RuntimeError('打开官网前不在学信网搜索结果')
        candidates=[n for n in self.nodes()
                    if ('www.chsi.com.cn' in self.label(n) or self.label(n)=='https://www.chsi.com.cn/')
                    and self.bounds(n)[1] > self.screen_size()[1]*.18]
        if candidates:
            self.click_node(sorted(candidates,key=lambda n:self.bounds(n)[1])[0])
            time.sleep(2)
        else:
            # 搜索网页没有正文节点时，按截图识别首条官方结果标题并按比例点击。
            rows = ScreenshotText().read(self.d)
            headings = [r for r in rows if '中国高等教育学生信息网' in r['text']
                        and .2 < r['y'] < .6]
            if headings:
                row = min(headings, key=lambda r: r['y'])
                self.pct(row['x'] + row['w']/2, row['y'] + row['h']/2)
                self.wait_for(lambda: bool(self.nodes(rid='third_web_search_title')),
                              '首条官方结果未打开', timeout=20)
                self.verify_address()
                self.adapt('搜索正文未导出控件，按截图标题的比例位置进入首条官方结果并核验域名')
        if not self.site_ready():
            self.shell('am start --display 0 -a android.intent.action.VIEW -d ' + self.OFFICIAL_URL + ' -p ' + self.PACKAGE)
            self.adapt('搜索首条结果未能核验官方域名，改为在 QQ 浏览器打开学信网官方 HTTPS 地址')
            self.wait_for(lambda: bool(self.nodes(rid='third_web_search_title')),
                          '官方地址页面未打开', timeout=20)
            self.verify_address()
        try:
            self.wait_for(self.site_ready,'官网页面标识未加载',timeout=25)
            self.wait_for(self.site_body_ready, '学信网官网正文未加载', timeout=45)
        except RuntimeError:
            # 网络/网站验证页只记录不可用，不操作验证码或账号登录。
            self._site_reason='当前网络或网站验证页面未展示学信网官网正文'
            raise QQStepSkipped(self._site_reason)

    def site_body_ready(self):
        # 地址栏可在断网错误页保留官网域名，必须另外确认网页正文已渲染。
        rows = ScreenshotText().read(self.d)
        body = [r['text'] for r in rows if .15 < r['y'] < .89]
        return (not any('当前网络不可用' in text or '网页无法打开' in text for text in body)
                and any('学信网' in text for text in body)
                and sum(len(text) >= 12 for text in body) >= 2)

    def browse_site(self):
        if self._site_reason:
            raise QQStepSkipped(self._site_reason)
        if not self.site_ready():
            raise RuntimeError('浏览前未确认学信网官网')
        self.wait_for(self.site_body_ready, '浏览前官网正文未加载', timeout=30)
        self.browse(2, 2)

    def body_labels(self):
        height=self.screen_size()[1]
        return {self.label(n) for n in self.nodes()
                if height*.16 < self.bounds(n)[1] < height*.89 and self.label(n)}

    def first_content(self):
        if self._site_reason:
            self._detail_reason=self._site_reason
            raise QQStepSkipped(self._detail_reason)
        self.wait_for(self.site_ready,'进入内容前不在官网')
        height=self.screen_size()[1]
        # 按可见顺序取官网正文链接；不固定会随时间更新的新闻标题。
        links=[n for n in self.nodes() if n.get('clickable')=='true'
               and len(self.label(n)) >= 12 and height*.2 < self.bounds(n)[1] < height*.85
               and not any(word in self.label(n) for word in ('登录','注册','搜索','隐私','高等教育学生信息网','chsi.com.cn'))]
        if not links:
            return self.first_content_from_screenshot_layout()
        before=self.body_labels()
        first=sorted(links,key=lambda n:(self.bounds(n)[1],self.bounds(n)[0]))[0]
        self.click_node(first)
        self.wait_for(lambda:len(self.body_labels().symmetric_difference(before))>=3,
                      '点击官网首条可见内容后页面未变化',timeout=25)
        self._detail_open=True

    def first_content_from_screenshot_layout(self):
        # 官网正文没有节点。先恢复顶部，按当前截图的首条正文标题定位，
        # 不依赖固定标题或绝对像素；点击后再次核验官方域名和网址变化。
        before = self.verify_address()
        for _ in range(3):
            self.swipe(y1=.32, y2=.78)
            time.sleep(.5)
        rows = ScreenshotText().read(self.d)
        headings = [r for r in rows if .36 < r['y'] < .65 and r['h'] < .06
                    and len(r['text']) >= 12
                    and not any(word in r['text'] for word in ('登录', '注册', '官方网站'))]
        if not headings:
            raise QQStepSkipped('官网首屏没有可核对的正文标题')
        row = min(headings, key=lambda r: r['y'])
        self.pct(row['x'] + row['w']/2, row['y'] + row['h']/2)
        time.sleep(2)
        after = self.verify_address()
        if after == before:
            # QQ 内核有时在官网容器内打开内容，原生栏仍保留首页网址。
            # 必须同时确认正文确实变化，不能只把同一页面再次截图当成详情。
            previous = {r['text'] for r in rows if .15 < r['y'] < .89}
            current = {r['text'] for r in ScreenshotText().read(self.d) if .15 < r['y'] < .89}
            if len(previous.symmetric_difference(current)) < 3:
                raise RuntimeError('点击官网首条内容后网址与正文均未变化')
            self.adapt('官网内容在浏览器容器内打开，核验官方域名及正文变化')
        self._detail_open = True
        self.adapt('网页正文未导出节点，按截图首条标题的比例位置点击并核验地址或正文变化')

    def browse_detail(self):
        if self._detail_reason or self._site_reason:
            raise QQStepSkipped(self._detail_reason or self._site_reason)
        if not getattr(self,'_detail_open',False):
            raise RuntimeError('未进入官网内容详情')
        self.browse(2, 2)
