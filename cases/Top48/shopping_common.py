"""商城用例的控件定位、比例手势、可选步骤和逐步性能采集。"""
import json
import logging
import os
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase
from aw_new import SeaOfStarsAW


class StepUnavailable(Exception):
    """当前版本/账号确实没有此入口，允许跳过并记录原因。"""


class ShoppingDynamicCase(DynamicAppCase):
    def nodes(self, rid=None, **kwargs):
        # React Native 使用不带包名前缀的 testID，京东模块使用独立资源包名。
        nodes = super().nodes(**kwargs)
        if rid:
            nodes = [n for n in nodes if n.get('resource-id') == rid
                     or n.get('resource-id') == self.PACKAGE + ':id/' + rid]
        return nodes

    def point(self, x, y):
        # 双屏 Android 设备的默认注入屏幕可能变化，显式指定主屏。
        self.foreground()
        result = self.d.shell('input -d 0 tap {} {}'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('主屏点击失败：' + result.output)

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
            raise RuntimeError('京东要求安全验证，请在手机上手动验证后重新运行')

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
                        except Exception:
                            if not failed:
                                raise
                            logging.exception('失败步骤的 trace 导出失败')
        finally:
            path = os.path.join(self.result_dir_path, 'shopping_steps.json')
            with open(path, 'w', encoding='utf-8') as output:
                json.dump(results, output, ensure_ascii=False, indent=2)
