import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_hanglvzongheng_0010(Case):
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
    #     清空后台

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
            SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
                                     self.screenshot_dir_path)

            # 1、启动航旅纵横，停留2s
            logging.info('启动航旅纵横，启动3s')
            SeaOfStarsAW.trace_thread.add_log('航旅纵横', '启动航旅纵横，查看机票')
            SeaOfStarsAW.ut_device.session().app_activate('com.travelsky.umetrip')
            time.sleep(5)
            # 2、点击“订机票 送福利”，停留3s
            SeaOfStarsAW.ut_device(labelContains="机票").click()
            time.sleep(1)

            # 3、点击搜索预定，停留4s
            SeaOfStarsAW.ut_device.click(0.491, 0.501)
            time.sleep(4)

            # 4、上滑3次，下滑4次，每次停留2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            for i in range(4):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 5、查看第一条搜索结果详情，停留4s
            SeaOfStarsAW.ut_device.click(0.367, 0.455)
            time.sleep(4)

            # 6、返回首页，停留2s
            for i in range(3):
                SeaOfStarsAW.ut_device.click(0.051, 0.094)
            time.sleep(2)

            # 7、点击火车票，停留1s
            SeaOfStarsAW.trace_thread.add_log('航旅纵横', '启动航旅纵横，查看火车票')
            SeaOfStarsAW.ut_device(labelContains="火车票").click()
            time.sleep(1)

            # 8、点击订火车票，停留3s
            SeaOfStarsAW.ut_device.click(0.501, 0.509)
            time.sleep(3)

            # 9、点击搜索预定，停留4s

            # 10、上滑3次，下滑4次，每次停留2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            for i in range(4):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 11、查看第一条搜索结果详情，停留3s
            SeaOfStarsAW.ut_device.click(0.468, 0.387)
            time.sleep(3)

            # 12、点击抢购第一条搜索结果，停留3s

            # 13、返回首页，停留2s
            for i in range(3):
                SeaOfStarsAW.ut_device.click(0.051, 0.094)
            time.sleep(2)
            # 14、上滑返回桌面，停留2s
            SeaOfStarsAW.trace_thread.add_log('航旅纵横', '返回桌面')
            SeaOfStarsAW.ut_device.app_terminate('com.travelsky.umetrip')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')