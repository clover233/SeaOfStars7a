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
#   @FileName:      PerformanceDynamic_meituan_0010.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   1、开通手机访问权限
#                   2、去除弹框
#                   3、提前登录
#   @详细场景:        
#                   美团搜索、浏览下单美食
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                   1、启动美团（停留3s）
#                   2、首页点击外卖（停留1s）
#                   3、点击美食（停留1s）
#                   4、点击搜索框（停留1s）
#                   5、输入黄焖鸡（停留1s）
#                   6、点击搜索（停留1s）
#                   7、滑动浏览（上滑5次，下滑5次，每次停留2s）
#                   8、点击第一家商铺（停留1s）
#                   9、上下各滑动1次浏览商家（停留1s）
#                   10、点击评价，上下各滑动2次浏览评价（停留1s）
#                   11、返回进入点菜界面（停留1s）
#                   12、点击推荐下的第一份食品（停留1s）
#                   13、点击加入购物车（停留1s）
#                   14、再次点击加入购物车（停留1s）
#                   15、点击购物车图标（停留1s）
#                   16、侧滑返回美食界面（停留1s）
#                   17、滑动浏览美食（上滑2次，下滑2次，每次停留2s）
#                   18、返回美团首页（停留1s）
#                   19、返回home界面（停留1s）
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_meituan_0010(Case):
    all_app_package_list = ['com.sankuai.meituan']
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
            # 1、启动美团（停留3s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动美团")
            SeaOfStarsAW.ut_device.app_start('com.sankuai.meituan', use_monkey=True)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、启动美团", "",
                                                     self.screenshot_dir_path)

            # 2、首页点击外卖（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、首页点击外卖")
            SeaOfStarsAW.ut_device.click(138, 541)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、首页点击外卖", "",
                                                     self.screenshot_dir_path)

            # 3、点击美食（停留1s）
            logging.info("3、点击美食")
            SeaOfStarsAW.start_perfetto_trace()
            SeaOfStarsAW.ut_device.click(160,560)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、点击美食", "",
                                                     self.screenshot_dir_path)

            # 4、点击搜索框（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、点击搜索框")
            SeaOfStarsAW.ut_device.click(357,377)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、点击搜索框", "",
                                                     self.screenshot_dir_path)

            # 5、输入黄焖鸡（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、输入黄焖鸡")
            SeaOfStarsAW.ut_device.send_keys('黄焖鸡')
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、输入黄焖鸡", "",
                                                     self.screenshot_dir_path)

            # 6、点击搜索（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、点击搜索")
            SeaOfStarsAW.ut_device.click(933,216)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、点击搜索", "",
                                                     self.screenshot_dir_path)

            # 7、滑动浏览（上滑5次，下滑5次，每次停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、滑动浏览")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、滑动浏览", "",
                                                     self.screenshot_dir_path)

            # 8、点击第一家商铺（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、点击第一家商铺")
            SeaOfStarsAW.ut_device.click(539,630)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、点击第一家商铺", "",
                                                     self.screenshot_dir_path)

            # 9、上下各滑动1次浏览商家（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、上下各滑动1次浏览商家")
            SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、上下各滑动1次浏览商家", "",
                                                     self.screenshot_dir_path)

            # 10、点击评价，上下各滑动2次浏览评价（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、点击评价，上下各滑动2次浏览评价")
            SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
            time.sleep(1)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、点击评价，上下各滑动2次浏览评价", "",
                                                     self.screenshot_dir_path)


            # 11、返回进入点菜界面（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、返回进入点菜界面")
            SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, 0.03)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, 0.03)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11、返回进入点菜界面", "",
                                                     self.screenshot_dir_path)

            # 12、点击推荐下的第一份食品（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、点击推荐下的第一份食品")
            SeaOfStarsAW.ut_device.click(452,1489)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12、点击推荐下的第一份食品", "",
                                                     self.screenshot_dir_path)

            # 13、点击加入购物车（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("13、点击加入购物车")
            SeaOfStarsAW.ut_device.click(1013, 1207)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(895,1617)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "13、点击加入购物车", "",
                                                     self.screenshot_dir_path)

            # 14、再次点击加入购物车（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("14、再次点击加入购物车")
            SeaOfStarsAW.ut_device.click(942, 1619)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "14、再次点击加入购物车", "",
                                                     self.screenshot_dir_path)

            # 15、点击购物车图标（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("15、点击购物车图标")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(119, 2227)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "15、点击购物车图标", "",
                                                     self.screenshot_dir_path)

            # 16、侧滑返回美食界面（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("16、侧滑返回美食界面")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "16、侧滑返回美食界面", "",
                                                     self.screenshot_dir_path)

            # 17、滑动浏览美食（上滑2次，下滑2次，每次停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("17、滑动浏览美食")
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "17、滑动浏览美食", "",
                                                     self.screenshot_dir_path)

            # 18、返回美团首页（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("18、返回美团首页")
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "18、返回美团首页", "",
                                                     self.screenshot_dir_path)

            # 19、返回home界面（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("19、返回home界面")
            SeaOfStarsAW.return_launcher()
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "19、返回home界面", "",
                                                     self.screenshot_dir_path)
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)