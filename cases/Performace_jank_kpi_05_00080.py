import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000080(Case):
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
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device().click(0.623, 0.606)
            # 浏览推荐视频
            logging.info('浏览推荐视频')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(20)

            step += 1
            # AAA 10010
            SeaOfStarsAW.check_status(xpath='//*[@label="Vahs Abb"]')
            SeaOfStarsAW.ut_device(xpath='//*[@label="Vahs Abb"]').click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(name='取消').click()
            time.sleep(2)
            step += 1
            # 打开联系人
            logging.info('打开联系人')
            SeaOfStarsAW.check_status(label='通讯录')
            SeaOfStarsAW.ut_device(label="通讯录").click()
            time.sleep(2)
            step += 1


            # 浏览联系人
            logging.info('浏览联系人')
            SeaOfStarsAW.ut_device.swipe(0.5, 0.4, 0.5, 0.8)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.5, 0.4)
            time.sleep(2)
            step += 1


            # 点击第一个联系人拨打电话
            logging.info('点击第一个联系人拨打电话')
            SeaOfStarsAW.check_status(label='Vahs Abb')
            SeaOfStarsAW.ut_device(label="Vahs Abb").click()
            time.sleep(2)
            SeaOfStarsAW.check_status(xpath='//*[@label="手机, 呼叫"]')
            SeaOfStarsAW.ut_device(xpath='//*[@label="手机, 呼叫"]').click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(name='取消').click()
            time.sleep(2)
            step += 1


            # 返回到上一层
            logging.info('返回到上一层')
            SeaOfStarsAW.ut_device(label='通讯录').click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0.5, 0.4, 0.5, 0.8)
            time.sleep(2)
            step += 1

            # 返回home
            logging.info('返回home')
            time.sleep(2)
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')