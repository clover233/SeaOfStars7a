import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000024(Case):
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
        # 清空后台


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

            # step1:应用启动
            logging.info('应用{}启动'.format("com.ss.iphone.article.News"))
            # SeaOfStarsAW.ut_device.session().app_activate("com.ss.iphone.article.News")
            # pos = SeaOfStarsAW.find_app_from_launcher('今日头条')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('今日头条')
            # pos = SeaOfStarsAW.find_app_from_launcher('今日头条')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.61, 0.374)

            # 启动应用等待
            time.sleep(15)

            # step2:点击视频-推荐
            logging.info('点击视频-推荐')
            SeaOfStarsAW.check_status(name="topbar_search_icon")

            # 点击视频
            SeaOfStarsAW.ut_device.click(0.29, 0.922)
            time.sleep(5)
            SeaOfStarsAW.check_status(label="分享")
            # 点击推荐
            SeaOfStarsAW.ut_device(label="推荐").click()
            time.sleep(2)

            # step3:自动播放第一条视频
            logging.info('自动播放第一条视频')

            time.sleep(10)

            # step4：返回头条首页，返回home
            logging.info('返回头条首页，返回home')

            SeaOfStarsAW.ut_device(label="头条").click()
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(name="topbar_search_icon")
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')