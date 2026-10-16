# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time
import uiautomator2 as u2
from uiautomator2 import Device
from Cases.CaseBase import Case
from aw_new import SeaOfStarsAW

class PerformanceDynamic_wpsoffice_0010(Case):

    all_app_package_list = [""]

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
        # SeaOfStarsAW.init_device()
        steps_num = 1

        app = 'cn.wps.moffice_eng'
        step = "1、启动WPS（等待2s）"

        SeaOfStarsAW.start_perfetto_trace()
        logging.info("启动{}中".format("WPS"))
        SeaOfStarsAW.ut_device.app_start(app, use_monkey=True)
        time.sleep(5)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "2、首页左右滑动各5次，每次停留2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(5):
            SeaOfStarsAW.swipe_right()
            time.sleep(2)
        for _ in range(5):
            SeaOfStarsAW.swipe_left()
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "3、点击底部导航云盘icon后，点击首页icon,重复五次每次停留2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(5):
            SeaOfStarsAW.ut_device(text="云盘").click()
            time.sleep(1)
            SeaOfStarsAW.ut_device(text="首页").click()
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "4、点击我,等待2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text="我").click()
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "5、点击设置，等待2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text="设置").click()
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "6、返回我的页面，停留2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.068, 0.086)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "7、点击超级会员，进入支付界面，停留2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text="超级会员").click()
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "8、返回我的页面，停留2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.068, 0.086)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        # 返回桌面
        step = "9、点击首页，停留2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text="首页").click()
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        # 返回桌面
        step = "10、点击欢迎使用WPS云文档（最近里面），停留2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text="最近").click()
        time.sleep(2)
        SeaOfStarsAW.ut_device(text="欢迎使用WPS云文档").click()
        time.sleep(2)

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        # 返回桌面
        step = "11、上下滑动5次浏览文档页，停留2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(5):
            SeaOfStarsAW.scroll_down()
            time.sleep(2)
        for _ in range(5):
            SeaOfStarsAW.scroll_up()
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        # 返回桌面
        step = "12、返回wps主界面，停留2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.068, 0.086)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        # 返回桌面
        step = "13、滑动返回Home页，停留2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.return_launcher()
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

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
