# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time
import uiautomator2 as u2
from uiautomator2 import Device
from Cases.CaseBase import Case
from aw_new import SeaOfStarsAW


class PerformanceDynamic_zuoyebang_0020(Case):


    all_app_package_list = ["com.xingin.xhs"]

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
        # 清空后台
        SeaOfStarsAW.stop_apps(phone_app_list)
        SeaOfStarsAW.clear_backgroud()
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
        # SeaOfStarsAW.init_device()
        #  todo
        # if SeaOfStarsAW.is_locked():
        #     SeaOfStarsAW.unlock_device()
        # SeaOfStarsAW.ut_device.watcher.when('com.xingin.xhs:id/a90').click()
        # SeaOfStarsAW.ut_device.watcher.when('com.xingin.xhs:id/b_5').click()
        # SeaOfStarsAW.ut_device.watcher.start()


        steps_num = 1
        # 应用启动
        step = "应用启动"
        app = 'com.xingin.xhs'

        SeaOfStarsAW.start_perfetto_trace()
        logging.info("启动{}中".format(app))
        SeaOfStarsAW.ut_device.app_start(app, use_monkey=True)
        time.sleep(7)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(steps_num) +"-"+ step, "", self.screenshot_dir_path)
        steps_num += 1

        # 进入收藏图片
        step = "进入收藏图片"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='我')[0].click()
        time.sleep(2)
        SeaOfStarsAW.ut_device(text='收藏')[0].click()
        time.sleep(2)
        SeaOfStarsAW.ut_device.click(280, 1600)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(steps_num) +"-"+ step,"", self.screenshot_dir_path)
        steps_num += 1

        # 浏览图片
        step  = "浏览图片"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(3):
            SeaOfStarsAW.ut_device.swipe(0.8, 0.4, 0.3, 0.4, duration=0.2)
            time.sleep(3)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(steps_num) +"-"+ step, "", self.screenshot_dir_path)
        steps_num += 1

        # 返回首页
        step = "返回首页"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.keyevent('back')
        time.sleep(1)
        SeaOfStarsAW.ut_device.keyevent('back')
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(steps_num) +"-"+ step,"", self.screenshot_dir_path)
        steps_num += 1

        # 首页浏览图片
        step = "首页浏览图片"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        time.sleep(2)
        for _ in range(3):
            SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.5, 0.3, duration=0.2)
            time.sleep(3)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(steps_num)+"-"+ step,"", self.screenshot_dir_path)
        steps_num += 1

        # 返回桌面
        step = "返回桌面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.return_launcher()
        time.sleep(4)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(steps_num)+"-"+ step,"", self.screenshot_dir_path)
        steps_num += 1

        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        """
        测试环境恢复
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        SeaOfStarsAW.clear_backgroud()
        logger = logging.getLogger()
        logger.removeHandler(self.fh)
