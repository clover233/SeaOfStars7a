import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_qqm_0030(Case):
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

            logging.info('启动QQ音乐')
            # SeaOfStarsAW.trace_thread.add_log('QQ音乐', '启动QQ音乐')
            # SeaOfStarsAW.ut_device.swipe_left()
            # SeaOfStarsAW.ut_device.click(0.847, 0.135)
            SeaOfStarsAW.ut_device.session().app_activate("com.tencent.QQMusic")
            time.sleep(8)
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击播放')
            # SeaOfStarsAW.trace_thread.add_log('QQ音乐', '查看本地')
            SeaOfStarsAW.ut_device.click(0.798, 0.888)
            time.sleep(1)
            # SeaOfStarsAW.trace_thread.add_log('QQ音乐', '上滑退出')
            logging.info('上滑退出')
            # SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            logging.info('启动微博')
            # SeaOfStarsAW.trace_thread.add_log('微博', '启动微博')
            # SeaOfStarsAW.ut_device.click(0.846, 0.125)
            SeaOfStarsAW.ut_device.session().app_activate("com.sina.weibo")
            time.sleep(8)
            logging.info('上滑5次，下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击发现')
            # SeaOfStarsAW.ut_device.click(0.056, 0.07)
            SeaOfStarsAW.ut_device(label='发现').click()
            time.sleep(2)
            logging.info('上滑2次，下滑2次')
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('返回首页')
            SeaOfStarsAW.ut_device.click(0.121, 0.944)
            time.sleep(2)
            logging.info('点击第一条文章')
            SeaOfStarsAW.ut_device.click(0.255, 0.176)
            time.sleep(2)
            logging.info('上滑5次，下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击返回')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('微博', '上滑退出')
            logging.info('上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            logging.info('主页下拉进入控制中心')
            SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.8, 1)
            time.sleep(2)
            logging.info('点击播放下一首')
            SeaOfStarsAW.ut_device.click(0.201, 0.26)
            time.sleep(2)
            logging.info('上滑')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            logging.info('上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            logging.info('启动京东')
            # SeaOfStarsAW.trace_thread.add_log('京东', '启动京东')
            # SeaOfStarsAW.ut_device.click(0.156, 0.244)
            SeaOfStarsAW.ut_device.session().app_activate("com.360buy.jdmobile")
            time.sleep(5)
            logging.info('上滑5次，下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击生鲜')
            SeaOfStarsAW.ut_device.click(0.115, 0.403)
            time.sleep(2)
            logging.info('上滑5次，下滑5次')
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for _ in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            logging.info('点击返回首页')
            SeaOfStarsAW.ut_device.click(0.067, 0.075)
            time.sleep(2)
            # SeaOfStarsAW.trace_thread.add_log('京东', '上滑退出')
            logging.info('上滑退出')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            logging.info('启动相机')
            # SeaOfStarsAW.trace_thread.add_log('相机', '启动相机')
            SeaOfStarsAW.ut_device.click(0.843, 0.929)
            time.sleep(4)
            for _ in range(3):
                logging.info('点击拍照3次')
                SeaOfStarsAW.ut_device.click(0.843, 0.929)
                time.sleep(2)
            logging.info('上滑退出相机')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            logging.info('主页下拉进入控制中心')
            SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.8, 1)
            time.sleep(2)
            logging.info('点击关闭音乐')
            SeaOfStarsAW.ut_device.click(0.201, 0.26)
            time.sleep(2)
            logging.info('上滑返回桌面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.ut_device.app_terminate("com.tencent.QQMusic")

        logging.info('用例执行结束')