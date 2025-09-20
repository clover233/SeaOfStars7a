import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class PerformanceDynamic_Camera_0030(Case):
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
            # 启动qq
            logging.info('启动相机')
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.mqq')
            SeaOfStarsAW.trace_thread.add_log('相机','应用启动')
            # pos = SeaOfStarsAW.find_app_from_launcher('QQ')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('QQ')
            # pos = SeaOfStarsAW.find_app_from_launcher('QQ')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            # time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.848, 0.136)
            time.sleep(2)

            # 点击动态
            # SeaOfStarsAW.check_status(labelContains='动态')
            logging.info('广角拍照')
            SeaOfStarsAW.trace_thread.add_log('相机', '广角拍照')

            SeaOfStarsAW.ut_device.click(0.447, 0.733)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.501, 0.875)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.548, 0.727)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.501, 0.875)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.656, 0.733)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.501, 0.875)
            time.sleep(2)
            logging.info('设置页面')
            SeaOfStarsAW.trace_thread.add_log('相机', '设置页面')

            SeaOfStarsAW.ut_device(label="相机控制").click()
            time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.1, 0.8)
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe(0.1, 0.8, 0.5, 0.8)
                time.sleep(2)
            SeaOfStarsAW.ut_device(label="宽高比").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.1, 0.782)
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="实况照片").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.1, 0.782)
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="相机控制").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.119, 0.873)
            time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe(0.5, 0.5, 0.1, 0.5)
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe(0.1, 0.5, 0.5, 0.5)
                time.sleep(2)
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)


            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('相机', '返回home')

            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')