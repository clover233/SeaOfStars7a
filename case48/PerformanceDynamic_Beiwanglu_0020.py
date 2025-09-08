import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Beiwanglu_0020(Case):
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

            # 1、启动备忘录
            logging.info('启动备忘录')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '启动备忘录')
            SeaOfStarsAW.ut_device.session().app_activate('com.apple.mobilenotes')
            time.sleep(1)

            # 2、上滑2次，下滑3次，查看备忘录列表
            logging.info('上滑2次，下滑3次，查看备忘录列表')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '上滑2次，下滑3次，查看备忘录列表')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)


            # 3、点击第一条备忘录查看内容
            logging.info('点击第一条备忘录查看内容')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '点击第一条备忘录查看内容')
            SeaOfStarsAW.ut_device.click(0.478, 0.322, 0.3)
            time.sleep(1)

            # 4、返回主界面
            logging.info('返回主界面')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '返回主界面')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(1)

            # 5、上滑返回桌面
            logging.info('上滑返回桌面')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '上滑返回桌面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

        logging.info('用例执行结束')