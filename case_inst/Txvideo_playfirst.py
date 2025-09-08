import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Txvideo_playfirst(Case):
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


            # 启动腾讯视频
            logging.info('启动')
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.live4iphone')


            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.607, 0.121)
            time.sleep(5)
            if SeaOfStarsAW.ut_device(label='我知道了').exists:
                SeaOfStarsAW.ut_device(label='我知道了').click()
            step += 1

            # 进入电视剧tab页
            logging.info('进入电视剧tab页')


            SeaOfStarsAW.ut_device(name='电视剧').click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.249, 0.581)
            SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
                                     self.screenshot_dir_path)
            SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.5, 0.5)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0.5, 0.5, 0.5, 0.8)

            SeaOfStarsAW.stop_trace()
            step += 1

            SeaOfStarsAW.ut_device.app_terminate('com.tencent.live4iphone')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')