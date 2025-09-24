import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class PerformanceDynamic_dazhongdianping_0010(Case):
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

            # 1、启动大众点评（停留3s）
            logging.info('1、启动大众点评')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '启动大众点评')
            SeaOfStarsAW.ut_device.session().app_activate('com.dianping.dpscope')
            time.sleep(3)

            # 2、点击美食（停留1s）
            logging.info('2、点击美食')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '2、点击美食')
            SeaOfStarsAW.ut_device.click(0.117, 0.163, 0.3)
            time.sleep(1)

            # 3、点击搜索框，输入“烧烤”（停留1s）
            logging.info('3、点击搜索框，输入“烧烤”')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '3、点击搜索框，输入“烧烤”')
            SeaOfStarsAW.ut_device.click(0.154, 0.143, 0.2)
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text('烧烤')
            time.sleep(1)
            time.sleep(1)

            # 4、点击搜索（停留1s）
            logging.info('4、点击搜索')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '4、点击搜索')
            SeaOfStarsAW.ut_device.click(0.931, 0.097, 0.3)
            time.sleep(1)

            # 5、滑动浏览烧烤搜索结果（上滑5次，下滑5次，每次停留2s）
            logging.info('5、滑动浏览烧烤搜索结果')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '5、滑动浏览烧烤搜索结果')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 6、点击进入第一家商铺（停留1s）
            logging.info('6、点击进入第一家商铺')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '6、点击进入第一家商铺')
            SeaOfStarsAW.ut_device.click(0.137, 0.329, 0.3)
            time.sleep(1)

            # 7、滑动浏览商铺（上滑5次，下滑5次，每次停留2s）
            logging.info('7、滑动浏览商铺')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '7、滑动浏览商铺')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 8、点击评价（停留1s）
            logging.info('8、点击评价')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '8、点击评价')
            SeaOfStarsAW.ut_device.click(0.578, 0.706, 0.3)
            time.sleep(1)

            # 9、点击查看全部（停留1s）
            logging.info('9、点击查看全部')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '9、点击查看全部')
            SeaOfStarsAW.ut_device.click(0.882, 0.194, 0.3)
            time.sleep(1)

            # 10、滑动浏览评论（上滑5次，下滑5次，每次停留2s）
            logging.info('10、滑动浏览评论')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '10、滑动浏览评论')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 11、返回美食页面（停留1s）
            logging.info('11、返回美食页面')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '11、返回美食页面')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
                time.sleep(1)

            # 12、滑动美食页面（上滑5次，下滑5次，每次停留2s）
            logging.info('12、滑动美食页面')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '12、滑动美食页面')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 13、返回大众点评首页（停留1s）
            logging.info('13、返回大众点评首页')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '13、返回大众点评首页')
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)

            # 14、返回home界面（停留1s）
            logging.info('14、返回home界面')
            SeaOfStarsAW.trace_thread.add_log('大众点评', '返回home界面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.dianping.dpscope')
            time.sleep(1)

        logging.info('用例执行结束')
