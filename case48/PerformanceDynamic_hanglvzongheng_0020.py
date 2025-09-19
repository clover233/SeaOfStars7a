import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_hanglvzongheng_0020(Case):
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
            # todo 后续放开log
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            # 1、启动航旅纵横，停留2s
            logging.info('启动航旅纵横，启动3s')
            SeaOfStarsAW.trace_thread.add_log('航旅纵横', '启动航旅纵横，浏览航旅纵横首页')
            SeaOfStarsAW.ut_device.session().app_activate('com.travelsky.umetrip')
            time.sleep(5)
            # 2、首页上滑1次，下滑2次，停留2s
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            SeaOfStarsAW.trace_thread.add_log('航旅纵横', '查询航班动态')
            # 5、点击航班动态，停留1s
            SeaOfStarsAW.ut_device.click(0.702, 0.926)
            time.sleep(4)

            # 6、点击搜索框，停留2s
            SeaOfStarsAW.ut_device.click(0.2, 0.236)
            time.sleep(4)

            # 7、输入1234，停留2s
            SeaOfStarsAW.ut_device.send_keys("1234")
            time.sleep(2)

            # 8、点击航班查询，停留2s
            SeaOfStarsAW.ut_device.click(0.511, 0.43)
            time.sleep(2)

            # 9、点击AA1234，停留3s
            SeaOfStarsAW.ut_device.click(0.17, 0.386)
            time.sleep(3)

            # 10、侧滑返回上一页，停留2s
            SeaOfStarsAW.ut_device.click(0.047, 0.097)
            time.sleep(2)

            # 11、点击“按起降地”，停留1s
            SeaOfStarsAW.ut_device.click(0.501, 0.16)
            time.sleep(3)

            # 12、点击“航班查询”，停留2s
            SeaOfStarsAW.ut_device.click(0.508, 0.43)
            time.sleep(3)

            # 13、上滑3次，下滑4次，停留2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            for i in range(4):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 14、查看第一条搜索结果详情，停留3s
            SeaOfStarsAW.ut_device.click(0.408, 0.309)
            time.sleep(3)

            # 15、返回首页，停留2s
            for i in range(2):
                SeaOfStarsAW.ut_device.click(0.047, 0.097)
                time.sleep(2)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.096, 0.923)
            time.sleep(2)

            # 16、上滑返回桌面，停留2s
            SeaOfStarsAW.trace_thread.add_log('航旅纵横', '返回桌面')
            SeaOfStarsAW.ut_device.app_terminate('com.travelsky.umetrip')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')