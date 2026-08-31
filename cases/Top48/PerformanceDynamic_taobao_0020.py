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
#   @FileName:      PerformanceDynamic_taobao_0020.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                 1、登录淘宝
#                 2、去除弹框
#   @详细场景:        
#                 淘宝首页tab栏切换并浏览-购物
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                 1.打开淘宝 (启动5s，可能有广告，停留2s)
#                 2.进入“推荐”页面
#                 3.进入第三个tab图标页面
#                 4.第三个tab图标页面，上滑5次，下滑5次，每次停留2s
#                 5.返回推荐界面
#                 6.“推荐”页面上滑5次，下滑5次，每次停留2s
#                 7.点击“关注”，上滑5次，下滑5次，每次停留2s
#                 8.点击tab栏逛逛  等待2s，浏览“逛逛”页面，上滑5次，下滑5次，右滑3次，左滑3次，每次停留2s
#                 9.点击tab栏我的淘宝  等待2s
#                 10.点击“我的订单”，等待2s
#                 11.查看不同状态的订单，左滑5次，右滑5次
#                 12、返回首页，返回home页面（停留2s)
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_taobao_0020(Case):
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
            # 1.打开淘宝 (启动5s，可能有广告，停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1.打开淘宝")
            SeaOfStarsAW.ut_device.app_start('com.taobao.taobao', use_monkey=True)
            time.sleep(5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1.打开淘宝", "",
                                                     self.screenshot_dir_path)
            # 2.进入“推荐”页面
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2.进入“推荐”页面")
            SeaOfStarsAW.ut_device.click(238, 202)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2.进入“推荐”页面", "",
                                                     self.screenshot_dir_path)
            # 3.进入第三个tab图标页面
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3.进入第三个tab图标页面")
            SeaOfStarsAW.ut_device.click(433, 202)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3.进入第三个tab图标页面", "",
                                                     self.screenshot_dir_path)
            # 4.第三个tab图标页面，上滑5次，下滑5次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4.第三个tab图标页面，上滑5次，下滑5次，每次停留2s")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4.第三个tab图标页面，上滑5次，下滑5次，每次停留2s", "",
                                                     self.screenshot_dir_path)
            # 5.返回推荐界面
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5.返回推荐界面")
            SeaOfStarsAW.ut_device.click(238, 202)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5.返回推荐界面", "",
                                                     self.screenshot_dir_path)
            # 6.“推荐”页面上滑5次，下滑5次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6.“推荐”页面上滑5次，下滑5次，每次停留2s")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6.“推荐”页面上滑5次，下滑5次，每次停留2s", "",
                                                     self.screenshot_dir_path)
            # 7.点击“关注”，上滑5次，下滑5次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7.点击“关注”，上滑5次，下滑5次，每次停留2s")
            SeaOfStarsAW.ut_device.click(95, 202)
            time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7.点击“关注”，上滑5次，下滑5次，每次停留2s", "",
                                                     self.screenshot_dir_path)

            # 8.点击tab栏逛逛  等待2s，浏览“逛逛”页面，上滑5次，下滑5次，右滑3次，左滑3次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8.点击tab栏逛逛  等待2s，浏览“逛逛”页面，上滑5次，下滑5次，右滑3次，左滑3次，每次停留2s")
            SeaOfStarsAW.ut_device.click(238, 202)
            time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, 0.03)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8.点击tab栏逛逛  等待2s，浏览“逛逛”页面，上滑5次，下滑5次，右滑3次，左滑3次，每次停留2s", "",
                                                     self.screenshot_dir_path)
            # 9.点击tab栏我的淘宝  等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9.点击tab栏我的淘宝  等待2s")
            SeaOfStarsAW.ut_device.click(972, 2264)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9.点击tab栏我的淘宝  等待2s", "",
                                                     self.screenshot_dir_path)
            # 10.点击“我的订单”，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10.点击“我的订单”，等待2s")
            SeaOfStarsAW.ut_device.click(132, 847)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10.点击“我的订单”，等待2s", "",
                                                     self.screenshot_dir_path)
            # 11.查看不同状态的订单，左滑5次，右滑5次
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11.查看不同状态的订单，左滑5次，右滑5次")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, 0.03)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11.查看不同状态的订单，左滑5次，右滑5次", "",
                                                     self.screenshot_dir_path)
            # 12、返回首页，返回home页面（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、返回首页，返回home页面")
            SeaOfStarsAW.return_launcher()
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12、返回首页，返回home页面", "",
                                                     self.screenshot_dir_path)
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)