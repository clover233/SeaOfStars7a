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
#   @FileName:      PerformanceDynamic_Douyin_0050.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   1、登录
#                   2、收藏胡锡进的前三个作品
#   @详细场景:        
#                   抖音tab页浏览
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                 1、点击进入抖音（停留3s）
#                 2、点击顶部经验，停留1s
#                 3、上滑3次，下滑3次，停留1s
#                 4、点击热点，，停留1s
#                 5、上滑3次，下滑3次，停留1s
#                 6、点击查看热榜，停留1s
#                 7、点击完整热榜，停留1s
#                 8、向左滑动6次，停留1s
#                 9、返回热点，停留1s
#                 10、点击直播，停留1s
#                 11、向上滑动6次，停留1s
#                 12、点击长视频，停留1s
#                 13、上滑3次，下滑3次，停留1s
#                 14、点击+号，停留1s
#                 15、点击相册，停留1s
#                 16、上滑3次，下滑3次，停留1s
#                 17、返回上一层，停留1s
#                 18、点击选择音乐，停留1s
#                 19、向上滑动6次，停留1s
#                 20、返回首页，停留1s
#                 21、点击我，停留1s
#                 22、点击收藏，停留1s
#                 23、点第一个收藏的作品，停留1s
#                 24、向上滑动3次浏览，停留1s
#                 25、返回我页面，停留1s
#                 26、点击我的钱包，停留1s
#                 27、返回首页，停留1s
#                 28、退出抖音
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_Douyin_0050(Case):
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
            # 1、点击进入抖音（停留3s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、点击进入抖音")
            SeaOfStarsAW.ut_device.app_start('com.ss.android.ugc.aweme', use_monkey=True)
            time.sleep(3)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、点击进入抖音", "",
                                                     self.screenshot_dir_path)

            # 2、点击顶部经验，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、点击顶部经验，停留1s")
            SeaOfStarsAW.ut_device.click(234, 219)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(234, 219)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(234, 219)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、点击顶部经验，停留1s", "",
                                                     self.screenshot_dir_path)

            # 3、上滑3次，下滑3次，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、上滑3次，下滑3次，停留1s")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(1)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、上滑3次，下滑3次，停留1s", "",
                                                     self.screenshot_dir_path)

            # 4、点击热点，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、点击热点")
            SeaOfStarsAW.ut_device.click(550, 228)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、点击热点", "",
                                                     self.screenshot_dir_path)

            # 5、上滑3次，下滑3次，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、上滑3次，下滑3次")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(1)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、上滑3次，下滑3次", "",
                                                     self.screenshot_dir_path)

            # 6、点击查看热榜，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、点击查看热榜")
            SeaOfStarsAW.ut_device.click(870, 600)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、点击查看热榜", "",
                                                     self.screenshot_dir_path)

            # 7、点击完整热榜，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、点击完整热榜")
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、点击完整热榜", "",
                                                     self.screenshot_dir_path)

            # 8、向左滑动6次，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、向左滑动6次")
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、向左滑动6次", "",
                                                     self.screenshot_dir_path)

            # 9、返回热点，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、返回热点")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、返回热点", "",
                                                     self.screenshot_dir_path)

            # 10、点击直播，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、点击直播")
            SeaOfStarsAW.ut_device.click(800, 219)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、点击直播", "",
                                                     self.screenshot_dir_path)

            # 11、向上滑动6次，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、向上滑动6次")
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11、向上滑动6次", "",
                                                     self.screenshot_dir_path)

            # 12、点击长视频，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、点击长视频")
            SeaOfStarsAW.ut_device.click(585, 1480)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12、点击长视频", "",
                                                     self.screenshot_dir_path)

            # 13、上滑3次，下滑3次，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("13、上滑3次，下滑3次")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(1)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "13、上滑3次，下滑3次", "",
                                                     self.screenshot_dir_path)

            # 14、点击+号，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("14、点击+号")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(540, 2270)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "14、点击+号", "",
                                                     self.screenshot_dir_path)

            # 15、点击相册，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("15、点击相册")
            SeaOfStarsAW.ut_device.click(868, 1903)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "15、点击相册", "",
                                                     self.screenshot_dir_path)

            # 16、上滑3次，下滑3次，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("16、上滑3次，下滑3次")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(1)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.05)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "16、上滑3次，下滑3次", "",
                                                     self.screenshot_dir_path)

            # 17、返回上一层，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("17、返回上一层")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "17、返回上一层", "",
                                                     self.screenshot_dir_path)

            # 18、点击选择音乐，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("18、点击选择音乐")
            SeaOfStarsAW.ut_device.click(571, 235)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "18、点击选择音乐", "",
                                                     self.screenshot_dir_path)

            # 19、向上滑动6次，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("19、向上滑动6次")
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "19、向上滑动6次", "",
                                                     self.screenshot_dir_path)

            # 20、返回首页，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("20、返回首页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "20、返回首页", "",
                                                     self.screenshot_dir_path)

            # 21、点击我，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("21、点击我")
            SeaOfStarsAW.ut_device.click(971, 2269)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "21、点击我", "",
                                                     self.screenshot_dir_path)

            # 22、点击收藏，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("22、点击收藏")
            SeaOfStarsAW.ut_device.click(675, 1426)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "22、点击收藏", "",
                                                     self.screenshot_dir_path)

            # 23、点第一个收藏的作品，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("23、点第一个收藏的作品")
            SeaOfStarsAW.ut_device.click(179, 2037)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "23、点第一个收藏的作品", "",
                                                     self.screenshot_dir_path)

            # 24、向上滑动3次浏览，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("24、向上滑动3次浏览")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "24、向上滑动3次浏览", "",
                                                     self.screenshot_dir_path)

            # 25、返回我页面，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("25、返回我页面")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "25、返回我页面", "",
                                                     self.screenshot_dir_path)

            # 26、点击我的钱包，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("26、点击我的钱包")
            SeaOfStarsAW.ut_device.click(520, 1193)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "26、点击我的钱包", "",
                                                     self.screenshot_dir_path)

            # 27、返回首页，停留1s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("27、返回首页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "27、返回首页", "",
                                                     self.screenshot_dir_path)

            # 28、退出抖音
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("28、退出抖音")
            SeaOfStarsAW.return_launcher()
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "28、退出抖音", "",
                                                     self.screenshot_dir_path)
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)