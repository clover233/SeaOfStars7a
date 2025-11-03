import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Douyin_0010(Case):
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
            logging.info('静置')
            SeaOfStarsAW.trace_thread.add_log('抖音', '静置')
            time.sleep(5)


            # 1、点击进入抖音，启动5s，等待2s
            logging.info('点击进入抖音，启动5s，等待2s')
            SeaOfStarsAW.trace_thread.add_log('抖音', '启动抖音，上下切换视频')
            SeaOfStarsAW.ut_device.session().app_activate('com.ss.iphone.ugc.Aweme')
            time.sleep(5)

            # 2、浏览推荐视频3次
            logging.info('浏览推荐视频3次')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(10)

            # 3、点击视频评论按钮
            logging.info('3、点击视频评论按钮')
            SeaOfStarsAW.trace_thread.add_log('抖音', '3、点击视频评论按钮')
            SeaOfStarsAW.ut_device.click(0.93, 0.603)
            time.sleep(2)

            # 4、浏览推荐视频3次，2s
            logging.info('4、浏览推荐视频评论')
            SeaOfStarsAW.trace_thread.add_log('抖音', '4、浏览推荐视频评论')
            SeaOfStarsAW.ut_device.click(0.494, 0.212)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 5、点击评论按钮浏览
            logging.info('5、点击评论按钮浏览')
            SeaOfStarsAW.trace_thread.add_log('抖音', '5、点击评论按钮浏览')
            SeaOfStarsAW.ut_device.click(0.93, 0.603)
            time.sleep(2)

            # 6、点击输入框
            logging.info('6、点击输入框')
            SeaOfStarsAW.trace_thread.add_log('抖音', '6、点击输入框')
            SeaOfStarsAW.ut_device.click(0.221, 0.929)
            time.sleep(2)

            # 7、输入“我是评论ABC”
            logging.info('7、输入“我是评论ABC”')
            SeaOfStarsAW.trace_thread.add_log('抖音', '7、输入“我是评论ABC”')
            SeaOfStarsAW.ut_device().set_text("我是评论ABC")
            time.sleep(1)

            # 8、点击发送
            logging.info('8、点击发送')
            SeaOfStarsAW.trace_thread.add_log('抖音', '8、点击发送')
            SeaOfStarsAW.ut_device.click(0.91, 0.532)
            time.sleep(2)

            # 9、返回推荐视频
            logging.info('9、返回推荐视频')
            SeaOfStarsAW.trace_thread.add_log('抖音', '9、返回推荐视频')
            time.sleep(1)

            # 10、返回home页，等待2s
            logging.info('10、返回home页')
            SeaOfStarsAW.trace_thread.add_log('抖音', '10、返回home页')
            SeaOfStarsAW.ut_device.app_terminate('com.ss.iphone.ugc.Aweme')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
