import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Dongchedi_0020(Case):
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

            # 1、打开懂车帝，等待2s
            logging.info('打开懂车帝，等待2s')
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '打开懂车帝，点击兴趣圈滑动')
            # todo 微博的坐标地址要改下
            SeaOfStarsAW.ut_device.session().app_activate('com.ss.ios.auto')
            time.sleep(3)

            # 2、点击兴趣圈，停留1s
            SeaOfStarsAW.ut_device(labelContains="车友圈").click()
            time.sleep(1)

            # 3、上滑5次，下滑5次，浏览兴趣圈，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 4、点击"话题"帖子，停留2s
            SeaOfStarsAW.trace_thread.add_log('懂车帝', '点击话题的第一条帖子并滑动')
            SeaOfStarsAW.ut_device.click(0.175, 0.55)
            time.sleep(2)

            # 5、点击第一条帖子，停留2s
            SeaOfStarsAW.ut_device.click(0.489, 0.681)
            time.sleep(2)

            # 6、上滑3次，下滑3次，每次停留2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 7、右下角点赞，停留1s
            SeaOfStarsAW.ut_device.click(0.679, 0.936)
            time.sleep(2)

            # 8、点击评论查看，等待1s
            SeaOfStarsAW.ut_device.click(0.567, 0.934)
            time.sleep(2)

            # 9、返回首页，等待1s
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(1)

            # 10、返回home界面，停留1s
            SeaOfStarsAW.ut_device.app_terminate('com.ss.ios.auto')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')