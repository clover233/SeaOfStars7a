import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Appmarket_0010(Case):
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

            # 1、启动应用市场（停留2s）
            logging.info('启动应用市场')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '启动应用市场')
            SeaOfStarsAW.ut_device.session().app_activate('com.apple.AppStore')
            time.sleep(2)

            # 2、下滑进入本周热门应用（停留2S）
            logging.info('进入本周热门应用')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '进入本周热门应用')
            SeaOfStarsAW.ut_device.click(0.871, 0.93, 0.3)
            time.sleep(2)

            # 3、点击本周热门app
            logging.info('点击本周热门app')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '点击本周热门app')
            SeaOfStarsAW.ut_device.click(0.73, 0.667, 0.3)
            time.sleep(2)

            # 4、上滑1次，下滑1次，（停留2s）
            logging.info('上滑1次，下滑1次')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '上滑1次，下滑1次')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 5、侧滑返回首页（停留2S）
            logging.info('侧滑返回首页')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '侧滑返回首页')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(2)

            # 6、点击搜索框（停留2s）
            logging.info('点击搜索框')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '点击搜索框')
            SeaOfStarsAW.ut_device.click(0.415, 0.158, 0.5)
            time.sleep(2)

            # 7、26键的键盘输入“kxxxl”，等待1s
            logging.info('26键的键盘输入“kxxxl”')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '26键的键盘输入“kxxxl”')
            SeaOfStarsAW.ut_device.click(0.793, 0.75, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.297, 0.819, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.297, 0.819, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.297, 0.819, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.899, 0.754, 0.3)
            time.sleep(1)

            # 8、点击第一条文字内容，等待1s
            logging.info('点击第一条文字内容')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '点击第一条文字内容')
            SeaOfStarsAW.ut_device.click(0.148, 0.636, 0.3)
            time.sleep(1)

            # 9、点击小艺输入法中的搜索图标
            logging.info('点击小艺输入法中的搜索图标')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '点击小艺输入法中的搜索图标')
            SeaOfStarsAW.ut_device.click(0.879, 0.884, 0.3)
            time.sleep(2)

            # 10、点击第一个搜索结果（停留2s）
            logging.info('点击第一个搜索结果')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '点击第一个搜索结果')
            SeaOfStarsAW.ut_device.click(0.507, 0.649, 0.3)
            time.sleep(2)

            # 11、浏览界面（上滑下滑各5次，每次停留2s）
            logging.info('浏览界面')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '浏览界面')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 12、返回首页(停留2s)
            logging.info('返回首页')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '返回首页')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(2)

            # 13、返回Home界面(停留2s)
            logging.info('返回Home界面')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '返回Home界面')
            SeaOfStarsAW.ut_device.click(0.123, 0.932, 0.5)
            time.sleep(2)

            # 14、返回首页(停留2s)
            # 15、返回Home界面(停留2s)
            logging.info('返回Home界面')
            SeaOfStarsAW.trace_thread.add_log('应用市场', '返回Home界面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

        logging.info('用例执行结束')