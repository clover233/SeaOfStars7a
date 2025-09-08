import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000050(Case):
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
            # 应用启动
            logging.info('应用启动')
            SeaOfStarsAW.trace_thread.add_log('相机', '应用启动')
            SeaOfStarsAW.ut_device(label="相机").click() #相机app无法获取包名
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="弱光").click()


            # 点击屏幕中间，拍摄照片
            logging.info('点击屏幕中间，拍摄照片')
            SeaOfStarsAW.trace_thread.add_log('相机', '点击屏幕中间，拍摄照片')
            SeaOfStarsAW.ut_device.click(0.5, 0.878)
            time.sleep(2)

            # 点击左下方缩略图查看图片
            logging.info('点击左下方缩略图查看图片')
            SeaOfStarsAW.trace_thread.add_log('相机', '点击左下方缩略图查看图片')
            # iphone 15
            # SeaOfStarsAW.ut_device(label="照片与视频显示器").click()
            SeaOfStarsAW.ut_device(label="照片与视频检视器").click()
            time.sleep(2)
            # 左滑一次查看其他图片
            logging.info('左滑一次查看其他图片')
            SeaOfStarsAW.trace_thread.add_log('相机', '左滑一次查看其他图片')
            SeaOfStarsAW.ut_device.swipe_right()
            time.sleep(2)
            # 返回相机
            logging.info('返回相机')
            SeaOfStarsAW.trace_thread.add_log('相机', '返回相机')
            # SeaOfStarsAW.ut_device(name="BackButton").click()
            SeaOfStarsAW.ut_device(label="关闭").click()
            time.sleep(2)
            # 点击视频
            logging.info('点击视频')
            SeaOfStarsAW.trace_thread.add_log('相机', '点击视频')
            SeaOfStarsAW.ut_device.click(0.368, 0.806)
            time.sleep(2)
            # 点击录像
            logging.info('点击录像')
            SeaOfStarsAW.trace_thread.add_log('相机', '点击录像')
            SeaOfStarsAW.ut_device.click(0.5, 0.878)
            time.sleep(10)
            # 结束录像
            logging.info('点击录像')
            SeaOfStarsAW.trace_thread.add_log('相机', '点击录像')
            SeaOfStarsAW.ut_device.click(0.5, 0.878)
            time.sleep(4)
            # 点击左下角查看视频
            logging.info('点击左下角查看视频')
            SeaOfStarsAW.trace_thread.add_log('相机', '点击左下角查看视频')
            # SeaOfStarsAW.ut_device(label="照片与视频显示器").click()
            SeaOfStarsAW.ut_device(label="照片与视频检视器").click()
            # 等待视频播放
            time.sleep(10)
            # 返回相机
            logging.info('返回相机')
            SeaOfStarsAW.trace_thread.add_log('相机', '返回相机')
            # SeaOfStarsAW.ut_device(name="BackButton").click()
            SeaOfStarsAW.ut_device(label="关闭").click()
            time.sleep(2)
            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('相机', '返回home')
            SeaOfStarsAW.ut_device.click(0.638, 0.803)
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')