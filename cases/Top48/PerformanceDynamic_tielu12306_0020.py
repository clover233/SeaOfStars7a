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
#   @FileName:      PerformanceDynamic_tielu12306_0020.py
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
#                     1、启动铁路12306（停留1s）
#                     2、向上抛滑2次，浏览首页
#                     3、点击任一酒店（停留1s）
#                     4、返回上一页（停留1s）
#                     5、点击出行服务（停留1s）
#                     6、点击订单（停留1s）
#                     7、点击铁路会员（停留1s）
#                     8、点击首页（停留1s）
#                     9、下抛滑2次，浏览信息，每次等待2s
#                     10、上滑退回到桌面   
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_tielu12306_0020(Case):
    all_app_package_list = ['com.MobileTicket']
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
            # 1、启动铁路12306（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动铁路12306")
            SeaOfStarsAW.ut_device.app_start('com.MobileTicket', use_monkey=True)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、启动铁路12306", "",
                                                     self.screenshot_dir_path)

            # 2、向上抛滑2次，浏览首页
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、向上抛滑2次，浏览首页")
            time.sleep(3)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、向上抛滑2次，浏览首页", "",
                                                     self.screenshot_dir_path)

            # 3、点击任一酒店（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、点击任一酒店")
            SeaOfStarsAW.ut_device.click(572,1620)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、点击任一酒店", "",
                                                     self.screenshot_dir_path)

            # 4、返回上一页（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、返回上一页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、返回上一页", "",
                                                     self.screenshot_dir_path)

            # 5、点击出行服务（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、点击出行服务")
            SeaOfStarsAW.ut_device.click(366, 2254)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、点击出行服务", "",
                                                     self.screenshot_dir_path)

            # 6、点击订单（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、点击订单")
            SeaOfStarsAW.ut_device.click(605, 2254)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、点击订单", "",
                                                     self.screenshot_dir_path)

            # 7、点击铁路会员（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、点击铁路会员")
            SeaOfStarsAW.ut_device.click(851, 2254)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、点击铁路会员", "",
                                                     self.screenshot_dir_path)

            # 8、点击首页（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、点击首页")
            SeaOfStarsAW.ut_device.click(116, 2254)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、点击首页", "",
                                                     self.screenshot_dir_path)

            # 9、下抛滑2次，浏览信息，每次等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、下抛滑2次，浏览信息")
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、下抛滑2次，浏览信息", "",
                                                     self.screenshot_dir_path)

            # 10、上滑退回到桌面
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、上滑退回到桌面")
            SeaOfStarsAW.return_launcher()
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、上滑退回到桌面", "",
                                                     self.screenshot_dir_path)

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
        logger = logging.getLogger()
        logger.removeHandler(self.fh)