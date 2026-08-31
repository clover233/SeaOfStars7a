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
#   @FileName:      PerformanceDynamic_Douyin_0030.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   1、登录账号
#                   2、关注好友并且发送消息(好友名称为：动态XX)
#   @详细场景:        
#                   抖音查看好友消息详情、系统消息
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                   1、点击进入抖音（停留3s）
#                   2、进入消息页面（1s）
#                   3、进入测试账号聊天界面（2s）
#                   4、发送文字“华为手机”（2s）
#                   5、点击“+”（停留1S）
#                   6、点击“拍摄”（停留2S）
#                   7、拍摄图片（停留2s）
#                   8、点击发送（停留2S）
#                   9、点击“+”（停留1S）
#                   10、点击相册（停留1S）
#                   11、上滑3次，下滑3次（停留2S）
#                   12、点击第一张图片（停留1S）
#                   13、点击发送（停留2S）
#                   14、返回消息页面（1s）
#                   15、查看系统消息（2s）
#                   16、上滑2次，下滑2次，等待2s
#                   17、返回主页（1s）
#                   18、返回home界面（1s）
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_Douyin_0030(Case):
    all_app_package_list = ['com.ss.android.ugc.aweme']
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
            # 1、点击进入抖音（停留3s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、点击进入抖音")
            SeaOfStarsAW.ut_device.app_start('com.ss.android.ugc.aweme', use_monkey=True)
            time.sleep(3)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、点击进入抖音", "",
                                                     self.screenshot_dir_path)

            # 2、进入消息页面（1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、进入消息页面")
            SeaOfStarsAW.ut_device.click(796,2281)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、进入消息页面", "",
                                                     self.screenshot_dir_path)

            # 3、进入测试账号聊天界面（2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、进入测试账号聊天界面")
            SeaOfStarsAW.ut_device.click(52,1555)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、进入测试账号聊天界面", "",
                                                     self.screenshot_dir_path)

            # 4、发送文字“华为手机”（2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、发送文字“华为手机”")
            SeaOfStarsAW.ut_device.click(287,2260)
            time.sleep(2)
            SeaOfStarsAW.ut_device.send_keys('华为手机')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(952,2181)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、发送文字“华为手机”", "",
                                                     self.screenshot_dir_path)

            # 5、点击“+”（停留1S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、点击“+”")
            SeaOfStarsAW.ut_device.click(980,2200)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' +"5、点击“+”" , "",
                                                     self.screenshot_dir_path)

            # 6、点击“拍摄”（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info(" 6、点击“拍摄”")
            SeaOfStarsAW.ut_device.click(412,1644)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + " 6、点击“拍摄”", "",
                                                     self.screenshot_dir_path)

            # 7、拍摄图片（停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、拍摄图片")
            SeaOfStarsAW.ut_device.click(600, 1862)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、拍摄图片", "",
                                                     self.screenshot_dir_path)

            # 8、点击发送（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、点击发送")
            SeaOfStarsAW.ut_device.click(885,2204)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、点击发送", "",
                                                     self.screenshot_dir_path)

            # 9、点击“+”（停留1S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、点击“+”")
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、点击“+”", "",
                                                     self.screenshot_dir_path)

            # 10、点击相册（停留1S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、点击相册")
            SeaOfStarsAW.ut_device.click(140,1604)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、点击相册", "",
                                                     self.screenshot_dir_path)

            # 11、上滑3次，下滑3次（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、上滑3次，下滑3次")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' +"11、上滑3次，下滑3次", "",
                                                     self.screenshot_dir_path)

            # 12、点击第一张图片（停留1S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、点击第一张图片")
            SeaOfStarsAW.ut_device.click(281, 649)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' +"12、点击第一张图片", "",
                                                     self.screenshot_dir_path)

            # 13、点击发送（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("13、点击发送")
            SeaOfStarsAW.ut_device.click(882,2257)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' +"13、点击发送", "",
                                                     self.screenshot_dir_path)

            # 14、返回消息页面（1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("14、返回消息页面")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' +"14、返回消息页面", "",
                                                     self.screenshot_dir_path)

            # 15、查看系统消息（2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("15、查看系统消息")
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' +"15、查看系统消息", "",
                                                     self.screenshot_dir_path)

            # 16、上滑2次，下滑2次，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("16、上滑2次，下滑2次")
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "16、上滑2次，下滑2次", "",
                                                     self.screenshot_dir_path)

            # 17、返回主页（1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("17、返回主页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "17、返回主页", "",
                                                     self.screenshot_dir_path)

            # 18、返回home界面（1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("18、返回home界面")
            SeaOfStarsAW.return_launcher()
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "18、返回home界面", "",
                                                     self.screenshot_dir_path)
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)