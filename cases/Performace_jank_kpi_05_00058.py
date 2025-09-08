import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000058(Case):
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
            logging.info('应用{}启动'.format("图库"))
            SeaOfStarsAW.trace_thread.add_log('图库', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate("com.jiangjia.gif")
            SeaOfStarsAW.ut_device(label='照片').click()
            # 启动应用等待
            time.sleep(2)

            # step2:进入所有图片
            logging.info('进入所有图片')
            SeaOfStarsAW.trace_thread.add_log('图库', '进入所有图片')
            # SeaOfStarsAW.ut_device(label='图库').click()
            # SeaOfStarsAW.ut_device(label='全部').click()
            time.sleep(2)

            # 浏览图片缩略图
            SeaOfStarsAW.trace_thread.add_log('图库', '浏览图片缩略图')
            for _ in range(3):
                SeaOfStarsAW.ut_device.swipe(0.5,0.2,0.5,0.8,duration=0.3)
                time.sleep(2)
            # 点击一张图片查看
            SeaOfStarsAW.ut_device.click(0.159, 0.229)
            time.sleep(2)



            # step5：返回主界面，返回home
            logging.info('返回主界面，返回home')
            SeaOfStarsAW.trace_thread.add_log('图库', '返回主界面，返回home')

            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')