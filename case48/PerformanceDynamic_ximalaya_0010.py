import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_ximalaya_0010(Case):
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

            app_name ="喜马拉雅"

            step1 = "1、打开喜马拉雅,等待10s"
            logging.info('启动喜马拉雅')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.865, 0.699)
            time.sleep(10)

            step2 = "2、点击分类"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            SeaOfStarsAW.ut_device(labelContains="分类").click()

            step3 = "3、上滑3次 下滑3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)


            step4 = "4、返回首页 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device(label="首页").click()
            time.sleep(1)

            step5 = "5、上滑3次 下滑3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step6 = "6、点击右下角 我的"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device(label="我的").click()

            step7 = "7、点击本地 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device(label="本地").click()
            time.sleep(2)

            step8 = "8、点击 右下角 订阅"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device(label="订阅").click()



            step9 = "9、点击 活着"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            # 需要提前订阅号活着
            SeaOfStarsAW.ut_device.click(0.198,0.617)
            time.sleep(2)

            step10 = "10、点击 进行播放"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            SeaOfStarsAW.ut_device(label="开始播放").click()
            time.sleep(2)

            step11 = "11、点击评论"
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            SeaOfStarsAW.ut_device(label="评论").click()

            step12 = "12、上滑3次 下滑3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step13 = "13、点击 暂停播放"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            SeaOfStarsAW.ut_device(label="暂停").click()
            time.sleep(1)

            step14 = "14、返回首页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step14)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(0.025,0.5, 0.925,0.5)
            SeaOfStarsAW.ut_device(label="首页").click()
            time.sleep(1)

            step15 = "15、点击搜索栏"
            SeaOfStarsAW.trace_thread.add_log(app_name, step15)
            SeaOfStarsAW.ut_device.click(0.332, 0.07)
            time.sleep(1)

            step16 = "16、搜索 活着"
            SeaOfStarsAW.trace_thread.add_log(app_name, step16)
            SeaOfStarsAW.ut_device().set_text("活着")

            step17 = "17、上滑3次 下滑3次 停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step17)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step18 = "18、返回首页 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step18)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe(0.025,0.5, 0.925,0.5)


            step19 = "19、上滑 返回桌面"
            SeaOfStarsAW.trace_thread.add_log(app_name, step19)
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.app_terminate("com.gemd.iting")


        logging.info('用例执行结束')