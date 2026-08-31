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
#   @FileName:      PerformanceDynamic_qunaer_0010.py
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
#                     1、启动去哪儿旅行（停留2s）
#                     2、点击 “机票”（停留2s）
#                     3、点击“搜索”（停留4s）
#                     4、点击“明天”（停留4s）
#                     5、上滑5次、下滑5次（每次停留2s）
#                     6、上滑到最顶，点击第一个方案（停留4s）
#                     7、上滑5次、下滑5次（每次停留2s）
#                     8、右滑返回去哪儿旅行主页（停留2s）
#                     9、点击“酒店”（停留2S）
#                     10、点击城市，选择西安
#                     11、点击“酒店订单”（停留2S）
#                     12、侧滑返回上一级页面（停留1S）
#                     13、点击开始搜索（停留2S）
#                     14、滑动浏览（上滑2次，下滑2次，每次停留2s）
#                     15、点击搜索结果第一条（停留2S）
#                     16、点击酒店图片（停留1S）
#                     17、滑动浏览（左滑3次，右滑3次，每次停留2S）
#                     18、侧滑5次返回首页（停留2S）
#                     19、上滑返回桌面（停留2s）
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_qunaer_0010(Case):
    all_app_package_list = ['com.Qunar']
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
            # 1、启动去哪儿旅行（停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动去哪儿旅行")
            SeaOfStarsAW.ut_device.app_start('com.Qunar', use_monkey=True)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、启动去哪儿旅行” ", "",
                                                     self.screenshot_dir_path)
            # 2、点击 “机票”（停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、点击 “机票”")
            SeaOfStarsAW.ut_device.click(200, 788)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、点击 “机票” ", "",
                                                     self.screenshot_dir_path)

            # 3、点击“搜索”（停留4s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、点击“搜索”")
            SeaOfStarsAW.ut_device.click(600, 1680)
            time.sleep(4)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、点击“搜索” ", "",
                                                     self.screenshot_dir_path)

            # 4、点击“明天”（停留4s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、点击“明天”")
            SeaOfStarsAW.ut_device.click(260, 380)
            time.sleep(4)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、点击“明天” ", "",
                                                     self.screenshot_dir_path)

            # 5、上滑5次、下滑5次（每次停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、上滑5次、下滑5次")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、上滑5次、下滑5次 ", "",
                                                     self.screenshot_dir_path)

            # 6、上滑到最顶，点击第一个方案（停留4s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、上滑到最顶，点击第一个方案 ")
            SeaOfStarsAW.ut_device.click(700, 1150)
            time.sleep(4)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、上滑到最顶，点击第一个方案 ", "",
                                                     self.screenshot_dir_path)

            # 7、上滑5次、下滑5次（每次停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、上滑5次、下滑5次")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、上滑5次、下滑5次 ", "",
                                                     self.screenshot_dir_path)

            # 8、右滑返回去哪儿旅行主页（停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、右滑返回去哪儿旅行主页")
            for i in range(4):
                SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + " ", "",
                                                     self.screenshot_dir_path)

            # 9、点击“酒店”（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、点击“酒店”")
            SeaOfStarsAW.ut_device.click(200, 600)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、点击“酒店” ", "",
                                                     self.screenshot_dir_path)

            # 10、点击城市，选择西安
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、点击城市，选择西安")
            SeaOfStarsAW.ut_device.click(120, 600)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(400, 1150)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、点击城市，选择西安 ", "",
                                                     self.screenshot_dir_path)

            # 11、点击“酒店订单”（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、点击“酒店订单”")
            SeaOfStarsAW.ut_device.click(300, 1620)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11、点击“酒店订单” ", "",
                                                     self.screenshot_dir_path)

            # 12、侧滑返回上一级页面（停留1S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、侧滑返回上一级页面 ")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12、侧滑返回上一级页面 ", "",
                                                     self.screenshot_dir_path)

            # 13、点击开始搜索（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("13、点击开始搜索")
            SeaOfStarsAW.ut_device.click(600, 1250)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "13、点击开始搜索 ", "",
                                                     self.screenshot_dir_path)

            # 14、滑动浏览（上滑2次，下滑2次，每次停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("14、滑动浏览")
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "14、滑动浏览 ", "",
                                                     self.screenshot_dir_path)

            # 15、点击搜索结果第一条（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("15、点击搜索结果第一条 ")
            SeaOfStarsAW.ut_device.click(500, 1900)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "15、点击搜索结果第一条 ", "",
                                                     self.screenshot_dir_path)

            # 16、点击酒店图片（停留1S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("16、点击酒店图片 ")
            SeaOfStarsAW.ut_device.click(610, 300)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "16、点击酒店图片 ", "",
                                                     self.screenshot_dir_path)

            # 17、滑动浏览（左滑3次，右滑3次，每次停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("17、滑动浏览")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "17、滑动浏览 ", "",
                                                     self.screenshot_dir_path)

            # 18、侧滑5次返回首页（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("18、侧滑5次返回首页 ")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "18、侧滑5次返回首页 ", "",
                                                     self.screenshot_dir_path)

            # 19、上滑返回桌面（停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("19、上滑返回桌面")
            SeaOfStarsAW.return_launcher()
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "19、上滑返回桌面 ", "",
                                                     self.screenshot_dir_path)
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)