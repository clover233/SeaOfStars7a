import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000010(Case):
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
            # 应用启动
            logging.info('应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate("com.dragon.read")
            # pos = SeaOfStarsAW.find_app_from_launcher('番茄小说')
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '应用启动')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('番茄小说')
            # pos = SeaOfStarsAW.find_app_from_launcher('番茄小说')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.159, 0.263)
            time.sleep(2)

            # 进入书架
            logging.info('进入书架')
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '进入书架')
            SeaOfStarsAW.ut_device(label="书架").click()
            time.sleep(2)

            # 点击书籍进行阅读
            logging.info('点击书籍进行阅读')
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '点击书籍进行阅读')
            SeaOfStarsAW.ut_device.click(0.161, 0.34)
            time.sleep(2)

            # 阅读书籍
            logging.info('阅读书籍')
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '阅读书籍')
            for _ in range(8):

                SeaOfStarsAW.ut_device.swipe(0.8, 0.5, 0.2, 0.5)
                time.sleep(15)

            # 返回番茄小说首页
            logging.info('返回番茄小说首页')
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '返回番茄小说首页')
            SeaOfStarsAW.ut_device.click(0.068, 0.062)
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="书城").click()
            time.sleep(2)

            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')