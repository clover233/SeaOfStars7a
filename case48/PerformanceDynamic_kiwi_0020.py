import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_kiwi_0020(Case):
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
            time.sleep(3)

            # 2、点击第一个直播间，等待10s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '查看首页直播间')
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.24, 0.23)
            time.sleep(10)

            # 3、返回首页，等待2s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '搜索查找直播间')
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 4、点击搜索框，等待2s
            SeaOfStarsAW.ut_device.click(0.277, 0.093)
            time.sleep(2)

            # 5、搜索王者荣耀，停留2s
            SeaOfStarsAW.ut_device.send_keys('王者荣耀')
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(2)

            # 6、浏览搜索结果，上滑2次，下滑2次，每次停留2s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 7、点击直播，等待2s
            SeaOfStarsAW.ut_device.click(0.193, 0.143)
            time.sleep(2)

            # 8、浏览直播搜索结果，上滑5次，下滑5次，每次停留2s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '查看搜索到的直播间')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 9、点击进入第一个直播间，等待5s
            SeaOfStarsAW.ut_device.click(0.224, 0.326)
            time.sleep(5)

            # 10、上下滑动切换直播间，下滑5次，上滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 11、返回首页推荐页，等待2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)

            # 12、返回home页面，等待2s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '退出应用')
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(2)
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '返回桌面')
            SeaOfStarsAW.ut_device.app_terminate('com.yy.kiwi')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')