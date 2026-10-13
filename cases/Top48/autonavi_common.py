"""高德地图动态性能场景共用的页面定位和手势。"""
import logging
import re
import time
import xml.etree.ElementTree as ET

from Cases.Top48.baidu_common import BaiduDynamicCase
from aw_new import SeaOfStarsAW


class AutonaviDynamicCase(BaiduDynamicCase):
    PACKAGE = 'com.autonavi.minimap'
    AMAP = PACKAGE
    XHS = 'com.xingin.xhs'
    DOUYIN = 'com.ss.android.ugc.aweme'
    PREFIX = PACKAGE + ':id/'
    PERMISSIONS = ('ACCESS_COARSE_LOCATION', 'ACCESS_FINE_LOCATION')
    all_app_package_list = [PACKAGE]

    @SeaOfStarsAW.function_log
    def set_up(self):
        for package in self.all_app_package_list:
            if not self.d.app_info(package):
                raise RuntimeError('未安装应用：{}'.format(package))
        super().set_up()

    def nodes(self):
        self.foreground()
        return list(ET.fromstring(self.d.dump_hierarchy()).iter('node'))

    def has(self, *, text=None, desc=None, rid=None, class_name=None):
        return any((text is None or n.get('text') == text) and
                   (desc is None or n.get('content-desc') == desc) and
                   (rid is None or n.get('resource-id') == rid) and
                   (class_name is None or n.get('class') == class_name)
                   for n in self.nodes())

    @staticmethod
    def bounds(node):
        numbers = [int(x) for x in re.findall(r'\d+', node.get('bounds', ''))]
        if len(numbers) != 4:
            raise RuntimeError('控件无有效 bounds：{}'.format(node.attrib))
        return numbers

    def node_click(self, node):
        left, top, right, bottom = self.bounds(node)
        self.click_point((left + right) // 2, (top + bottom) // 2)

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
                        lambda: self.has(desc='搜索', class_name='android.view.ViewGroup'),
                        '未进入高德搜索页')

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
        self.click_node(desc='搜索', class_name='android.view.ViewGroup')
        self.wait_for(lambda: self.has(desc='搜索框，' + query) and
                      self.has(desc=result or query, class_name='android.view.ViewGroup'),
                      '未出现搜索结果 {}'.format(query), timeout=20)

    def result_route(self, result):
        # 路线属于指定结果行，不能用全局“路线”，否则会点到第二条。
        self.transition(lambda: self.tap_route_child(result),
                        lambda: any(n.get('content-desc', '').startswith('终点，')
                                    for n in self.nodes()),
                        '未进入路线规划')

    def tap_route_child(self, result):
        self.foreground()
        row = self.d(description=result, className='android.view.ViewGroup')
        if not row.wait(timeout=8):
            raise RuntimeError('未找到目的地结果 {}'.format(result))
        route = row.child(description='路线', className='android.view.ViewGroup')
        if route.count != 1:
            raise RuntimeError('目的地路线按钮未找到或不唯一 {}'.format(result))
        box = route.info['bounds']
        self.click_point((box['left'] + box['right']) // 2,
                         (box['top'] + box['bottom']) // 2)

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
        self.wait_for(lambda: self.has(desc='开始导航', class_name='android.view.ViewGroup'),
                      '路线未加载开始导航按钮', timeout=30)
        self.transition(lambda: self.click_node(desc='开始导航', class_name='android.view.ViewGroup'),
                        lambda: self.has(desc='退出导航按钮'), '未开始导航')

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

    def navigation_visible(self):
        self.wait_for(lambda: self.has(desc='退出导航按钮'), '后台导航未恢复', timeout=25)

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
                if 'launcher' in self.current_app()['activity'].lower():
                    return
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
