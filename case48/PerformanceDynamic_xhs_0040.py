import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_xhs_0040(Case):
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

            step1 = "'打开小红书,等待10s'"
            logging.info('启动小红书')
            SeaOfStarsAW.trace_thread.add_log('小红书', step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.149, 0.714)
            time.sleep(10)

            step2 = "点击我"
            SeaOfStarsAW.trace_thread.add_log('小红书', step2)
            SeaOfStarsAW.ut_device.click(0.904, 0.936)


            step3 = "点击收藏"
            SeaOfStarsAW.trace_thread.add_log('小红书', step3)
            SeaOfStarsAW.ut_device(labelContains="收藏").click()
            time.sleep(1)

            step4 = "上滑浏览1次 "
            SeaOfStarsAW.trace_thread.add_log('小红书', step4)
            SeaOfStarsAW.ut_device.swipe_up()

            step5 = "下滑浏览1次"
            SeaOfStarsAW.trace_thread.add_log('小红书', step5)
            SeaOfStarsAW.ut_device.swipe_down()

            step6 = "点击赞"
            SeaOfStarsAW.trace_thread.add_log('小红书', step6)
            SeaOfStarsAW.ut_device(labelContains="赞").click()

            step7 = "上滑浏览1次"
            SeaOfStarsAW.trace_thread.add_log('小红书', step7)
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)

            step8 = "下滑浏览1次"
            SeaOfStarsAW.trace_thread.add_log('小红书', step8)
            SeaOfStarsAW.ut_device.swipe_down()

            step9 = "返回home页面"
            SeaOfStarsAW.trace_thread.add_log('小红书', step9)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

        logging.info('用例执行结束')