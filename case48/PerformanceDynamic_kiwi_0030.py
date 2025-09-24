import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_kiwi_0030(Case):
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

            # 1、启动虎牙直播，等待2s
            logging.info('启动虎牙直播，等待2s')
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '启动虎牙直播')
            SeaOfStarsAW.ut_device.session().app_activate('com.yy.kiwi')
            time.sleep(5)

            # 2、点击第一个直播间，等待10s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '直播间互动')
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.267, 0.243)
            time.sleep(10)

            # 3、点击发送弹幕“好”，等待2s
            SeaOfStarsAW.ut_device.click(0.391, 0.932)
            time.sleep(2)
            SeaOfStarsAW.ut_device.send_keys('好')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.899, 0.592)
            time.sleep(2)

            # 4、下滑切换直播间，下滑5次，上滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)


            # 5、返回推荐页，停留2s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '退出应用')
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 6、返回home页，停留2s
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.app_terminate('com.yy.kiwi')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')