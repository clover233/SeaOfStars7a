import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_weipinhui_0020(Case):
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
            app_name ="唯品会"

            step1 = "'1、打开唯品会,等待10s'"
            logging.info('启动唯品会')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.367, 0.593)
            time.sleep(10)

            step2 = "2、点击右上角的 =  进入分类拓展界面"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device.click(0.15, 0.233)

            step3 = "3、浏览结果 上滑2次 下滑3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step4 = "4、返回上一级界面"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device.click(0.052, 0.097)

            step5 = "5、点击进入个人中心"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            SeaOfStarsAW.ut_device(label="个人中心").click()

            step6 = "6、查看待付款 返回个人中心界面"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device(label="待付款").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.08, 0.09)


            step7 = "7、查看待收货 返回个人中心界面"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device(label="待收货").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.08, 0.09)

            step8 = "8、查看待评价 返回个人中心界面"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device(label="待评价").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.08, 0.09)

            step9 = "9、返回首页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            SeaOfStarsAW.ut_device(label="首页").click()
            time.sleep(1)

            step10 = "10、返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)
            SeaOfStarsAW.ut_device.app_terminate("com.vipshop.iphone")

        logging.info('用例执行结束')