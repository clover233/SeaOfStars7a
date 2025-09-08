import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Call_0020(Case):
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

            # 2、点击电话，查看所有通话
            logging.info('点击电话，查看所有通话')
            SeaOfStarsAW.trace_thread.add_log('电话', '点击电话，查看所有通话')
            SeaOfStarsAW.ut_device.click(0.398, 0.089, 0.3)
            time.sleep(2)

            # 3、输入号码“10086”后，删除键删除号码
            logging.info('输入号码“10086”后，删除键删除号码')
            SeaOfStarsAW.trace_thread.add_log('电话', '输入号码“10086”后，删除键删除号码')
            SeaOfStarsAW.ut_device.click(0.699, 0.924, 0.3)
            time.sleep(1)

            SeaOfStarsAW.ut_device.click(0.24, 0.357, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.501, 0.694, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.501, 0.694, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.504, 0.583, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.762, 0.467, 0.3)
            time.sleep(1)

            for i in range(5):
                SeaOfStarsAW.ut_device.click(0.765, 0.807, 0.3)
                time.sleep(1)

            # 4、点击拨号键盘上方空白处，等待1s
            logging.info('点击拨号键盘上方空白处')
            SeaOfStarsAW.trace_thread.add_log('电话', '点击拨号键盘上方空白处')
            SeaOfStarsAW.ut_device.click(0.498, 0.198, 0.3)
            time.sleep(1)

            # 5、上滑5次，下滑5次，等待2s
            logging.info('上滑5次，下滑5次')
            SeaOfStarsAW.trace_thread.add_log('电话', '上滑5次，下滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 6、上滑返回home界面
            logging.info('上滑返回home界面')
            SeaOfStarsAW.trace_thread.add_log('电话', '上滑返回home界面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)
        logging.info('用例执行结束')