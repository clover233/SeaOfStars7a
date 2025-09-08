import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Weixin_checktext(Case):
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

            # 应用启动
            logging.info('应用启动')
            SeaOfStarsAW.trace_thread.add_log('微信', '应用启动')

            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.xin')
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.611, 0.238)
            time.sleep(2)

            time.sleep(2)

            # 进入群聊
            logging.info('进入群聊')
            SeaOfStarsAW.trace_thread.add_log('微信', '进入群聊')
            # SeaOfStarsAW.check_status(label='测试群聊')
            SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
                                     self.screenshot_dir_path)
            SeaOfStarsAW.ut_device(label="测试用例36").click()
            time.sleep(3)

            SeaOfStarsAW.stop_trace()
            step += 1



            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 返回home
            SeaOfStarsAW.trace_thread.add_log('微信', '返回home')
            logging.info('返回home')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.tencent.xin')
            time.sleep(2)
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')