import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000035(Case):
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
        # 清空后台


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

            # step1:应用启动
            logging.info('应用{}启动'.format("com.alipay.iphoneclient"))
            SeaOfStarsAW.trace_thread.add_log('支付宝', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate("com.alipay.iphoneclient")
            # pos = SeaOfStarsAW.find_app_from_launcher('支付宝')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('支付宝')
            # pos = SeaOfStarsAW.find_app_from_launcher('支付宝')
            # SeaOfStarsAW.click_pos_from_launcher(pos)

            SeaOfStarsAW.ut_device.click(0.613, 0.596)
            # 启动应用等待
            time.sleep(2)

            # SeaOfStarsAW.ut_device.click(0.496, 0.431)
            # time.sleep(2)

            # SeaOfStarsAW.ut_device.swipe_up()
            # time.sleep(2)

            # 首页消息 -- 口碑好店
            logging.info('首页消息 -- 口碑好店')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '首页消息 -- 口碑好店')
            SeaOfStarsAW.ut_device(label="口碑团购").click()
            time.sleep(2)
            time.sleep(5)
            # 口碑好店浏览
            SeaOfStarsAW.trace_thread.add_log('支付宝', '口碑好店浏览')
            for _ in range(3):
                logging.info('口碑好店浏览')
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            # 返回支付宝主页面
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回支付宝主页面')
            SeaOfStarsAW.ut_device(label="关闭").click()
            time.sleep(2)
            # SeaOfStarsAW.ut_device.click(0.051, 0.092)
            # time.sleep(2)



            # step5：返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('支付宝', '返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')