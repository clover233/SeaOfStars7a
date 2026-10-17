# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time
import uiautomator2 as u2
from uiautomator2 import Device
from Cases.Top48.observed_apps_common import ObservedAppCase
from aw_new import SeaOfStarsAW

class PerformanceDynamic_xhs_0030(ObservedAppCase):

    PACKAGE = 'com.xingin.xhs'
    COMPONENT = PACKAGE + '/.index.v2.IndexActivityV2'
    QUERY = '穿搭图片'
    all_app_package_list = [PACKAGE]

    def dismiss_ads(self):
        if self.has(text='免流量升级') and self.has(text='稍后再说'):
            self.click(text='稍后再说')
            time.sleep(.5)
        height = self.d.window_size()[1]
        skips = [n for n in self.nodes(text='跳过广告', prefix=True)
                 if self.bounds(n)[3] < height * .16]
        if len(skips) == 1:
            self.click_node(skips[0])
            time.sleep(.5)

    def main_ready(self):
        return self.has(desc='首页') and self.has(text='发现')

    def main_page(self):
        self.dismiss_ads()
        self.return_to(self.main_ready, '未返回小红书主界面', limit=6)

    def launch(self):
        self._hot_query = None
        self.start()
        def ready():
            self.dismiss_ads()
            return self.main_ready()
        self.wait_for(ready, '小红书首页未加载', timeout=30)

    def search_ready(self):
        return any(n.get('class') == 'android.widget.EditText' for n in self.nodes())

    def results_ready(self):
        return self.has(text='全部') and self.has(text='综合') and not self.search_ready()

    def search_header(self, query):
        height = self.d.window_size()[1]
        return [n for n in self.nodes(text=query) if self.bounds(n)[3] < height * .14]

    def open_search(self):
        for _ in range(6):
            self.dismiss_ads()
            if self.search_ready():
                return
            if self.main_ready():
                self.click(desc='搜索')
            elif self.results_ready():
                # 点实际搜索词回到编辑页，不按固定次数返回到发现首页。
                height = self.d.window_size()[1]
                titles = [n for n in self.nodes() if n.get('class') == 'android.widget.TextView'
                          and n.get('clickable') == 'true' and n.get('text') not in ('搜索', '')
                          and self.bounds(n)[3] < height * .14]
                if len(titles) != 1:
                    raise RuntimeError('小红书搜索结果顶部词条不唯一')
                self.click_node(titles[0])
            else:
                self.back()
            time.sleep(.5)
        self.wait_for(self.search_ready, '小红书搜索编辑页未打开')

    def set_query(self):
        self.open_search()
        self.d(packageName=self.PACKAGE, className='android.widget.EditText').set_text(self.QUERY)
        self.invalidate()

    def submit_query(self):
        self.require(text=self.QUERY)
        buttons = [n for n in self.nodes(text='搜索') if self.bounds(n)[3] < self.d.window_size()[1]*.14]
        if len(buttons) != 1:
            raise RuntimeError('小红书搜索提交入口不唯一')
        self.click_node(buttons[0])
        self.wait_for(lambda: self.results_ready() and bool(self.search_header(self.QUERY)),
                      '小红书搜索结果未加载', timeout=25)

    def return_results(self):
        self.return_to(self.results_ready, '未返回小红书搜索结果页', limit=4)

    def return_search(self):
        self._hot_query = None
        self.open_search()
        self.d(packageName=self.PACKAGE, className='android.widget.EditText').set_text('')
        self.invalidate()
        self.wait_for(lambda: any(self.has(text=label) for label in
                                 ('搜索发现', '小红书热榜', '猜你想搜')),
                      '清空搜索词后搜索发现区域未显示')

    def first_hot(self):
        self.return_search()
        header = next((label for label in ('搜索发现', '小红书热榜', '猜你想搜')
                       if self.has(text=label)), None)
        if header is None:
            raise RuntimeError('当前小红书没有可核验的搜索发现入口')
        top = self.bounds(self.node(text=header))[3]
        width, height = self.d.window_size()
        rows = [n for n in self.nodes() if n.get('class') == 'android.widget.TextView'
                and len(n.get('text', '').strip()) >= 2
                and not n.get('text', '').strip().isdigit()
                and top < self.bounds(n)[1] < height * .85
                and self.bounds(n)[0] < width * .5
                and self.bounds(n)[2] < width * .65]
        if not rows:
            raise RuntimeError('搜索发现区域没有可核验的第一条条目')
        first = min(rows, key=lambda n: (self.bounds(n)[1], self.bounds(n)[0]))
        query = first.get('text')
        self.click_node(first)
        self.wait_for(lambda: self.results_ready() and bool(self.search_header(query)),
                      '点击搜索发现首条后结果未加载', timeout=25)
        self._hot_query = query
        if header == '猜你想搜':
            reason = '本版本搜索发现显示“猜你想搜”，浏览当前第一条建议“{}”，替代旧热搜入口'.format(query)
            self.adapt(reason)
            logging.warning('ADAPTED：%s', reason)

    def browse_hot(self):
        if not self._hot_query or not self.results_ready() or not self.search_header(self._hot_query):
            raise RuntimeError('尚未进入当前搜索发现条目的结果页，停止浏览')
        for _ in range(2):
            self.browse(3, 3)

    @SeaOfStarsAW.function_log
    def run_case(self):
        if not getattr(self, '_prepared', False):
            self.set_up()
        try:
            self._run_steps()
        finally:
            # main.py 的 clean_up 目前关闭，异常与正常结束都恢复输入法。
            self.restore_ime()

    def _run_steps(self):
        """
        测试用例执行
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        if not getattr(self, "_prepared", False):
            self.set_up()
        self._adaptations = []
        logging.info("用例开始执行!")
        steps_num = 1

        app = 'com.xingin.xhs'
        step = "1、打开小红书（等待2s）"

        SeaOfStarsAW.start_perfetto_trace()
        logging.info("启动{}中".format("小红书"))
        self.launch()
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "2、点击右上角搜索"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self.open_search()
        time.sleep(1)

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "3、搜索穿搭图片，返回上一级，重复操作3次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self.set_query()
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "4、搜索穿搭图片"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self.submit_query()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "5、点击左上角第一条消息"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.236, 0.386)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "6、上滑1次，下滑1次浏览笔记详情   "
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.scroll_down(0.5)
        time.sleep(2)
        SeaOfStarsAW.scroll_up(0.5)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "7、点击图片看大图，左滑3次，右滑3次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.492, 0.363)
        time.sleep(1)
        for _ in range(3):
            SeaOfStarsAW.swipe_right()
            time.sleep(2)
        for _ in range(3):
            SeaOfStarsAW.swipe_left()
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "8、返回搜索结果页面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self.return_results()
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "9、上滑3次，下滑3次浏览搜索结果，重复操作2次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for i in range(2):
            for _ in range(3):
                SeaOfStarsAW.scroll_down()
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.scroll_up()
                time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "10、返回搜索页面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self.return_search()
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "11、点击搜索发现下的第一条热搜"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self.first_hot()
        if self._adaptations:
            step += "_ADAPTED"
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "12、上滑3次，下滑3次浏览热搜，重复操作2次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self.browse_hot()
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "13、返回小红书主界面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self.main_page()
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        step = "14、返回home页面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self.home()
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        super().clean_up()
