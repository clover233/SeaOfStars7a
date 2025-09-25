import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Kuaishou_0010(Case):
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

            # 1、点击进入快手，启动5s，等待2s
            logging.info('启动快手，等待7s')
            SeaOfStarsAW.trace_thread.add_log('快手', '1、浏览视频')
            SeaOfStarsAW.ut_device.session().app_activate('com.jiangjia.gif')
            time.sleep(7)

            # 2、浏览并向下滑切换视频，视频浏览10s，下滑切换下一个，浏览三个
            SeaOfStarsAW.trace_thread.add_log('快手', '2、浏览并向下滑切换视频，视频浏览10s，下滑切换下一个，浏览三个')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(10)

            # 3、点击评论
            SeaOfStarsAW.trace_thread.add_log('快手', '3、点击评论')
            SeaOfStarsAW.ut_device(labelContains="评论").click()
            time.sleep(2)

            # 4、上滑2次，下滑2次
            SeaOfStarsAW.trace_thread.add_log('快手', '4、上滑2次，下滑2次')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="关闭评论区").click()
            time.sleep(2)

            # 5、点击“赞”
            SeaOfStarsAW.trace_thread.add_log('快手', '5、点击“赞”')
            SeaOfStarsAW.ut_device(labelContains="赞").click()
            time.sleep(2)

            # 6、点击“收藏”
            SeaOfStarsAW.trace_thread.add_log('快手', '6、点击“收藏”')
            SeaOfStarsAW.ut_device(labelContains="收藏").click()
            time.sleep(2)

            # 7、点击消息，2s
            SeaOfStarsAW.trace_thread.add_log('快手', '7、点击消息，2s')
            SeaOfStarsAW.ut_device(label="消息").click()
            time.sleep(2)

            # 8、点击测试账号聊天，2s
            SeaOfStarsAW.trace_thread.add_log('快手', '8、点击测试账号聊天，2s')
            SeaOfStarsAW.ut_device(labelContains="测试").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.212, 0.921)
            time.sleep(2)
            SeaOfStarsAW.ut_device.send_keys('AutoTest')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.414, 0.243)
            time.sleep(2)

            # 9、发送华为手机给测试账号
            SeaOfStarsAW.trace_thread.add_log('快手', '9、发送华为手机给测试账号')
            SeaOfStarsAW.ut_device.click(0.287, 0.93)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.301, 0.581)
            time.sleep(2)
            SeaOfStarsAW.ut_device.send_keys('华为手机')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.876, 0.583)
            time.sleep(2)

            # 10、返回快手首页，2s
            SeaOfStarsAW.trace_thread.add_log('快手', '10、返回桌面')
            SeaOfStarsAW.ut_device.click(0.07, 0.101)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)
            SeaOfStarsAW.ut_device(labelContains="精选").click()
            time.sleep(2)

            # 11、返回home界面，2s
            SeaOfStarsAW.trace_thread.add_log('快手', '11、返回home界面，2s')
            SeaOfStarsAW.ut_device.app_terminate('com.jiangjia.gif')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')