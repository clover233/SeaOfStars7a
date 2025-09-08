import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000055(Case):
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
    
            # 进入逛逛
            logging.info('进入逛逛')
            SeaOfStarsAW.trace_thread.add_log('淘宝', '进入逛逛')
            if SeaOfStarsAW.ut_device(label="视频").exists:
                SeaOfStarsAW.ut_device(label="视频").click()
            if SeaOfStarsAW.ut_device(label="直播").exists:
                SeaOfStarsAW.ut_device(label="直播").click()
            else:
                SeaOfStarsAW.ut_device(label="逛逛").click()
            time.sleep(1)
            # if SeaOfStarsAW.ut_device(label="视频").exists:
            #     SeaOfStarsAW.ut_device.click(0.5, 0.72)
            #     time.sleep(2)

            SeaOfStarsAW.ut_device(label="关注,未选中,按钮").click()
            time.sleep(2)
            time.sleep(10)
            # 点击第一个直播
            logging.info('点击第一个直播')
            SeaOfStarsAW.trace_thread.add_log('淘宝', '点击第一个直播')
            SeaOfStarsAW.ut_device.click(0.073, 0.864)
            time.sleep(2)
            
            # 停顿十秒
            logging.info('停顿十秒')
            time.sleep(10)

            # 返回淘宝首页，返回home页面
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('淘宝', '返回home')
            if SeaOfStarsAW.ut_device(label="关闭").exists:
                SeaOfStarsAW.ut_device(label="关闭").click()
                time.sleep(2)
            else:

                SeaOfStarsAW.ut_device.click(0.054, 0.104)
                time.sleep(2)
            SeaOfStarsAW.ut_device(label="首页").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.stop_trace()

            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()



        logging.info('用例执行结束')