import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000056(Case):
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
            SeaOfStarsAW.trace_thread.add_log('快手', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate('com.jiangjia.gif')
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
            time.sleep(7)

            if SeaOfStarsAW.ut_device(label="我知道了").exists:
                SeaOfStarsAW.ut_device(label="我知道了").click()
                time.sleep(2)
            if SeaOfStarsAW.ut_device(label="取消").exists:
                SeaOfStarsAW.ut_device(label="取消").click()
                time.sleep(2)
            if SeaOfStarsAW.ut_device(label="恭喜获得新人礼包").exists:
                SeaOfStarsAW.ut_device.click(0.917, 0.185)
                time.sleep(2)
            if SeaOfStarsAW.ut_device(label="新人福利7天领8.3元").exists:
                SeaOfStarsAW.ut_device.click(0.885, 0.198)
                time.sleep(2)
            if SeaOfStarsAW.ut_device(label="老友福利7天领6.2元").exists:
                SeaOfStarsAW.ut_device.click(0.885, 0.198)
                time.sleep(2)
            if SeaOfStarsAW.ut_device(label="禁止").exists:
                SeaOfStarsAW.ut_device(label="禁止").click()
                time.sleep(2)

            if SeaOfStarsAW.ut_device(label="限时3天高额奖励").exists:
                SeaOfStarsAW.ut_device.click(0.91, 0.218)
                time.sleep(2)
            if SeaOfStarsAW.ut_device(label="恭喜获得老友回归红包").exists:
                SeaOfStarsAW.ut_device.click(0.92, 0.182)
                time.sleep(2)

            # 浏览并向下滑切换视频
            logging.info('浏览并向下滑切换视频')
            SeaOfStarsAW.trace_thread.add_log('快手', '浏览并向下滑切换视频')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(10)
            # 返回home页面
            logging.info('返回home页面')
            SeaOfStarsAW.trace_thread.add_log('快手', '返回home页面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')