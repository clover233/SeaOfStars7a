import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_58city_0010(Case):
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
            SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
                                     self.screenshot_dir_path)

            #1.启动58同城
            logging.info('1、应用启动')
            SeaOfStarsAW.trace_thread.add_log('58同城', '应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('com.taofang.iphone')

            #2.向上抛划5次，浏览首页
            logging.info('2、向上抛划5次')
            SeaOfStarsAW.trace_thread.add_log('58同城', '向上抛划5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            # 3.向下抛划5次，浏览首页
            logging.info('3、向下抛划5次')
            SeaOfStarsAW.trace_thread.add_log('58同城', '向下抛划5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 4.点击"租房"按钮，进入租房页面
            logging.info('4、点击"租房"按钮，进入租房页面')
            SeaOfStarsAW.ut_device.click(0.304, 0.211, 1.0)
            time.sleep(1)

            # 5.向上滑5次
            logging.info('5、向上滑5次')
            SeaOfStarsAW.trace_thread.add_log('58同城', '向上滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            # 6.向下滑5次
            logging.info('6、向下滑5次')
            SeaOfStarsAW.trace_thread.add_log('58同城', '向下滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 7.点击搜索框
            logging.info('7、点击搜索框')
            SeaOfStarsAW.trace_thread.add_log('58同城', '点击搜索框')
            SeaOfStarsAW.ut_device.click(0.37, 0.155, 1.0)
            time.sleep(2)

            # 8.输入西研所，点击搜索
            logging.info('8、输入西研所，点击搜索')
            SeaOfStarsAW.trace_thread.add_log('58同城', '输入西研所')
            SeaOfStarsAW.ut_device().set_text("西研所")
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.873, 0.084, 1.0)
            time.sleep(2)

            # 9.点击第一个租房信息
            logging.info('9、点击第一个租房信息')
            SeaOfStarsAW.trace_thread.add_log('58同城', '点击第一个租房信息')
            SeaOfStarsAW.ut_device.click(0.537, 0.467, 1.0)
            time.sleep(2)

            #10.向上抛滑5次，浏览详细信息
            logging.info('10、向上抛滑5次')
            SeaOfStarsAW.trace_thread.add_log('58同城', '向上抛滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(1)

            # 11.向下抛滑5次，浏览详细信息
            logging.info('11、向下抛滑5次')
            SeaOfStarsAW.trace_thread.add_log('58同城', '向下抛滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(1)

            # 12.侧滑2次返回主页面
            logging.info('12、侧滑2次返回主页面')
            SeaOfStarsAW.trace_thread.add_log('58同城', '侧滑2次返回主页面')
            SeaOfStarsAW.ut_device.swipe(0.017, 0.809, 0.933, 0.805, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.017, 0.809, 0.933, 0.805, 0.5)
            time.sleep(1)

            # 13.上滑返回桌面
            logging.info('13、上滑返回桌面')
            SeaOfStarsAW.ut_device.app_terminate('com.taofang.iphone')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')
