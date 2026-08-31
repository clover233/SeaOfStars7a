# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time
import uiautomator2 as u2
from uiautomator2 import Device
from Cases.CaseBase import Case
from aw_new import SeaOfStarsAW


class PerformanceDynamic_weixin_0050(Case):
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
        steps_num = 1

        app = 'com.tencent.mm'
        step = "1、启动微信(启动2s，停留2s)"

        SeaOfStarsAW.start_perfetto_trace()
        logging.info("启动{}中".format("微信"))
        SeaOfStarsAW.ut_device.app_start(app, use_monkey=True)
        time.sleep(5)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "2、点击进入群聊天页面(2s，停留2s) "
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(700, 350)
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(50, 170)
        time.sleep(1)

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "3、点击【华为手机】的公众号名片(2s，停留4s)"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(900, 180)
        time.sleep(1)
        SeaOfStarsAW.ut_device.send_keys("华为手机")
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(450, 560)
        time.sleep(1)

        SeaOfStarsAW.ut_device.click(560, 1900)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "4、浏览公众号（上滑3cm，2s，停留2s，下滑3cm，2s，停留2s重复3次）"
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

        step = "5、点击第一个文章（2s，停留3s）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(500, 2200)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "6、浏览搜索结果（上滑3cm，2s，停留2s，重复3次）"
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

        step = "7、返回测试公众号群的聊天界面（2s，停留2s）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(1):
            SeaOfStarsAW.ut_device.click(55, 170)
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "8、点击【HarmonyOS】的公众号名片(2s，停留4s)"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(450, 200)
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(1000, 200)
        time.sleep(1)
        SeaOfStarsAW.ut_device.send_keys("HarmonyOS")
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(1000, 350)
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(630, 700)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "9、点击【发消息】进入公众号对话界面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(800, 800)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "10、点击屏幕底部【HMOS】后点击【最新咨询】，等待2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(600, 2300)
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(580, 2150)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "11、上滑2次，下滑2次浏览文章"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.scroll_up(0.5)
            time.sleep(2)
        for _ in range(2):
            SeaOfStarsAW.scroll_down(0.5)
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "12、返回测试公众号群的聊天界面（2s，停留2s）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.ut_device.click(55, 170)
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "13、点击【腾讯新闻】的公众号名片(2s，停留4s)"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(450, 200)
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(1000, 200)
        time.sleep(1)
        SeaOfStarsAW.ut_device.send_keys("腾讯新闻")
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(1000, 350)
        time.sleep(1)

        SeaOfStarsAW.ut_device.click(630, 650)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "14、点击【发消息】进入公众号对话界面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(800, 800)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "15、点击屏幕底部【早报晚报】后点击【晚报】，等待2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(600, 2300)
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(600, 2150)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "16、浏览晚报，上滑5次，下滑5次"
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

        step = "17、返回测试公众号群的聊天界面（2s，停留2s）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.ut_device.click(55, 170)
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "18、点击【央视新闻】的公众号名片(2s，停留4s)"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(450, 200)
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(1000, 200)
        time.sleep(1)
        SeaOfStarsAW.ut_device.send_keys("央视新闻")
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(1000, 350)
        time.sleep(1)

        SeaOfStarsAW.ut_device.click(630, 650)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "19、点击【发消息】进入公众号对话界面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)

        SeaOfStarsAW.ut_device.click(600, 500)
        time.sleep(1)

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "20、点击屏幕底部【文博日历】查看详情，等待2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(600, 2300)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "21、浏览【文博日历】，上滑2次，下滑2次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)

        for _ in range(2):
            SeaOfStarsAW.scroll_up(0.5)
            time.sleep(2)
        for _ in range(2):
            SeaOfStarsAW.scroll_down(0.5)
            time.sleep(2)

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "22、返回央视新闻对话界面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(1):
            SeaOfStarsAW.ut_device.click(55, 170)
            time.sleep(1)

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "23、点击屏幕底部【夜读】查看详情，等待2s"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(600, 2300)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "24、浏览【夜读】，上滑2次，下滑2次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.scroll_up(0.5)
            time.sleep(2)
        for _ in range(2):
            SeaOfStarsAW.scroll_down(0.5)
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "25、返回微信主界面(2s，停留2s)"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(9):
            SeaOfStarsAW.ut_device.click(55, 170)
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        # step = "26、点击订阅号"
        # SeaOfStarsAW.start_perfetto_trace()
        # logging.info(step)
        # SeaOfStarsAW.return_launcher()
        # time.sleep(2)
        # SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
        #                                          'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        # steps_num += 1
        #
        # step = "27、点击腾讯新闻"
        # SeaOfStarsAW.start_perfetto_trace()
        # logging.info(step)
        # SeaOfStarsAW.return_launcher()
        # time.sleep(2)
        # SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
        #                                          'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        # steps_num += 1
        #
        # step = "28、下滑3次"
        # SeaOfStarsAW.start_perfetto_trace()
        # logging.info(step)
        # SeaOfStarsAW.return_launcher()
        # time.sleep(2)
        # SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
        #                                          'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        # steps_num += 1
        #
        # step = "29、侧滑2次至微信首页"
        # SeaOfStarsAW.start_perfetto_trace()
        # logging.info(step)
        # SeaOfStarsAW.return_launcher()
        # time.sleep(2)
        # SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
        #                                          'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        # steps_num += 1

        step = "30、上滑退出微信"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.return_launcher()
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
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
