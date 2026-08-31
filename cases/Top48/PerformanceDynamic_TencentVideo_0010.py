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
#   @FileName:      PerformanceDynamic_TencentVideo_0010.py
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
#                     1、启动腾讯视频（停留3s）
#                     2、主页浏览（上滑5次，下滑5次，每次停留2s）
#                     3、点击主页第一个推荐视频（1s，停留30s）
#                     4、切换到全屏模式（停留10s）
#                     5、退出全屏（停留1s）
#                     6、浏览【为你推荐】上滑3次，下滑3次
#                     7、侧滑返回首页
#                     8、点击搜索框
#                     9、输入【斗破苍穹】并搜索
#                     10、上滑3次，下滑3次浏览搜索结果
#                     11、点击【影视】，切换到影视界面
#                     12、上滑1次，下滑1次。浏览影视搜索结果
#                     13、侧滑2次返回首
#                     14、上滑返回桌面
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""


class PerformanceDynamic_TencentVideo_0010(Case):
    all_app_package_list = ['com.tencent.qqlive']
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
            # 1、启动腾讯视频（停留3s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动腾讯视频")
            SeaOfStarsAW.ut_device.app_start('com.tencent.qqlive', use_monkey=True)
            time.sleep(3)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "1、启动腾讯视频 ", "",
                                                     self.screenshot_dir_path)
            # 2、主页浏览（上滑5次，下滑5次，每次停留2s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("2、主页浏览 ")
            for _ in range(5):
                SeaOfStarsAW.scroll_down(0.5)
                time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.scroll_up(0.5)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "2、主页浏览 ", "",
                                                     self.screenshot_dir_path)

            # 3、点击主页第一个推荐视频（1s，停留30s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("3、点击主页第一个推荐视频 ")
            SeaOfStarsAW.ut_device.click(300, 1770)
            time.sleep(10)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "3、点击主页第一个推荐视频 ", "",
                                                     self.screenshot_dir_path)

            # 4、切换到全屏模式（停留10s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("4、切换到全屏模式 ")
            SeaOfStarsAW.ut_device.click(1000, 640)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "4、切换到全屏模式 ", "",
                                                     self.screenshot_dir_path)

            # 5、退出全屏（停留1s）
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("5、退出全屏 ")
            SeaOfStarsAW.ut_device.click(60, 64)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "5、退出全屏 ", "",
                                                     self.screenshot_dir_path)

            # 6、浏览【为你推荐】上滑3次，下滑3次
            SeaOfStarsAW.start_perfetto_trace()
            logging.info(" 6、浏览【为你推荐】 ")
            SeaOfStarsAW.ut_device.click(60, 175)
            time.sleep(1)

            for _ in range(3):
                SeaOfStarsAW.scroll_down(0.5)
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.scroll_up(0.5)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + " 6、浏览【为你推荐】 ", "",
                                                     self.screenshot_dir_path)

            # 7、侧滑返回首页
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("7、侧滑返回首页 ")
            pass
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "7、侧滑返回首页 ", "",
                                                     self.screenshot_dir_path)

            # 8、点击搜索框
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("8、点击搜索框 ")
            SeaOfStarsAW.ut_device.click(500, 175)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "8、点击搜索框 ", "",
                                                     self.screenshot_dir_path)

            # 9、输入【斗破苍穹】并搜索
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("9、输入【斗破苍穹】并搜索 ")
            SeaOfStarsAW.ut_device.send_keys("斗破苍穹")
            time.sleep(1)

            SeaOfStarsAW.ut_device.click(990, 180)
            time.sleep(1)

            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "9、输入【斗破苍穹】并搜索 ", "",
                                                     self.screenshot_dir_path)

            # 10、上滑3次，下滑3次浏览搜索结果
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("10、上滑3次，下滑3次浏览搜索结果 ")
            for _ in range(3):
                SeaOfStarsAW.scroll_down(0.5)
                time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.scroll_up(0.5)
                time.sleep(2)

            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "10、上滑3次，下滑3次浏览搜索结果 ", "",
                                                     self.screenshot_dir_path)

            # 11、点击【影视】，切换到影视界面
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("11、点击【影视】，切换到影视界面 ")
            SeaOfStarsAW.ut_device.click(215, 280)
            time.sleep(1)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + " 11、点击【影视】，切换到影视界面", "",
                                                     self.screenshot_dir_path)

            # 12、上滑1次，下滑1次。浏览影视搜索结果
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("12、上滑1次，下滑1次。浏览影视搜索结果 ")
            for _ in range(1):
                SeaOfStarsAW.scroll_down(0.5)
                time.sleep(2)
            for _ in range(1):
                SeaOfStarsAW.scroll_up(0.5)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "12、上滑1次，下滑1次。浏览影视搜索结果 ", "",
                                                     self.screenshot_dir_path)

            # 13、侧滑2次返回首页
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("13、侧滑2次返回首页")
            for _ in range(2):
                SeaOfStarsAW.ut_device.click(50, 180)
                time.sleep(2)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "13、侧滑2次返回首页", "",
                                                     self.screenshot_dir_path)

            # 14、上滑返回桌面
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
        """
        测试环境恢复
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)