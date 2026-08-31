import logging
import os
import shutil
import time
import uiautomator2 as u2
from uiautomator2 import Device
from Cases.CaseBase import Case
from aw_new import SeaOfStarsAW

"""
#!+======================================================================================
# 版权 (C) 海思半导体有限公司 2025 海思Kirin解决方案集成与验证部用户体验组
# Copyright (C) Hisilicon Technologies Co., Ltd. 2025. All rights reserved.
#========================================================================================
#   @FileName:      PerformanceDynamic_Kuaishou_0020.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   1、登录快手账号
#                   2、允许相关弹窗
#   @详细场景:        
#                   快手搜索，观看直播间
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                   1、启动快手（5s）
#                   2、点击首页右上角搜索图标，1s（2-6单框架功能均未开发）
#                   3、搜索：“华为手机”（停留2S）
#                   4、上滑3次，下滑3次，（停留2s）
#                   5、返回搜索页
#                   6、点击直播榜（1s）
#                   7、点击排名第一的直播账号，查看直播15s
#                   8、上滑查看下一个直播，15s
#                   9、左滑3次返回首页
#                   10、上滑返回桌面
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_Kuaishou_0020(Case):
    all_app_package_list = ['com.smile.gifmaker']
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
            # 1、启动快手（5s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动快手")
            SeaOfStarsAW.ut_device.app_start('com.smile.gifmaker', use_monkey=True)
            time.sleep(5)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、启动快手", "",
                                                     self.screenshot_dir_path)

            # 2、点击首页右上角搜索图标，1s（2-6单框架功能均未开发）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、点击首页右上角搜索图标")
            SeaOfStarsAW.ut_device.click(995,206)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、点击首页右上角搜索图标", "",
                                                     self.screenshot_dir_path)

            # 3、搜索：“华为手机”（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、搜索：“华为手机”")
            SeaOfStarsAW.ut_device.send_keys('华为手机')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(914, 219)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、搜索：“华为手机”", "",
                                                     self.screenshot_dir_path)

            # 4、上滑3次，下滑3次，（停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、上滑3次，下滑3次")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、上滑3次，下滑3次", "",
                                                     self.screenshot_dir_path)

            # 5、返回搜索页
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、返回搜索页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、返回搜索页", "",
                                                     self.screenshot_dir_path)

            # 6、点击直播榜（1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、点击直播榜")
            SeaOfStarsAW.ut_device.click(900,1399)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、点击直播榜", "",
                                                     self.screenshot_dir_path)

            # 7、点击排名第一的直播账号，查看直播15s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、点击排名第一的直播账号，查看直播15s")
            SeaOfStarsAW.ut_device.click(342,1747)
            time.sleep(15)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、点击排名第一的直播账号，查看直播15s", "",
                                                     self.screenshot_dir_path)

            # 8、上滑查看下一个直播，15s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、上滑查看下一个直播")
            SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
            time.sleep(15)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、上滑查看下一个直播", "",
                                                     self.screenshot_dir_path)

            # 9、左滑3次返回首页
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、左滑3次返回首页")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、左滑3次返回首页", "",
                                                     self.screenshot_dir_path)

            # 10、上滑返回桌面
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、上滑返回桌面")
            SeaOfStarsAW.return_launcher()
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、上滑返回桌面", "",
                                                     self.screenshot_dir_path)

        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)