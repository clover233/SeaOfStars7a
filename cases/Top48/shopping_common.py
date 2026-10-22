"""商城用例的控件定位、比例手势、可选步骤和逐步性能采集。"""
import json
import logging
import re
import os
import time
import xml.etree.ElementTree as ET

from Cases.Top48.dynamic_apps_common import DynamicAppCase
from Cases.Top48.weixin_common import WeixinDynamicCase
from aw_new import SeaOfStarsAW


class StepUnavailable(Exception):
    """当前版本/账号确实没有此入口，允许跳过并记录原因。"""


class AccountBlocked(StepUnavailable):
    """安全验证遮挡应用，后续业务步骤都依赖人工完成账号验证。"""
    blocks_case = True


class ShoppingDynamicCase(DynamicAppCase):
    def nodes(self, rid=None, **kwargs):
        # React Native 使用不带包名前缀的 testID，京东模块使用独立资源包名。
        nodes = super().nodes(**kwargs)
        if rid:
            nodes = [n for n in nodes if n.get('resource-id') == rid
                     or n.get('resource-id') == self.PACKAGE + ':id/' + rid]
        return nodes

    def point(self, x, y):
        # 显式指定主屏，且维持 250ms 按下。本机部分商城按钮会过滤
        # adb tap 的过短触摸；同点 swipe 不产生位移，也不会触发长按。
        super().point(x, y)

    def back(self):
        self.foreground()
        result = self.d.shell('input -d 0 keyevent 4')
        if result.exit_code:
            raise RuntimeError('主屏返回失败：' + result.output)
        time.sleep(1)

    def home(self):
        self.foreground()
        self.swipe(.5, .995, .5, .62, 250)
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(),
                      '滑动后未返回桌面', timeout=8)

    def activity_has(self, *names):
        return any(name in self.current_app()['activity'] for name in names)

    def find_label(self, *labels, prefix=False):
        nodes = self.nodes()
        width, height = self.d.window_size()
        for label in labels:
            matches = [n for n in nodes
                       if any((n.get(k, '').startswith(label) if prefix
                               else n.get(k) == label)
                              for k in ('text', 'content-desc'))
                       and 0 <= self.bounds(n)[0] < width
                       and height*.06 <= (self.bounds(n)[1]+self.bounds(n)[3])/2 < height*.975]
            if matches:
                # 优先点击可点击的父节点，避开同名的装饰性文字。
                return sorted(matches, key=lambda n: n.get('clickable') != 'true')[0]
        return None

    def label(self, *labels, prefix=False, optional=False):
        node = self.find_label(*labels, prefix=prefix)
        if node is None:
            # H5 和原生页面往往先显示框架，再填充文字，不能把这一瞬态当成功能缺失。
            time.sleep(.6)
            node = self.find_label(*labels, prefix=prefix)
        if node is None:
            if optional:
                raise StepUnavailable('当前页面没有入口：' + '/'.join(labels))
            raise RuntimeError('当前页面缺少必需入口：' + '/'.join(labels))
        self.click_node(node)

    def check_access(self):
        if self.activity_has('JDRiskHandleActivity'):
            raise AccountBlocked('京东要求账号安全验证，跳过当前受限功能；验证后可重新运行')
        if self.PACKAGE == 'com.jingdong.app.mall' and self.activity_has(
                'SMSCheckActivity', 'LoginActivity', 'LoginMainActivity'):
            raise StepUnavailable('京东当前功能要求重新登录，跳过依赖登录的步骤')

    def dismiss_popup(self):
        labels = ('关闭浮层活动', '知道了', '我知道了', '暂不', '以后再说')
        for node in self.nodes():
            if node.get('text') in labels or node.get('content-desc') in labels:
                self.click_node(node)
                time.sleep(.5)
                return

    def launch(self):
        self.start()
        self.check_access()
        self.main_page()

    def group(self, key, action):
        self._groups[key] = False
        action()
        self._groups[key] = True

    def within(self, key, action):
        if not self._groups.get(key, False):
            raise StepUnavailable('前置功能不可用：' + key)
        self.check_access()
        action()

    def reveal_label(self, *labels, attempts=5):
        for _ in range(attempts + 1):
            node = self.find_label(*labels, prefix=True)
            if node is not None:
                return node
            self.swipe()
            time.sleep(.7)
        raise StepUnavailable('滑动后仍未找到：' + '/'.join(labels))

    @SeaOfStarsAW.function_log
    def run_case(self):
        if not getattr(self, '_prepared', False):
            self.set_up()
        results = []
        try:
            for run in range(self.TEST_TIME):
                self._groups = {}
                for index, (name, action, stay) in enumerate(self.steps(), 1):
                    record = dict(run=run + 1, step=index, name=name, status='PASS')
                    logging.info('%s、%s', index, name)
                    SeaOfStarsAW.start_perfetto_trace()
                    failed = False
                    try:
                        self.check_access()
                        action()
                        time.sleep(stay)
                        self.check_access()
                    except StepUnavailable as error:
                        record.update(status='SKIP', reason=str(error))
                        logging.warning('SKIP %s、%s：%s', index, name, error)
                    except Exception as error:
                        failed = True
                        record.update(status='FAIL', reason=str(error))
                        logging.exception('步骤 %s、%s 失败', index, name)
                        raise
                    finally:
                        results.append(record)
                        try:
                            SeaOfStarsAW.stop_and_get_perfetto_trace(
                                self.trace_dir_path, self.__class__.__name__,
                                'step_{}、{}{}'.format(index, name,
                                    '' if record['status'] == 'PASS' else '_' + record['status']),
                                '', self.screenshot_dir_path)
                        except Exception as error:
                            if not failed:
                                record.update(status='FAIL', reason='trace 导出失败：' + str(error))
                                raise
                            logging.exception('失败步骤的 trace 导出失败')
        finally:
            path = os.path.join(self.result_dir_path, 'shopping_steps.json')
            with open(path, 'w', encoding='utf-8') as output:
                json.dump(results, output, ensure_ascii=False, indent=2)


class VisualShoppingDynamicCase(ShoppingDynamicCase):
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
