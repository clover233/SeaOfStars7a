import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_AttachedScreen_0020(Case):
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

            # 1、进入负一屏（停留2s）
            logging.info('进入负一屏')
            SeaOfStarsAW.trace_thread.add_log('负一屏', '进入负一屏')
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(2)

            # 2、点击搜索框输入“优惠加油”
            logging.info('点击搜索框输入“优惠加油”')
            SeaOfStarsAW.trace_thread.add_log('负一屏', '点击搜索框输入“优惠加油”')
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text("优惠加油")
            time.sleep(1)

            # 3、点击优惠加油
            logging.info('点击优惠加油')
            SeaOfStarsAW.trace_thread.add_log('负一屏', '点击优惠加油')
            SeaOfStarsAW.ut_device.click(0.495, 0.151, 0.3)
            time.sleep(2)

            # 4、上滑3次，下滑3次
            logging.info('上滑3次，下滑3次')
            SeaOfStarsAW.trace_thread.add_log('负一屏', '上滑3次，下滑3次')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 5、返回负一屏主页
            logging.info('返回负一屏主页')
            SeaOfStarsAW.trace_thread.add_log('负一屏', '返回负一屏主页')
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            # 6、点击搜索框输入“手机充值”点击手机充值
            logging.info('点击搜索框输入“手机充值”点击手机充值')
            SeaOfStarsAW.trace_thread.add_log('负一屏', '点击搜索框输入“手机充值”点击手机充值')
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text("手机充值")
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.495, 0.151, 0.3)
            time.sleep(2)

            # 7、上滑1次，下滑一次，返回上一层（重复3次）
            logging.info('上滑1次，下滑一次，返回上一层')
            SeaOfStarsAW.trace_thread.add_log('负一屏', '上滑1次，下滑一次，返回上一层')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 8、返回负一屏主页
            logging.info('返回负一屏主页')
            SeaOfStarsAW.trace_thread.add_log('负一屏', '返回负一屏主页')
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            # 9、返回home界面，等待2s
            logging.info('返回home界面')
            SeaOfStarsAW.trace_thread.add_log('负一屏', '返回home界面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')