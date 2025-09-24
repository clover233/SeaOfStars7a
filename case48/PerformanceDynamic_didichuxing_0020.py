import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class PerformanceDynamic_didichuxing_0020(Case):
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

            # 1、启动滴滴出行(停留3s)
            logging.info('1、启动滴滴出行')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '启动滴滴出行')
            SeaOfStarsAW.ut_device.session().app_activate('com.xiaojukeji.didi')
            time.sleep(3)

            # 2、点击我的(停留2s)
            logging.info('2、点击我的')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '2、点击我的')
            SeaOfStarsAW.ut_device.click(0.896, 0.935, 0.3)
            time.sleep(2)

            # 3、点击“钱包”（停留2S）
            logging.info('3、点击“钱包”')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '3、点击“钱包”')
            SeaOfStarsAW.ut_device.click(0.123, 0.459, 0.3)
            time.sleep(1)
            # 4、右滑返回上一级页面（2S）
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(2)

            # 5、点击订单后返回(停留2s)
            logging.info('5、点击订单后返回')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '5、点击订单后返回')
            SeaOfStarsAW.ut_device.click(0.126, 0.367, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(2)

            # 6、点击设置后返回(停留2s)
            logging.info('6、点击设置后返回')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '6、点击设置后返回')
            SeaOfStarsAW.ut_device.click(0.905, 0.09, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(2)

            # 7、点击首页，回到首页(停留2s)
            logging.info('7、点击首页，回到首页')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '7、点击首页，回到首页')
            SeaOfStarsAW.ut_device.click(0.097, 0.936, 0.3)
            time.sleep(2)

            # 8、点击特价拼车后返回(停留2s)
            logging.info('8、点击特价拼车后返回')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '8、点击特价拼车后返回')
            SeaOfStarsAW.ut_device.click(0.117, 0.703, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(2)

            # 9、点击火车票机票(停留2s)
            logging.info('9、点击火车票机票')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '9、点击火车票机票')
            SeaOfStarsAW.ut_device.click(0.882, 0.77, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.117, 0.584, 0.3)
            time.sleep(2)

            # 10、浏览火车票机票页面，上滑1次，下1次
            logging.info('10、浏览火车票机票页面，上滑1次，下1次')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '10、浏览火车票机票页面，上滑1次，下1次')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

            # 11、返回首页(停留2s)
            logging.info('11、返回首页')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '11、返回首页')
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(2)

            # 12、点击搜索框(停留2s)
            logging.info('12、点击搜索框')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '12、点击搜索框')
            SeaOfStarsAW.ut_device.click(0.26, 0.504, 0.3)
            time.sleep(2)

            # 13、输入大雁塔北广场南停车场(停留2s)
            logging.info('13、输入大雁塔北广场南停车场')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '13、输入大雁塔北广场南停车场')
            SeaOfStarsAW.ut_device().set_text("大雁塔北广场南停车场")
            time.sleep(2)

            # 14、浏览搜索结果，上滑2次，下2次
            logging.info('14、浏览搜索结果，上滑2次，下2次')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '14、浏览搜索结果，上滑2次，下2次')
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)


            # 15、返回首页
            logging.info('15、返回首页')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '15、返回首页')
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)

            # 16、点击车主(停留2s)
            logging.info('16、点击车主')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '16、点击车主')
            SeaOfStarsAW.ut_device.click(0.297, 0.934, 0.3)
            time.sleep(2)

            # 17、点击特惠洗车并浏览，上滑5次，
            logging.info('17、点击特惠洗车并浏览，上滑5次')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '17、点击特惠洗车并浏览，上滑5次')
            SeaOfStarsAW.ut_device.click(0.859, 0.332, 0.3)
            time.sleep(1)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # 18、点击看车选车并浏览，上滑5次，下5次
            logging.info('18、点击看车选车并浏览，上滑5次，下5次')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '18、点击看车选车并浏览，上滑5次，下5次')
            SeaOfStarsAW.ut_device.click(0.856, 0.404, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.315, 0.801, 0.3)
            time.sleep(1)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(5):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # 19、返回首页
            logging.info('19、返回首页')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '19、返回首页')
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe(0.005, 0.585, 0.999, 0.585, 1.0)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.097, 0.932, 0.3)
            time.sleep(1)

            # 20、返回home界面
            logging.info('20、返回home界面')
            SeaOfStarsAW.trace_thread.add_log('滴滴出行', '返回home界面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.xiaojukeji.didi')
            time.sleep(1)

        logging.info('用例执行结束')