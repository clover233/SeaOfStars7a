import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000006(Case):
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
            # SeaOfStarsAW.ut_device.session().app_activate('tv.danmaku.bilianime')
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
            time.sleep(6) # 广告

            if SeaOfStarsAW.ut_device(label="我知道了").exists:
                SeaOfStarsAW.ut_device(label="我知道了").click()
                time.sleep(2)
            if SeaOfStarsAW.ut_device(label="暂不").exists:
                SeaOfStarsAW.ut_device(label="暂不").click()
                time.sleep(2)

            # 首页--推荐
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '首页--推荐')
            SeaOfStarsAW.check_status(label='推荐')
            logging.info('首页--推荐')
            SeaOfStarsAW.ut_device(label="推荐").click()
            time.sleep(2)

            # 浏览（上滑8次）
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '浏览（上滑8次）')
            logging.info('浏览（上滑8次）')
            for _ in range(8):
                SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.5, 0.3)
                time.sleep(2)

            # 进入热门
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '进入热门')
            logging.info('进入热门')
            SeaOfStarsAW.check_status(label='热门')
            SeaOfStarsAW.ut_device(label="热门").click()
            time.sleep(2)

            # 点击第一个视频播放
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击第一个视频播放')
            logging.info('点击第一个视频播放')
            SeaOfStarsAW.ut_device.click(0.411, 0.457)
            time.sleep(20)

            # 点击视频的up主
            logging.info('点击视频的up主')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '点击视频的up主')
            if SeaOfStarsAW.ut_device(label='创作团队').exists:
                SeaOfStarsAW.ut_device.click(0.207, 0.439)
            else:
                SeaOfStarsAW.ut_device(label='up主头像').click() #一直在变
            time.sleep(2)

            # 浏览up主
            logging.info('浏览up主')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '浏览up主')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe(0.5, 0.7, 0.5, 0.2)
                time.sleep(2)

            # 返回bilibili首页
            logging.info('返回bilibili首页')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '返回bilibili首页')
            SeaOfStarsAW.ut_device.click(0.066, 0.079)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.5, 0.324)
            time.sleep(1)
            SeaOfStarsAW.ut_device(label='返回上一页').click()
            time.sleep(1)


            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('哔哩哔哩', '返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')