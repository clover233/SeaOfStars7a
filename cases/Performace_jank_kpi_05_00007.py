import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000007(Case):
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
            # pos = SeaOfStarsAW.find_app_from_launcher('哔哩哔哩')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '应用启动')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('哔哩哔哩')
            # pos = SeaOfStarsAW.find_app_from_launcher('哔哩哔哩')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.389, 0.716)
            time.sleep(6)
            # 广告
            if SeaOfStarsAW.ut_device(label="我知道了").exists:
                SeaOfStarsAW.ut_device(label="我知道了").click()
                time.sleep(2)

            # 搜索铠甲勇士

            logging.info('搜索铠甲勇士')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '搜索铠甲勇士')
            SeaOfStarsAW.check_status(label='搜索栏')
            SeaOfStarsAW.ut_device(label="搜索栏").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device().set_text("铠甲勇士")
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="搜索").click()
            time.sleep(2)


            # 点击立即观看
            logging.info('点击立即观看')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击立即观看')
            # 场景变更
            # SeaOfStarsAW.check_status(label='1')
            SeaOfStarsAW.ut_device.click(0.182, 0.37)
            time.sleep(20)
            # 快进
            logging.info('快进')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '快进')
            SeaOfStarsAW.ut_device.swipe(0.25, 0.18, 0.75, 0.18)
            time.sleep(20)
            logging.info('第一段trace')
            SeaOfStarsAW.stop_trace()

            SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
                                     self.screenshot_dir_path)


            # 调大音量
            logging.info('调大音量')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '调大音量')
            SeaOfStarsAW.ut_device.swipe(0.848, 0.265, 0.809, 0.112)
            time.sleep(20)
            # 调小音量
            logging.info('调小音量')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '调小音量')
            SeaOfStarsAW.ut_device.swipe(0.848, 0.112, 0.809, 0.265)
            time.sleep(20)
            # 调高亮度
            logging.info('调高亮度')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '调高亮度')
            SeaOfStarsAW.ut_device.swipe(0.145, 0.2, 0.145, 0.088)
            time.sleep(20)
            # 调低亮度
            logging.info('调低亮度')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '调低亮度')
            SeaOfStarsAW.ut_device.swipe(0.145, 0.088, 0.145, 0.2)
            time.sleep(20)
            # 播放下一集
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '播放下一集')
            SeaOfStarsAW.check_status(label='2')
            logging.info('播放下一集')
            SeaOfStarsAW.ut_device(label="2").click()
            time.sleep(20)
            logging.info('第二段trace')
            SeaOfStarsAW.stop_trace()
            step += 1



            # 返回bilibili首页
            logging.info('返回bilibili首页')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '返回bilibili首页')
            SeaOfStarsAW.ut_device.click(0.466, 0.187)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.055, 0.097)
            time.sleep(2)
            SeaOfStarsAW.ut_device(className='XCUIElementTypeButton').click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(className='XCUIElementTypeButton').click()
            time.sleep(2)


            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')