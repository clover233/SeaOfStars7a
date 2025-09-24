import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qiyi_0010(Case):
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

            logging.info('启动爱奇艺')
            SeaOfStarsAW.trace_thread.add_log('爱奇艺', '启动爱奇艺')
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.85, 0.145)

            time.sleep(5)
            logging.info('点击搜索')
            SeaOfStarsAW.ut_device(label='搜索框').click()
            time.sleep(2)
            logging.info('输入大话天仙')
            SeaOfStarsAW.ut_device.send_keys('大话天仙')
            time.sleep(1)
            logging.info('点击搜索')
            SeaOfStarsAW.ut_device.click(0.93, 0.075)
            time.sleep(2)
            logging.info('返回')
            SeaOfStarsAW.ut_device.click(0.046, 0.076)
            time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device.click(0.05, 0.075)
            time.sleep(2)
            logging.info('点击热点')
            SeaOfStarsAW.ut_device(label='热点').click()
            time.sleep(3)
            logging.info('点击首页')  # 右滑无法切换tab
            SeaOfStarsAW.ut_device.click(0.183, 0.115)
            time.sleep(2)
            logging.info('点击主页第1个推荐视频')  # 注意有广告情况
            # SeaOfStarsAW.trace_thread.add_log('微信', '启动微信')
            SeaOfStarsAW.ut_device.click(0.256, 0.559)
            time.sleep(10)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='pread mini back iphone').click()
            time.sleep(2)
            logging.info('点击主页第2个推荐视频')  # 注意有广告情况
            SeaOfStarsAW.ut_device.click(0.25, 0.734)
            time.sleep(10)
            logging.info('切换到全屏')
            SeaOfStarsAW.ut_device(label='全屏观看').click()
            time.sleep(15)
            logging.info('点击屏幕现实横屏标志')
            SeaOfStarsAW.ut_device.click(0.936, 0.281)
            time.sleep(1)
            logging.info('退出全屏')
            SeaOfStarsAW.ut_device(label='pread mini back iphone').click()
            time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='pread mini back iphone').click()
            time.sleep(2)
            logging.info('点击主页第3个推荐视频')
            SeaOfStarsAW.ut_device.click(0.73, 0.738)
            time.sleep(10)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='pread mini back iphone').click()
            time.sleep(2)
            logging.info('点击主页第4个推荐视频')
            SeaOfStarsAW.ut_device.click(0.256, 0.892)
            time.sleep(10)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device(label='pread mini back iphone').click()
            time.sleep(2)
            logging.info('点击主页第5个推荐视频')
            SeaOfStarsAW.ut_device.click(0.743, 0.884)
            time.sleep(10)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device.click(0.056, 0.07)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('爱奇艺', '上滑退出')
            logging.info('上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.ut_device.app_terminate("com.qiyi.iphone")
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')