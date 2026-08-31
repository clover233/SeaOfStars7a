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
#   @FileName:      PerformanceDynamic_Kuaishou_0010.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   1、登录快手账号
#                   2、允许相关弹窗
#                   3、添加测试账号
#   @详细场景:        
#                   快手观看推荐视频，和测试账号聊天
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                   1、点击进入快手(启动5s，可能有广告，停留2s)
#                   2、浏览并向下滑切换视频（视频浏览10s，20S,下滑切换1s，浏览三个）
#                   3、点击评论（单框架上评论功能未开发完成）
#                   4、上滑2次，下滑2次
#                   5、点击“赞”
#                   6、点击“收藏”
#                   7、点击消息（2s）
#                   8、点击测试账号聊天（2s）
#                   9、发送“华为手机”给测试账号（2s）
#                   10、返回快手首页（2s）
#                   11、返回home界面（2s）
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_Kuaishou_0010(Case):
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
            # 1、点击进入快手(启动5s，可能有广告，停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、点击进入快手")
            SeaOfStarsAW.ut_device.app_start('com.smile.gifmaker', use_monkey=True)
            time.sleep(5)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、点击进入快手", "",
                                                     self.screenshot_dir_path)

            # 2、浏览并向下滑切换视频（视频浏览10s，20S,下滑切换1s，浏览三个）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、浏览并向下滑切换视频")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(10)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、浏览并向下滑切换视频", "",
                                                     self.screenshot_dir_path)

            # 3、点击评论（单框架上评论功能未开发完成）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、点击评论")
            SeaOfStarsAW.ut_device.click(921, 1459)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、点击评论", "",
                                                     self.screenshot_dir_path)

            # 4、上滑2次，下滑2次
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、上滑2次，下滑2次")
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(3)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、上滑2次，下滑2次", "",
                                                     self.screenshot_dir_path)

            # 5、点击“赞”
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、点击“赞”")
            SeaOfStarsAW.ut_device.click(995, 1235)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、点击“赞”", "",
                                                     self.screenshot_dir_path)

            # 6、点击“收藏”
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、点击“收藏”")
            SeaOfStarsAW.ut_device.click(955, 1606)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、点击“收藏”", "",
                                                     self.screenshot_dir_path)

            # 7、点击消息（2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、点击消息")
            SeaOfStarsAW.ut_device.click(759,2289)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、点击消息", "",
                                                     self.screenshot_dir_path)

            # 8、点击测试账号聊天（2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、点击测试账号聊天")
            SeaOfStarsAW.ut_device.click(280,1281)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、点击测试账号聊天", "",
                                                     self.screenshot_dir_path)

            # 9、发送“华为手机”给测试账号（2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、发送“华为手机”给测试账号")
            SeaOfStarsAW.ut_device.click(475,2243)
            time.sleep(2)
            SeaOfStarsAW.ut_device.send_keys('华为手机')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(955, 2103)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、发送“华为手机”给测试账号", "",
                                                     self.screenshot_dir_path)

            # 10、返回快手首页（2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、返回快手首页")
            SeaOfStarsAW.ut_device.click(48, 222)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(106, 2282)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、返回快手首页", "",
                                                     self.screenshot_dir_path)

            # 11、返回home界面（2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、返回home界面")
            SeaOfStarsAW.return_launcher()
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11、返回home界面", "",
                                                     self.screenshot_dir_path)
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)