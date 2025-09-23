import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class PerformanceDynamic_dazhongdianping_0020(Case):
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
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            # 1、启动大众点评（停留3s）
            logging.info('1、启动大众点评')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '启动大众点评')
            SeaOfStarsAW.ut_device.session().app_activate('com.dianping.dpscope')
            time.sleep(3)

            # 2、主页浏览（上滑5次，下滑5次，每次停留2s）

            # 3、点击推荐旁边的美食（停留1s）

            # 4、滑动浏览美食（上滑5次，下滑5次，每次停留2s）

            # 5、点击推荐旁边的旅行（停留1s）

            # 6、滑动浏览旅行（上滑5次，下滑5次，每次停留2s）

            # 7、点击推荐旁边的玩乐（停留1s）

            # 8、滑动浏览玩乐（上滑5次，下滑5次，每次停留2s）

            # 9、返回大众点评首页（停留1s）

            # 10、返回home界面（停留1s）
            logging.info('10、返回home界面')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '返回home界面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.dianping.dpscope')
            time.sleep(1)

        logging.info('用例执行结束')