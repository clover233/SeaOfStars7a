import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000040(Case):
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
            # logging.info('应用启动')
            SeaOfStarsAW.trace_thread.add_log('微信', '应用启动')
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.xin')
            # pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.click(337, 322)
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 进入好友聊天窗口
            # logging.info('进入好友聊天窗口')
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
            SeaOfStarsAW.ut_device(label='视频通话').click()
            time.sleep(10)
            SeaOfStarsAW.check_status(label='取消')
            SeaOfStarsAW.ut_device(label='取消').click()
            time.sleep(2)
            # step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 发起语音通话
            SeaOfStarsAW.trace_thread.add_log('微信', '发起语音通话')
            SeaOfStarsAW.ut_device.click(0.933, 0.93)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.616, 0.737)
            time.sleep(2)
            # SeaOfStarsAW.check_status(label='语音通话')
            SeaOfStarsAW.ut_device(label='语音通话').click()
            time.sleep(10)
            # SeaOfStarsAW.check_status(label='取消')
            SeaOfStarsAW.ut_device(label='取消').click()
            time.sleep(2)
            # step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 返回主页面
            # logging.info('返回主页面')
            SeaOfStarsAW.trace_thread.add_log('微信', '返回主页面')
            SeaOfStarsAW.ut_device.click(0.055, 0.094)
            time.sleep(2)
            # step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('微信', '返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')