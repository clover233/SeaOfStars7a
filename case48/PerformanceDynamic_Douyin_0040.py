import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Douyin_0040(Case):
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

            # 1、点击进入抖音，启动5s，等待2s
            logging.info('点击进入抖音，等待3s')
            SeaOfStarsAW.trace_thread.add_log('抖音', '启动抖音，上下滑动10次')
            SeaOfStarsAW.ut_device.session().app_activate('com.ss.iphone.ugc.Aweme')
            time.sleep(5)

            # 2、上滑10次浏览页推荐视频
            logging.info('2、上滑10次浏览页推荐视频')
            SeaOfStarsAW.trace_thread.add_log('抖音', '2、上滑10次浏览页推荐视频')
            for i in range(10):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 3、下滑10次浏览页推荐视频
            logging.info('3、下滑10次浏览页推荐视频')
            SeaOfStarsAW.trace_thread.add_log('抖音', '3、下滑10次浏览页推荐视频')
            for i in range(10):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 4、搜索胡锡进
            logging.info('4、搜索胡锡进')
            SeaOfStarsAW.trace_thread.add_log('抖音', '搜索胡锡进')
            SeaOfStarsAW.ut_device.click(0.936, 0.086)
            time.sleep(1)
            SeaOfStarsAW.ut_device.send_keys("胡锡进")
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.919, 0.097)
            time.sleep(2)

            # 5、返回首页
            logging.info('5、返回首页')
            SeaOfStarsAW.trace_thread.add_log('抖音', '5、返回首页')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
                time.sleep(2)


            # 6、点击评论按钮
            logging.info('6、点击评论按钮')
            SeaOfStarsAW.trace_thread.add_log('抖音', '6、点击评论按钮')
            SeaOfStarsAW.trace_thread.add_log('抖音', '返回首页，点击评论，输入评论并发送')
            SeaOfStarsAW.ut_device.click(0.931, 0.629)
            time.sleep(1)

            # 7、点击输入框
            logging.info('7、点击输入框')
            SeaOfStarsAW.trace_thread.add_log('抖音', '7、点击输入框')
            SeaOfStarsAW.ut_device.click(0.287, 0.938)
            time.sleep(2)

            # 8、输入"我是评论ABC"
            logging.info('8、输入"我是评论ABC"')
            SeaOfStarsAW.trace_thread.add_log('抖音', '8、输入"我是评论ABC"')
            SeaOfStarsAW.ut_device.send_keys("我是评论ABC")
            time.sleep(2)

            # 9、点击发送
            logging.info('9、点击发送')
            SeaOfStarsAW.trace_thread.add_log('抖音', '9、点击发送')
            SeaOfStarsAW.ut_device.click(0.908, 0.584)
            time.sleep(2)

            # 10、侧滑一次返回
            logging.info('10、侧滑一次返回')
            SeaOfStarsAW.trace_thread.add_log('抖音', '10、侧滑一次返回')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(1)

            # 11、点击点赞按钮
            logging.info('11、点击点赞按钮')
            SeaOfStarsAW.trace_thread.add_log('抖音', '11、点击点赞按钮')
            SeaOfStarsAW.ut_device.click(0.928, 0.555)
            time.sleep(2)

            # 12、点击商城，2s
            SeaOfStarsAW.trace_thread.add_log('抖音', '点击商城，搜索商品，浏览，点击客服，点击店铺')
            SeaOfStarsAW.ut_device.click(0.696, 0.096)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.102, 0.413)
            time.sleep(1)

            # 13、上滑三次浏览推荐商品，2s
            logging.info('13、上滑三次浏览推荐商品')
            SeaOfStarsAW.trace_thread.add_log('抖音', '13、上滑三次浏览推荐商品')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 14、下滑三次浏览推荐商品，2s
            logging.info('14、下滑三次浏览推荐商品')
            SeaOfStarsAW.trace_thread.add_log('抖音', '14、下滑三次浏览推荐商品')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 15、搜索华为P70，2s
            logging.info('15、搜索华为P70')
            SeaOfStarsAW.trace_thread.add_log('抖音', '15、搜索华为P70')
            SeaOfStarsAW.ut_device.click(0.356, 0.093)
            time.sleep(1)
            SeaOfStarsAW.ut_device().set_text("华为P70")
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.922, 0.097)
            time.sleep(2)

            # 16、上滑三次浏览推荐商品，2s
            logging.info('16、上滑三次浏览推荐商品')
            SeaOfStarsAW.trace_thread.add_log('抖音', '16、上滑三次浏览推荐商品')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 17、下滑三次浏览推荐商品，2s
            logging.info('17、下滑三次浏览推荐商品')
            SeaOfStarsAW.trace_thread.add_log('抖音', '17、下滑三次浏览推荐商品')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 18、点击第一个商品，2s
            logging.info('18、点击第一个商品')
            SeaOfStarsAW.trace_thread.add_log('抖音', '18、点击第一个商品')
            SeaOfStarsAW.ut_device.click(0.178, 0.326)
            time.sleep(2)

            # 19、上滑三次浏览推荐商品，2s
            logging.info('19、上滑三次浏览推荐商品')
            SeaOfStarsAW.trace_thread.add_log('抖音', '19、上滑三次浏览推荐商品')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 20、点击左下角客服，2s
            logging.info('20、点击左下角客服')
            SeaOfStarsAW.trace_thread.add_log('抖音', '20、点击左下角客服')
            SeaOfStarsAW.ut_device.click(0.191, 0.924)
            time.sleep(2)

            # 21、返回到商品详情页，2s
            logging.info('21、返回到商品详情页')
            SeaOfStarsAW.trace_thread.add_log('抖音', '21、返回到商品详情页')
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)

            # 22、点击左下角进入店铺，2s
            logging.info('22、点击左下角进入店铺')
            SeaOfStarsAW.trace_thread.add_log('抖音', '22、点击左下角进入店铺')
            SeaOfStarsAW.ut_device.click(0.075, 0.924)
            time.sleep(2)

            # 23、上滑三次浏览推荐商品，2s
            logging.info('23、上滑三次浏览推荐商品')
            SeaOfStarsAW.trace_thread.add_log('抖音', '23、上滑三次浏览推荐商品')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 24、点击首页，返回推荐页面，2s
            SeaOfStarsAW.trace_thread.add_log('抖音', '返回首页，点击精选-团购-关注-推荐')
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
                time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.1, 0.934)
            time.sleep(2)

            # 25、点击长视频，2s
            logging.info('25、点击长视频')
            SeaOfStarsAW.trace_thread.add_log('抖音', '25、点击长视频')
            SeaOfStarsAW.ut_device.click(0.24, 0.097)
            time.sleep(2)

            # 26、向左滑动，依次切换顶部tab页（长视频-关注-商城-推荐），循环3次
            logging.info('26、向左滑动，依次切换顶部tab页')
            SeaOfStarsAW.trace_thread.add_log('抖音', '26、向左滑动，依次切换顶部tab页')
            for i in range(3):
                SeaOfStarsAW.ut_device.click(0.521, 0.097)
                time.sleep(2)
                SeaOfStarsAW.ut_device.click(0.722, 0.094)
                time.sleep(2)
                SeaOfStarsAW.ut_device.click(0.81, 0.097)
                time.sleep(2)

            # 27、返回home页，等待2s
            SeaOfStarsAW.ut_device.app_terminate('com.ss.iphone.ugc.Aweme')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()
            SeaOfStarsAW.stop_trace()

        logging.info('用例执行结束')
