import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_jingdong_0020(Case):
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
            SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
                                     self.screenshot_dir_path)

            # 1、启动京东，等待3s
            logging.info('启动京东')
            SeaOfStarsAW.trace_thread.add_log('京东', '启动京东，等待3s')
            # todo 微博的坐标地址要改下
            SeaOfStarsAW.ut_device.session().app_activate('com.360buy.jdmobile')
            time.sleep(3)
            time.sleep(2)

            # 2、点击上方京东超市，等待2s
            logging.info('首页浏览，上滑5次，下滑5次，每次停留2s')
            SeaOfStarsAW.trace_thread.add_log('京东', '首页浏览，上滑5次，下滑5次，每次停留2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 3、点击上方粮油调味，等待2s
            logging.info('点击上方粮油调味，等待2s-浏览')
            SeaOfStarsAW.trace_thread.add_log('京东', '点击上方粮油调味，等待2s-浏览')
            SeaOfStarsAW.ut_device.click(0.429, 0.185)
            # SeaOfStarsAW.ut_device(labelContains="京东超市").click()
            time.sleep(2)
            # SeaOfStarsAW.ut_device(labelContains="粮油调味").click()
            SeaOfStarsAW.ut_device.click(0.133, 0.334)
            time.sleep(2)
            # 4、粮油调味页面浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 5、加入第一个商品到购物车，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '加入第一个商品到购物车，等待2s')
            SeaOfStarsAW.ut_device.click(0.225, 0.515)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.454, 0.933)
            time.sleep(1)
            SeaOfStarsAW.ut_device(labelContains="确定").click()
            time.sleep(2)
            # 6、点击结算，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击结算，停留2s')
            SeaOfStarsAW.ut_device.click(0.722, 0.935)
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="去结算").click()
            time.sleep(2)
            # 7、点击新建地址，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击新建地址，等待2s')
            SeaOfStarsAW.ut_device.click(0.664, 0.554)
            time.sleep(2)
            # 8、返回首页，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '返回首页，等待2s')
            for i in range(4):
                SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
                time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.931, 0.218)
            time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
                time.sleep(1)
            # 9、点击购物车，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击购物车，等待2s')
            SeaOfStarsAW.ut_device(labelContains="购物车").click()
            time.sleep(2)
            # 10、点击去结算，等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '点击去结算，停留2s')
            SeaOfStarsAW.ut_device(labelContains="去结算").click()
            time.sleep(2)
            # 11、返回首页等待2s
            SeaOfStarsAW.trace_thread.add_log('京东', '返回首页等待2s')
            SeaOfStarsAW.ut_device.click(0.335, 0.557)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(2)

            # 12、返回home页，等待2s
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.360buy.jdmobile')
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
