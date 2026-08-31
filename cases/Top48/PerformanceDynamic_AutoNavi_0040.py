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
#   @FileName:      PerformanceDynamic_AutoNavi_0040.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   1、点击同意权限弹窗、首页扫描权限、打字权限
#   @详细场景:        
#                  高德地图导航美食-出行
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                 1.启动高德地图（停留7s）
#                 2.点击搜索框（停留5s）
#                 3.点击美食，等待3秒
#                 4.上滑3次浏览美食，每次间隔1秒
#                 5.下滑3次浏览美食，每次间隔1秒
#                 6.点击第一条搜索结果（停留7s）
#                 7.点击路线（停留5s）
#                 8.点击开始导航（停留7s）
#                 9.向右滑动（停留3s）
#                 10.点击推出导航（停留3s）
#                 11.上滑返回桌面（停留1s）
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_AutoNavi_0040(Case):
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
            # 1、打开高德地图
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、打开高德地图")
            SeaOfStarsAW.ut_device.app_start('com.autonavi.minimap', use_monkey=True)
            time.sleep(5)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、打开高德地图", "",
                                                     self.screenshot_dir_path)

            # 2.点击搜索框（停留5s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2.点击搜索框")
            SeaOfStarsAW.ut_device.click(350, 1285)
            time.sleep(5)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2.点击搜索框", "",
                                                     self.screenshot_dir_path)

            # 3.点击美食，等待3秒
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3.点击美食")
            SeaOfStarsAW.ut_device.click(130, 400)
            time.sleep(3)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3.点击美食", "",
                                                     self.screenshot_dir_path)

            # 4.上滑3次浏览美食，每次间隔1秒
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4.上滑3次浏览美食，每次间隔1秒")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4.上滑3次浏览美食，每次间隔1秒", "",
                                                     self.screenshot_dir_path)

            # 5.下滑3次浏览美食，每次间隔1秒
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5.下滑3次浏览美食，每次间隔1秒")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + " 5.下滑3次浏览美食，每次间隔1秒", "",
                                                     self.screenshot_dir_path)

            # 6.点击第一条搜索结果（停留7s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6.点击第一条搜索结果")
            SeaOfStarsAW.ut_device.click(190, 950)
            time.sleep(7)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6.点击第一条搜索结果", "",
                                                     self.screenshot_dir_path)

            # 7.点击路线（停留5s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7.点击路线")
            SeaOfStarsAW.ut_device.click(930, 2260)
            time.sleep(7)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7.点击路线", "",
                                                     self.screenshot_dir_path)

            # 8.点击开始导航（停留7s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8.点击开始导航")
            SeaOfStarsAW.ut_device.click(800, 2230)
            time.sleep(7)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8.点击开始导航", "",
                                                     self.screenshot_dir_path)

            # 9.向右滑动（停留3s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9.向右滑动")
            SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
            time.sleep(3)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9.向右滑动", "",
                                                     self.screenshot_dir_path)

            # 10.点击推出导航（停留3s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10.点击推出导航")
            SeaOfStarsAW.ut_device.click(135, 2210)
            time.sleep(3)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10.点击推出导航", "",
                                                     self.screenshot_dir_path)

            # 11.上滑返回桌面（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11.上滑返回桌面")
            SeaOfStarsAW.return_launcher()
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11.上滑返回桌面", "",
                                                     self.screenshot_dir_path)

        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)