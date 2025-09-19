import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_Beiwanglu_0010(Case):
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

            # 1、启动备忘录
            logging.info('启动备忘录')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '启动备忘录')
            SeaOfStarsAW.ut_device.session().app_activate('com.apple.mobilenotes')
            time.sleep(1)

            # 2、点击右下角新建图标
            logging.info('点击右下角新建图标')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '点击右下角新建图标')
            SeaOfStarsAW.ut_device.click(0.928, 0.935, 0.3)
            time.sleep(1)

            # 3、输入“动态”并点击保存
            logging.info('输入“动态”并点击保存')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '输入“动态”并点击保存')
            SeaOfStarsAW.ut_device().set_text("动态")
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.914, 0.089, 0.3)
            time.sleep(1)

            # 4、返回主界面
            logging.info('返回主界面')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '返回主界面')
            SeaOfStarsAW.ut_device.click(0.108, 0.088, 0.3)
            time.sleep(1)

            # 5、点击屏幕底部待办，切换到待办页
            logging.info('点击屏幕底部待办，切换到待办页')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '点击屏幕底部待办，切换到待办页')
            SeaOfStarsAW.ut_device.click(0.928, 0.935, 0.3)
            time.sleep(1)
            SeaOfStarsAW.ut_device.click(0.306, 0.579, 0.3)
            time.sleep(1)

            # 6、点击新建按钮，拉起小艺输入法
            logging.info('点击新建按钮，拉起小艺输入法')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '点击新建按钮，拉起小艺输入法')
            SeaOfStarsAW.ut_device().set_text("test")
            time.sleep(1)

            # 7、26键盘输入“test”，点击键盘上的回车按钮
            logging.info('26键盘输入“test”，点击键盘上的回车按钮')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '26键盘输入“test”，点击键盘上的回车按钮')
            SeaOfStarsAW.ut_device.click(0.876, 0.884, 0.3)
            time.sleep(1)

            # 8、点击保存按钮
            logging.info('点击屏幕底部“笔记”返回主界面')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '点击屏幕底部“笔记”返回主界面')
            SeaOfStarsAW.ut_device.click(0.914, 0.089, 0.3)
            time.sleep(1)

            # 9、点击屏幕底部“笔记”返回主界面
            logging.info('点击屏幕底部“笔记”返回主界面')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '点击屏幕底部“笔记”返回主界面')
            SeaOfStarsAW.ut_device.swipe(0.010, 0.809, 0.933, 0.805, 0.5)
            time.sleep(2)

            # 10、上滑返回桌面
            logging.info('上滑返回桌面')
            SeaOfStarsAW.trace_thread.add_log('备忘录', '上滑返回桌面')
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.ut_device.app_terminate('com.apple.mobilenotes')
            time.sleep(2)

        logging.info('用例执行结束')