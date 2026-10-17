# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time
import uiautomator2 as u2
from uiautomator2 import Device
from Cases.Top48.dynamic_apps_common import DynamicAppCase
from aw_new import SeaOfStarsAW

class PerformanceDynamic_zhihu_0030(DynamicAppCase):

    PACKAGE = "com.zhihu.android"
    all_app_package_list = [PACKAGE]

    def __init__(self, result_path):
        super().__init__(result_path)

    @SeaOfStarsAW.function_log
    def set_up(self):
        super().set_up()

    def home_ready(self):
        return self.has(rid='title', text='推荐') and self.has(rid='title', text='热榜')

    def launch(self):
        self.start()
        def ready():
            if self.has(rid='btn_skip', text='跳过', prefix=True):
                self.click(rid='btn_skip', text='跳过', prefix=True)
            # 只关闭已识别登录页，不点击登录、协议或切换账号。
            if self.has(rid='operate_login_text') and self.has(rid='close'):
                self.click(rid='close')
            return self.home_ready()
        self.wait_for(ready, '知乎首页推荐/热榜入口未加载', timeout=25)

    def channel(self, name):
        self.wait_for(self.home_ready, '知乎首页频道未就绪')
        self.transition(lambda: self.click(rid='title', text=name),
                        lambda: any(n.get('selected') == 'true'
                                    for n in self.nodes(rid='title', text=name)),
                        '未切换到知乎' + name)

    def recommend(self):
        self.channel('推荐')

    def hot(self):
        self.channel('热榜')

    @SeaOfStarsAW.function_log
    def run_case(self):
        """
        测试用例执行
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        if not getattr(self, "_prepared", False):
            self.set_up()
        logging.info("用例开始执行!")
        steps_num = 1

        app = 'com.zhihu.android'
        step = "1、启动知乎"

        SeaOfStarsAW.start_perfetto_trace()
        logging.info("启动{}中".format("知乎"))
        self.launch()
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "2、点击屏幕顶部推荐"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self.recommend()
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "3、上滑2次，下滑3次浏览推荐"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.scroll_down()
            time.sleep(2)
        for _ in range(3):
            SeaOfStarsAW.scroll_up()
            time.sleep(2)

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "4、点击屏幕顶部热榜"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self.hot()
        time.sleep(5)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "5、上滑2次，下滑3次浏览热榜"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.scroll_down()
            time.sleep(2)
        for _ in range(3):
            SeaOfStarsAW.scroll_up()
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "6、点击热榜第一条查看详情"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.394, 0.346)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "7、上滑2次，下滑3次浏览详情"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.scroll_down()
            time.sleep(2)
        for _ in range(3):
            SeaOfStarsAW.scroll_up()
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "8、点击第一条文章查看具体信息"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.432, 0.697)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "9、上滑2次，下滑3次浏览文章"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.scroll_down()
            time.sleep(2)
        for _ in range(3):
            SeaOfStarsAW.scroll_up()
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "10，点击右下角评论按钮"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.822, 0.951)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "11、上滑2次，下滑3次浏览评论"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.scroll_down()
            time.sleep(2)
        for _ in range(3):
            SeaOfStarsAW.scroll_up()
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "12，返回推荐页"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(3):
            SeaOfStarsAW.ut_device.swipe(0.99, 0.423, 0.636, 0.423)
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "13、搜索一组桌面壁纸"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.526, 0.08)
        time.sleep(1)
        SeaOfStarsAW.ut_device.send_keys("一组桌面壁纸")
        time.sleep(1)
        SeaOfStarsAW.ut_device(text="搜索").click()
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "14、点击搜索的第一条结果"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.264, 0.334)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "15、点击图片"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.26, 0.422)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "16、左滑2次，右滑2次浏览图片"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.swipe_right()
            time.sleep(1)
        for _ in range(2):
            SeaOfStarsAW.swipe_left()
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "17、返回知乎首页"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(5):
            SeaOfStarsAW.ut_device.swipe(0.99, 0.423, 0.636, 0.423)
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        step = "18、点击底部tab栏看山"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text="看山").click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        step = "19、返回知乎主界面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.swipe(0.99, 0.423, 0.636, 0.423)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        step = "20、返回home页面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.return_launcher()
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        """
        清理日志，保留应用后台
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("用例结束，保留应用后台，仅清理日志处理器。")
        logger = logging.getLogger()
        logger.removeHandler(self.fh)
