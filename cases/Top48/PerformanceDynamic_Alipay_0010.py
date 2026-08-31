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
#   @FileName:      PerformanceDynamic_Alipay_0010.py
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
#                   1、启动支付宝(启动2s，停留1s)
#                   2、点击出行(停留2s)
#                   3、切换到地铁页（停留1s）
#                   4、返回上一页（停留1s）
#                   5、点击卡包（停留2s）
#                   6、返回上一页（停留1s）
#                   7、点击“我的”
#                   8、切回到支付宝主界面（停留1s）
#                   9、收付款(停留1s)
#                   10、点击“转账”按钮(停留1s)
#                   11、点击“转到银行卡”（停留1s)
#                   12、返回上一页（停留1s）
#                   13、点击“转到支付宝”(停留1s)
#                   14、返回支付宝主界面(停留1s)
#                   15、首页--扫一扫(停留1s)
#                   16、点击“相册”按钮(停留1s)
#                   17、点击当前页面的第一个图片（停留1s，预览大图2s）
#                   18、返回支付宝主界面(停留1s)
#                   19、返回home页面(停留1s))
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_Alipay_0010(Case):
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
            # 1、启动支付宝(启动2s，停留1s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动支付宝")
            SeaOfStarsAW.ut_device.app_start('com.eg.android.AlipayGphone', use_monkey=True)
            time.sleep(5)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、启动支付宝", "",
                                                     self.screenshot_dir_path)

            # 2、点击出行(停留2s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、点击出行")
            SeaOfStarsAW.ut_device.click(706, 327)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、点击出行", "",
                                                     self.screenshot_dir_path)

            # 3、切换到地铁页（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、切换到地铁页")
            SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, 0.1)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.1)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、切换到地铁页", "",
                                                     self.screenshot_dir_path)

            # 4、返回上一页（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、返回上一页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、返回上一页", "",
                                                     self.screenshot_dir_path)

            # 5、点击卡包（停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、点击卡包")
            SeaOfStarsAW.ut_device.click(950,327)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' +"5、点击卡包", "",
                                                     self.screenshot_dir_path)

            # 6、返回上一页（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("6、返回上一页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "6、返回上一页", "",
                                                     self.screenshot_dir_path)

            # 7、点击“我的”
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、点击“我的”")
            SeaOfStarsAW.ut_device.click(977,2250)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、点击“我的”", "",
                                                     self.screenshot_dir_path)

            # 8、切回到支付宝主界面（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、切回到支付宝主界面")
            SeaOfStarsAW.ut_device.click(101,2250)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、切回到支付宝主界面", "",
                                                     self.screenshot_dir_path)

            # 9、收付款(停留1s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、收付款")
            SeaOfStarsAW.ut_device.click(401,357)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、收付款", "",
                                                     self.screenshot_dir_path)

            # 10、点击“转账”按钮(停留1s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、点击“转账”按钮")
            SeaOfStarsAW.ut_device.click(355,2200)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、点击“转账”按钮", "",
                                                     self.screenshot_dir_path)

            # 11、点击“转到银行卡”（停留1s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、点击“转到银行卡”")
            SeaOfStarsAW.ut_device.click(533,624)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "11、点击“转到银行卡”", "",
                                                     self.screenshot_dir_path)

            # 12、返回上一页（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、返回上一页")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12、返回上一页", "",
                                                     self.screenshot_dir_path)

            # 13、点击“转到支付宝”(停留1s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("13、点击“转到支付宝”")
            SeaOfStarsAW.ut_device.click(143,624)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "13、点击“转到支付宝”", "",
                                                     self.screenshot_dir_path)

            # 14、返回支付宝主界面(停留1s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("14、返回支付宝主界面")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "14、返回支付宝主界面", "",
                                                     self.screenshot_dir_path)

            # 15、首页--扫一扫(停留1s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("15、首页--扫一扫")
            SeaOfStarsAW.ut_device.click(96,327)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "15、首页--扫一扫", "",
                                                     self.screenshot_dir_path)

            # 16、点击“相册”按钮(停留1s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("16、点击“相册”按钮")
            SeaOfStarsAW.ut_device.click(920,1800)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "16、点击“相册”按钮", "",
                                                     self.screenshot_dir_path)

            # 17、点击当前页面的第一个图片（停留1s，预览大图2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("17、点击当前页面的第一个图片")
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(336, 821)
            time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "17、点击当前页面的第一个图片", "",
                                                     self.screenshot_dir_path)

            # 18、返回支付宝主界面(停留1s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("18、返回支付宝主界面")
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0, 1500, 600, 1500, 0.5)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "18、返回支付宝主界面", "",
                                                     self.screenshot_dir_path)

            # 19、返回home页面(停留1s)
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("19、返回home页面")
            SeaOfStarsAW.return_launcher()
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "19、返回home页面", "",
                                                     self.screenshot_dir_path)

        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)