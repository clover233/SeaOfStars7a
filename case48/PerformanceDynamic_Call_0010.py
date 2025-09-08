import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Call_0010(Case):
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

            # 1、进入电话(停留1s)
            logging.info('应用启动')
            SeaOfStarsAW.trace_thread.add_log('电话', '应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('com.apple.mobilephone')
            time.sleep(1)

            # 2、点击屏幕底部“联系人”(2s，停留2s)
            logging.info('点击屏幕底部')
            SeaOfStarsAW.trace_thread.add_log('电话', '点击屏幕底部')
            SeaOfStarsAW.ut_device.click(0.501, 0.932, 0.3)
            time.sleep(1)

            # 3、浏览联系人（上下滑动各2次，2s，停留1s）
            logging.info('浏览联系人')
            SeaOfStarsAW.trace_thread.add_log('电话', '浏览联系人')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            time.sleep(1)

            # 4、点击搜索框，输入atest，点击第一条搜索记录，进入详情页面，停留2s
            logging.info('点击搜索框，输入atest，点击第一条搜索记录')
            SeaOfStarsAW.trace_thread.add_log('电话', '点击搜索框，输入atest，点击第一条搜索记录')
            SeaOfStarsAW.ut_device.click(0.194, 0.197, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text("atest")
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.1, 0.221, 0.3)
            time.sleep(2)

            # 5、左滑返回联系人界面，停留1s
            logging.info('左滑返回联系人界面')
            SeaOfStarsAW.trace_thread.add_log('电话', '左滑返回联系人界面')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(2)

            # 6、上下滑动5次，停留1s
            logging.info('上下滑动5次')
            SeaOfStarsAW.trace_thread.add_log('电话', '上下滑动5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 7、点击atest联系人
            logging.info('点击atest联系人')
            SeaOfStarsAW.trace_thread.add_log('电话', '点击atest联系人')
            SeaOfStarsAW.ut_device.click(0.1, 0.221, 0.3)
            time.sleep(2)

            # 8、返回电话首页面
            logging.info('返回电话首页面')
            SeaOfStarsAW.trace_thread.add_log('电话', '返回电话首页面')
            SeaOfStarsAW.ut_device.click(0.699, 0.927, 0.3)
            time.sleep(2)

            # 9、上滑返回home界面(2s，停留2s)
            logging.info('上滑返回桌面')
            SeaOfStarsAW.trace_thread.add_log('电话', '上滑返回桌面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')