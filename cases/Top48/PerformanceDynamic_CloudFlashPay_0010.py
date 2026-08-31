import logging
import os
import shutil
import time
import uiautomator2 as u2
from uiautomator2 import Device
from Cases.CaseBase import Case
from aw_new import SeaOfStarsAW

action_perf_on = 0
"""
#!+======================================================================================
# 版权 (C) 海思半导体有限公司 2025 海思Kirin解决方案集成与验证部用户体验组
# Copyright (C) Hisilicon Technologies Co., Ltd. 2025. All rights reserved.
#========================================================================================
#   @FileName:      PerformanceDynamic_CloudFlashPay_0010.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   去除弹窗
#   @详细场景:        
#                   云闪付主页浏览
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                 1、启动云闪付（3s）
#                 2、主页浏览（上下各滑动1次，循环5次，每次停留2s）
#                 3、点击收付款（停留1s）
#                 4、点击扫一扫（停留1s）
#                 5、返回首页，点击扫一扫（停留1s）
#                 6、点击优惠（停留1s）
#                 7、浏览优惠页（上下各滑动1次，循环5次，每次停留2s）
#                 8、点击惠生活（停留1s）
#                 9、浏览惠生活（上下各滑动1次，循环5次，每次停留2s）
#                 10、返回上一层，点击享美食（停留1s）
#                 11、返回首页（停留1s）
#                 12、返回Home界面（停留1s）
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_CloudFlashPay_0010(Case):
    all_app_package_list = ["com.autonavi.minimap"]
    TEST_TIME = 1

    def __init__(self, result_path):
        super().__init__(result_path)

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info("测试环境开始准备!")
        # 解锁屏幕
        if SeaOfStarsAW.is_locked():
            SeaOfStarsAW.unlock_device()
        # 清空后台
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logging.info("测试环境准备完成!")

    @SeaOfStarsAW.function_log
    def run_case(self):
        logging.info("用例开始执行!")
        if SeaOfStarsAW.is_locked():
            SeaOfStarsAW.unlock_device()
        time.sleep(2)
        for test_time in range(0, self.TEST_TIME):
            # 1、启动云闪付（3s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动云闪付")
            SeaOfStarsAW.ut_device.app_start('com.unionpay', use_monkey=True)
            time.sleep(3)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、启动云闪付", "",
                                                     self.screenshot_dir_path)

            # 2、主页浏览（上下各滑动1次，循环5次，每次停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、主页浏览")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、主页浏览", "",
                                                     self.screenshot_dir_path)

            # 3、点击收付款（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、点击收付款")
            SeaOfStarsAW.ut_device.click(135, 430)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、点击收付款", "",
                                                     self.screenshot_dir_path)

            # 4、返回首页（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、返回首页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、点击扫一扫", "",
                                                     self.screenshot_dir_path)

            # 5、点击扫一扫（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、返回首页，点击扫一扫")
            SeaOfStarsAW.ut_device.click(670, 430)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、返回首页，点击扫一扫", "",
                                                     self.screenshot_dir_path)

            # 6、点击优惠（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、点击优惠")
            SeaOfStarsAW.ut_device.click(340, 2230)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、点击优惠", "",
                                                     self.screenshot_dir_path)

            # 7、浏览优惠页（上下各滑动1次，循环5次，每次停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、浏览优惠页")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、浏览优惠页", "",
                                                     self.screenshot_dir_path)

            # 8、点击惠生活（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、点击惠生活")
            SeaOfStarsAW.ut_device.click(179, 1744)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、点击惠生活", "",
                                                     self.screenshot_dir_path)

            # 9、浏览惠生活（上下各滑动1次，循环5次，每次停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、浏览惠生活")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、浏览惠生活", "",
                                                     self.screenshot_dir_path)

            # 10、返回上一层，点击享美食（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、返回上一层，点击享美食")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(312, 518)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、返回上一层，点击享美食", "",
                                                     self.screenshot_dir_path)

            # 11、返回首页（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、返回首页")
            SeaOfStarsAW.ut_device.click(135, 2230)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11、返回首页", "",
                                                     self.screenshot_dir_path)

            # 12、返回Home界面（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、返回Home界面")
            SeaOfStarsAW.return_launcher()
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12、返回Home界面", "",
                                                     self.screenshot_dir_path)

        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)