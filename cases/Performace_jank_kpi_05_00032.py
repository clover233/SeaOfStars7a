import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000032(Case):
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
            logging.info('应用{}启动'.format("com.tencent.live4iphone"))
            SeaOfStarsAW.trace_thread.add_log('腾讯视频', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate("com.tencent.live4iphone")
            # pos = SeaOfStarsAW.find_app_from_launcher('腾讯视频')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('腾讯视频')
            # pos = SeaOfStarsAW.find_app_from_launcher('腾讯视频')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.386, 0.486)

            # 启动应用等待
            time.sleep(15)
            if SeaOfStarsAW.ut_device(label="pr float close").exists:
                SeaOfStarsAW.ut_device(label="pr float close").click()
                time.sleep(2)

            # step2:搜索视频“大话西游”，重复搜索7次
            logging.info('搜索视频“大话西游”')
            SeaOfStarsAW.trace_thread.add_log('腾讯视频', '搜索视频“大话西游”')
            SeaOfStarsAW.check_status(label="首页", name="首页")

            for i in range(0, 7):
                # 点击搜索框
                SeaOfStarsAW.ut_device.click(0.643, 0.09)
                time.sleep(2)
                # 界面判断
                # SeaOfStarsAW.check_status(label="历史")
                # time.sleep(2)
                # 输入“大话西游”，点击搜索
                SeaOfStarsAW.ut_device.xpath('//*[@label=""]').set_text("大话西游")
                time.sleep(2)
                SeaOfStarsAW.ut_device(label="搜索").click()
                time.sleep(2)
                # 界面判断
                # SeaOfStarsAW.check_status(label="全部")
                # time.sleep(2)
                if i in range(0, 6):
                    SeaOfStarsAW.ut_device(label="取消", name="取消").click()
                    time.sleep(2)
                    # 界面判断
                    # SeaOfStarsAW.check_status(label="历史")
                    # time.sleep(2)
                    SeaOfStarsAW.ut_device(label="取消", name="取消").click()
                    time.sleep(2)
            SeaOfStarsAW.stop_trace()
            step += 1
            # step3:点击电影播放
            logging.info('点击电影播放')
            SeaOfStarsAW.trace_thread.add_log('腾讯视频', '点击电影播放')
            SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
                                     self.screenshot_dir_path)
            # 点击电影
            SeaOfStarsAW.ut_device(label='大话西游：至尊宝 至尊宝为紫霞大战牛魔王').click()
            time.sleep(2)
            # 界面判断
            # SeaOfStarsAW.check_status(label="西游题材")
            time.sleep(80)

            # step4：返回主界面
            logging.info('返回主界面')
            SeaOfStarsAW.trace_thread.add_log('腾讯视频', '返回主界面')
            # 点击返回
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="取消", name="取消").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="取消", name="取消").click()
            time.sleep(2)
            # 界面判断
            # SeaOfStarsAW.check_status(label="TAB首页")
            # time.sleep(2)

            # step5：返回home
            logging.info('返回home')

            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')