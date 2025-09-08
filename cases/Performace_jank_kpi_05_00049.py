import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000049(Case):
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
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.mqq')
            # SeaOfStarsAW.trace_thread.add_log('QQ', '应用启动')
            # pos = SeaOfStarsAW.find_app_from_launcher('QQ')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('QQ')
            # pos = SeaOfStarsAW.find_app_from_launcher('QQ')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            # time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.156, 0.142)
            time.sleep(2)
            if SeaOfStarsAW.ut_device(label="重新登录").exists:
                SeaOfStarsAW.ut_device(label="重新登录").click()
            time.sleep(5) # 有广告

            # 消息-好友聊天窗口
            logging.info('消息-好友聊天窗口')
            SeaOfStarsAW.trace_thread.add_log('QQ', '消息-好友聊天窗口')
            SeaOfStarsAW.check_status(label="测试聊天")
            SeaOfStarsAW.ut_device(label="测试聊天").click()
            time.sleep(2)

            # 浏览消息
            logging.info('浏览消息')
            SeaOfStarsAW.trace_thread.add_log('QQ', '浏览消息')
            SeaOfStarsAW.ut_device.swipe(0.5, 0.3, 0.5, 0.8)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.5, 0.3)
            time.sleep(2)

            # 浏览图片
            logging.info('浏览图片')
            SeaOfStarsAW.trace_thread.add_log('QQ', '浏览图片')
            SeaOfStarsAW.ut_device.click(0.71, 0.773)
            time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe(0.3, 0.5, 0.8, 0.5)
                time.sleep(2)

            # 返回qq主界面
            logging.info('返回qq主界面')
            SeaOfStarsAW.trace_thread.add_log('QQ', '返回qq主界面')
            SeaOfStarsAW.ut_device.click(0.5, 0.5)
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)

            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('QQ', '返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')