import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Browser_0010(Case):
    all_app_package_list = ['']
    TEST_TIME = 1

    def __init__(self, result_path):
        super().__init__(result_path)
        SeaOfStarsAW.current_running_class_name = self.__class__.__name__

    @SeaOfStarsAW.function_log
    def set_up(self):
        logging.info('测试环境开始准备')
        phone_app_list = SeaOfStarsAW.get_app_list()
        for per_app in self.all_app_package_list:
            if per_app not in phone_app_list:
                return False

    @SeaOfStarsAW.function_log
    def run_case(self):
        """
        测试用例执行
        """
        logging.info("用例开始执行")
        if SeaOfStarsAW.ut_device.locked():
            SeaOfStarsAW.ut_device.unlock()
            time.sleep(2)
        for test_time in range(0, self.TEST_TIME):
            step = 0

            # 1、打开华为浏览器(启动3s，停留2s)
            # iOS暂无华为浏览器，定为Safari
            logging.info('应用启动')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('com.apple.mobilesafari')

            # 2、进入首页（停留1s），单框架（点击首页后点击百度），双框架（点击屏幕底部首页图标即可）
            logging.info('进入首页')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '进入首页')
            SeaOfStarsAW.ut_device.click(0.375, 0.216, 0.3)
            time.sleep(1)

            # 3、上滑5次，下滑5次，停留2s
            logging.info('进入首页')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '进入首页')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 4、点击第一条新闻，浏览新闻（上下滑动5次，每次停顿2s）
            logging.info('点击第一条新闻，浏览新闻')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '点击第一条新闻，浏览新闻')
            SeaOfStarsAW.ut_device.click(0.441, 0.496, 0.3)
            time.sleep(2)

            # 5、返回首页（停留1s）单框架（点击屏幕底部首页图标），双框架（左滑返回首页）
            logging.info('返回首页')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '返回首页')
            SeaOfStarsAW.ut_device.swipe(0.008, 0.586, 0.979, 0.586, 0.3)
            time.sleep(1)

            # 6、上滑返回home页面（停留1s）
            logging.info('上滑返回home页面')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '上滑返回home页面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.apple.mobilesafari')
            time.sleep(1)

        logging.info('用例执行结束')