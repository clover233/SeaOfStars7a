import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_mangguoTV_0010(Case):
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

            # 1、启动应用，停留8s
            logging.info('启动芒果tv，等待8s')
            SeaOfStarsAW.trace_thread.add_log('芒果tv', '首页浏览')
            SeaOfStarsAW.ut_device.session().app_activate('com.hunantv.imgotv')
            time.sleep(8)

            # 2、首页浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 3、点击综艺，停留1s
            SeaOfStarsAW.trace_thread.add_log('芒果tv', '浏览综艺')
            SeaOfStarsAW.ut_device(labelContains="综艺").click()
            time.sleep(2)

            # 4、浏览综艺，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 5、点击上方tab栏“电视剧”，切换至电视剧界面，停留1s
            SeaOfStarsAW.trace_thread.add_log('芒果tv', '浏览电视剧')
            SeaOfStarsAW.ut_device(labelContains="电视剧").click()
            time.sleep(2)

            # 6、电视剧界面上滑5次，下滑至顶部
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 7、点击搜素框，停留1s
            SeaOfStarsAW.trace_thread.add_log('芒果tv', '搜索电视剧')
            SeaOfStarsAW.ut_device.click(0.441, 0.092)
            time.sleep(1)

            # 8、输入天天向上
            SeaOfStarsAW.ut_device.click(0.461, 0.095)
            time.sleep(1)
            SeaOfStarsAW.ut_device.send_keys('天天向上')
            time.sleep(2)

            # 9、点击第一条显示结果，停留3s
            SeaOfStarsAW.trace_thread.add_log('芒果tv', '播放电视剧')
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(2)

            # 10、点击播放，停留10s
            SeaOfStarsAW.ut_device(labelContains="播放").click()
            time.sleep(10)

            # 11、点击切换到全屏，播放15s
            SeaOfStarsAW.ut_device(labelContains="ad fullscreen icon").click()
            time.sleep(15)

            # 12、取消全屏模式
            SeaOfStarsAW.ut_device(labelContains="mediaControl back").click()
            time.sleep(2)

            # 13、点击讨论，停留1s
            SeaOfStarsAW.ut_device(labelContains="讨论").click()
            time.sleep(1)

            # 14、查看评论，上滑5次，下滑5，停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 15、返回首页，停留1s
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_right()
                time.sleep(2)

            # 16、上滑返回桌面
            SeaOfStarsAW.ut_device.app_terminate('com.hunantv.imgotv')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')