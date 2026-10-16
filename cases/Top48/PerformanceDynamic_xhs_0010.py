# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time
import uiautomator2 as u2
from uiautomator2 import Device
from Cases.CaseBase import Case
from aw_new import SeaOfStarsAW


class PerformanceDynamic_xhs_0010(Case):
    all_app_package_list = [""]

    def __init__(self, result_path):
        super().__init__(result_path)

    @SeaOfStarsAW.function_log
    def set_up(self):
        """
        测试环境准备
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("测试环境开始准备!")
        # 判断手机上是否已安装好TOP30应用,未安装则用例失败
        phone_app_list = SeaOfStarsAW.get_app_list()
        for per_app in self.all_app_package_list:
            if per_app not in phone_app_list:
                return False
        # 设置系统语言为中文
        SeaOfStarsAW.set_system_language_cn()
        # 解锁屏幕
        if SeaOfStarsAW.is_locked():
            SeaOfStarsAW.unlock_device()
        # 设置屏幕锁定时间为10min
        SeaOfStarsAW.set_screen_lock_long_time()
        # 保留已有应用后台
        logging.info("测试环境准备完成!")

    @SeaOfStarsAW.function_log
    def run_case(self):
        """
        测试用例执行
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("用例开始执行!")
        steps_num = 1

        app = 'com.xingin.xhs'
        step = "1、打开小红书（等待2s）"

        SeaOfStarsAW.start_perfetto_trace()
        logging.info("启动{}中".format("小红书"))
        SeaOfStarsAW.ut_device.app_start(app, use_monkey=True)
        time.sleep(5)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "2、点击 我的-进入收藏-图片的链接(停留1s)"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='我')[0].click()
        time.sleep(1)

        SeaOfStarsAW.ut_device(text='收藏').click()
        time.sleep(1)

        SeaOfStarsAW.ut_device.click(0.274, 0.807)
        time.sleep(1)

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "3、左下角点赞（停留1s）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.48, 0.945)
        time.sleep(1)

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "4、浏览图片（向左滑动3次，每次停留2s）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.464, 0.458)
        time.sleep(1)
        for _ in range(2):
            SeaOfStarsAW.swipe_right(1)
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "5、返回我的页面（停留1s）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.ut_device.click(0.056, 0.081)
            time.sleep(1)
        SeaOfStarsAW.ut_device(text='笔记')[0].click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "6、点击设置图标（停留1s）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(description="菜单").click()
        time.sleep(1)
        SeaOfStarsAW.ut_device(description="设置").click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "7、返回首页（停留1s）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.062, 0.084)
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(0.942, 0.391)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "8、上滑5次，下滑5次（每次停留2s）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(5):
            SeaOfStarsAW.scroll_up(0.5)
            time.sleep(2)
        for _ in range(5):
            SeaOfStarsAW.scroll_down(0.5)
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "9、点击消息"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='消息').click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "10、点击我"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='我')[0].click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "11、点击消息"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='消息').click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "12、点击首页"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='首页')[0].click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "13、点击“+”进入相册（停留2S）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.498, 0.954)
        time.sleep(1)
        SeaOfStarsAW.ut_device(text='从相册选择')[0].click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "14、上滑3次，下滑3次（停留2S）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(3):
            SeaOfStarsAW.scroll_up(0.5)
            time.sleep(2)
        for _ in range(3):
            SeaOfStarsAW.scroll_down(0.5)
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "15、点击第一张照片大图查看（停留2S）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.164, 0.244)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "16、滑动浏览（左滑3次，右滑3次，每次停留2S）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(3):
            SeaOfStarsAW.swipe_left(0.5)
            time.sleep(2)
        for _ in range(3):
            SeaOfStarsAW.swipe_right(0.5)
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "17、侧滑两次返回首页（停留1S）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.ut_device.click(0.078, 0.065)
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        step = "19、返回home页面（停留1s）"
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
