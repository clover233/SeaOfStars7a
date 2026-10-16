"""微博/唯品会共用定位：优先活动窗口，兼容标准 uiautomator2。"""
import xml.etree.ElementTree as ET
import time
import re

from Cases.Top48.shopping_common import ShoppingDynamicCase
from Cases.Top48.weixin_common import WeixinDynamicCase


class WeiboVipDynamicCase(ShoppingDynamicCase):
    # 复用工程现有的本地 Vision OCR，控件树缺失时按截图文字边界兜底。
    prepare_ocr = WeixinDynamicCase.prepare_ocr
    normalized = staticmethod(WeixinDynamicCase.normalized)
    screen = WeixinDynamicCase.screen
    invalidate = WeixinDynamicCase.invalidate

    def screen_size(self):
        # 折叠测试机的后台 Display 1 为横屏，adbutils.rotation() 可能取错屏。
        output = self.d.shell('dumpsys window displays').output
        match = re.search(r'Display: mDisplayId=0\b[^\n]*\n[^\n]*\bcur=(\d+)x(\d+)', output)
        if match:
            return tuple(map(int, match.groups()))
        return self.d.screenshot(display_id=0).size

    def click_node(self, node):
        l, t, r, b = self.bounds(node)
        width, height = self.screen_size()
        l, t, r, b = max(0, l), max(0, t), min(width, r), min(height, b)
        if r <= l or b <= t:
            raise RuntimeError('控件不在主屏可见区域')
        self.point((l+r)/2, (t+b)/2)

    def pct(self, x, y):
        if not (0 < x < 1 and 0 < y < 1):
            raise ValueError('点击坐标必须是屏幕比例')
        width, height = self.screen_size()
        self.point(width*x, height*y)

    def swipe(self, x1=.5, y1=.78, x2=.5, y2=.32, duration=400):
        self.foreground()
        width, height = self.screen_size()
        result = self.d.shell('input mouse -d 0 swipe {} {} {} {} {}'.format(
            round(width*x1), round(height*y1), round(width*x2), round(height*y2), duration))
        if result.exit_code:
            raise RuntimeError('主屏滑动失败：' + result.output)
        self.invalidate()

    def set_up(self):
        super().set_up()
        self._screen_cache = None
        self._ocr_command = None
        self.prepare_ocr()

    def tap_visual(self, row):
        self.pct(row['x']+row['w']/2, row['y']+row['h']/2)

    def visual_rows(self):
        if not hasattr(self, '_ocr_command'):
            self._screen_cache = None
            self._ocr_command = None
            self.prepare_ocr()
        return self.screen()

    def find_label(self, *labels, prefix=False):
        width, height = self.screen_size()
        native = self.nodes()
        for label in labels:
            for node in native:
                if any((node.get(k, '').startswith(label) if prefix else node.get(k) == label)
                       for k in ('text', 'content-desc')) and 0 <= self.bounds(node)[0] < width and .06*height < (self.bounds(node)[1]+self.bounds(node)[3])/2 < height*.975:
                    return node
        for label in labels:
            query = self.normalized(label)
            for row in self.visual_rows():
                text = self.normalized(row['text'])
                if (text.startswith(query) if prefix else text == query) and .06 < row['y'] < .975:
                    return ET.Element('node', text=row['text'], **{'package': self.PACKAGE,
                        'bounds': '[{},{}][{},{}]'.format(round(width*row['x']), round(height*row['y']),
                            round(width*(row['x']+row['w'])), round(height*(row['y']+row['h'])))})
        return None

    def point(self, x, y):
        self.foreground()
        result = self.d.shell('input mouse -d 0 swipe {0} {1} {0} {1} 250'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('主屏点击失败：' + result.output)
        self.invalidate()

    def back(self):
        self.foreground()
        self.d.press('back')
        self.invalidate()
        time.sleep(.7)

    def home(self):
        self.foreground()
        width, height = self.screen_size()
        self.d.shell('input touchscreen -d 0 swipe {} {} {} {} 300'.format(
            round(width*.5), round(height*.995), round(width*.5), round(height*.62)))
        time.sleep(.8)
        if 'launcher' not in self.current_app()['activity'].lower():
            self.d.shell('input -d 0 keyevent HOME')
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(), '未返回主屏桌面')

    def hierarchy(self):
        # 工程的 Android 17 u2 支持活动窗口 root；全窗口 dump 偶尔会循环
        # 返回底栏。标准版没有该参数时退回常规 dump，不强制依赖定制 jar。
        if getattr(self, '_active_root_supported', True):
            try:
                result = self.d.dump_hierarchy(root_in_active=True)
                self._active_root_supported = True
                return result
            except TypeError:
                self._active_root_supported = False
            except Exception as error:
                if 'method parameters invalid' not in str(error):
                    raise
                self._active_root_supported = False
        return self.d.dump_hierarchy()

    def nodes(self, text=None, desc=None, rid=None, prefix=False, package=None):
        package = package or self.PACKAGE
        found, seen = [], set()
        for node in ET.fromstring(self.hierarchy()).iter('node'):
            if node.get('package') != package or node.get('display-id', '0') != '0':
                continue
            if node.get('visible-to-user') == 'false':
                continue
            if rid and node.get('resource-id') not in (rid, package+':id/'+rid):
                continue
            if any(value is not None and not (node.get(key, '').startswith(value) if prefix else node.get(key) == value)
                   for key, value in (('text', text), ('content-desc', desc))):
                continue
            box = self.bounds(node)
            if len(box) != 4 or box[2] <= box[0] or box[3] <= box[1]:
                continue
            key = (node.get('resource-id'), node.get('text'), node.get('content-desc'), box)
            if key not in seen:
                seen.add(key)
                found.append(node)
        return found
