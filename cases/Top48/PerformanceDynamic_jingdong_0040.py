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
#   @FileName:      PerformanceDynamic_jingdong_0040.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   1、登录京东
#                   2、去除弹框
#   @详细场景:        
#                   京东观看直播-购物
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                   1.点击启动京东，等待3s
#                   2.点击底部直播，等待2s
#                   3.浏览直播页面，上滑5次，下滑5次，每次停留2s
#                   4.点击第一个直播间进入，等待2s
#                   5.点击底部输入框，等待2s
#                   6.输入不错并发送，等待2s
#                   7.点击右边购物袋，等待2s
#                   8.浏览购物袋，上滑5次，下滑5次，每次停留2s
#                   9.返回主页面，等待2s
#                   10.点击我的，等待2s
#                   11.点击全部订单，等待2s
#                   12.浏览全部订单页面，上滑2次，下滑2次，每次停留2s
#                   13.点击待收货，等待2s
#                   14.返回首页，等待2s
#                   15.返回home页面，等待2s
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_jingdong_0040(Case):
    all_app_package_list = ['com.jingdong.app.mall']
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
            # 1.点击启动京东，等待3s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1.点击启动京东")
            SeaOfStarsAW.ut_device.app_start('com.jingdong.app.mall', use_monkey=True)
            time.sleep(3)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1.点击启动京东", "",
                                                     self.screenshot_dir_path)

            # 2.点击底部直播，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2.点击底部直播")
            SeaOfStarsAW.ut_device.click(324,2241)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2.点击底部直播", "",
                                                     self.screenshot_dir_path)


            # 3.浏览直播页面，上滑5次，下滑5次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3.浏览直播页面，上滑5次，下滑5次")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.ut_device.click(580, 227)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3.浏览直播页面，上滑5次，下滑5次", "",
                                                     self.screenshot_dir_path)

            # 4.点击第一个直播间进入，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4.点击第一个直播间进入")
            SeaOfStarsAW.ut_device.click(300, 520)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4.点击第一个直播间进入", "",
                                                     self.screenshot_dir_path)

            # 5.点击底部输入框，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5.点击底部输入框")
            SeaOfStarsAW.ut_device.click(339,2261)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5.点击底部输入框", "",
                                                     self.screenshot_dir_path)

            # 6.输入不错并发送，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6.输入不错并发送")
            SeaOfStarsAW.ut_device.send_keys('不错')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(908,2103)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6.输入不错并发送", "",
                                                     self.screenshot_dir_path)

            # 7.点击右边购物袋，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7.点击右边购物袋")
            SeaOfStarsAW.ut_device.click(982,2263)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7.点击右边购物袋", "",
                                                     self.screenshot_dir_path)

            # 8.浏览购物袋，上滑5次，下滑5次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8.浏览购物袋，上滑5次，下滑5次")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8.浏览购物袋，上滑5次，下滑5次", "",
                                                     self.screenshot_dir_path)

            # 9.返回主页面，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info(" 9.返回主页面")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + " 9.返回主页面", "",
                                                     self.screenshot_dir_path)

            # 10.点击我的，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10.点击我的")
            SeaOfStarsAW.ut_device.click(972,2218)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10.点击我的", "",
                                                     self.screenshot_dir_path)

            # 11.点击全部订单，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11.点击全部订单")
            SeaOfStarsAW.ut_device.click(972,1318)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11.点击全部订单", "",
                                                     self.screenshot_dir_path)

            # 12.浏览全部订单页面，上滑2次，下滑2次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12.浏览全部订单页面，上滑2次，下滑2次")
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12.浏览全部订单页面，上滑2次，下滑2次", "",
                                                     self.screenshot_dir_path)

            # 13.点击待收货，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("13.点击待收货")
            SeaOfStarsAW.ut_device.click(380,521)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "13.点击待收货", "",
                                                     self.screenshot_dir_path)

            # 14.返回首页，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("14.返回首页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(115, 2512)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "14.返回首页", "",
                                                     self.screenshot_dir_path)

            # 15.返回home页面，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("15.返回home页面")
            SeaOfStarsAW.return_launcher()
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "15.返回home页面", "",
                                                     self.screenshot_dir_path)

        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)