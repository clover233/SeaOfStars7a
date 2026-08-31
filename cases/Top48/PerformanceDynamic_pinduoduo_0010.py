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
#   @FileName:      PerformanceDynamic_pinduoduo_0010.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   登录账号
#   @详细场景:        
#                   拼多多搜索商品-购物
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                 1、启动拼多多(启动2s，停留2s)
#                 2、上滑3次，下滑3次，每次停留2s
#                 3、左滑5次，右滑5次，每次停留1s
#                 4、点击上方搜索框，等待1s
#                 5、输入华为手机，点击搜索，等待2s
#                 6、搜索界面滑动，上滑3次，下滑3次，每次等待2s
#                 7、点击第一个商品，等待2s
#                 8、商品详情页滑动，上滑2次，下滑2次，每次等待2s
#                 9、点击左下角店铺，等待2s
#                 10、上滑2次，下滑2次，每次等待2s
#                 11、侧滑5次返回首页
#                 12、上滑返回桌面
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_pinduoduo_0010(Case):
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
            # 1、启动拼多多(启动2s，停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动拼多多")
            SeaOfStarsAW.ut_device.app_start('com.xunmeng.pinduoduo', use_monkey=True)
            time.sleep(2)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、启动拼多多", "",
                                                     self.screenshot_dir_path)
            # 2、上滑3次，下滑3次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、上滑3次，下滑3次，每次停留2s")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、上滑3次，下滑3次，每次停留2s", "",
                                                     self.screenshot_dir_path)
            # 3、左滑5次，右滑5次，每次停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、左滑5次，右滑5次，每次停留1s")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, 0.03)
                time.sleep(1)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、左滑5次，右滑5次，每次停留1s", "",
                                                     self.screenshot_dir_path)
            # 4、点击上方搜索框，等待1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、点击上方搜索框，等待1s")
            SeaOfStarsAW.ut_device.click(545, 231)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、点击上方搜索框，等待1s", "",
                                                     self.screenshot_dir_path)
            # 5、输入华为手机，点击搜索，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、输入华为手机，点击搜索")
            SeaOfStarsAW.ut_device.send_keys('华为手机')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(985, 231)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、输入华为手机，点击搜索", "",
                                                     self.screenshot_dir_path)
            # 6、搜索界面滑动，上滑3次，下滑3次，每次等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、搜索界面滑动，上滑3次，下滑3次")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, 0.03)
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、搜索界面滑动，上滑3次，下滑3次", "",
                                                     self.screenshot_dir_path)
            # 7、点击第一个商品，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、点击第一个商品")
            SeaOfStarsAW.ut_device.click(215, 810)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、点击第一个商品", "",
                                                     self.screenshot_dir_path)
            # 8、商品详情页滑动，上滑2次，下滑2次，每次等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、商品详情页滑动，上滑2次，下滑2次")
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, 0.03)
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、商品详情页滑动，上滑2次，下滑2次", "",
                                                     self.screenshot_dir_path)
            # 9、点击左下角店铺，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、点击左下角店铺")
            SeaOfStarsAW.ut_device.click(64, 2234)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、点击左下角店铺", "",
                                                     self.screenshot_dir_path)
            # 10、上滑2次，下滑2次，每次等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、上滑2次，下滑2次")
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, 0.03)
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、上滑2次，下滑2次", "",
                                                     self.screenshot_dir_path)
            # 11、侧滑5次返回首页
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、侧滑5次返回首页")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11、侧滑5次返回首页", "",
                                                     self.screenshot_dir_path)
            # 12、上滑返回桌面
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、上滑返回桌面")
            SeaOfStarsAW.return_launcher()
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12、上滑返回桌面", "",
                                                     self.screenshot_dir_path)
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)