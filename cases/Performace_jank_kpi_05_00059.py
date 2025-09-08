import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000059(Case):
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
            SeaOfStarsAW.ut_device.session().app_activate('com.meituan.imeituan')
            pos = SeaOfStarsAW.find_app_from_launcher('美团')
            while str(pos) == ('Point(x=0, y=0)'):
                SeaOfStarsAW.ut_device.swipe_left()
                pos = SeaOfStarsAW.find_app_from_launcher('美团')
            pos = SeaOfStarsAW.find_app_from_launcher('美团')
            SeaOfStarsAW.click_pos_from_launcher(pos)

            time.sleep(2)

            # 首页-美食-外卖
            logging.info('首页-美食-外卖')
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="外卖").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="美食").click()
            time.sleep(2)

            # 点击排序的第一个
            logging.info('点击排序的第一个')
            SeaOfStarsAW.ut_device.click(0.181, 0.712)
            time.sleep(2)

            # 浏览
            logging.info('浏览')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # 查看商品详情
            logging.info('查看商品详情')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains='月售').click()
            time.sleep(2)

            # 浏览商品详情
            logging.info('浏览商品详情')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            #返回美团首页，返回home页面
            logging.info('返回美团首页，返回home页面')
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')