import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Browser_0020(Case):
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

            # 2、进入我的页面，停留1s。单框架（点击右下角 “: :” 按钮）,双框架（点击屏幕底部“我的”图标）
            logging.info('返回首页')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '返回首页')
            SeaOfStarsAW.ut_device.click(0.71, 0.935, 0.3)
            time.sleep(2)

            # 3、点击历史（停留1s）
            logging.info('返回首页')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '返回首页')
            SeaOfStarsAW.ut_device.click(0.808, 0.554, 0.3)
            time.sleep(2)

            # 4、点击第一条新闻，上下滑动5次（每次停顿2s）
            logging.info('返回首页')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '返回首页')
            SeaOfStarsAW.ut_device.click(0.495, 0.743, 0.3)
            time.sleep(2)

            # 5、返回首页（停留1s）
            logging.info('返回首页')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '返回首页')
            SeaOfStarsAW.ut_device.click(0.922, 0.936, 0.3)
            time.sleep(2)


            # 6、返回浏览器首页界面(停留1s)
            logging.info('返回首页')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '返回首页')
            SeaOfStarsAW.ut_device.click(0.071, 0.934, 0.3)
            time.sleep(2)

            # 7、返回home页面（停留1s）
            logging.info('返回首页')
            SeaOfStarsAW.trace_thread.add_log('浏览器', '返回首页')
            SeaOfStarsAW.ut_device.swipe(0.008, 0.586, 0.979, 0.586, 0.3)
            time.sleep(1)

        logging.info('用例执行结束')