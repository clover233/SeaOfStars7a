"""WPS 首页、云盘、设置、会员支付页和示例文档；用例表1877～1889行。"""
import time
import json
from pathlib import Path
import subprocess
import tempfile

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_wpsoffice_0010(DynamicAppCase):
    PACKAGE = 'cn.wps.moffice_eng'
    all_app_package_list = [PACKAGE]
    TAB_ID = 'phone_home_toolbar_item_text'
    DOCUMENT = '欢迎使用WPS云文档'
    FIXTURE = 'SeaOfStars_WPS_Browse.docx'
    REMOTE_FIXTURE = '/sdcard/Download/SeaOfStarsFixtures/' + FIXTURE

    def set_up(self):
        super().set_up()
        self._locators = set()
        from Cases.Top48.weixin_common import WeixinDynamicCase
        self._ocr_command = None
        WeixinDynamicCase.prepare_ocr(self)
        fixture = Path(__file__).resolve().parents[2]/'Resources'/'fixtures'/self.FIXTURE
        if not fixture.is_file():
            raise RuntimeError('缺少WPS文档浏览测试素材：' + str(fixture))
        self.d.shell(['mkdir', '-p', str(Path(self.REMOTE_FIXTURE).parent)])
        self.d.push(str(fixture), self.REMOTE_FIXTURE)

    def body_rows(self):
        if not self._ocr_command:
            raise RuntimeError('WPS正文未导出控件，需要本地OCR确认页面内容')
        with tempfile.TemporaryDirectory(prefix='wps-screen-') as folder:
            shot = str(Path(folder)/'screen.png')
            self.d.screenshot(shot, display_id=0)
            result = subprocess.run(self._ocr_command+[shot], check=True,
                                    capture_output=True, text=True, timeout=30)
        return [r for r in json.loads(result.stdout) if .15 < r['y'] < .8
                and len(r['text'].strip()) >= 8]

    def readable_document(self):
        ready = self.document_ready() and len(self.body_rows()) >= 3
        if ready:
            self._locators.add('screenshot-ocr-relative')
        return ready

    def navigation_ready(self):
        return (self.current_app()['activity'].endswith('HomeRootActivity')
                and all(self.has(rid=self.TAB_ID, text=name) for name in ('首页', '云盘', '我')))

    def tab_selected(self, name):
        return any(n.get('selected') == 'true' for n in self.nodes(rid=self.TAB_ID, text=name))

    def select_tab(self, name):
        self.wait_for(self.navigation_ready, 'WPS底部导航未加载', timeout=30)
        self.transition(lambda: self.click(rid=self.TAB_ID, text=name),
                        lambda: self.navigation_ready() and self.tab_selected(name),
                        'WPS未切换到' + name)

    def member_offer_closes(self):
        # 会员挽留弹窗的 X 无名称，但导出了独立的小型 clickable View。
        # 实机截图和树一致：居中、弹窗下方；不匹配付款按钮。
        if not self.has(text='会员支付'):
            return []
        width, height = self.screen_size()
        result = []
        for node in self.nodes():
            left, top, right, bottom = self.bounds(node)
            if (node.get('class') == 'android.view.View' and node.get('clickable') == 'true'
                    and not node.get('text') and not node.get('content-desc')
                    and .4 < (left+right)/2/width < .6 and .65 < top/height < .85
                    and .05 < (right-left)/width < .15 and .02 < (bottom-top)/height < .08):
                result.append(node)
        return result

    def return_navigation(self):
        for _ in range(7):
            if self.navigation_ready():
                return
            closes = self.member_offer_closes()
            if len(closes) == 1:
                self._locators.add('tree')
                self.click_node(closes[0])
                # 挽留弹窗关闭时也会结束会员页；下轮先检查导航，避免多按返回退出应用。
                time.sleep(.8)
            elif self.has(rid='component_btn_close', desc='关闭'):
                self.click(rid='component_btn_close', desc='关闭')
                time.sleep(.8)
            else:
                self.back()
        self.wait_for(self.navigation_ready, '未返回WPS底部导航')

    def launch(self):
        self.start()
        if self.current_app()['activity'].endswith('HomeRootActivity'):
            self.wait_for(self.navigation_ready, 'WPS启动后导航未加载', timeout=30)
        self.main_page()

    def main_page(self):
        self.return_navigation()
        self.select_tab('首页')
        self.wait_for(lambda: self.has(rid='search_content_alphaLinearLayout_hor', desc='搜索'),
                      'WPS首页内容未加载')

    def horizontal_home(self):
        self.main_page()
        for start, end in ((.8, .2), (.2, .8)):
            for _ in range(5):
                self.swipe(start, .6, end, .6)
                time.sleep(2)
        self.wait_for(lambda: self.navigation_ready() and self.tab_selected('首页'),
                      '左右浏览后离开WPS首页')

    def cloud_home_roundtrip(self):
        for _ in range(5):
            self.select_tab('云盘')
            self.wait_for(lambda: self.has(rid='tv_cloud_space_text') and self.has(rid='iv_drive_filter'),
                          'WPS云盘内容未加载', timeout=30)
            time.sleep(2)
            self.select_tab('首页')
            self.wait_for(lambda: self.has(rid='search_content_alphaLinearLayout_hor'),
                          'WPS首页内容未恢复')
            time.sleep(2)

    def my_page(self):
        self.return_navigation()
        self.select_tab('我')
        self.wait_for(lambda: self.has(text='超级会员', rid='title'), 'WPS我的页面未加载')

    def settings(self):
        self.reveal('WPS我的页缺少设置入口', rid='phone_documents_settings_detail', desc='设置')
        self.open_control(lambda: self.has(rid='titlebar_text', text='设置')
                          and self.has(text='功能设置'), 'WPS设置页未打开',
                          rid='phone_documents_settings_detail', desc='设置')

    def member(self):
        self.click(text='超级会员', rid='title')
        # 只浏览业务要求的支付页面；等待 H5 导出内容，不触发套餐开通。
        self.wait_for(lambda: self.has(text='会员支付') and self.has(text='支付方式')
                      and self.has(text='确认协议并开通'), 'WPS会员支付页未加载', timeout=30)

    def document_ready(self):
        return ('writer.multiactivity.Writer' in self.current_app()['activity']
                and self.has(rid='writer_layout'))

    def fit_reading(self):
        if self.has(rid='bottom_arrange', text='退出沉浸'):
            return
        if not self.has(rid='bottom_arrange', text='阅读模式'):
            # 沉浸阅读会自动隐藏工具栏，点击正文容器恢复控件后再判断模式。
            self.click(rid='writer_layout')
            self.wait_for(lambda: self.has(rid='bottom_arrange'), 'WPS阅读工具栏未恢复')
            if self.has(rid='bottom_arrange', text='退出沉浸'):
                return
        self.click(rid='bottom_arrange', text='阅读模式')
        self.wait_for(lambda: self.has(rid='tv_fit_title', text='沉浸式阅读'),
                      'WPS本地阅读模式入口未打开')
        self.click(rid='tv_fit_title', text='沉浸式阅读')
        self.wait_for(lambda: self.has(rid='bottom_arrange', text='退出沉浸'),
                      'WPS文档未适应屏幕阅读')

    def document(self):
        self.main_page()
        self.click(desc='最近')
        self.wait_for(lambda: any(n.get('selected') == 'true' for n in self.nodes(desc='最近')),
                      'WPS最近文档列表未打开')
        if not self.has(text=self.DOCUMENT, rid='history_record_item_name'):
            self.select_tab('云盘')
            self.wait_for(lambda: self.has(text=self.DOCUMENT, rid='item_name'),
                          '最近及云盘均没有WPS示例文档', timeout=30)
            self._adaptation = '最近列表无示例文档，从云盘打开同一份欢迎使用WPS云文档'
            selector = {'text': self.DOCUMENT, 'rid': 'item_name'}
        else:
            selector = {'text': self.DOCUMENT, 'rid': 'history_record_item_name'}
        def open_document():
            if not self.current_app()['activity'].endswith('HomeRootActivity'):
                return  # Writer已启动但尚在加载时不重复点击列表。
            cards = [n for n in self.nodes(desc=self.DOCUMENT, prefix=True)
                     if n.get('clickable') == 'true']
            if len(cards) == 1:
                self.click_node(cards[0])
            else:
                self.click(**selector)
        self.transition(open_document, self.document_ready, 'WPS示例文档未打开')
        self.wait_for(self.document_ready, 'WPS示例文档未进入阅读页面', timeout=30)
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            if self.readable_document():
                self.fit_reading()
                self.wait_for(self.readable_document, '切换阅读模式后正文不可见')
                return
            time.sleep(.5)
        # 实机的欢迎云文档正文为0字符。保留原文件，以专用四页素材验证相同阅读流程。
        self.return_navigation()
        result = self.d.shell(['am', 'start', '-W', '--display', '0',
                               '-a', 'android.intent.action.VIEW',
                               '-t', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                               '-d', 'file://' + self.REMOTE_FIXTURE, '-p', self.PACKAGE])
        if result.exit_code or 'Error:' in result.output:
            raise RuntimeError('WPS测试文档启动失败：' + result.output)
        self.wait_for(self.document_ready, 'WPS专用测试文档未打开', timeout=30)
        self.fit_reading()
        self.wait_for(self.readable_document, 'WPS专用测试文档没有显示正文', timeout=30)
        self._adaptation = '原欢迎云文档未显示正文，改用本地四页专用文档完成适应屏幕阅读浏览'

    def browse_document(self):
        if not self.readable_document():
            raise RuntimeError('当前不是WPS示例文档阅读页')
        self.browse(5, 5)
        self.wait_for(self.readable_document, '浏览后WPS文档正文不可见')

    def home(self):
        self.foreground()
        self.swipe(.5, .985, .5, .62, 300)
        time.sleep(.8)
        if 'launcher' not in self.current_app()['activity'].lower():
            self.d.shell('input -d 0 keyevent 3')
            self._adaptation = '系统未响应上滑手势，使用主屏Home键返回桌面'
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(), '未返回桌面')

    def steps(self):
        return [
            ('启动WPS', self.launch, 2),
            ('首页左右滑动各5次，每次停留2秒', self.horizontal_home, 2),
            ('云盘与首页来回切换5次，每次停留2秒', self.cloud_home_roundtrip, 2),
            ('点击我', self.my_page, 2),
            ('点击设置', self.settings, 2),
            ('返回我的页面', self.my_page, 2),
            ('点击超级会员进入支付页面', self.member, 2),
            ('返回我的页面', self.my_page, 2),
            ('点击首页', self.main_page, 2),
            ('最近列表打开欢迎使用WPS云文档', self.document, 2),
            ('上下滑动各5次浏览文档', self.browse_document, 2),
            ('返回WPS主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
