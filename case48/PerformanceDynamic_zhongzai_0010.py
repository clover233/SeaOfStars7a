import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_zhongzai_0010(Case):
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
            app_name ="重载"

            step1 = "'1、打开qq音乐,等待10s'"
            logging.info('启动qq音乐')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.847, 0.135)
            time.sleep(10)

            step2 = "2、浏览首页 上滑2次 下滑2次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step3 = "3、点击第一个音乐卡片 进行播放  停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            SeaOfStarsAW.ut_device.click(0.552, 0.794)
            time.sleep(1)

            step4 = "4、上滑qq音乐进入后台 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step5 = "5、启动高德地图 停留3s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.click(0.602, 0.128)
            time.sleep(3)

            step6 = "6、点击搜索框 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device.click(0.656, 0.623)
            time.sleep(1)

            step7 = "7、输入 西安北站 并搜索 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device().set_text("西安北站")

            time.sleep(1)

            step8 = "8、点击第一个结果 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device(label="西安北站").click()
            time.sleep(1)

            step9 = "9、点击 开始导航 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            SeaOfStarsAW.ut_device.click(0.648, 0.927)
            time.sleep(10)
            time.sleep(1)

            step10 = "10、上滑 将高德放入后台 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step11 = "11、打开相机 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            SeaOfStarsAW.ut_device.click(0.832, 0.92)
            time.sleep(2)

            step12 = "12、连续拍摄5次 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            for i in range(5):
                SeaOfStarsAW.ut_device(label="拍照").click()
            time.sleep(1)

            step13 = "13、打开缩略图 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            SeaOfStarsAW.ut_device(label="照片与视频显示器").click()
            time.sleep(1)

            step14 = "14、向左滑动6次 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step14)
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(1)

            step15 = "15、返回相机拍摄页面 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step15)
            SeaOfStarsAW.ut_device(label="首页").click()
            SeaOfStarsAW.ut_device.click(0.068, 0.083)
            time.sleep(1)

            step16 = "16、退出相机 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step16)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step17 = "17、打开爱奇艺 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step17)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.85, 0.144)
            time.sleep(10)

            step18 = "18、向上滑动8次 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step18)
            for i in range(8):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)

            step19 = "19、向下滑动8次 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step19)
            for i in range(8):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

            step20 = "20、退出爱奇艺 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step20)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step21 = "21、打开优酷视频 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step21)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.388, 0.144)
            time.sleep(10)

            step22 = "22、向上滑动8次 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step22)
            for i in range(8):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)

            step23 = "23、向下滑动8次 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step23)
            for i in range(8):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

            step24 = "24、退出优酷视频 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step24)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step25 = "25、启动高德导航 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step25)
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.click(0.602, 0.128)
            time.sleep(1)

            step26 = "26、退出高德 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step26)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step27 = "27、启动qq音乐 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step27)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.847, 0.135)
            time.sleep(8)

            step28 = "28、点击暂停 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step28)
            SeaOfStarsAW.ut_device(label="播放").click()
            time.sleep(1)

            step29 = "29、返回首页 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step29)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step30 = "30、退出qq音乐 停留1s、"
            SeaOfStarsAW.trace_thread.add_log(app_name, step30)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(1)
            SeaOfStarsAW.ut_device.app_terminate("com.autonavi.amap")
            SeaOfStarsAW.ut_device.app_terminate("com.tencent.QQMusic")
            SeaOfStarsAW.ut_device.app_terminate("com.qiyi.iphone")
            SeaOfStarsAW.ut_device.app_terminate("com.youku.YouKu")


        logging.info('用例执行结束')