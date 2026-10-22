"""动态性能场景共用的主屏控件定位与比例手势。"""
import logging
import re
import time
import xml.etree.ElementTree as ET

from Cases.Top48.baidu_common import BaiduDynamicCase


class DynamicAppCase(BaiduDynamicCase):
    def nodes(self, text=None, desc=None, rid=None, prefix=False, package=None):
        root = ET.fromstring(self.d.dump_hierarchy())
        package = package or self.PACKAGE
        result = []
        seen = set()
        for node in root.iter('node'):
            if node.get('package') != package or node.get('display-id', '0') != '0':
                continue
            if node.get('visible-to-user') == 'false':
                continue
            if rid and node.get('resource-id') != (rid if ':id/' in rid else package + ':id/' + rid):
                continue
            if text is not None and not (node.get('text', '').startswith(text) if prefix else node.get('text') == text):
                continue
            if desc is not None and not (node.get('content-desc', '').startswith(desc) if prefix else node.get('content-desc') == desc):
                continue
            box = self.bounds(node)
            if len(box) != 4 or box[2] <= box[0] or box[3] <= box[1]:
                continue
            key = (node.get('resource-id'), node.get('text'), node.get('content-desc'), box)
            if key not in seen:
                seen.add(key)
                result.append(node)
        return result

    def has(self, **kw):
        return bool(self.nodes(**kw))

    def node(self, index=0, **kw):
        nodes = self.nodes(**kw)
        if len(nodes) <= index:
            raise RuntimeError('未找到控件 {}（第 {} 个），当前应用 {}'.format(kw, index + 1, self.current_app()))
        return nodes[index]

    @staticmethod
    def bounds(node):
        return tuple(map(int, re.findall(r'-?\d+', node.get('bounds', ''))))

    def point(self, x, y):
        self.foreground()
        result = self.d.shell('input -d 0 swipe {0} {1} {0} {1} 250'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('主屏点击失败：' + result.output)

    def click(self, index=0, **kw):
        self.click_node(self.node(index=index, **kw))

    def click_node(self, node):
        left, top, right, bottom = self.bounds(node)
        width, height = self.screen_size()
        left, top = max(0, left), max(0, top)
        right, bottom = min(width, right), min(height, bottom)
        if right <= left or bottom <= top:
            raise RuntimeError('控件不在主屏可见区域')
        self.point((left + right) / 2, (top + bottom) / 2)

    def open_control(self, ready, message, **selector):
        self.transition(lambda: self.click(**selector), ready, message)

    def return_to(self, ready, message, limit=6):
        for _ in range(limit):
            if ready():
                return
            self.back()
            time.sleep(.7)
        self.wait_for(ready, message, timeout=3)

    def reveal(self, message, attempts=6, **selector):
        for _ in range(attempts):
            if self.has(**selector):
                return
            self.swipe()
            time.sleep(1)
        if not self.has(**selector):
            raise RuntimeError('{}：{}'.format(message, selector))

    def pct(self, x, y):
        if not (0 < x < 1 and 0 < y < 1):
            raise ValueError('比例必须在 0 到 1 之间')
        width, height = self.screen_size()
        self.point(width * x, height * y)

    def swipe(self, x1=.5, y1=.78, x2=.5, y2=.32, duration=400):
        self.foreground()
        width, height = self.screen_size()
        result = self.d.shell('input -d 0 swipe {} {} {} {} {}'.format(
            round(width*x1), round(height*y1), round(width*x2), round(height*y2), duration))
        if result.exit_code:
            raise RuntimeError('主屏滑动失败：' + result.output)

    def browse(self, up=5, down=5, pause=2):
        for _ in range(up):
            self.swipe()
            time.sleep(pause)
        for _ in range(down):
            self.swipe(y1=.32, y2=.78)
            time.sleep(pause)

    def alternating(self, count=5, pause=2):
        for _ in range(count):
            self.browse(1, 1, pause)

    def back(self):
        self.foreground()
        result = self.d.shell('input -d 0 keyevent 4')
        if result.exit_code:
            raise RuntimeError('返回失败：' + result.output)
        time.sleep(.8)

    def start(self):
        # 启动与后续前台检查统一使用主显示屏 display 0。
        output = self.d.shell(['cmd', 'package', 'resolve-activity', '--brief',
                               '-a', 'android.intent.action.MAIN',
                               '-c', 'android.intent.category.LAUNCHER', self.PACKAGE]).output
        component = next((line.strip() for line in output.splitlines()
                          if line.strip().startswith(self.PACKAGE + '/')), None)
        if not component:
            raise RuntimeError('未找到应用启动入口：' + self.PACKAGE)
        result = self.d.shell(['am', 'start', '-W', '--display', '0', '-n', component])
        if result.exit_code or 'Error:' in result.output:
            raise RuntimeError('应用启动失败：' + result.output)
        self.wait_for(lambda: self.current_app()['package'] == self.PACKAGE,
                      '应用未进入前台', timeout=25)
        time.sleep(2)

    def home(self):
        self.foreground()
        self.swipe(.5, .995, .5, .62, 250)
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(),
                      '未返回桌面', timeout=8)

    def require(self, **kw):
        if not self.has(**kw):
            raise RuntimeError('页面不符合预期，缺少控件 {}'.format(kw))

    def after(self, action, **kw):
        action()
        self.wait_for(lambda: self.has(**kw), '点击后未出现控件 {}'.format(kw))

    def first_shop(self):
        # 搜索结果动态排序；取当前屏幕第一条商户条目，而非写死商户名称。
        width, height = self.screen_size()
        nodes = [n for n in self.nodes(desc='gridView_item_wrapper')
                 if self.bounds(n)[2] - self.bounds(n)[0] > width * .8
                 and self.bounds(n)[3] - self.bounds(n)[1] > height * .09
                 and any('¥' in c.get('text', '') and '/人' in c.get('text', '')
                         for c in n.iter('node'))]
        if not nodes:
            raise RuntimeError('未找到烧烤搜索结果的商户卡片')
        first = sorted(nodes, key=lambda n: self.bounds(n)[1])[0]
        # 首条标题可能被吸顶筛选栏遮挡，点击同卡片内的“人均价格”行；
        # 该行属于商户详情入口，既避开筛选栏，也避开下方团购子项。
        price = next(c for c in first.iter('node')
                     if '¥' in c.get('text', '') and '/人' in c.get('text', ''))
        self.click_node(price)
