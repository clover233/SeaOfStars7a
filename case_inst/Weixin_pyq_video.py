import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Weixin_pyq_video(Case):
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

            # 应用启动
            logging.info('应用启动')
            SeaOfStarsAW.trace_thread.add_log('微信', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.xin')
            logging.info('应用启动')
            SeaOfStarsAW.trace_thread.add_log('微信', '应用启动')

            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.xin')
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.611, 0.238)
            time.sleep(2)

            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            SeaOfStarsAW.trace_thread.add_log('微信', '进入好友聊天窗口')
            # SeaOfStarsAW.check_status(label='kirintest')
            SeaOfStarsAW.ut_device(label='测试用例40&38').click()
            time.sleep(2)
            # step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 发起视频通话
            # logging.info('发起视频通话')
            SeaOfStarsAW.trace_thread.add_log('微信', '发起视频通话')

            SeaOfStarsAW.ut_device.click(0.933, 0.93)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.616, 0.737)
            time.sleep(2)

            # SeaOfStarsAW.check_status(label='视频通话')
            SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
                                     self.screenshot_dir_path)
            SeaOfStarsAW.ut_device(label='视频通话').click()
            time.sleep(10)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.check_status(label='取消')
            SeaOfStarsAW.ut_device(label='取消').click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label='返回').click()

            # 返回到home页面
            logging.info('返回到home页面')
            SeaOfStarsAW.trace_thread.add_log('微信', '返回到home页面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.tencent.xin')
            time.sleep(2)
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()
        logging.info('用例执行结束')