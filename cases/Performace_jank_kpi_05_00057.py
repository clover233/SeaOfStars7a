import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000057(Case):
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
            logging.info('应用{}启动'.format("com.jiangjia.gif"))
            SeaOfStarsAW.trace_thread.add_log('快手', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate("com.jiangjia.gif")
            # pos = SeaOfStarsAW.find_app_from_launcher('快手')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('快手')
            # pos = SeaOfStarsAW.find_app_from_launcher('快手')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.386, 0.37)
            # 启动应用等待
            time.sleep(15)

            # step2:点击“我的”
            logging.info('点击“我的”')
            SeaOfStarsAW.trace_thread.add_log('快手', '点击“我的”')
            # SeaOfStarsAW.check_status(label="关注", name="关注")
            # time.sleep(2)

            # 点击“我的”
            SeaOfStarsAW.ut_device(label="我").click()
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(label="更多")

            # step3:点击查看第一个作品，浏览10s，下滑三次
            logging.info('点击查看第一个作品')
            SeaOfStarsAW.trace_thread.add_log('快手', '点击查看第一个作品')
            # 点击第一个作品
            SeaOfStarsAW.ut_device.click(0.179, 0.702)
            # 界面判断
            # SeaOfStarsAW.check_status(name="ToolBarGroupComment")
            time.sleep(10)
            for i in range(0, 2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(10)
            # 界面判断
            # SeaOfStarsAW.check_status(name="ToolBarGroupComment")

            # step5：返回主界面，返回home
            logging.info('返回主界面，返回home')
            SeaOfStarsAW.trace_thread.add_log('快手', '返回主界面，返回home')
            # 点击返回
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="首页").click()
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(label="关注", name="关注")
            time.sleep(2)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')