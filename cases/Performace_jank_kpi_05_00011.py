import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000011(Case):
    all_app_package_list = ['']
    TEST_TIME = 2

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
            # 启动京东
            logging.info('启动京东')
            SeaOfStarsAW.trace_thread.add_log('京东', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate("com.360buy.jdmobile")
            # pos = SeaOfStarsAW.find_app_from_launcher('京东')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('京东')
            # pos = SeaOfStarsAW.find_app_from_launcher('京东')
            # SeaOfStarsAW.click_pos_from_launcher(pos)

            SeaOfStarsAW.ut_device.click(0.849, 0.6)
            time.sleep(5)
            if SeaOfStarsAW.ut_device(label="关闭按钮").exists:
                SeaOfStarsAW.ut_device(label="关闭按钮").click()
                time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
            #         '%H%M%S', time.localtime()) + '.png')

            # 首页—搜索"华为新款手机"
            logging.info('首页-搜索华为新款手机')
            SeaOfStarsAW.trace_thread.add_log('京东', '首页-搜索华为新款手机')
            SeaOfStarsAW.check_status(label="拍照购")
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.411, 0.13)
            time.sleep(2)
            SeaOfStarsAW.ut_device.xpath('//SearchField').set_text('华为新款手机')
            time.sleep(2)
            SeaOfStarsAW.check_status(label="搜索")
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="搜索").click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
            #         '%H%M%S', time.localtime()) + '.png')

            # 浏览商品
            logging.info('浏览商品')
            SeaOfStarsAW.trace_thread.add_log('京东', '浏览商品')
            SeaOfStarsAW.check_status(xpath='//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/CollectionView[1]/Other[1]/Other[1]/Other[1]/CollectionView[1]/Cell[1]')
            time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.5, 0.2)
                time.sleep(2)
                step += 1
                # SeaOfStarsAW.ut_device.screenshot(
                #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(
                #         step) + '_' + time.strftime('%H%M%S', time.localtime()) + '.png')

            # 点击查看商品详情
            logging.info('点击查看商品详情')
            SeaOfStarsAW.trace_thread.add_log('京东', '点击查看商品详情')
            SeaOfStarsAW.ut_device.click(0.242, 0.856)
            time.sleep(3)
            SeaOfStarsAW.check_status(label="购物车")
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
            #         '%H%M%S', time.localtime()) + '.png')

            # 浏览商品详情
            logging.info('浏览商品详情')
            SeaOfStarsAW.trace_thread.add_log('京东', '浏览商品详情')
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.5, 0.2)
                time.sleep(2)
                step += 1
                # SeaOfStarsAW.ut_device.screenshot(
                #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(
                #         step) + '_' + time.strftime('%H%M%S', time.localtime()) + '.png')

            # 加入购物车
            logging.info('加入购物车')
            SeaOfStarsAW.trace_thread.add_log('京东', '加入购物车')
            SeaOfStarsAW.check_status(label="加入购物车")
            SeaOfStarsAW.ut_device(label="加入购物车").click()
            time.sleep(2)
            SeaOfStarsAW.check_status(label="确定")
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="确定").click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
            #         '%H%M%S', time.localtime()) + '.png')

            # 去结算
            logging.info('去结算')
            SeaOfStarsAW.trace_thread.add_log('京东', '去结算')
            if SeaOfStarsAW.ut_device(label="去购物车结算").exists:
                SeaOfStarsAW.ut_device(label="去购物车结算").click()
                time.sleep(2)
            else:
                SeaOfStarsAW.ut_device.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[4]/Button[3]').click()
                time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
            #         '%H%M%S', time.localtime()) + '.png')

            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('京东', '返回home')
            SeaOfStarsAW.check_status(label="返回")
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.check_status(label="返回")
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.check_status(label="返回")
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.check_status(label="返回")
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            SeaOfStarsAW.check_status(label="首页")
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')