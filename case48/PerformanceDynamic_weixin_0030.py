import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class PerformanceDynamic_weixin_0030(Case):
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
            # 启动相机
            logging.info('启动微信')
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.mqq')
            SeaOfStarsAW.trace_thread.add_log('微信','应用启动')
            # pos = SeaOfStarsAW.find_app_from_launcher('QQ')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('QQ')
            # pos = SeaOfStarsAW.find_app_from_launcher('QQ')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            # time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.598, 0.598)
            time.sleep(2)

            SeaOfStarsAW.trace_thread.add_log('微信', '进入通讯录浏览')
            SeaOfStarsAW.ut_device.click(0.373, 0.921)
            time.sleep(2)
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe(0.5, 0.7, 0.5, 0.2)
                time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.7)
                time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0.5, 0.7, 0.5, 0.2)
            time.sleep(2)

            SeaOfStarsAW.trace_thread.add_log('微信', '进入好友界面')
            SeaOfStarsAW.ut_device(label="测试").click()
            time.sleep(2)

            SeaOfStarsAW.trace_thread.add_log('微信', '进入好友 朋友圈')
            SeaOfStarsAW.ut_device(label="朋友圈").click()
            time.sleep(2)

            SeaOfStarsAW.trace_thread.add_log('微信', '点击朋友圈图片')
            SeaOfStarsAW.ut_device.click(0.284, 0.67)
            time.sleep(2)

            for _ in range(6):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)

            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)

            SeaOfStarsAW.ut_device.click(0.121, 0.944)
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="快捷操作").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="扫一扫").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.879, 0.812)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.633, 0.555)
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="关闭").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="关闭").click()
            time.sleep(2)
            # 返回home
            SeaOfStarsAW.trace_thread.add_log('微信', '返回home')
            logging.info('返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()
            SeaOfStarsAW.ut_device.app_terminate("com.tencent.xin")
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')