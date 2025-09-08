import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000029(Case):
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
            logging.info('应用{}启动'.format("com.qiyi.iphone"))
            SeaOfStarsAW.trace_thread.add_log('爱奇艺', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate("com.qiyi.iphone")
            # pos = SeaOfStarsAW.find_app_from_launcher('爱奇艺')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('爱奇艺')
            # pos = SeaOfStarsAW.find_app_from_launcher('爱奇艺')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.15, 0.491)
            # 启动应用等待
            time.sleep(15)

            # step2:搜索视频“大话天仙”，重复搜索7次
            logging.info('搜索视频“大话天仙”')
            SeaOfStarsAW.trace_thread.add_log('爱奇艺', '搜索视频“大话天仙”，重复搜索7次')
            SeaOfStarsAW.check_status(label="直播")
            for i in range(0, 7):
                # 点击搜索框
                SeaOfStarsAW.ut_device(label="搜索框").click()
                time.sleep(2)
                # 界面判断
                # SeaOfStarsAW.check_status(label="语音搜索")
                # 输入“大话天仙”，点击搜索
                SeaOfStarsAW.ut_device(label="搜索框").set_text("大话天仙")
                time.sleep(2)
                SeaOfStarsAW.ut_device(label="搜索").click()
                time.sleep(2)
                # 界面判断
                SeaOfStarsAW.check_status(label="下载")
                if i in range(0, 6):
                    SeaOfStarsAW.ut_device.click(0.065, 0.093)
                    time.sleep(3)
                    SeaOfStarsAW.ut_device.click(0.065, 0.093)
                    time.sleep(3)
                    # 界面判断
                    SeaOfStarsAW.check_status(label="直播")

            # step3:点击电影播放,停留80s
            logging.info('点击电影播放')
            SeaOfStarsAW.trace_thread.add_log('微博', '点击电影播放')
            # 点击电影
            if SeaOfStarsAW.ut_device(label='立即播放').exists:
                SeaOfStarsAW.ut_device(label='立即播放').click()
                time.sleep(2)
            else:
                SeaOfStarsAW.ut_device(label='继续播放').click()
                time.sleep(2)
            # 界面判断     
            # SeaOfStarsAW.check_status(label="猜你喜欢")
            time.sleep(80)

            # step4：返回主界面
            logging.info('返回主界面')
            SeaOfStarsAW.trace_thread.add_log('微博', '返回主界面')
            # 点击返回
            for _ in range(0, 3):
                SeaOfStarsAW.ut_device.click(0.059, 0.09)
                time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(label="直播")

            # step5：返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('微博', '返回home')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')