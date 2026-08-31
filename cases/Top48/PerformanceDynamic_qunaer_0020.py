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
#   @FileName:      PerformanceDynamic_qunaer_0020.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                     1、登陆账号
#                     2、关闭弹窗
#                     3、火车高铁预置西安至北京
#   @详细场景:        
#                   去哪儿旅行-值机选座-出行
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                 1、启动去哪儿旅行（停留2s）
#                 2、点击 “机票”（停留2s）
#                 3、点击搜索（停留2S）
#                 4、点击搜索结果第一条（停留2S）
#                 5、点击预订（停留1S）
#                 6、滑动浏览（上滑2次，下滑2次，每次停留2s）
#                 7、侧滑3次返回机票页
#                 8、点击“值机选座”（停留2S）
#                 9、上滑1次、下滑1次（每次停留2s）
#                 10、右滑返回去哪儿旅行主页（停留2s）
#                 11、点击“火车高铁”（停留1S）
#                 12、点击“搜索”，进入车次选择页面（停留2S）
#                 13、侧滑2次返回首页（停留2S）
#                 14、上滑返回桌面（停留2s）
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_qunaer_0020(Case):
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
            # 1、启动去哪儿旅行（停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动去哪儿旅行")
            SeaOfStarsAW.ut_device.app_start('com.Qunar', use_monkey=True)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、启动去哪儿旅行", "",
                                                     self.screenshot_dir_path)
            # 2、点击 “机票”（停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、点击 “机票”")
            SeaOfStarsAW.ut_device.click(198, 788)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、点击 “机票”", "",
                                                     self.screenshot_dir_path)
            # 3、点击搜索（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、点击搜索")
            SeaOfStarsAW.ut_device.click(540, 1666)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、点击搜索", "",
                                                     self.screenshot_dir_path)
            # 4、点击搜索结果第一条（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、点击搜索结果第一条")
            SeaOfStarsAW.ut_device.click(540, 1090)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、点击搜索结果第一条", "",
                                                     self.screenshot_dir_path)
            # 5、点击预订（停留1S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、点击预订")
            SeaOfStarsAW.ut_device.click(925, 1850)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、点击预订", "",
                                                     self.screenshot_dir_path)
            # 6、滑动浏览（上滑2次，下滑2次，每次停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、滑动浏览")
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、滑动浏览", "",
                                                     self.screenshot_dir_path)
            # 7、侧滑3次返回机票页
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、侧滑3次返回机票页")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、侧滑3次返回机票页", "",
                                                     self.screenshot_dir_path)
            # 8、点击“值机选座”（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、点击“值机选座”")
            # SeaOfStarsAW.ut_device(description="值机选座").click()
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、点击“值机选座”（", "",
                                                     self.screenshot_dir_path)
            # 9、上滑1次、下滑1次（每次停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、上滑1次、下滑1次")
            SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、上滑1次、下滑1次", "",
                                                     self.screenshot_dir_path)
            # 10、右滑返回去哪儿旅行主页（停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、右滑返回去哪儿旅行主页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、右滑返回去哪儿旅行主页", "",
                                                     self.screenshot_dir_path)
            # 11、点击“火车高铁”（停留1S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、点击“火车高铁”")
            SeaOfStarsAW.ut_device.click(472, 788)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11、点击“火车高铁”", "",
                                                     self.screenshot_dir_path)
            # 12、点击“搜索”，进入车次选择页面（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、点击“搜索”，进入车次选择页面")
            SeaOfStarsAW.ut_device.click(640, 1367)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12、点击“搜索”，进入车次选择页面", "",
                                                     self.screenshot_dir_path)
            # 13、侧滑2次返回首页（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("13、侧滑2次返回首页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "13、侧滑2次返回首页", "",
                                                     self.screenshot_dir_path)
            # 14、上滑返回桌面（停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("14、上滑返回桌面")
            SeaOfStarsAW.return_launcher()
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "14、上滑返回桌面", "",
                                                     self.screenshot_dir_path)


        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)