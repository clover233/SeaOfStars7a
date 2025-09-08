import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000043(Case):
    all_app_package_list = ['']
    TEST_TIME = 2

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
            # 微信启动
            logging.info('微信启动')
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.xin')
            pos = SeaOfStarsAW.find_app_from_launcher('微信')
            while str(pos) == ('Point(x=0, y=0)'):
                SeaOfStarsAW.ut_device.swipe_left()
                pos = SeaOfStarsAW.find_app_from_launcher('微信')
            pos = SeaOfStarsAW.find_app_from_launcher('微信')
            SeaOfStarsAW.click_pos_from_launcher(pos)
            time.sleep(2)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 微信公开课-央视财经
            logging.info('微信公开课-央视财经')
            SeaOfStarsAW.check_status(xpath='//Table/SearchField[2]')
            SeaOfStarsAW.ut_device.xpath('//Table/SearchField[2]').click()
            time.sleep(2)

            SeaOfStarsAW.check_status(xpath='//SearchField')
            SeaOfStarsAW.ut_device.xpath('//SearchField').set_text('央视财经')
            time.sleep(2)
            SeaOfStarsAW.check_status(xpath='//Table/Cell[2]/StaticText[1]')
            time.sleep(2)
            SeaOfStarsAW.ut_device.xpath('//Table/Cell[2]/StaticText[1]').click()
            time.sleep(2)
            time.sleep(10)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(
                self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
                    '%H%M%S', time.localtime()) + '.png')

            # 央视财经进入返回各10次
            logging.info('央视财经进入返回各10次')
            for i in range(10):
                SeaOfStarsAW.check_status(label="更多")
                time.sleep(2)
                SeaOfStarsAW.ut_device(label="更多").click()
                time.sleep(2)
                SeaOfStarsAW.check_status(label="返回")
                SeaOfStarsAW.ut_device(label="返回").click()
                time.sleep(2)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 央视财经-红色财经-红色财经信物百年
            logging.info('央视财经-红色财经-红色财经信物百年')
            SeaOfStarsAW.check_status(label="更多")
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="更多").click()
            time.sleep(2)
            SeaOfStarsAW.check_status(label="搜索")
            SeaOfStarsAW.ut_device(label="搜索").click()
            time.sleep(2)
            SeaOfStarsAW.check_status(xpath='//SearchField')
            SeaOfStarsAW.ut_device.xpath('//SearchField').set_text('红色财经')
            time.sleep(2)
            SeaOfStarsAW.check_status(label="搜索")
            SeaOfStarsAW.ut_device(label="搜索").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.426, 0.372)
            time.sleep(6)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 返回央视财经主界面
            SeaOfStarsAW.ut_device(label="关闭").click()
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="返回").click()
            SeaOfStarsAW.check_status(label="更多")
            time.sleep(2)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(
                self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
                    '%H%M%S', time.localtime()) + '.png')

            # 返回微信主页面
            logging.info('返回主页面')
            SeaOfStarsAW.check_status(label="返回")
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.xpath('//Window[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Other[2]').click()
            SeaOfStarsAW.check_status(xpath='//*[@label="标签栏"]/Button[2]/Button[1]')
            time.sleep(2)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')