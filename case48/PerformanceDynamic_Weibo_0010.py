import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Weibo_0010(Case):
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

            # 1、启动微博
            logging.info('启动微博')
            SeaOfStarsAW.trace_thread.add_log('微博', '1、打开微博,等待3s')
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.155, 0.6)
            time.sleep(10)

            # 2、点击发现，等待1s
            SeaOfStarsAW.trace_thread.add_log('微博', '2、点击发现，等待1s')
            SeaOfStarsAW.ut_device.click(0.507, 0.942)
            time.sleep(1)

            # 3、点击搜索栏、输入"我和我的祖国视频" 并搜索 等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '3、点击搜索栏、输入"我和我的祖国视频" 并搜索 等待2s')
            SeaOfStarsAW.ut_device.click(0.391, 0.087)
            SeaOfStarsAW.ut_device.send_keys("我和我的祖国视频")
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(2)
            # 4、上滑5次，下滑6次，等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '4、上滑5次，下滑6次，等待2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 5、点击第一条博文视频播放5s
            SeaOfStarsAW.trace_thread.add_log('微博', '5、点击第一条博文视频播放5s')
            SeaOfStarsAW.ut_device(labelContains="正文").click()
            time.sleep(5)

            # 6、返回，等待1s
            SeaOfStarsAW.trace_thread.add_log('微博', '6、左滑返回，等待1s')
            SeaOfStarsAW.ut_device.click(0.05, 0.085)
            time.sleep(1)

            # 7、点击评论，等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '7、点击评论，等待2s')
            SeaOfStarsAW.ut_device.swipe_up()
            SeaOfStarsAW.ut_device(labelContains="评论").click()
            time.sleep(2)
            # 8、上滑5次、下滑6次，等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '8、上滑5次，下滑6次，等待2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)
            # 9、左滑4次返回 发现页
            SeaOfStarsAW.trace_thread.add_log('微博', '9、左滑4次返回 发现页')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_right()
            # 10、点击搜索栏、输入 九宫格图片 并搜索 等待3s
            SeaOfStarsAW.trace_thread.add_log('微博', '10、点击搜索栏、输入 九宫格图片 并搜索 等待3s')
            SeaOfStarsAW.ut_device.click(0.391, 0.087)
            SeaOfStarsAW.ut_device().set_text("九宫格图片")
            SeaOfStarsAW.ut_device(labelContains="搜索").click()
            time.sleep(3)

            # 11、上滑5次、下滑6次，等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '11、上滑5次，下滑6次，等待2s')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)
            # 12、点击第一条博文的第一张图片 查看大图，等待1s
            SeaOfStarsAW.trace_thread.add_log('微博', '12、点击第一条博文的第一张图片 查看大图，等待1s')
            SeaOfStarsAW.ut_device.click(0.459, 0.463)
            time.sleep(1)

            # 13、屏幕中间左滑5次，依次查看5张照片
            SeaOfStarsAW.trace_thread.add_log('微博', '13、屏幕中间左滑5次，依次查看5张照片')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_left()
                time.sleep(1)

            # 14、返回微博正文，等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '14、返回微博正文，等待2s')
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(2)

            # 15、左滑3次，返回页面
            SeaOfStarsAW.trace_thread.add_log('微博', '15、左滑3次，返回页面')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_right()
            # 16、上滑返回到home 等待2s
            SeaOfStarsAW.trace_thread.add_log('微博', '16、上滑返回到home 等待2s')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.app_terminate("com.sina.weibo")
            time.sleep(2)

            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')