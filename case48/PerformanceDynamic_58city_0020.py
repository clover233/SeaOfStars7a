import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_58city_0020(Case):
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

            # 1.启动58同城
            logging.info('1、应用启动')
            SeaOfStarsAW.trace_thread.add_log('58同城', '应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('com.taofang.iphone')
            time.sleep(1)

            # 2.点击本地服务
            logging.info('2、点击本地服务')
            SeaOfStarsAW.trace_thread.add_log('58同城', '点击本地服务')
            SeaOfStarsAW.ut_device.click(0.882, 0.223, 1.0)
            time.sleep(3)

            # 3.浏览本地服务界面
            logging.info('3、向上滑5次')
            SeaOfStarsAW.trace_thread.add_log('58同城', '向上滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            logging.info('3、向下滑5次')
            SeaOfStarsAW.trace_thread.add_log('58同城', '向下滑5次')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 4.点击搜索框
            logging.info('4、输入保洁')
            SeaOfStarsAW.trace_thread.add_log('58同城', '输入保洁，点击搜索')
            SeaOfStarsAW.ut_device.click(0.560, 0.147, 0.1)
            time.sleep(1)

            # 5.输入“保洁”进行搜索
            logging.info('5、输入“保洁”进行搜索')
            SeaOfStarsAW.trace_thread.add_log('58同城', '输入“保洁”进行搜索')
            SeaOfStarsAW.ut_device().set_text("保洁")
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.896, 0.095, 1.0)
            time.sleep(15)

            # 6.点击搜索后的第一条结果
            logging.info('6、点击搜索后结果')
            SeaOfStarsAW.trace_thread.add_log('58同城', '点击搜索后结果')
            SeaOfStarsAW.ut_device.click(0.39, 0.269, 1.0)
            time.sleep(5)

            # 7.浏览详情
            logging.info('7、浏览详情')
            SeaOfStarsAW.trace_thread.add_log('58同城', '浏览详情')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 8.返回首页
            logging.info('8、返回首页')
            SeaOfStarsAW.trace_thread.add_log('58同城', '返回首页')
            for i in range(4):
                SeaOfStarsAW.ut_device.click(0.057, 0.081, 0.1)
                time.sleep(1)

            # 9.返回home界面
            logging.info('9、返回Home界面')
            SeaOfStarsAW.ut_device.app_terminate('com.taofang.iphone')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
