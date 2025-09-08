import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000001(Case):
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
            # 启动qq
            logging.info('启动qq')
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.mqq')
            SeaOfStarsAW.trace_thread.add_log('QQ','应用启动')
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
            SeaOfStarsAW.ut_device.click(0.15, 0.139)
            time.sleep(2)

            # 点击动态
            # SeaOfStarsAW.check_status(labelContains='动态')
            logging.info('点击动态')
            SeaOfStarsAW.trace_thread.add_log('QQ', '点击动态')
            SeaOfStarsAW.ut_device(labelContains="动态").click()
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # 点击阅读
            SeaOfStarsAW.check_status(label='阅读')

            SeaOfStarsAW.trace_thread.add_log('QQ', '点击阅读')
            logging.info('点击阅读')
            SeaOfStarsAW.ut_device(label="阅读").click()

            if SeaOfStarsAW.ut_device.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1'
                                            ']/Other[2]/WebView[1]/WebView[1]/WebView[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[5]').exists:
                SeaOfStarsAW.ut_device.click(0.84, 0.191)
            time.sleep(2)

            # 进入书架
            logging.info('进入书架')
            SeaOfStarsAW.trace_thread.add_log('QQ', '进入书架')
            SeaOfStarsAW.ut_device.click(0.124, 0.91)
            time.sleep(2)
            
            # 查看第一本书
            logging.info('查看第一本书')
            SeaOfStarsAW.trace_thread.add_log('QQ', '查看第一本书')
            # SeaOfStarsAW.check_status(label="最近阅读")
            SeaOfStarsAW.ut_device(label="看到").click()
            time.sleep(2)

            # 内容浏览
            logging.info('内容浏览')
            SeaOfStarsAW.trace_thread.add_log('QQ','内容浏览')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(0.8, 0.5, 0.2, 0.5)
                time.sleep(5)

            # 返回qq主界面
            logging.info('返回qq主界面')
            SeaOfStarsAW.trace_thread.add_log('QQ', '返回qq主界面')
            # SeaOfStarsAW.check_status(label='返回')
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(3)
            if SeaOfStarsAW.ut_device(label="退出阅读").exists:
                SeaOfStarsAW.ut_device(label="退出阅读").click()
                time.sleep(2)
            if SeaOfStarsAW.ut_device(label="好的").exists:
                SeaOfStarsAW.ut_device(label="好的").click()
                time.sleep(2)
            # SeaOfStarsAW.check_status(label='返回')
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)

            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('QQ', '返回home')
            # SeaOfStarsAW.check_status(labelContains='消息')
            SeaOfStarsAW.ut_device(labelContains="消息").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')