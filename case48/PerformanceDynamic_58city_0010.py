import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_58city_0010(Case):
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

        logging.info('应用启动')
        SeaOfStarsAW.trace_thread.add_log('58同城', '应用启动')
        SeaOfStarsAW.ut_device.session().app_activate('com.taofang.iphone')

        # for test_time in range(0, self.TEST_TIME):
        #     step = 0
        #     SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
        #                              self.screenshot_dir_path)
        #     # 启动58同城
        #     logging.info('应用启动')
        #     SeaOfStarsAW.trace_thread.add_log('58同城', '应用启动')
        #     SeaOfStarsAW.ut_device.session().app_activate('com.taofang.iphone')
        #     SeaOfStarsAW.ut_device.swipe_left()
        #     time.sleep(2)
        #     SeaOfStarsAW.ut_device.swipe_left()
        #     time.sleep(2)
        #     SeaOfStarsAW.ut_device.click(0.611, 0.238)
        #     time.sleep(2)

            # for i in range(5):
            #     SeaOfStarsAW.ut_device.swipe(0.500, 0.800, 0.500, 0.200, duration=0.02)
            #     time.sleep(1)
            # for i in range(5):
            #     SeaOfStarsAW.ut_device.swipe(0.500, 0.200, 0.500, 0.800, duration=0.02)
            #     time.sleep(1)


            # step += 1
            #
            # SeaOfStarsAW.ut_device.app_terminate('com.taofang.iphone')
            # SeaOfStarsAW.swipe_to_launcher()
            # SeaOfStarsAW.go_home()

        logging.info('用例执行结束')