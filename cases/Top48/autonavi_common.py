"""高德地图动态性能场景共用的页面定位和手势。"""
import logging
import re
import time
import xml.etree.ElementTree as ET

from Cases.Top48.baidu_common import BaiduDynamicCase
from Cases.Top48.main_display import MainDisplayMixin, ForegroundNotReady
from aw_new import SeaOfStarsAW


class AutonaviDynamicCase(MainDisplayMixin, BaiduDynamicCase):
    PACKAGE = 'com.autonavi.minimap'
    AMAP = PACKAGE
    XHS = 'com.xingin.xhs'
    DOUYIN = 'com.ss.android.ugc.aweme'
    PREFIX = PACKAGE + ':id/'
    PERMISSIONS = ('ACCESS_COARSE_LOCATION', 'ACCESS_FINE_LOCATION')
    BACKGROUND_NAVIGATION = False
    all_app_package_list = [PACKAGE]

    @SeaOfStarsAW.function_log
    def set_up(self):
        for package in self.all_app_package_list:
            if not self.d.app_info(package):
                raise RuntimeError('未安装应用：{}'.format(package))
        super().set_up()
        if self.BACKGROUND_NAVIGATION:
            sdk = int(self.d.shell('getprop ro.build.version.sdk').output)
            permissions = ['RECORD_AUDIO']
            if sdk >= 29:
                permissions.append('ACCESS_BACKGROUND_LOCATION')
            for permission in permissions:
                result = self.d.shell('pm grant {} android.permission.{}'.format(self.AMAP, permission))
                if result.exit_code or 'Exception' in result.output or 'Error' in result.output:
                    raise RuntimeError('高德导航授权失败 {}：{}'.format(permission, result.output))

    def nodes(self):
        self.foreground()
        width, height = self.d.window_size()
        result = []
        for node in ET.fromstring(self.d.dump_hierarchy()).iter('node'):
            if (node.get('package') != self.PACKAGE or node.get('display-id', '0') != '0'
                    or node.get('visible-to-user') == 'false'):
                continue
            left, top, right, bottom = self.bounds(node)
            if (right > left and bottom > top and left < width and top < height
                    and right > 0 and bottom > 0):
                result.append(node)
        return result

    def has(self, *, text=None, desc=None, rid=None, class_name=None):
        return any((text is None or n.get('text') == text) and
                   (desc is None or n.get('content-desc') == desc) and
                   (rid is None or n.get('resource-id') == rid) and
                   (class_name is None or n.get('class') == class_name)
                   for n in self.nodes())

    @staticmethod
    def bounds(node):
        numbers = [int(x) for x in re.findall(r'-?\d+', node.get('bounds', ''))]
        if len(numbers) != 4:
            raise RuntimeError('控件无有效 bounds：{}'.format(node.attrib))
        return numbers

    def node_click(self, node):
        left, top, right, bottom = self.bounds(node)
        width, height = self.d.window_size()
        left, top, right, bottom = max(0, left), max(0, top), min(width, right), min(height, bottom)
        if right <= left or bottom <= top:
            raise RuntimeError('控件不在主屏可见区域')
        self.click_point((left + right) // 2, (top + bottom) // 2)

    def click_point(self, x, y):
        self.foreground()
        result = self.d.shell('input -d 0 tap {} {}'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('主屏点击失败：' + result.output)

    def find_node(self, *, text=None, desc=None, rid=None, class_name=None, first=False):
        matches = [n for n in self.nodes()
                   if (text is None or n.get('text') == text)
                   and (desc is None or n.get('content-desc') == desc)
                   and (rid is None or n.get('resource-id') == rid)
                   and (class_name is None or n.get('class') == class_name)]
        if not matches:
            raise RuntimeError('未找到控件：{}'.format((text, desc, rid, class_name)))
        if not first and len(matches) != 1:
            raise RuntimeError('控件不唯一：{}'.format((text, desc, rid, class_name)))
        return matches[0]

    def click_node(self, **kwargs):
        self.node_click(self.find_node(**kwargs))

    def launch(self, package=AMAP):
        self.PACKAGE = package
        self.d.app_start(package, use_monkey=True)
        self.wait_for(lambda: self.current_app()['package'] == package,
                      '未进入应用 {}'.format(package), timeout=25)

    def amap_home(self):
        self.PACKAGE = self.AMAP
        if self.has(rid=self.PREFIX + 'txt_hotword'):
            return
        if self.has(desc='退出导航按钮') or self.has(rid=self.PREFIX + 'hc_navi_exit_navi_bar_positive'):
            raise RuntimeError('仍在导航；应先执行退出导航步骤')
        # 高德返回栈含路线、地点、搜索结果和输入页；按页面状态退出。
        for _ in range(6):
            if self.has(rid=self.PREFIX + 'txt_hotword'):
                return
            if self.has(text='首页', rid=self.PREFIX + 'tab_name_v2'):
                self.click_node(text='首页', rid=self.PREFIX + 'tab_name_v2')
            else:
                self.d.press('back')
            time.sleep(0.6)
        self.wait_for(lambda: self.has(rid=self.PREFIX + 'txt_hotword'), '未返回高德地图首页')

    def search_page(self):
        self.transition(lambda: self.click_node(rid=self.PREFIX + 'txt_hotword'),
                        self.search_page_ready,
                        '未进入高德搜索页')

    def search_page_ready(self):
        return any(n.get('class') == 'android.widget.EditText' and n.get('enabled') == 'true'
                   for n in self.nodes())

    def dismiss_account_prompt(self):
        if 'AccountActivity' not in self.current_app()['activity']:
            return
        if not (self.has(desc='本机号码一键登录') and self.has(desc='关闭页面')):
            raise RuntimeError('高德账号页面未就绪，请先核实登录状态')
        # 搜索后会弹出可关闭的一键登录引导；返回后仍是已加载的搜索结果。
        self.d.press('back')
        self.wait_for(lambda: 'AccountActivity' not in self.current_app()['activity'],
                      '高德登录引导未关闭')

    def search(self, query, result=None):
        # EditText 可 set_text；首页自绘搜索框可能暂未生成 EditText，先点框聚焦。
        edit = next((n for n in self.nodes() if n.get('class') == 'android.widget.EditText'
                     and n.get('enabled') == 'true'), None)
        if edit is None:
            width, height = self.d.window_size()
            edit = next((n for n in self.nodes()
                         if n.get('class') == 'android.view.View'
                         and n.get('text')
                         and (lambda b: b[0] < width * .25 and
                              height * .05 < b[1] < height * .12 and
                              b[2] - b[0] > width * .3)(self.bounds(n))), None)
        if edit is not None:
            self.node_click(edit)
        self.wait_for(lambda: any(
            n.get('class') == 'android.widget.EditText' and n.get('enabled') == 'true'
            and n.get('focused') == 'true' for n in self.nodes()),
            '未聚焦高德搜索框', timeout=5)
        self.d(className='android.widget.EditText', enabled=True).set_text(query)
        self.wait_for(lambda: self.has(text=query, class_name='android.widget.EditText'),
                      '搜索词未写入 {}'.format(query), timeout=6)
        def results_ready():
            self.dismiss_account_prompt()
            return ((self.has(desc='搜索框，' + query)
                     or self.has(text=query, class_name='android.widget.EditText'))
                    and self.has(desc=result or query, class_name='android.view.ViewGroup'))
        def submit_ready():
            self.dismiss_account_prompt()
            return self.has(desc='搜索', class_name='android.view.ViewGroup')
        self.wait_for(submit_ready, '高德搜索按钮未就绪')
        self.click_node(desc='搜索', class_name='android.view.ViewGroup')
        self.wait_for(results_ready, '未出现搜索结果 {}'.format(query), timeout=20)

    def result_route(self, result):
        # 路线属于指定结果行，不能用全局“路线”，否则会点到第二条。
        self.transition(lambda: self.tap_route_child(result),
                        lambda: any(n.get('content-desc', '').startswith('终点，')
                                    for n in self.nodes()),
                        '未进入路线规划')

    def tap_route_child(self, result):
        row = self.find_node(desc=result, class_name='android.view.ViewGroup')
        left, top, right, bottom = self.bounds(row)
        # 新版将“路线”导出为结果标题的兄弟节点；用同一行的几何关系关联，
        # 不能全局取第一个按钮，也不能假定它永远是标题的 child。
        routes = [node for node in row.iter('node') if node.get('content-desc') == '路线'
                  and node.get('class') == 'android.view.ViewGroup']
        if not routes:
            routes = [node for node in self.nodes()
                      if node.get('content-desc') == '路线' and node.get('class') == 'android.view.ViewGroup'
                      and (lambda box: top <= (box[1]+box[3])/2 <= bottom
                           and box[0] >= right)(self.bounds(node))]
        if len(routes) != 1:
            raise RuntimeError('目的地路线按钮未找到或不唯一 {}'.format(result))
        self.node_click(routes[0])

    def drive(self):
        for _ in range(3):
            if any(n.get('content-desc', '').startswith('驾车，') and
                   '已选中' in n.get('content-desc', '') for n in self.nodes()):
                return
            candidates = [n for n in self.nodes() if n.get('content-desc', '') == '驾车'
                          or n.get('content-desc', '').startswith('驾车，')]
            if candidates:
                self.node_click(candidates[0])
                self.wait_for(lambda: any(n.get('content-desc', '').startswith('驾车，') and
                                          '已选中' in n.get('content-desc', '')
                                          for n in self.nodes()), '未切换驾车路线')
                return
            self.swipe_ratio(.18, .16, .82, .16)
        raise RuntimeError('路线方式栏没有驾车标签')

    def start_navigation(self):
        if self.has(desc='退出导航按钮'):
            return
        if not self.has(text='驾车导航使用提示'):
            self.wait_for(lambda: self.has(desc='开始导航', class_name='android.view.ViewGroup'),
                          '路线未加载开始导航按钮', timeout=30)
            self.transition(lambda: self.click_node(desc='开始导航', class_name='android.view.ViewGroup'),
                            lambda: self.has(desc='退出导航按钮') or self.has(text='驾车导航使用提示'),
                            '未开始导航')
        if self.has(text='驾车导航使用提示'):
            # 用户已明确同意该导航提示；只处理这一已核实的页面。
            logging.info('确认驾车导航使用提示')
            node = self.find_node(text='同意', class_name='android.view.View')
            left, top, right, bottom = self.bounds(node)
            # 该页忽略驻留手势，使用普通主屏 tap。
            result = self.d.shell('input -d 0 tap {} {}'.format((left+right)//2, (top+bottom)//2))
            if result.exit_code:
                raise RuntimeError('导航使用提示确认失败：' + result.output)
        self.wait_for(lambda: self.has(desc='退出导航按钮'), '未进入驾车导航页面', timeout=25)

    def open_exit(self):
        self.transition(lambda: self.click_node(desc='退出导航按钮'),
                        lambda: self.has(rid=self.PREFIX + 'hc_navi_exit_navi_bar_positive'),
                        '未出现退出导航确认条')

    def confirm_exit(self):
        # 确认条在 trace 导出期间可能收起；只在它确实消失时重新打开。
        if not self.has(rid=self.PREFIX + 'hc_navi_exit_navi_bar_positive'):
            self.open_exit()
        self.click_node(rid=self.PREFIX + 'hc_navi_exit_navi_bar_positive')
        self.wait_for(lambda: not self.has(desc='退出导航按钮') and
                      not self.has(rid=self.PREFIX + 'hc_navi_exit_navi_bar_positive'),
                      '导航未退出', timeout=20)

    def navigation_visible(self, message='后台导航未恢复，请确认导航已启动且后台未被清理'):
        self.wait_for(lambda: self.has(desc='退出导航按钮'),
                      message, timeout=25)

    def swipe_ratio(self, x1, y1, x2, y2, duration=0.4):
        self.foreground()
        width, height = self.d.window_size()
        self.d.swipe(round(width * x1), round(height * y1),
                     round(width * x2), round(height * y2), duration=duration)

    def scroll_page(self, up=1, down=1, x=0.5, upper=0.3, lower=0.78, pause=1):
        for _ in range(up):
            self.swipe_ratio(x, lower, x, upper)
            time.sleep(pause)
        for _ in range(down):
            self.swipe_ratio(x, upper, x, lower)
            time.sleep(pause)

    def map_swipe(self, direction):
        gestures = {'up': (.5, .47, .5, .26), 'down': (.5, .26, .5, .47),
                    'left': (.75, .36, .25, .36), 'right': (.25, .36, .75, .36)}
        self.swipe_ratio(*gestures[direction])

    def map_pinch(self):
        self.foreground()
        width, height = self.d.window_size()
        point = lambda x, y: (round(width * x), round(height * y))
        # 两指分开为放大，合拢为缩小；全部按屏幕比例生成。
        self.d().gesture(point(.46, .35), point(.54, .35),
                         point(.27, .35), point(.73, .35), steps=30)
        time.sleep(1)
        self.d().gesture(point(.27, .35), point(.73, .35),
                         point(.46, .35), point(.54, .35), steps=30)

    def home_gesture(self):
        self.foreground()
        for start, end, duration in ((.995, .62, .25), (.965, .5, .35)):
            self.swipe_ratio(.5, start, .5, end, duration)
            deadline = time.monotonic() + 3
            while time.monotonic() < deadline:
                try:
                    if 'launcher' in self.current_app()['activity'].lower():
                        return
                except ForegroundNotReady:
                    pass
                time.sleep(.3)
        # 小红书会吞掉系统边缘手势；用系统 Home 键保持返回桌面的结果。
        self.d.press('home')
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(),
                      '未返回系统桌面')

    def xhs_tab(self, title):
        self.PACKAGE = self.XHS
        ready = (lambda: self.has(desc='首页', class_name='android.view.ViewGroup') and
                 self.has(text='发现')) if title == '首页' else lambda: self.has(desc='已选定' + title)
        self.transition(lambda: self.click_node(text=title, class_name='android.widget.TextView'),
                        ready,
                        '小红书未进入 {}'.format(title))

    def douyin_tab(self, title):
        self.PACKAGE = self.DOUYIN
        self.transition(lambda: self.click_node(text=title, rid=self.DOUYIN + ':id/5dv'),
                        lambda: self.has(desc='已选中，{}，按钮'.format(title)),
                        '抖音未进入 {}'.format(title))

    def first_visible_result(self, min_y, min_height, exclude=()):
        candidates = []
        for node in self.nodes():
            if node.get('class') != 'android.view.ViewGroup':
                continue
            desc = node.get('content-desc', '')
            if not desc or any(word in desc for word in exclude):
                continue
            left, top, right, bottom = self.bounds(node)
            if top >= min_y and bottom - top >= min_height and right - left > 500:
                candidates.append((top, node))
        if not candidates:
            raise RuntimeError('未找到首条可见结果')
        self.node_click(min(candidates, key=lambda item: item[0])[1])
