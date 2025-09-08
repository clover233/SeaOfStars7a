import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class Performance_jank_kpi_05_000000(Case):
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
            SeaOfStarsAW.trace_thread.add_log('QQ', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.mqq')
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.15, 0.139)
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.xin')
            # pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # SeaOfStarsAW.click_pos_from_launcher(pos)

            time.sleep(2)

            # 点击动态
            logging.info('点击动态')
            SeaOfStarsAW.trace_thread.add_log('QQ', '点击动态')
            # SeaOfStarsAW.check_status(labelContains='动态')
            SeaOfStarsAW.ut_device(labelContains="动态").click()
            time.sleep(2)

            # 点击好友动态
            # SeaOfStarsAW.check_status(label='好友动态')
            logging.info('点击好友动态')
            SeaOfStarsAW.trace_thread.add_log('QQ', '点击好友动态')
            SeaOfStarsAW.ut_device(label="好友动态").click()
            time.sleep(2)

            # 进入我的空间
            # SeaOfStarsAW.check_status(label='我的头像')
            SeaOfStarsAW.trace_thread.add_log('QQ', '进入我的空间')
            logging.info('进入我的空间')
            SeaOfStarsAW.ut_device(label="我的头像").click()
            time.sleep(2)

            # 查看动态图片详情
            logging.info('查看动态图片详情')
            SeaOfStarsAW.trace_thread.add_log('QQ', '查看动态图片详情')
            SeaOfStarsAW.ut_device.swipe(0.4, 0.7, 0.4, 0.3)
            time.sleep(2)
            SeaOfStarsAW.check_status(label='图片')
            SeaOfStarsAW.ut_device(label="图片").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0.8, 0.5, 0.2, 0.5)
            time.sleep(3)
            SeaOfStarsAW.ut_device.swipe(0.8, 0.5, 0.2, 0.5)
            time.sleep(3)
            SeaOfStarsAW.ut_device.swipe(0.8, 0.5, 0.2, 0.5)
            time.sleep(3)

            # 返回空间
            logging.info('返回空间')
            SeaOfStarsAW.trace_thread.add_log('QQ', '返回空间')
            SeaOfStarsAW.ut_device.click(0.5, 0.5)
            time.sleep(2)

            # 返回动态主页
            SeaOfStarsAW.check_status(label='图片')
            SeaOfStarsAW.trace_thread.add_log('QQ', '返回动态主页')
            logging.info('返回动态主页')
            SeaOfStarsAW.ut_device.click(0.058, 0.079)
            time.sleep(2)

            # 返回动态
            logging.info('返回动态')
            SeaOfStarsAW.trace_thread.add_log('QQ', '返回动态')



            SeaOfStarsAW.ut_device.click(0.047, 0.082)
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