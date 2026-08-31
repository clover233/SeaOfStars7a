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
#   @FileName:      PerformanceDynamic_Alipay_0070.py
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
#                     1、启动支付宝（停留2s)
#                     2、点击“医疗健康”（停留2s)
#                     3、侧滑返回首页（停留2s)
#                     4、第二次点击“医疗健康”（停留2s)
#                     5、上滑1次浏览（停留2s)
#                     6、下滑1次浏览（停留2s)
#                     7、侧滑返回首页（停留2s)
#                     8、点击“蚂蚁森林”（停留2s)
#                     9、上滑1次浏览（停留2s)
#                     10、下滑1次浏览（停留2s)
#                     11、点击“返回”按钮，返回首页（停留2s)
#                     12、点击视频（停留2s)
#                     13、上滑5次，下滑5次观看视频（停留2s)
#                     14、点击评论（停留2s)
#                     15、退出评论（停留2s)
#                     16、点击直播（停留2s)
#                     17、上滑5次，下滑5次观看视频（停留1s)
#                     18、进入直播间观看直播10s
#                     19、退出直播间（停留2s)
#                     20、点击短剧（停留2s)
#                     21、上滑5次，下滑5次浏览短剧页面（停留2s)
#                     22、点击热播榜（停留2s)
#                     23、上滑2次，下滑2次浏览热播榜（停留2s)
#                     24、点击播放热播榜第一的短剧观看15s
#                     25、返回视频页（停留2s)
#                     26、返回首页（停留2s)
#                     27、返回home页
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_Alipay_0070(Case):
    all_app_package_list = ['com.eg.android.AlipayGphone']
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
            # 1、启动支付宝（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动支付宝")
            SeaOfStarsAW.ut_device.app_start('com.eg.android.AlipayGphone', use_monkey=True)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、启动支付宝", "",
                                                     self.screenshot_dir_path)

            # 2、点击“医疗健康”（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、点击“医疗健康”")
            SeaOfStarsAW.ut_device.click(540, 590)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、点击“医疗健康”", "",
                                                     self.screenshot_dir_path)

            # 3、侧滑返回首页（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、侧滑返回首页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、侧滑返回首页", "",
                                                     self.screenshot_dir_path)

            # 4、第二次点击“医疗健康”（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、第二次点击“医疗健康”")
            SeaOfStarsAW.ut_device.click(540, 590)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、第二次点击“医疗健康”", "",
                                                     self.screenshot_dir_path)

            # 5、上滑1次浏览（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、上滑1次浏览")
            SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、上滑1次浏览", "",
                                                     self.screenshot_dir_path)

            # 6、下滑1次浏览（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、下滑1次浏览")
            SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、下滑1次浏览", "",
                                                     self.screenshot_dir_path)

            # 7、侧滑返回首页（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、侧滑返回首页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、侧滑返回首页", "",
                                                     self.screenshot_dir_path)

            # 8、点击“蚂蚁森林”（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、点击“蚂蚁森林”")
            SeaOfStarsAW.ut_device.click(140, 600)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、点击“蚂蚁森林”", "",
                                                     self.screenshot_dir_path)

            # 9、上滑1次浏览（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、上滑1次浏览")
            SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、上滑1次浏览", "",
                                                     self.screenshot_dir_path)

            # 10、下滑1次浏览（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、下滑1次浏览")
            SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、下滑1次浏览", "",
                                                     self.screenshot_dir_path)

            # 11、点击“返回”按钮，返回首页（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info(" 11、点击“返回”按钮，返回首页")
            SeaOfStarsAW.ut_device.click(60, 230)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + " 11、点击“返回”按钮，返回首页", "",
                                                     self.screenshot_dir_path)

            # 12、点击视频（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、点击视频")
            SeaOfStarsAW.ut_device.click(540, 2240)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12、点击视频", "",
                                                     self.screenshot_dir_path)

            # 13、上滑5次，下滑5次观看视频（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("13、上滑5次，下滑5次观看视频")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "13、上滑5次，下滑5次观看视频", "",
                                                     self.screenshot_dir_path)

            # 14、点击评论（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("14、点击评论")
            SeaOfStarsAW.ut_device.click(990, 1500)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "14、点击评论", "",
                                                     self.screenshot_dir_path)

            # 15、退出评论（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("15、退出评论")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "15、退出评论", "",
                                                     self.screenshot_dir_path)

            # 16、点击直播（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("16、点击直播")
            SeaOfStarsAW.ut_device.click(550, 200)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "16、点击直播", "",
                                                     self.screenshot_dir_path)

            # 17、上滑5次，下滑5次观看视频（停留1s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("17、上滑5次，下滑5次观看视频")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "17、上滑5次，下滑5次观看视频", "",
                                                     self.screenshot_dir_path)

            # 18、进入直播间观看直播10s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("18、进入直播间观看直播")
            SeaOfStarsAW.ut_device.click(500, 1670)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "18、进入直播间观看直播", "",
                                                     self.screenshot_dir_path)

            # 19、退出直播间（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("19、退出直播间")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "19、退出直播间", "",
                                                     self.screenshot_dir_path)

            # 20、点击短剧（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("20、点击短剧")
            SeaOfStarsAW.ut_device.click(740, 220)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "20、点击短剧", "",
                                                     self.screenshot_dir_path)

            # 21、上滑5次，下滑5次浏览短剧页面（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("21、上滑5次，下滑5次浏览短剧页面")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "21、上滑5次，下滑5次浏览短剧页面", "",
                                                     self.screenshot_dir_path)

            # 22、点击热播榜（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("22、点击热播榜")
            SeaOfStarsAW.ut_device.click(1000, 220)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "22、点击热播榜", "",
                                                     self.screenshot_dir_path)

            # 23、上滑2次，下滑2次浏览热播榜（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("23、上滑2次，下滑2次浏览热播榜")
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "23、上滑2次，下滑2次浏览热播榜", "",
                                                     self.screenshot_dir_path)

            # 24、点击播放热播榜第一的短剧观看15s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("24、点击播放热播榜第一的短剧观看15s")
            SeaOfStarsAW.ut_device.click(600, 1400)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "24、点击播放热播榜第一的短剧观看15s", "",
                                                     self.screenshot_dir_path)

            # 25、返回视频页（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("25、返回视频页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "25、返回视频页", "",
                                                     self.screenshot_dir_path)

            # 26、返回首页（停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("26、返回首页")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "26、返回首页", "",
                                                     self.screenshot_dir_path)

            # 27、返回home页
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("27、返回home页")
            SeaOfStarsAW.return_launcher()
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "27、返回home页", "",
                                                     self.screenshot_dir_path)

        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)