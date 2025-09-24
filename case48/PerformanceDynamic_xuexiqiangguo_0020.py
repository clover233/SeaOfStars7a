import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_xuexiqiangguo_0020(Case):
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
            app_name ="学习强国"

            step1 = "'打开学习强国,等待10s'"
            logging.info('启动学习强国')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.155, 0.141)
            time.sleep(10)

            step2 = "点击学习停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device.click(0.494, 0.943)
            time.sleep(2)

            step2 = "左滑5次  每次间隔2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)

            step3 = "上滑5次 下滑5次 停留2次"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step4 = "右滑5次 间隔2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)

            step5 = "上滑5次 下滑5次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step6 = "点击右上角符号 展开全部频道 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device(label="STFeedsChannelEditBtn").click()

            step7 = "点击 融媒中心 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device(label="融媒中心").click()
            time.sleep(1)

            step8 = "点击第一条内容  停留2s 上下个滑动5s 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device.click(0.382, 0.7)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step9 = "点击 电视台 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            SeaOfStarsAW.ut_device.click(0.06, 0.086)

            SeaOfStarsAW.ut_device.click(0.702, 0.928)
            time.sleep(2)

            step10 = "点击电台 上下各滑动5次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            SeaOfStarsAW.ut_device.click(0.902, 0.931)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step11 = "点击听原著 2s 左滑5ci 每次2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            SeaOfStarsAW.ut_device.click(0.308, 0.131)
            # for i in range(5):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     time.sleep(2)

            step12 = "点击播放全部 2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            SeaOfStarsAW.ut_device.click(0.638, 0.574)
            SeaOfStarsAW.ut_device.click(0.842, 0.317)
            time.sleep(2)


            step13 = "点击暂停 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            SeaOfStarsAW.ut_device.click(0.518, 0.932)
            time.sleep(1)

            step14 = "点击开展播放列表 停留1s 下滑1s 停留1s 点击关闭 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step14)
            SeaOfStarsAW.ut_device.click(0.084, 0.1)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.084, 0.1)
            time.sleep(1)

            step15 = "返回1次 到电视台 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step15)
            SeaOfStarsAW.ut_device.click(0.706, 0.934)
            time.sleep(1)

            step16 = "点击百灵 点击首页 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step16)
            SeaOfStarsAW.ut_device.click(0.3, 0.934)
            time.sleep(1)

            step17 = "返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step17)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)
            SeaOfStarsAW.ut_device.app_terminate("cn.xuexi.qg")
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')