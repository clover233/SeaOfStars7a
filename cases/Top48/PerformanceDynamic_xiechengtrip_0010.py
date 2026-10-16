# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time
import uiautomator2 as u2
from uiautomator2 import Device
from Cases.CaseBase import Case
from aw_new import SeaOfStarsAW

class PerformanceDynamic_xiechengtrip_0010(Case):

    all_app_package_list = ["ctrip.android.view"]

    def __init__(self, result_path):
        super().__init__(result_path)

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info("测试环境开始准备!")
        # 判断手机上是否已安装好TOP30应用,未安装则用例失败
        phone_app_list = SeaOfStarsAW.get_app_list()
        for per_app in self.all_app_package_list:
            if per_app not in phone_app_list:
                return False
        # 设置系统语言为中文
        SeaOfStarsAW.set_system_language_cn()
        # 解锁屏幕
        if SeaOfStarsAW.is_locked():
            SeaOfStarsAW.unlock_device()
        # 设置屏幕锁定时间为10min
        SeaOfStarsAW.set_screen_lock_long_time()
        # 保留已有应用后台
        logging.info("测试环境准备完成!")


    @SeaOfStarsAW.function_log
    def run_case(self):
        """
        测试用例执行
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("用例开始执行!")
        steps_num = 1

        app = 'ctrip.android.view'
        step = "1、启动携程旅行"

        SeaOfStarsAW.start_perfetto_trace()
        logging.info("启动{}中".format("携程旅行"))
        SeaOfStarsAW.ut_device.app_start(app, use_monkey=True)
        time.sleep(5)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "2、向上抛滑1次，浏览首页"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.scroll_down()
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "3、向下抛滑2次，浏览首页"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.scroll_up()
            time.sleep(2)

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "4、点击民宿客栈,切换到民宿客栈页面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text="民宿/客栈").click()
        time.sleep(5)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "5、向上抛滑2次，浏览民宿客栈页面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.scroll_down()
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "6、向下抛滑3次，浏览民宿客栈页面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(3):
            SeaOfStarsAW.scroll_up()
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "7、点击查询按钮，切换到查询页面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.466, 0.248)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "8、输入臻选民宿，点击搜索"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.send_keys("臻选民宿")
        time.sleep(1)
        SeaOfStarsAW.ut_device(text="搜索").click()
        time.sleep(5)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "9、点击第一个民"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.492, 0.419)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "10、向上抛滑2次，浏览详细信息"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.scroll_down()
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "11、点击评论定位到房客点评"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='评价').click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "12、点击全部评论，切换到评论页"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='房客点评').click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "13、评论页上滑2次，下滑3次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            SeaOfStarsAW.scroll_down()
            time.sleep(1)
        for _ in range(3):
            SeaOfStarsAW.scroll_up()
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "14、左侧滑1次，返回民宿详情页"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.swipe(0.99, 0.423, 0.636, 0.423)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "15、点击全部设施，切换到全部设施页"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='设施').click()
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(0.836, 0.193)
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "16、点击弹窗右上角的x"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device.click(0.932, 0.063)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "17、向下抛滑3次，浏览详细信息"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(3):
            SeaOfStarsAW.scroll_up()
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        step = "18、返回携程旅行主界面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(3):
            SeaOfStarsAW.ut_device.swipe(0.99, 0.423, 0.636, 0.423)
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)

        steps_num += 1

        step = "19、返回home页面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.return_launcher()
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        """
        清理日志，保留应用后台
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("用例结束，保留应用后台，仅清理日志处理器。")
        logger = logging.getLogger()
        logger.removeHandler(self.fh)
