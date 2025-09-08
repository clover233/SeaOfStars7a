import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Taobao_checkgoods(Case):
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

            # 应用启动
            logging.info('应用启动')
            SeaOfStarsAW.trace_thread.add_log('淘宝', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate('com.taobao.taobao4iphone')
            # pos = SeaOfStarsAW.find_app_from_launcher('淘宝')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('淘宝')
            # pos = SeaOfStarsAW.find_app_from_launcher('淘宝')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.388, 0.125)
            time.sleep(2)
            if SeaOfStarsAW.ut_device(label="关闭按钮").exists:
                SeaOfStarsAW.ut_device(label="关闭按钮").click()
                time.sleep(2)
    
            # 搜索清风卫生纸
            logging.info('搜索清风卫生纸')
            SeaOfStarsAW.trace_thread.add_log('淘宝', '搜索清风卫生纸')
            time.sleep(5)
            SeaOfStarsAW.ut_device(label="搜索栏").click()
            time.sleep(5)
            SeaOfStarsAW.ut_device.send_keys('清风卫生纸')
            time.sleep(2)
            SeaOfStarsAW.ut_device(label='搜索').click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')
            # 查看商品详情
            while SeaOfStarsAW.ut_device(labelContains='淘宝买菜').exists or SeaOfStarsAW.ut_device( labelContains='买过的店盒 马进店').exists or SeaOfStarsAW.ut_device(labelContains='km').exists:
                SeaOfStarsAW.ut_device.swipe_up()
            logging.info('查看商品详情')
            SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
                                     self.screenshot_dir_path)
            SeaOfStarsAW.trace_thread.add_log('淘宝', '查看商品详情')
            # while SeaOfStarsAW.ut_device(labelContains='百亿补贴').exists():
            #     SeaOfStarsAW.ut_device.swipe(0.45, 0.8, 0.45, 0.2, duration=0.2)
            SeaOfStarsAW.ut_device.xpath('//CollectionView/Cell[4]').click()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()

            time.sleep(5)

            step += 1
            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('淘宝', '返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)

            SeaOfStarsAW.ut_device.app_terminate('com.taobao.taobao4iphone')
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

            step += 1


            logging.info('用例执行结束')