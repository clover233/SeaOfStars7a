import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_kiwi_0010(Case):
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

            # 1、启动虎牙直播，等待2s
            logging.info('启动虎牙直播，等待2s')
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '启动虎牙直播')
            SeaOfStarsAW.ut_device.session().app_activate('com.yy.kiwi')
            time.sleep(3)

            # 2、点击推荐页，等待2s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '浏览不同分类页')
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(2)

            # 3、浏览推荐页，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 4、点击第一个直播间进入，等待5s
            SeaOfStarsAW.ut_device.click(0.24, 0.23)
            time.sleep(5)

            # 5、点击关注，等待2s
            SeaOfStarsAW.ut_device(labelContains="关注").click()
            time.sleep(2)

            # 6、返回首页，停留2s
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 7、点击热门页，停留2s
            SeaOfStarsAW.ut_device(labelContains="热门").click()
            time.sleep(2)

            # 8、浏览热门页面，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 9、点击进入第一个直播间，等待5s
            SeaOfStarsAW.ut_device(labelContains="点击进入直播间").click()
            time.sleep(5)

            # 10、点击关注，等待2s
            SeaOfStarsAW.ut_device.click(0.404, 0.089)
            time.sleep(2)

            # 11、返回首页，等待2s
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 12、查看更多分类，等待2s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '浏览更多分类选择')
            SeaOfStarsAW.ut_device.click(0.842, 0.09)
            time.sleep(2)

            # 13、点击网游竞技，等待2s
            SeaOfStarsAW.ut_device.click(0.227, 0.438)
            time.sleep(2)

            # 14、浏览此页，上滑2次，下滑2次，每次停留2s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            # 15、
            # 16、点击单机热游，等待2s
            SeaOfStarsAW.ut_device.click(0.408, 0.438)
            time.sleep(2)

            # 17、浏览单机热游，上滑2次，下滑2次，每次停留2s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 18、返回首页，等待2s
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 19、点击推荐页面，等待2s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '查看推荐页面')
            SeaOfStarsAW.ut_device(labelContains="推荐").click()
            time.sleep(2)

            # 20、点击社区，等待2s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '浏览社区页面')
            SeaOfStarsAW.ut_device(labelContains="社区").click()
            time.sleep(2)

            # 21、浏览社区页面，上滑3次，下滑3次，等待2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 22、点击赛事，等待2s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '浏览赛事页面')
            SeaOfStarsAW.ut_device(labelContains="赛事").click()
            time.sleep(2)

            # 23、浏览赛事页面，上滑3次，下滑3次，等待2s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 24、返回首页，等待2s
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            time.sleep(2)
            # 25、返回home界面，停留2s
            SeaOfStarsAW.trace_thread.add_log('虎牙直播', '返回桌面')
            SeaOfStarsAW.ut_device.app_terminate('com.yy.kiwi')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')