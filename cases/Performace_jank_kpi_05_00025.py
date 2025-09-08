import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000025(Case):
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
            logging.info('应用{}启动'.format("com.sina.weibo"))
            SeaOfStarsAW.trace_thread.add_log('微博', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate("com.sina.weibo")
            # pos = SeaOfStarsAW.find_app_from_launcher('微博')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('微博')
            # pos = SeaOfStarsAW.find_app_from_launcher('微博')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.15, 0.491)

            # 启动应用等待
            time.sleep(15)
            if SeaOfStarsAW.ut_device(label="连续签到3天，可赚连签奖0.05元").exists:
                SeaOfStarsAW.ut_device.click(0.501, 0.781)

            # step2:进入“我的”
            logging.info('进入“我的”')
            SeaOfStarsAW.trace_thread.add_log('微博', '进入“我的”')
            SeaOfStarsAW.check_status(label="关注", name="关注")

            # 点击“我”
            SeaOfStarsAW.ut_device.click(0.894, 0.933)
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(label="navigationbar icon setting v2")

            # step3:点击“赞/收藏”
            logging.info('点击“赞/收藏”')
            SeaOfStarsAW.trace_thread.add_log('微博', '点击“赞/收藏”')
            SeaOfStarsAW.ut_device.xpath('//CollectionView/Cell[6]/Other[1]/Other[1]/Other[1]').click()
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(label="我的赞", name="WBNavigationTitleView")

            # step4：点击第一条查看图片，左滑三次
            logging.info('点击第一条查看图片，左滑三次')
            SeaOfStarsAW.trace_thread.add_log('微博', '点击第一条查看图片，左滑三次')
            SeaOfStarsAW.ut_device.click(0.168, 0.548)
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(label="太酷了")
            # 左滑三次
            for i in range(0, 3):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(2)

            # step5：返回微博首页，返回home
            logging.info('返回微博首页，返回home')
            SeaOfStarsAW.trace_thread.add_log('微博', '返回微博首页，返回home')
            SeaOfStarsAW.ut_device.click(0.509, 0.413)
            time.sleep(2)
            SeaOfStarsAW.check_status(label="我的赞", name="WBNavigationTitleView")
            SeaOfStarsAW.ut_device(label="返回", name="返回").click()
            time.sleep(2)
            SeaOfStarsAW.check_status(label="navigationbar icon addfriends ")
            SeaOfStarsAW.ut_device.xpath('//*[@label="标签页栏"]/Other[1]/Button[1]').click()
            time.sleep(2)
            SeaOfStarsAW.check_status(label="关注", name="关注")
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')