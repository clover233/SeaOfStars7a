"""电话动态性能场景：控件树定位、号码状态校验及比例手势。"""
import re
import time
import xml.etree.ElementTree as ET

from Cases.Top48.baidu_common import BaiduDynamicCase


class CallDynamicCase(BaiduDynamicCase):
    PACKAGE = 'com.android.contacts'
    PREFIX = PACKAGE + ':id/'
    all_app_package_list = [PACKAGE]
    PERMISSIONS = ('READ_CONTACTS', 'READ_CALL_LOG')

    def shell(self, command):
        result = self.d.shell(command)
        if result.exit_code:
            raise RuntimeError('设备命令失败：{} {}'.format(command, result.output))
        return result.output

    def nodes(self, rid=None, **selector):
        if rid:
            selector['resource-id'] = rid if ':' in rid else self.PREFIX + rid
        return [n for n in ET.fromstring(self.d.dump_hierarchy()).iter('node')
                if n.get('package') == self.PACKAGE
                and n.get('display-id', '0') == '0'
                and n.get('visible-to-user') != 'false'
                and all(n.get(k) == v for k, v in selector.items())]

    def has(self, rid=None, **selector):
        return bool(self.nodes(rid, **selector))

    @staticmethod
    def bounds(node):
        return tuple(map(int, re.findall(r'\d+', node.get('bounds'))))

    def click_point(self, x, y):
        self.foreground()
        # 当前测试机过滤过短的按下，用100ms系统注入手势点击实时控件中心。
        self.shell('input swipe {0} {1} {0} {1} 100'.format(round(x), round(y)))

    def click_node(self, node):
        l, t, r, b = self.bounds(node)
        if r <= l or b <= t:
            raise RuntimeError('控件没有有效边界')
        self.click_point((l+r)/2, (t+b)/2)

    def click(self, rid=None, **selector):
        ns = self.nodes(rid, **selector)
        if len(ns) != 1:
            raise RuntimeError('控件不存在或不唯一：{}'.format((rid, selector)))
        self.click_node(ns[0])

    def tab_nodes(self, title):
        # 新版 MIUI 改用 action_page 容器和 miuix 导航文字。
        for rid, attrs in (('navigation_title', {'text': title}),
                           ('miuix_navigation_bar_item_label_view', {'text': title})):
            nodes = self.nodes(rid, **attrs)
            if nodes:
                return nodes
        return []

    def tab_selected(self, title):
        return any(n.get('selected') == 'true' for n in self.tab_nodes(title))

    def contacts_ready(self):
        return self.tab_selected('联系人') and not self.has('search_text_cancel')

    def phone_ready(self):
        return self.tab_selected('通话') and not self.has('search_text_cancel')

    def launch(self):
        # 先等导航出现；启动动画期间 Back 会直接退出到桌面。
        self.d.app_start(self.PACKAGE, use_monkey=True)
        self.wait_for(lambda: bool(self.tab_nodes('通话')) or self.has('search_text_cancel'),
                      '电话导航未加载', timeout=25)
        time.sleep(.8)
        for _ in range(5):
            if self.tab_nodes('通话') and not self.has('search_text_cancel'):
                self.phone()
                return
            self.foreground()
            if self.has('search_text_cancel'):
                self.click('search_text_cancel')
            else:
                self.shell('input -d 0 keyevent 4')
            time.sleep(.8)
        raise RuntimeError('未进入电话主界面')

    def contacts(self):
        self.transition(lambda: self.click_node(self.tab_nodes('联系人')[0]),
                        self.contacts_ready, '未进入联系人页')

    def phone(self):
        self.wait_for(lambda: bool(self.tab_nodes('通话')), '电话底部导航未加载')
        self.transition(lambda: self.click_node(self.tab_nodes('通话')[0]),
                        self.phone_ready, '未进入电话页')
        self.clear_number()

    def search_box(self):
        if not self.contacts_ready():
            raise RuntimeError('搜索前不在联系人页')
        self.click('android:id/input')
        self.wait_for(lambda: self.has('search_text_cancel'), '未进入联系人搜索页')

    def search_contact(self):
        self.d(resourceId='android:id/input', packageName=self.PACKAGE).set_text('atest')
        self.wait_for(lambda: self.has('android:id/input', text='atest'), '搜索词未写入atest')
        self.wait_for(lambda: self.has('name', text='atest'), '未找到atest，请预置该测试联系人')
        matches = self.nodes('content_layout')
        matches = [n for n in matches if any(c.get('resource-id') == self.PREFIX+'name'
                   and c.get('text') == 'atest' for c in n.iter('node'))]
        if not matches:
            raise RuntimeError('没有atest搜索结果条目')
        # 点击第一条搜索记录进入详情；不点击详情中的号码或拨号按钮。
        first = min(matches, key=lambda n: (self.bounds(n)[1], self.bounds(n)[0]))
        self.click_node(first)
        self.wait_for(lambda: self.has('custom_title', text='atest'), '未进入atest联系人详情')

    def return_contacts(self):
        for _ in range(5):
            if self.contacts_ready():
                return
            self.foreground()
            if self.has('search_text_cancel'):
                self.click('search_text_cancel')
            else:
                self.shell('input keyevent 4')
            time.sleep(.6)
        self.wait_for(self.contacts_ready, '未返回联系人列表')

    def dialed_number(self):
        ns = self.nodes('digits')
        if not ns:
            return ''
        if len(ns) != 1:
            raise RuntimeError('拨号输入框不唯一')
        # MIUI在每位数字间插入零宽空格，按数字内容校验。
        return re.sub(r'[^0-9*#+]', '', ns[0].get('text', ''))

    def clear_number(self):
        for _ in range(30):
            before = self.dialed_number()
            if not before:
                return
            expected = before[:-1]
            self.transition(lambda: self.click('clear_button'),
                            lambda: self.dialed_number() == expected, '删除键未删除一位号码')
        raise RuntimeError('号码未清空')

    def keypad_control(self, description):
        controls = self.nodes(**{'content-desc': description})
        if len(controls) != 1:
            raise RuntimeError('拨号键盘开关不唯一：' + description)
        self.click_node(controls[0])

    def number_and_delete(self):
        if not self.phone_ready():
            raise RuntimeError('输入号码前不在电话页')
        if not self.has('one'):
            self.keypad_control('打开拨号键盘')
        self.wait_for(lambda: self.has('one'), '未展开拨号键盘')
        self.clear_number()
        for rid, expected in (('one', '1'), ('zero', '10'), ('zero', '100'),
                              ('eight', '1008'), ('six', '10086')):
            self.transition(lambda rid=rid: self.click(rid),
                            lambda expected=expected: self.dialed_number() == expected,
                            '拨号键输入结果不符')
        self.clear_number()
        self.wait_for(lambda: not self.dialed_number(), '10086未完全删除')
        self.wait_for(lambda: self.has('android:id/input'), '号码搜索结果未退出')

    def hide_keypad_by_blank(self):
        if self.dialed_number() or not self.has('android:id/input'):
            raise RuntimeError('号码未清空或仍在搜索状态，停止点击')
        # 在搜索栏/提示/记录条目之后、拨号键盘之前找真实空白，防止误点通话记录。
        ns = self.nodes()
        pads = [n for n in ns if n.get('resource-id') == self.PREFIX+'dialer_view_stub']
        if len(pads) != 1:
            raise RuntimeError('拨号键盘容器不可定位')
        top = self.bounds(pads[0])[1]
        blockers = [self.bounds(n) for n in ns if n.get('resource-id') in
                    ('android:id/input', self.PREFIX+'header_view',
                     self.PREFIX+'content_layout', self.PREFIX+'identify_numbers_text')]
        w, h = self.screen_size()
        bottom = max((b for _, _, _, b in blockers if b <= top), default=top)
        x, y = w*.5, (bottom+top)/2
        # 记录填满页面时没有安全空白，直接使用收起键盘控件适配该布局。
        safe_blank = top-bottom >= h*.025 and not any(
            l <= x <= r and t <= y <= b for l, t, r, b in blockers)
        if safe_blank:
            self.click_point(x, y)
            time.sleep(.6)
        # MIUI点击空白不自动收起键盘；完成表中点击后，通过有语义的控件收起。
        if self.has('one'):
            if self.dialed_number():
                raise RuntimeError('收起键盘前号码非空')
            self.keypad_control('关闭拨号键盘')
        self.wait_for(lambda: not self.has('one') and self.phone_ready(), '未收起拨号键盘')

    def browse(self, up=5, down=5):
        if not (self.contacts_ready() or (self.phone_ready() and not self.has('one'))):
            raise RuntimeError('浏览前必须在联系人列表或已收起键盘的通话记录页')
        for count, start, end in ((up, .78, .32), (down, .32, .78)):
            for _ in range(count):
                self.foreground()
                w, h = self.screen_size()
                self.shell('input swipe {} {} {} {} 400'.format(
                    round(w*.5), round(h*start), round(w*.5), round(h*end)))
                time.sleep(2)

    def launcher_gesture(self):
        def go_home():
            self.foreground()
            w, h = self.screen_size()
            self.shell('input swipe {} {} {} {} 250'.format(
                round(w*.5), round(h*.995), round(w*.5), round(h*.62)))
        self.transition(go_home,
                        lambda: 'launcher' in self.current_app()['activity'].lower(),
                        '上滑未返回桌面')
