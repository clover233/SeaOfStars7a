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
#   @FileName:      PerformanceDynamic_jingdong_0030.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   1、登录京东
#                   2、去除弹框
#   @详细场景:        
#                   京东搜索商品购物，查看商品图片，进入客服界面
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                   1.点击启动京东，等待3s
#                   2.点击搜索框，等待2s
#                   3.搜索华为手机，等待2s
#                   4.搜索结果页浏览，上滑5次，下滑5次，每次停留2s
#                   5.点击顶部“销量“，等待2s
#                   6.点击第一个商品进入详情页，等待2s
#                   7.浏览详情页，上滑5次，下滑5次，每次停留2s
#                   8、点击商品图片（停留2S）
#                   9、滑动浏览（左滑3次，右滑3次，每次停留2S）
#                   10、侧滑返回商品详情页
#                   11、上滑至“评价”
#                   12.点击评价，等待2s
#                   13.点击全部评价，等待2s
#                   14.浏览全部评价，上滑3次，下滑3次，每次停留2s
#                   15.点击左下角店铺，等待2s
#                   16.浏览店铺，上滑3次，下滑3次，每次停留2s
#                   17.返回商品详情页，等待2s
#                   18.点击客服，等待2s
#                   19.返回商品详情页，等待2s
#                   20.点击立即购买，等待2s
#                   21.点击确认，等待2s
#                   22.返回首页，等待2s
#                   23.返回home页面，等待2s
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_jingdong_0030(Case):
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

            # 2.点击搜索框，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2.点击搜索框")
            SeaOfStarsAW.ut_device.click(350, 350)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2.点击搜索框", "",
                                                     self.screenshot_dir_path)

            # 3.搜索华为手机，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3.搜索华为手机")
            SeaOfStarsAW.ut_device.send_keys('华为手机')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(902,234)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3.搜索华为手机", "",
                                                     self.screenshot_dir_path)

            # 4.搜索结果页浏览，上滑5次，下滑5次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4.搜索结果页浏览，上滑5次，下滑5次")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4.搜索结果页浏览，上滑5次，下滑5次", "",
                                                     self.screenshot_dir_path)

            # 5.点击顶部“销量“，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5.点击顶部“销量“")
            SeaOfStarsAW.ut_device.click(793,369)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5.点击顶部“销量“", "",
                                                     self.screenshot_dir_path)

            # 6.点击第一个商品进入详情页，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6.点击第一个商品进入详情页")
            SeaOfStarsAW.ut_device.click(533,968)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6.点击第一个商品进入详情页", "",
                                                     self.screenshot_dir_path)

            # 7.浏览详情页，上滑5次，下滑5次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7.浏览详情页，上滑5次，下滑5次")
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7.浏览详情页，上滑5次，下滑5次", "",
                                                     self.screenshot_dir_path)

            # 8、点击商品图片（停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、点击商品图片")
            SeaOfStarsAW.ut_device.click(600, 600)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、点击商品图片", "",
                                                     self.screenshot_dir_path)

            # 9、滑动浏览（左滑3次，右滑3次，每次停留2S）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、滑动浏览 左滑3次，右滑3次")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, 0.03)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、滑动浏览 左滑3次，右滑3次", "",
                                                     self.screenshot_dir_path)

            # 10、侧滑返回商品详情页
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、侧滑返回商品详情页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、侧滑返回商品详情页", "",
                                                     self.screenshot_dir_path)

            # 11、上滑至“评价”
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、上滑至“评价”")
            SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11、上滑至“评价”", "",
                                                     self.screenshot_dir_path)

            # 12.点击评价，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12.点击评价")
            SeaOfStarsAW.ut_device.click(306,250)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12.点击评价", "",
                                                     self.screenshot_dir_path)

            # 13.点击全部评价，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("13.点击全部评价")
            SeaOfStarsAW.ut_device.click(152,392)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "13.点击全部评价", "",
                                                     self.screenshot_dir_path)

            # 14.浏览全部评价，上滑3次，下滑3次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("14.浏览全部评价，上滑3次，下滑3次")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "14.浏览全部评价，上滑3次，下滑3次", "",
                                                     self.screenshot_dir_path)

            # 15.点击左下角店铺，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("15.点击左下角店铺")
            SeaOfStarsAW.ut_device.click(72,2209)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "15.点击左下角店铺", "",
                                                     self.screenshot_dir_path)

            # 16.浏览店铺，上滑3次，下滑3次，每次停留2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("16.浏览店铺，上滑3次，下滑3次")
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1500, 550, 1000, 0.04)
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(550, 1000, 550, 1500, 0.04)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "16.浏览店铺，上滑3次，下滑3次", "",
                                                     self.screenshot_dir_path)

            # 17.返回商品详情页，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("17.返回商品详情页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "17.返回商品详情页", "",
                                                     self.screenshot_dir_path)

            # 18.点击客服，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("18.点击客服")
            SeaOfStarsAW.ut_device.click(209,2209)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "18.点击客服", "",
                                                     self.screenshot_dir_path)

            # 19.返回商品详情页，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("19.返回商品详情页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "19.返回商品详情页", "",
                                                     self.screenshot_dir_path)

            # 20.点击立即购买，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("20.点击立即购买")
            SeaOfStarsAW.ut_device.click(950,2268)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "20.点击立即购买", "",
                                                     self.screenshot_dir_path)

            # 21.点击确认，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("21.点击确认")
            SeaOfStarsAW.ut_device.click(555,2229)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "21.点击确认", "",
                                                     self.screenshot_dir_path)

            # 22.返回首页，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("22.返回首页")
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "22.返回首页", "",
                                                     self.screenshot_dir_path)

            # 23.返回home页面，等待2s
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("23.返回home页面")
            SeaOfStarsAW.return_launcher()
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "23.返回home页面", "",
                                                     self.screenshot_dir_path)
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)