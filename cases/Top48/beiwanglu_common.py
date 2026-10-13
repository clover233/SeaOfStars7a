"""小米备忘录动态场景；控件定位及键盘区域比例手势。"""
import time
import re
import xml.etree.ElementTree as ET

from Cases.Top48.baidu_common import BaiduDynamicCase
from aw_new import SeaOfStarsAW


class BeiwangluDynamicCase(BaiduDynamicCase):
    PACKAGE = 'com.miui.notes'
    PREFIX = PACKAGE + ':id/'
    IME = 'com.baidu.input_mi/.ImeService'
    IME_PACKAGE = 'com.baidu.input_mi'
    all_app_package_list = [PACKAGE]

    def shell(self, command):
        result = self.d.shell(command)
        if result.exit_code:
            raise RuntimeError('设备命令失败：{}；{}'.format(command, result.output))
        return result.output

    def click_point(self, x, y):
        self.foreground()
        # 此机 u2 的短按可能被过滤。系统注入的 100ms 原地手势已实测可用。
        self.shell('input swipe {0} {1} {0} {1} 100'.format(round(x), round(y)))

    def obj(self, **selector):
        selector.setdefault('packageName', self.PACKAGE)
        return self.d(**selector)

    def has(self, **selector):
        return bool(self.nodes(**selector))

    def nodes(self, **selector):
        keys = {'packageName': 'package', 'resourceId': 'resource-id',
                'description': 'content-desc', 'text': 'text', 'className': 'class'}
        selector.setdefault('packageName', self.PACKAGE)
        return [n for n in ET.fromstring(self.d.dump_hierarchy()).iter('node')
                if all(n.get(keys[k]) == v for k, v in selector.items())]

    def box(self, **selector):
        nodes = self.nodes(**selector)
        if len(nodes) != 1:
            raise RuntimeError('控件不存在或不唯一：{}'.format(selector))
        left, top, right, bottom = map(int, re.findall(r'\d+', nodes[0].get('bounds')))
        return dict(left=left, top=top, right=right, bottom=bottom)

    def click(self, **selector):
        self.foreground()
        # 输入法菜单的虚拟节点可见于 hierarchy，但 UiSelector.wait 可能漏报。
        b = self.box(**selector)
        self.click_point((b['left'] + b['right']) / 2, (b['top'] + b['bottom']) / 2)

    def is_home(self):
        return self.has(resourceId=self.PREFIX + 'rvNotes')

    def notes_home(self):
        for _ in range(5):
            if self.is_home():
                return
            self.foreground()
            self.shell('input keyevent 4')
            time.sleep(.6)
        self.wait_for(self.is_home, '未返回备忘录笔记列表')

    def launch(self):
        self.d.app_start(self.PACKAGE, use_monkey=True)
        self.wait_for(lambda: self.current_app()['package'] == self.PACKAGE, '备忘录未启动')
        self.notes_home()

    def new_note(self):
        if not self.is_home():
            raise RuntimeError('新建笔记前不在笔记列表')
        # 当前新版底栏标签错位：btnAdd 实际为导入，右侧加号为 btnHandwrite。
        # 仅在该新版底栏存在时使用实测 ID；旧版使用“新建笔记”语义。
        if self.has(resourceId=self.PREFIX + 'bottomBar'):
            self.click(resourceId=self.PREFIX + 'btnHandwrite')
        else:
            self.click(description='新建笔记')
        self.wait_for(lambda: self.has(resourceId=self.PREFIX + 'editor_root_container')
                      and self.has(description='完成'), '未进入新建笔记编辑页')

    def write_note(self):
        editor = self.obj(className='android.widget.EditText', focused=True)
        if not editor.wait(timeout=5):
            raise RuntimeError('新建笔记没有聚焦的编辑器')
        # set_text 写中文，不依赖输入法候选；待办步骤单独使用真实 26 键。
        editor.set_text('动态')
        self.wait_for(lambda: self.has(className='android.widget.EditText', text='动态'),
                      '笔记正文未写入动态')
        self.click(description='完成')
        self.wait_for(lambda: self.has(description='分享') and not self.has(description='完成'),
                      '笔记未保存')

    def todos(self):
        self.click(description='待办')
        self.wait_for(lambda: self.has(resourceId=self.PREFIX + 'content_add'), '未进入待办列表')

    def new_todo(self):
        installed = self.shell('ime list -s').splitlines()
        if self.IME not in installed:
            raise RuntimeError('26 键实测输入法未安装：{}'.format(self.IME))
        self._original_ime = self.shell('settings get secure default_input_method').strip()
        self.shell('ime set ' + self.IME)
        self.click(resourceId=self.PREFIX + 'content_add')
        self.wait_for(lambda: self.has(resourceId=self.PREFIX + 'rich_editor'), '未打开待办编辑框')
        self.wait_for(lambda: self.has(packageName=self.IME_PACKAGE, resourceId='android:id/inputArea'),
                      '未拉起可见键盘')

    def keyboard_box(self):
        return self.box(packageName=self.IME_PACKAGE, resourceId='android:id/inputArea')

    def key_ratio(self, x, y):
        # 在键盘 inputArea 实时边界内换算，不使用固定分辨率/绝对屏幕坐标。
        b = self.keyboard_box()
        self.click_point(b['left'] + (b['right'] - b['left']) * x,
                         b['top'] + (b['bottom'] - b['top']) * y)
        time.sleep(.2)

    def type_todo(self):
        # 工具栏位于 candidatesArea；打开布局菜单，明确选择英文26键。
        b = self.box(packageName=self.IME_PACKAGE, resourceId='android:id/candidatesArea')
        self.click_point(b['left'] + (b['right'] - b['left']) * .21,
                         (b['top'] + b['bottom']) / 2)
        self.wait_for(lambda: self.has(packageName=self.IME_PACKAGE, description='英文26键'),
                      '未打开键盘布局选择菜单')
        self.click(packageName=self.IME_PACKAGE, description='英文26键')
        self.wait_for(lambda: not self.has(packageName=self.IME_PACKAGE, description='英文26键'),
                      '未切换英文26键')
        for x, y in ((.45, .12), (.25, .12), (.20, .37), (.45, .12)):
            self.key_ratio(x, y)
        self.wait_for(lambda: self.has(resourceId=self.PREFIX + 'rich_editor', text='test'),
                      '26 键输入结果不是 test')
        self.key_ratio(.92, .87)  # 键盘回车，实测会将正文转为待办清单。
        self.wait_for(lambda: any('test' in n.get('text', '') for n in
                      ET.fromstring(self.d.dump_hierarchy()).iter('node')
                      if n.get('resource-id') == self.PREFIX + 'editor'),
                      '回车未生成 test 待办项')

    def save_todo(self):
        self.click(resourceId=self.PREFIX + 'send_button')
        self.wait_for(lambda: not self.has(resourceId=self.PREFIX + 'todo_edit_mask')
                      and self.has(resourceId=self.PREFIX + 'content', text='test'),
                      '待办未保存到列表')
        self.restore_ime()

    def restore_ime(self):
        original = getattr(self, '_original_ime', None)
        if original:
            self.shell('ime set ' + original)
            self._original_ime = None

    def browse_notes(self):
        if not self.is_home():
            raise RuntimeError('浏览前不在笔记列表')
        for start, end in ((.78, .32),) * 2 + ((.32, .78),) * 2:
            self.foreground()
            w, h = self.d.window_size()
            self.shell('input swipe {} {} {} {} 400'.format(
                round(w * .5), round(h * start), round(w * .5), round(h * end)))
            time.sleep(2)

    def first_note(self):
        cards = self.nodes(resourceId=self.PREFIX + 'cardView')
        if not cards:
            raise RuntimeError('笔记列表为空，请先预置至少一条笔记')
        # 按可见卡片的 top、left 排序，适配双列布局；不依赖笔记标题。
        boxes = [list(map(int, re.findall(r'\d+', n.get('bounds')))) for n in cards]
        left, top, right, bottom = min(boxes, key=lambda b: (b[1], b[0]))
        self.click_point((left + right) / 2, (top + bottom) / 2)
        self.wait_for(lambda: self.has(resourceId=self.PREFIX + 'editor_root_container'),
                      '未打开第一条笔记')

    def launcher_gesture(self):
        self.foreground()
        w, h = self.d.window_size()
        self.shell('input swipe {} {} {} {} 250'.format(
            round(w * .5), round(h * .995), round(w * .5), round(h * .62)))
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(), '上滑未返回桌面')

    @SeaOfStarsAW.function_log
    def run_case(self):
        try:
            super().run_case()
        finally:
            self.restore_ime()
