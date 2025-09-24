import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_sodamusic_0010(Case):
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
            # step = 0
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            logging.info('启动汽水音乐')
            # SeaOfStarsAW.trace_thread.add_log('汽水音乐', '启动汽水音乐')
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.clickd(0.16, 0.372)
            # SeaOfStarsAW.trace_thread.add_log('汽水音乐', '搜索国歌页面浏览')
            logging.info('点击搜索标志')
            SeaOfStarsAW.ut_device.click(0.92, 0.072)
            time.sleep(2)
            logging.info('输入国歌')
            SeaOfStarsAW.ut_device.send_keys('国歌')
            time.sleep(2)
            logging.info('点击搜索')
            SeaOfStarsAW.ut_device(label='搜索').click()
            time.sleep(2)
            logging.info('上滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            logging.info('下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='取消').click()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('汽水音乐', '点击播放')
            logging.info('点击播放按钮')
            SeaOfStarsAW.ut_device.click(0.5, 0.938)
            time.sleep(2)
            logging.info('点击我的')
            SeaOfStarsAW.ut_device.click(0.903, 0.943)
            time.sleep(1)
            logging.info('点击我喜欢的音乐')   #  无法登录
            SeaOfStarsAW.ut_device(label='我喜欢的音乐').click()
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('汽水音乐', '上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.ut_device.app_terminate("com.soda.music")

        logging.info('用例执行结束')