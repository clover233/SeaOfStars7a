"""QQ浏览器20.6.7：原生搜索入口及学信网公开网页浏览。"""
import time

from Cases.Top48.qq_common import QQDynamicBase, QQStepSkipped


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
        return self.has(desc='搜索栏') and self.has(rid='right_top_multi_window')

    def main_page(self):
        for _ in range(8):
            if self.main_ready():
                return
            if self.has(desc='首页'):
                self.click(desc='首页')
                time.sleep(1)
            else:
                self.back()
        self.wait_for(self.main_ready, '未返回 QQ 浏览器主界面')

    def launch(self):
        self._site_reason = None
        self._detail_reason = None
        self._detail_open = False
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
        self.wait_for(lambda:self.has(rid='white_tv_title', text='学信网'),
                      '未进入学信网搜索结果', timeout=25)
        time.sleep(2)

    def browse_results(self):
        self.require(rid='white_tv_title', text='学信网')
        self.browse(2, 2)

    def site_ready(self):
        # 搜索结果也包含站名，不能仅靠“学信网”三个字判断已进入官网。
        labels=[self.label(n) for n in self.nodes()]
        return (not self.has(rid='white_tv_title', text='学信网')
                and any('高等教育学生信息网' in text or 'chsi.com.cn' in text for text in labels))

    def official(self):
        self.require(rid='white_tv_title', text='学信网')
        candidates=[n for n in self.nodes()
                    if ('www.chsi.com.cn' in self.label(n) or self.label(n)=='https://www.chsi.com.cn/')
                    and self.bounds(n)[1] > self.d.window_size()[1]*.18]
        if candidates:
            self.click_node(sorted(candidates,key=lambda n:self.bounds(n)[1])[0])
            time.sleep(2)
        if not self.site_ready():
            self.shell('am start --display 0 -a android.intent.action.VIEW -d ' + self.OFFICIAL_URL + ' -p ' + self.PACKAGE)
            self.adapt('搜索首条结果未能核验官方域名，改为在 QQ 浏览器打开学信网官方 HTTPS 地址')
        try:
            self.wait_for(self.site_ready,'官网页面标识未加载',timeout=25)
            time.sleep(2)
        except RuntimeError:
            # 网络/网站验证页只记录不可用，不操作验证码或账号登录。
            self._site_reason='当前网络或网站验证页面未展示学信网官网正文'
            raise QQStepSkipped(self._site_reason)

    def browse_site(self):
        if self._site_reason:
            raise QQStepSkipped(self._site_reason)
        if not self.site_ready():
            raise RuntimeError('浏览前未确认学信网官网')
        self.browse(2, 2)

    def body_labels(self):
        height=self.d.window_size()[1]
        return {self.label(n) for n in self.nodes()
                if height*.16 < self.bounds(n)[1] < height*.89 and self.label(n)}

    def first_content(self):
        if self._site_reason:
            self._detail_reason=self._site_reason
            raise QQStepSkipped(self._detail_reason)
        self.wait_for(self.site_ready,'进入内容前不在官网')
        height=self.d.window_size()[1]
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
        # QQ 内核未导出网页正文节点。实机截图核对：移动首页首条内容在
        # 原生地址栏下方约 0.585 个屏幕宽度处；随宽度缩放，不能用固定像素。
        titles=self.nodes(rid='third_web_search_title')
        bars=self.nodes(desc='PortalAddressBarView')
        if not titles or not bars or titles[0].get('text')!='chsi.com.cn/wap/index.jsp':
            self._detail_reason='网页正文未导出控件，且当前布局不符合已核对的移动官网首页'
            raise QQStepSkipped(self._detail_reason)
        for _ in range(3):
            self.swipe(y1=.32,y2=.78)
            time.sleep(.5)
        width,height=self.d.window_size()
        y=self.bounds(bars[0])[3]+width*.585
        if y>=height*.85:
            self._detail_reason='当前屏幕比例无法容纳已核对的官网首条内容位置'
            raise QQStepSkipped(self._detail_reason)
        self.point(width*.5,y)
        def changed():
            nodes=self.nodes(rid='third_web_search_title')
            if not nodes:
                return False
            address=nodes[0].get('text','')
            host=address.split('/')[0]
            return (host=='chsi.com.cn' or host.endswith('.chsi.com.cn')) and address!='chsi.com.cn/wap/index.jsp'
        try:
            self.wait_for(changed,'比例点击后未确认进入官网内容页',timeout=20)
        except RuntimeError:
            self._detail_reason='官网布局可能变化，比例点击未确认进入内容页'
            raise QQStepSkipped(self._detail_reason)
        self._detail_open=True
        self.adapt('网页正文没有控件节点，按实机截图核对的相对位置点击首条内容，并验证官方域名及地址变化')

    def browse_detail(self):
        if self._detail_reason or self._site_reason:
            raise QQStepSkipped(self._detail_reason or self._site_reason)
        if not getattr(self,'_detail_open',False):
            raise RuntimeError('未进入官网内容详情')
        self.browse(2, 2)
