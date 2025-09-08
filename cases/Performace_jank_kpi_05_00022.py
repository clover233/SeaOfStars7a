import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000022(Case):
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
            logging.info('应用{}启动'.format("com.xingin.discover"))
            SeaOfStarsAW.trace_thread.add_log('小红书', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate("com.xingin.discover")
            # pos = SeaOfStarsAW.find_app_from_launcher('小红书')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('小红书')
            # pos = SeaOfStarsAW.find_app_from_launcher('小红书')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.156, 0.372)
            # 启动应用等待
            time.sleep(15)

            # step2:进入收藏-视频的链接
            logging.info('进入收藏-视频的链接）')
            SeaOfStarsAW.trace_thread.add_log('小红书', '进入收藏-视频的链接）')
            # 点击搜索框
            SeaOfStarsAW.ut_device.xpath('//*[@label="标签页栏"]/Other[1]/Button[5]').click()
            time.sleep(5)
            # 界面判断
            # SeaOfStarsAW.check_status(label="小红薯65B0EBBB")
            # 输入文本
            SeaOfStarsAW.ut_device(label="收藏").click()
            time.sleep(2)
            # 点击视频链接
            SeaOfStarsAW.ut_device.click(0.749, 0.667)
            time.sleep(2)

            # step3:观看视频，停留10s
            logging.info('观看视频，停留10s')

            time.sleep(10)

            # step4:进入视频专栏，滑动浏览其他视频
            logging.info('观看视频，停留10s')
            SeaOfStarsAW.trace_thread.add_log('小红书', '观看视频，停留10s')
            SeaOfStarsAW.ut_device.xpath('//Window/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/ScrollView[1]/'
                                         'Other[1]/Other[3]/Other[1]/Button[1]').click()
            # 界面判断
            SeaOfStarsAW.check_status(label="收藏")
            SeaOfStarsAW.ut_device.xpath('//*[@label="标签页栏"]/Other[1]/Button[1]').click()
            time.sleep(2)
            # 滑动使tab栏显示
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(label="推荐")
            SeaOfStarsAW.ut_device(label="视频").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # step5：返回home
            logging.info('返回home')
            # 界面判断
            SeaOfStarsAW.trace_thread.add_log('小红书', '返回home')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')