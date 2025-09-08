import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000054(Case):
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
            SeaOfStarsAW.trace_thread.add_log('淘宝', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate('com.taobao.taobao4iphone')
            # pos = SeaOfStarsAW.find_app_from_launcher('淘宝')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('淘宝')
            # pos = SeaOfStarsAW.find_app_from_launcher('淘宝')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.611, 0.365)
            time.sleep(2)
    
            # 进入我的淘宝
            logging.info('进入我的淘宝')
            SeaOfStarsAW.trace_thread.add_log('淘宝', '进入我的淘宝')
            SeaOfStarsAW.check_status(label="我的淘宝")
            SeaOfStarsAW.ut_device(label="我的淘宝").click()
            time.sleep(2)
            
            # 进入待收货
            logging.info('进入待收货')
            SeaOfStarsAW.trace_thread.add_log('淘宝', '进入待收货')
            SeaOfStarsAW.ut_device.click(0.496, 0.387)
            time.sleep(2)
            
            # 进入待付款
            logging.info('进入待付款')
            SeaOfStarsAW.trace_thread.add_log('淘宝', '进入待付款')
            SeaOfStarsAW.check_status(label="待付款未选中")
            SeaOfStarsAW.ut_device(label="待付款未选中").click()
            time.sleep(2)

            
            # 进入待评价
            logging.info('进入待评价')
            SeaOfStarsAW.trace_thread.add_log('淘宝', ' 进入待评价')
            SeaOfStarsAW.ut_device(label="待评价未选中").click()
            time.sleep(2)
            

            # 返回淘宝首页，返回home页面
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('淘宝', '返回home')
            SeaOfStarsAW.ut_device(label="返回").click()

            time.sleep(2)
            SeaOfStarsAW.ut_device(label="首页").click()
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')