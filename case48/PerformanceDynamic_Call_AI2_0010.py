import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Call_AI2_0010(Case):
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

            # 1. 进入电话 停留1s
            logging.info('应用启动')
            SeaOfStarsAW.trace_thread.add_log('电话', '应用启动')
            SeaOfStarsAW.ut_device.session().app_activate('com.apple.mobilephone')


            # 2.点击屏幕底部"联系人"(2s, 停留1s)

            # 3.浏览联系人(上下滑动各5次, 2s, 停留1s)

            # 4.点击搜索框

            # 5.输入atest, 点击第一条搜索记录，进入详情页面，停留2s

            # 6.左滑返回联系人界面停留1s

            # 7.上下滑动5次停留1s

            # 8.给"atest"联系人拨打电话

            # 9.返回电话首页面

            # 10.上滑返回Home界面(2s停留2s)

            # 11.打开淘宝浏览

            # 12.淘宝首页滑动

            # 13.退出淘宝

            # 14.打开抖音浏览

            # 15.抖音首页滑动

            # 16.退出抖音

            # 17.打开微博浏览

            # 18.微博首页浏览

            # 19.退出微博

            # 20.打开京东浏览

            # 21.京东首页浏览

            # 22.点击底部直播，等待2s

            # 23.浏览直播页面，上滑2次，下滑2次，每次停留2s

            # 24.点击第一个直播间进入，等待2s

            # 25.返回主页面，等待2s

            # 26.退出京东

            # 27.打开美团浏览

            # 28.美团首页浏览

            # 29.首页点击外卖（停留1s）

            # 30.点击美食（停留1s）

            # 31.点击搜索框（停留1s）

            # 32.输入黄焖鸡（停留1s）

            # 33.点击搜索（停留1s）

            # 34.滑动浏览（上滑2次，下滑2次，每次停留2s）

            # 35.返回美团首页（停留1s）

            # 36.退出美团


        logging.info('用例执行结束')