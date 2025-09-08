import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000026(Case):
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

            # step2:主页面-发现
            logging.info('进入主页面-发现')
            SeaOfStarsAW.trace_thread.add_log('微博', '进入主页面-发现')
            SeaOfStarsAW.check_status(label="关注", name="关注")
            SeaOfStarsAW.trace_thread.add_log('微博', '应用启动')
            # 点击“发现”
            SeaOfStarsAW.ut_device.xpath('//*[@label="标签页栏"]/Other[1]/Button[3]').click()
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(label="热点")
            if SeaOfStarsAW.ut_device(label="残忍离开").exists:
                SeaOfStarsAW.ut_device(label="残忍离开").click()

            # step3:搜索栏输入“新华社”
            logging.info('搜索栏输入“新华社”')
            SeaOfStarsAW.trace_thread.add_log('微博', '搜索栏输入“新华社”')

            # 点击搜索框
            SeaOfStarsAW.ut_device.click(0.444, 0.083)
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(name="WBSearchBar")
            SeaOfStarsAW.ut_device(name="WBSearchBar").set_text("新华社")
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.226, 0.13)
            time.sleep(2)

            # step4：点击第一条微博正文
            logging.info('点击第一条微博正文')
            SeaOfStarsAW.trace_thread.add_log('微博', '点击第一条微博正文')
            # 点击搜索联想页第一条内容
            SeaOfStarsAW.ut_device.click(0.39, 0.322)
            time.sleep(2)
            # 界面判断
            # SeaOfStarsAW.check_status(label="搜索")
            # 点击第一条微博正文
            # SeaOfStarsAW.ut_device.click(0.472, 0.343)
            # SeaOfStarsAW.ut_device.click(0.869, 0.402)
            # time.sleep(2)
            # 界面判断
            # SeaOfStarsAW.check_status(label="微博正文")

            # step5：浏览正文，上滑一次
            logging.info('浏览正文，上滑一次')
            SeaOfStarsAW.trace_thread.add_log('微博', '浏览正文，上滑一次')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(5)

            # step6：返回上一页面
            logging.info('返回上一页面')
            SeaOfStarsAW.trace_thread.add_log('微博', '返回上一页面')
            SeaOfStarsAW.ut_device.click(0.051, 0.09)
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(name="WBSearchBar")

            # step7：上滑1次
            logging.info('上滑一次')
            SeaOfStarsAW.trace_thread.add_log('微博', '上滑一次')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # step8：返回微博首页，返回home
            logging.info('返回微博首页，返回home')
            SeaOfStarsAW.trace_thread.add_log('微博', '返回微博首页，返回home')
            # 点击返回
            SeaOfStarsAW.ut_device(label="searchbar back withtext").click()
            time.sleep(2)
            # 点击取消
            SeaOfStarsAW.ut_device(label="取消").click()
            time.sleep(2)

            # 界面判断
            # SeaOfStarsAW.check_status(label="热点")
            # 点击微博首页lab
            SeaOfStarsAW.ut_device(label="微博").click()
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(label="关注", name="关注")
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')