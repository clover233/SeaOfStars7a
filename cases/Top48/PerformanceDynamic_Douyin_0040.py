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
#   @FileName:      PerformanceDynamic_Douyin_0040.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   1、登录抖音账号
#   @详细场景:        
#                   抖音首页-推荐观看视频并评论/点赞
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                   1、启动抖音
#                   2、上滑10次浏览推荐页面视频
#                   3、下滑10次浏览推荐页面视频
#                   4、搜索胡锡进
#                   5、返回首页
#                   6、点击评论按钮
#                   7、点击输入框
#                   8、输入“我是评论ABC”
#                   9、点击发送
#                   10、侧滑一次返回
#                   11、点击点赞按钮
#                   12、点击商城，2s
#                   13、上滑3次浏览推荐商品，2s
#                   14、下滑3次浏览推荐商品，2s
#                   15、搜索华为p70，2s
#                   16、上滑3次浏览推荐商品，2s
#                   17、下滑3次浏览推荐商品，2s
#                   18、点进第一个商品，2s
#                   19、上滑3次浏览，2s
#                   20、点击左下角客服，2s
#                   21、返回到商品详情页，1s
#                   22、点击左下角 进店，2s
#                   23、上滑3次浏览，2s
#                   24、返回抖音首页，2s
#                   25、点击长视频，2s
#                   26、向左滑动，依次切换顶部tab页(长视频-关注-商城-推荐)，循环3次
#                   27、上滑返回桌面，2s
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_Douyin_0040(Case):
    all_app_package_list = ['com.ss.android.ugc.aweme',]
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
            # 1、启动抖音
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动抖音")
            SeaOfStarsAW.ut_device.app_start('com.ss.android.ugc.aweme', use_monkey=True)
            time.sleep(3)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、点击进入抖音", "",
                                                     self.screenshot_dir_path)

            # 2、上滑10次浏览推荐页面视频
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、上滑10次浏览推荐页面视频")
            for i in range(10):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、上滑10次浏览推荐页面视频", "",
                                                     self.screenshot_dir_path)

            # 3、下滑10次浏览推荐页面视频
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、下滑10次浏览推荐页面视频")
            for i in range(10):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、下滑10次浏览推荐页面视频", "",
                                                     self.screenshot_dir_path)

            # 4、搜索胡锡进
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、搜索胡锡进")
            SeaOfStarsAW.ut_device.click(970,192)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(500, 220)
            time.sleep(2)
            SeaOfStarsAW.ut_device.send_keys('胡锡进')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(992, 225)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、搜索胡锡进", "",
                                                     self.screenshot_dir_path)

            # 5、返回首页
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、返回首页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.4)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.6)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.6)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、返回首页", "",
                                                     self.screenshot_dir_path)


            # 6、点击评论按钮
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、点击评论按钮")
            SeaOfStarsAW.ut_device.click(980,1410)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、点击评论按钮", "",
                                                     self.screenshot_dir_path)

            # 7、点击输入框
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、点击输入框")
            SeaOfStarsAW.ut_device.click(346,2248)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、点击输入框", "",
                                                     self.screenshot_dir_path)

            # 8、输入“我是评论ABC”
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、输入“我是评论ABC”")
            SeaOfStarsAW.ut_device.send_keys('我是评论ABC')
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、输入“我是评论ABC”", "",
                                                     self.screenshot_dir_path)

            # 9、点击发送
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、点击发送")
            SeaOfStarsAW.ut_device.click(912,2146)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、点击发送", "",
                                                     self.screenshot_dir_path)

            # 10、侧滑一次返回
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、侧滑一次返回")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、侧滑一次返回", "",
                                                     self.screenshot_dir_path)

            # 11、点击点赞按钮
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、点击点赞按钮")
            SeaOfStarsAW.ut_device.click(984,1188)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11、点击点赞按钮", "",
                                                     self.screenshot_dir_path)

            # 12、点击商城，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、点击商城")
            SeaOfStarsAW.ut_device.click(689,228)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12、点击商城", "",
                                                     self.screenshot_dir_path)

            # 13、上滑3次浏览推荐商品，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("13、上滑3次浏览推荐商品")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "13、上滑3次浏览推荐商品", "",
                                                     self.screenshot_dir_path)

            # 14、下滑3次浏览推荐商品，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("14、下滑3次浏览推荐商品")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "14、下滑3次浏览推荐商品", "",
                                                     self.screenshot_dir_path)

            # 15、搜索华为p70，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("15、搜索华为p70")
            SeaOfStarsAW.ut_device.click(114,352)
            time.sleep(2)
            SeaOfStarsAW.ut_device.send_keys('华为p70')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(865,350)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "15、搜索华为p70", "",
                                                     self.screenshot_dir_path)

            # 16、上滑3次浏览推荐商品，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("16、上滑3次浏览推荐商品")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "16、上滑3次浏览推荐商品", "",
                                                     self.screenshot_dir_path)

            # 17、下滑3次浏览推荐商品，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("17、下滑3次浏览推荐商品")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "17、下滑3次浏览推荐商品", "",
                                                     self.screenshot_dir_path)

            # 18、点进第一个商品，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("18、点进第一个商品")
            SeaOfStarsAW.ut_device.click(526,1591)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "18、点进第一个商品", "",
                                                     self.screenshot_dir_path)

            # 19、上滑3次浏览，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("19、上滑3次浏览")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "19、上滑3次浏览", "",
                                                     self.screenshot_dir_path)

            # 20、点击左下角客服，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("20、点击左下角客服")
            SeaOfStarsAW.ut_device.click(196,2235)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "20、点击左下角客服", "",
                                                     self.screenshot_dir_path)

            # 21、返回到商品详情页，1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("21、返回到商品详情页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "21、返回到商品详情页", "",
                                                     self.screenshot_dir_path)

            # 22、点击左下角 进店，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("22、点击左下角 进店")
            SeaOfStarsAW.ut_device.click(52,2235)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "22、点击左下角 进店", "",
                                                     self.screenshot_dir_path)

            # 23、上滑3次浏览，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("23、上滑3次浏览")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "23、上滑3次浏览", "",
                                                     self.screenshot_dir_path)

            # 24、返回抖音首页，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("24、返回抖音首页")
            for i in range(7):
                SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "24、返回抖音首页", "",
                                                     self.screenshot_dir_path)

            # 25、点击长视频，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("25、点击长视频")
            SeaOfStarsAW.ut_device.click(231,229)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "25、点击长视频", "",
                                                     self.screenshot_dir_path)

            # 26、向左滑动，依次切换顶部tab页(长视频-关注-商城-推荐)，循环3次
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("26、向左滑动，依次切换顶部tab页(长视频-关注-商城-推荐)，循环3次")
            for i in range(3):
                SeaOfStarsAW.ut_device.click(559,227)
                time.sleep(2)
                SeaOfStarsAW.ut_device.click(682,200)
                time.sleep(2)
                SeaOfStarsAW.ut_device.click(231,203)
                time.sleep(2)
                SeaOfStarsAW.ut_device.click(801,193)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "26、向左滑动，依次切换顶部tab页(长视频-关注-商城-推荐)，循环3次", "",
                                                     self.screenshot_dir_path)

            # 27、上滑返回桌面，2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("27、上滑返回桌面")
            SeaOfStarsAW.return_launcher()
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "27、上滑返回桌面", "",
                                                     self.screenshot_dir_path)

        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)