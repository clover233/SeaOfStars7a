# -*- coding: utf-8 -*-
"""百度地图导航至西安钟楼；步骤来自动态性能模型测试用例7.xlsx。"""
import time
import re
import xml.etree.ElementTree as ET

from Cases.Top48.baidu_common import BaiduDynamicCase


class PerformanceDynamic_baidumap_0010(BaiduDynamicCase):
    PACKAGE = 'com.baidu.BaiduMap'
    all_app_package_list = [PACKAGE]
    PERMISSIONS = ('ACCESS_COARSE_LOCATION', 'ACCESS_FINE_LOCATION')
    PREFIX = PACKAGE + ':id/'

    def control(self, name):
        return self.d(resourceId=self.PREFIX + name)

    def is_home(self):
        return (self.control('tv_searchbox_home_text_switcher').exists
                and self.control('new_route_text').exists)

    def is_navigation(self):
        return self.control('bnav_rg_bottombar_new_right_btn').exists

    def return_home(self):
        for _ in range(10):
            self.foreground()
            if self.is_home():
                return
            if self.is_navigation():
                raise RuntimeError('导航尚未退出，不能直接返回地图首页')
            self.d.press('back')
            time.sleep(0.8)
        raise RuntimeError('未返回百度地图主界面')

    def launch(self):
        self.d.app_start(self.PACKAGE, use_monkey=True)
        time.sleep(3)
        self.return_home()

    def search(self, query='钟楼'):
        if self.is_home():
            selector = 'tv_searchbox_home_text_switcher'
        elif self.control('tv_first_text').exists:
            selector = 'tv_first_text'
        else:
            raise RuntimeError('不在地点搜索入口页')
        self.transition(lambda: self.tap(resourceId=self.PREFIX + selector),
                        lambda: self.control('tvSearchBoxInput').exists, '未打开地图搜索输入框')
        self.control('tvSearchBoxInput').set_text(query)
        self.transition(lambda: self.tap(resourceId=self.PREFIX + 'aiSearchActionBtn'),
                        lambda: self.d(resourceId=self.PREFIX + 'tv_first_text', text=query).exists,
                        '钟楼搜索未提交')
        self.wait_for(lambda: self.d(className='android.webkit.WebView', text='检索列表页').exists,
                      '地点结果列表未加载，请检查网络', timeout=30)

    def select_xian_tower(self):
        # 用户测试机定位上海，直接“钟楼”会优先返回上海的同名景点。
        # 保留步骤2的原查询；步骤3补充城市限定，避免把错误钟楼作为导航目的地。
        if self.tower_result_box() is None:
            self.search('西安钟楼')
        self.wait_for(lambda: self.tower_result_box() is not None and self.d(textContains='西安市').exists,
                      '未找到西安市的西安钟楼结果', timeout=30)
        def select_result():
            box = self.tower_result_box()
            if box is None:
                raise RuntimeError('西安钟楼地点卡片消失')
            x1, y1, x2, y2 = box
            self.click_point((x1+x2)//2, (y1+y2)//2)
        self.transition(select_result,
                        lambda: self.control('iv_route_text').exists,
                        '未进入西安钟楼详情')
        self.wait_for(lambda: self.d(textContains='陕西省-西安市').exists,
                      '详情地址不是陕西省西安市，停止导航', timeout=20)

    def tower_result_box(self):
        # UiSelector 的空 resourceId 会被忽略；从 XML 严格排除顶部搜索栏。
        height = self.d.window_size()[1]
        candidates = []
        for node in ET.fromstring(self.d.dump_hierarchy()).iter('node'):
            if (node.get('text') == '西安钟楼' and not node.get('resource-id')
                    and node.get('class') == 'android.widget.TextView'):
                box = tuple(map(int, re.findall(r'\d+', node.get('bounds', ''))))
                if len(box) == 4 and height * 0.25 < box[1] < height * 0.9:
                    candidates.append(box)
        if len(candidates) > 1:
            raise RuntimeError('西安钟楼地点卡片不唯一')
        return candidates[0] if candidates else None

    def plan_route(self):
        if not self.control('iv_route_text').exists or not self.d(text='西安钟楼').exists:
            raise RuntimeError('当前不是西安钟楼详情页')
        self.transition(lambda: self.tap(resourceId=self.PREFIX + 'iv_route_text'),
                        lambda: self.control('to_pro_nav').exists, '未打开驾车路线规划')
        self.wait_for(lambda: self.d(resourceId=self.PREFIX + 'route_search_input_end_text', text='西安钟楼').exists,
                      '路线终点不是西安钟楼')

    def start_navigation(self):
        if not self.d(resourceId=self.PREFIX + 'route_search_input_end_text', text='西安钟楼').exists:
            raise RuntimeError('开始导航前目的地校验失败')
        self.transition(lambda: self.tap(resourceId=self.PREFIX + 'to_pro_nav'),
                        lambda: self.is_navigation() or self.d(textContains='百度智能定位为您持续导航').exists,
                        '未启动导航')
        # 首次隧道定位介绍是普通功能提示，严格按其标题识别，避免点击协议或授权。
        if self.d(textContains='百度智能定位为您持续导航').exists and self.control('second_btn').exists:
            self.tap(resourceId=self.PREFIX + 'second_btn')
        self.wait_for(self.is_navigation, '未进入实际导航页面', timeout=30)

    def exit_navigation(self):
        if not self.is_navigation():
            raise RuntimeError('当前不是导航页面')
        confirm = 'bnav_rg_operable_notification_confirm_text'
        self.transition(lambda: self.tap(resourceId=self.PREFIX + 'bnav_rg_bottombar_new_right_btn'),
                        lambda: self.control(confirm).exists or not self.is_navigation(), '未出现退出导航确认')
        if self.control(confirm).exists:
            self.tap(resourceId=self.PREFIX + confirm)
        self.wait_for(lambda: not self.is_navigation() and self.control('to_pro_nav').exists,
                      '退出导航后未返回路线页')

    def steps(self):
        return [
            ('启动百度地图', self.launch, 2),
            ('搜索框搜索钟楼', self.search, 2),
            ('选择西安钟楼', self.select_xian_tower, 2),
            ('点击到这去', self.plan_route, 2),
            ('点击开始导航', self.start_navigation, 2),
            ('点击退出导航', self.exit_navigation, 2),
            ('返回百度地图主界面', self.return_home, 2),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
