import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_fanqie_0010(Case):
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
            # todo 后续放开log
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)

            # 1、启动番茄小说，3s
            logging.info('启动番茄小说，3s')
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '浏览主页')
            # todo 微博的坐标地址要改下
            SeaOfStarsAW.ut_device.click(0.383, 0.127)
            time.sleep(5)

            # 2、主页浏览，上滑5次，下滑5次，每次停留2s
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            SeaOfStarsAW.trace_thread.add_log('番茄小说', '查看书架书籍')
            # 3、点击书架，停留1s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

            # 4、点击书籍进行阅读，停留1s
            SeaOfStarsAW.ut_device(labelContains="热点").click()
            time.sleep(1)
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '阅读书籍')
            # 5、阅读书籍，向左翻页5次，向右翻页5次，停留3s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

            # 6、重复操作4、5步骤两次
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)
            # 7、返回首页，停留1s
            SeaOfStarsAW.ut_device(labelContains="抖音热榜，完整热榜").click()
            time.sleep(1)
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '查看浏览历史')
            # 8、点击“我的”，停留1s
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(1)
            # 9、点击浏览历史，停留2s
            SeaOfStarsAW.ut_device(labelContains="返回按钮").click()
            time.sleep(2)

            # 10、返回首页，停留1s
            SeaOfStarsAW.ut_device(labelContains="直播").click()
            time.sleep(1)
            SeaOfStarsAW.trace_thread.add_log('番茄小说', '返回home界面')
            # 11、返回home界面，停留1s
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)

            # 12、点击长视频，停留1s
            SeaOfStarsAW.ut_device(labelContains="精选").click()
            time.sleep(1)

            # 13、上滑3次，下滑3次，停留1s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

            # 14、点击+号，停留1s
            SeaOfStarsAW.ut_device.click(0.5, 0.938)
            time.sleep(1)
            # 15、点击相册，停留1s
            SeaOfStarsAW.ut_device(labelContains="相册").click()
            time.sleep(1)
            # 16、上滑三次下滑三次，停留1s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)
            # 17、返回上一层，停留1s
            SeaOfStarsAW.ut_device(labelContains="关闭相册").click()
            time.sleep(1)
            # 18、点击选择音乐，停留1s
            SeaOfStarsAW.ut_device(labelContains="选择音乐").click()
            time.sleep(1)

            # 19、向上滑动6次，停留1s
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(2)

            # 20、返回首页，停留1s
            SeaOfStarsAW.ut_device.swipe(0.496, 0.49, 0.482, 0.916, 0.5)
            time.sleep(1)
            SeaOfStarsAW.ut_device(labelContains="关闭").click()
            time.sleep(1)

            # 21、点击我，停留1s
            SeaOfStarsAW.ut_device(labelContains="我").click()
            time.sleep(1)

            # 22、点击收藏，停留1s
            SeaOfStarsAW.ut_device(labelContains="收藏").click()
            time.sleep(1)

            # 23、点击第一个收藏的作品，停留1s
            SeaOfStarsAW.ut_device.click(0.143, 0.667)
            time.sleep(1)

            # 24、向上滑动三次浏览，停留1s
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)

            # 25、返回我页面，停留1s
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)

            # 26、点击我的钱包，停留1s
            SeaOfStarsAW.ut_device.click(0.356, 0.414)
            time.sleep(1)
            # 27、返回首页，停留1s
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)
            SeaOfStarsAW.ut_device(labelContains="首页").click()
            # 28、退出抖音

            SeaOfStarsAW.ut_device.home()
            time.sleep(2)



        logging.info('用例执行结束')