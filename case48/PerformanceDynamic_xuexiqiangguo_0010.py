import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_xuexiqiangguo_0010(Case):
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

            step1 = "1、打开学习强国,等待10s"
            logging.info('启动学习强国')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.155, 0.141)
            time.sleep(6)

            step2 = "2、左滑5次  每次间隔2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)

            step3 = "3、上滑5次 下滑5次 停留2次"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step4 = "4、右滑5次 间隔2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)

            step5 = "5、上滑5次 下滑5次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step6 = "6、点击第一条推荐 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device.click(0.4, 0.531)

            step7 = "7、浏览新闻内容 上下各滑动1次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step8 = "8、返回首页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device.click(0.05, 0.091)
            time.sleep(2)

            step9 = "9、点击 电视台 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            # SeaOfStarsAW.ut_device(label="去购物车").click()
            SeaOfStarsAW.ut_device.click(0.702, 0.928)
            time.sleep(2)

            step10 = "10、左滑5次  每次间隔2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)


            step11 = "11、上滑5次 下滑5次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step12 = "12、右滑5次  每次间隔2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)


            step13 = "13、上滑5次 下滑5次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step14 = "14、点击看党史 第一个视频播放 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step14)
            SeaOfStarsAW.ut_device(label="STFeedsChannelEditBtn").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="看党史").click()

            SeaOfStarsAW.ut_device.click(0.876, 0.342)
            time.sleep(1)

            step15 = "15、返回首页 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step15)
            SeaOfStarsAW.ut_device.click(0.494, 0.943)
            time.sleep(1)

            step16 = "16、点击百灵 点击首页 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step16)
            SeaOfStarsAW.ut_device.click(0.3, 0.934)
            time.sleep(1)

            step17 = "17、返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step17)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)
            SeaOfStarsAW.ut_device.app_terminate("cn.xuexi.qg")
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')