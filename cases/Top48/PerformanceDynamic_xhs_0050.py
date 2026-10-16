# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time
import uiautomator2 as u2
from uiautomator2 import Device
from Cases.CaseBase import Case
from aw_new import SeaOfStarsAW

class PerformanceDynamic_xhs_0050(Case):

    all_app_package_list = ["com.xingin.xhs"]

    def __init__(self, result_path):
        super().__init__(result_path)

    @SeaOfStarsAW.function_log
    def set_up(self):
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

        step = "2、点击右上角搜索"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(description='搜索')[0].click()
        time.sleep(1)

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "3、输入框输入图片"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.send_keys(text="穿搭图片")
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "4、点击搜索"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='搜索').click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "5、点击左上角第一条内容"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.236, 0.386)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        # TODO 需要搞定捏合放大的功能
        # steps_num += 1
        #
        # step = "6、双指捏合放大"
        # SeaOfStarsAW.start_perfetto_trace()
        # logging.info(step)
        # SeaOfStarsAW.scroll_down(0.5)
        # time.sleep(2)
        # SeaOfStarsAW.scroll_up(0.5)
        # time.sleep(2)
        # SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
        #                                          'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        # steps_num += 1
        #
        # step = "7、双指捏合缩小"
        # SeaOfStarsAW.start_perfetto_trace()
        # logging.info(step)
        # SeaOfStarsAW.ut_device.click(0.492, 0.363)
        # time.sleep(1)
        # for _ in range(3):
        #     SeaOfStarsAW.swipe_right()
        #     time.sleep(2)
        # for _ in range(3):
        #     SeaOfStarsAW.swipe_left()
        #     time.sleep(2)
        # SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
        #                                          'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        # steps_num += 1
        #
        # step = "8、6,7循环两遍"
        # SeaOfStarsAW.start_perfetto_trace()
        # logging.info(step)
        # for _ in range(2):
        #     SeaOfStarsAW.ut_device.click(0.058, 0.081)
        #     time.sleep(1)
        # SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
        #                                          'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "9、返回小红书主界面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.058, 0.081)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "10、点击视频tab页（RED）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text="视频").click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "11、随便点击一个视频，浏览10秒"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.236, 0.386)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "12、上滑3次，下滑3次每次间隔5秒"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(3):
            SeaOfStarsAW.scroll_down()
            time.sleep(5)
        for _ in range(3):
            SeaOfStarsAW.scroll_up()
            time.sleep(5)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "13、返回小红书主界面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(3):
            SeaOfStarsAW.ut_device.click(0.06, 0.086)
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        step = "14、返回home页面"
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
