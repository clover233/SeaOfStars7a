import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_youku_0010(Case):
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
            app_name ="优酷"

            step1 = "'1、打开优酷,等待10s'"
            logging.info('启动优酷')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.388, 0.144)
            time.sleep(10)

            step2 = "2、首页浏览 上下滑动各一次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step3 = "3、点击 会员 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            SeaOfStarsAW.ut_device(label="会员").click()
            time.sleep(1)

            step4 = "4、浏览会员页 上滑1次 下滑1次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step5 = "5、点击我的 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            SeaOfStarsAW.ut_device(label="我的").click()
            time.sleep(1)

            step6 = "6、浏览我的也 上滑5次 下滑5次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe_up()


            step7 = "7、点击设置"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device.click(0.058, 0.078)
            SeaOfStarsAW.ut_device.swipe_up()
            SeaOfStarsAW.ut_device(label="设置").click()
            time.sleep(2)


            step8 = "8、返回我的页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device.click(0.054, 0.083)
            time.sleep(2)

            # step9 = "9、点击更多"
            # SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            # SeaOfStarsAW.ut_device(label="更多").click()
            # time.sleep(2)
            #
            # step10 = "10、返回"
            # SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            # SeaOfStarsAW.ut_device.click(0.054, 0.083)
            # time.sleep(2)

            step11 = "11、点击我的下载 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            SeaOfStarsAW.ut_device.swipe_down()
            SeaOfStarsAW.ut_device(label="我的下载").click()
            time.sleep(2)

            step12 = "12、左滑返回上一级界面 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            SeaOfStarsAW.ut_device.click(0.054, 0.083)
            time.sleep(2)

            step13 = "13、回到首页 停留1s "
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            SeaOfStarsAW.ut_device(label="首页").click()
            time.sleep(2)

            step14 = "14、左滑5次 右滑5次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step14)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)

            step15 = "15、返回home 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step15)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)
            SeaOfStarsAW.ut_device.app_terminate("com.youku.YouKu")
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')