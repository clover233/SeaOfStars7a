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
#   @FileName:      PerformanceDynamic_AutoNavi_0050.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   1、开通手机访问权限
#                   2、支付宝登录
#   @详细场景:        
#                   支付宝转账
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                     1.启动高德地图（停留7s）
#                     2.地图界面上滑1次浏览（停留3s）
#                     3.地图界面下滑1次浏览（停留3s）
#                     4.地图界面左滑1次浏览（停留3s）
#                     5.地图界面右滑1次浏览（停留3s）
#                     6.双指捏合放大/缩小当前位置地图（停留3s）
#                     7.左滑退出首页（停留1s）
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_AutoNavi_0050(Case):
    all_app_package_list = ['com.autonavi.minimap']
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
            # 1.启动高德地图（停留7s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动高德地图")
            SeaOfStarsAW.ut_device.app_start('com.autonavi.minimap', use_monkey=True)
            time.sleep(7)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、启动高德地图", "",
                                                     self.screenshot_dir_path)

            # 2.地图界面上滑1次浏览（停留3s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2.地图界面上滑1次浏览")
            SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 500, 0.05)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2.地图界面上滑1次浏览", "",
                                                     self.screenshot_dir_path)
            # 3.地图界面下滑1次浏览（停留3s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3.地图界面下滑1次浏览")
            SeaOfStarsAW.scroll_up(0.5)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3.地图界面下滑1次浏览", "",
                                                     self.screenshot_dir_path)
            # 4.地图界面左滑1次浏览（停留3s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4.地图界面左滑1次浏览")
            SeaOfStarsAW.swipe_right(0.5)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4.地图界面左滑1次浏览", "",
                                                     self.screenshot_dir_path)
            # 5.地图界面右滑1次浏览（停留3s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5.地图界面右滑1次浏览")
            SeaOfStarsAW.swipe_left(0.5)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5.地图界面右滑1次浏览", "",
                                                     self.screenshot_dir_path)
            # 6.双指捏合放大 / 缩小当前位置地图（停留3s）
            # SeaOfStarsAW.start_perfetto_trace()
            # logging.info("6.双指捏合放大 / 缩小当前位置地图")
            # SeaOfStarsAW.ut_device.double_click(100, 200, 0.1)
            # time.sleep(3)
            # SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
            #                                          'step_' + "6.双指捏合放大 / 缩小当前位置地图", "",
            #                                          self.screenshot_dir_path)
            # 7.左滑退出首页（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7.左滑退出首页")
            SeaOfStarsAW.return_launcher()
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7.左滑退出首页", "",
                                                     self.screenshot_dir_path)
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)
