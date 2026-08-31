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
#   @FileName:      PerformanceDynamic_AutoNavi_0030.py
#   @Description:   该文件是用例的具体实现，请按用例描述编写用例脚本！
#   @场景类型描述:    
#                   
#   @预置条件:
#                   1、登陆账号
#                   2、关闭弹窗
#   @详细场景:        
#                   58同城搜索浏览租房信息
#   @用例动态负载预置: 
#                   
#   @测试操作步骤:    
#                   1、启动58同城
#                   2、向上抛滑5次，浏览首页
#                   3、向下抛滑5次，浏览首页
#                   4、点击“租房”按钮，进入租房页面
#                   5、向上滑动5次
#                   6、向下滑动5次
#                   7、点击搜索框，进入搜索页面
#                   8、输入“西研所”，点击搜索
#                   9、点击第一个租房信息
#                   10、向上抛滑5次，浏览详细信息
#                   11、向下抛滑5次，浏览详细信息
#                   12、侧滑2次返回主页面
#                   13、上滑返回桌面
#   @性能指标采集场景: 
#                   
#   @Author:        wangzijian w00854976
#   @Date:          2025-10-20
#   @History:       created by w00854976 at 2025-10-20
#   @Environment:   Python3.8
#!!======================================================================================
"""

class PerformanceDynamic_AutoNavi_0030(Case):
    all_app_package_list = ['']
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
        for test_time in range(0, self.TEST_TIME):
            # 1、启动
            SeaOfStarsAW.start_perfetto_trace()
            logging.info("1、启动")
            SeaOfStarsAW.ut_device.app_start('com.autonavi.minimap', use_monkey=True)
            time.sleep(5)
            SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                     'step_' + "", "",
                                                     self.screenshot_dir_path)


        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        logger = logging.getLogger()
        logger.removeHandler(self.fh)