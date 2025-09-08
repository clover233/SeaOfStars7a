import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000027(Case):
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
            # 启动百度
            logging.info('启动百度')
            # SeaOfStarsAW.ut_device.session().app_activate('com.baidu.BaiduMobile')
            pos = SeaOfStarsAW.find_app_from_launcher('百度')
            while str(pos) == ('Point(x=0, y=0)'):
                SeaOfStarsAW.ut_device.swipe_left()
                pos = SeaOfStarsAW.find_app_from_launcher('百度')
            pos = SeaOfStarsAW.find_app_from_launcher('百度')
            SeaOfStarsAW.click_pos_from_launcher(pos)
            time.sleep(2)

            # 浏览新闻
            logging.info('浏览新闻')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.5, 0.3)
                time.sleep(2)

            # 搜索爱国
            logging.info('搜索爱国')
            SeaOfStarsAW.ut_device.click(0.42, 0.13)
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="请输入搜索关键词").set_text('爱国')
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="搜索").click()
            time.sleep(2)

            # 点击查看第一条结果
            logging.info('点击查看第一条结果')
            SeaOfStarsAW.ut_device.click(0.213, 0.258)
            time.sleep(2)

            # 浏览图文信息
            logging.info('浏览图文信息')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.5, 0.3)
                time.sleep(2)

            # 分享给微信好友
            logging.info('分享给微信好友')
            if SeaOfStarsAW.ut_device(label="菜单").exists:
                SeaOfStarsAW.ut_device(label="菜单").click()
                time.sleep(2)
            else:
                SeaOfStarsAW.ut_device.swipe(0.5, 0.4, 0.5, 0.6)
                time.sleep(2)
                SeaOfStarsAW.ut_device.click(0.929, 0.083)
                time.sleep(2)
            SeaOfStarsAW.ut_device(label="分享").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="微信好友").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.325, 0.562)
            time.sleep(2)

            # 分享给第一个好友
            logging.info('分享给第一个好友')
            SeaOfStarsAW.ut_device(label="测试群聊1").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="发送").click()
            time.sleep(2)


            # 返回百度搜索页面
            logging.info('返回百度搜索页面')
            SeaOfStarsAW.ut_device(labelContains="返回百度").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0.1, 0.5, 0.9, 0.5)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.13, 0.929)
            time.sleep(2)
            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')