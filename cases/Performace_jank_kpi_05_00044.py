import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000044(Case):
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
            # 微信启动
            logging.info('微信启动')
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.xin')
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.xin')
            # pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.click(337, 322)
            time.sleep(2)
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 点击发现-进入朋友圈
            logging.info('点击发现-进入朋友圈')
            # SeaOfStarsAW.check_status(label="发现")
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="发现").click()
            time.sleep(2)
            SeaOfStarsAW.check_status(label="朋友圈")
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="朋友圈").click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 点击相机图标
            logging.info('点击相机图标')
            # SeaOfStarsAW.check_status(label="拍照")
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="拍照").click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 点击拍摄
            logging.info('点击拍摄')
            # SeaOfStarsAW.check_status(label="拍摄,照片或视频")
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="拍摄,照片或视频").click()
            time.sleep(7)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
            #         '%H%M%S', time.localtime()) + '.png')

            # 返回朋友圈
            logging.info('返回朋友圈')
            # SeaOfStarsAW.check_status(label="关闭")
            SeaOfStarsAW.ut_device(label="关闭").click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
                # self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
                #     '%H%M%S', time.localtime()) + '.png')

            # 点击从相册选择
            logging.info('点击从相册选择')
            # SeaOfStarsAW.check_status(label="拍照")
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="拍照").click()
            time.sleep(2)
            # SeaOfStarsAW.check_status(label="从手机相册选择")
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="从手机相册选择").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.8)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0.5, 0.8, 0.5, 0.2)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.2, 0.813)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.45, 0.809)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.693, 0.808)
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
            #         '%H%M%S', time.localtime()) + '.png')

            # 点击预览
            logging.info('点击预览')
            # SeaOfStarsAW.check_status(label="预览")
            time.sleep(2)
            SeaOfStarsAW.ut_device(label="预览").click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
            #         '%H%M%S', time.localtime()) + '.png')

            # 划动图片
            logging.info('划动图片')
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe(0.6, 0.5, 0.4, 0.5, 0.05)
                time.sleep(2)
                step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(
            #         step) + '_' + time.strftime('%H%M%S', time.localtime()) + '.png')

            # 点击完成
            logging.info('点击完成')
            # SeaOfStarsAW.check_status(xpath='//Window[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[4]/Button[3]/StaticText[1]')
            # time.sleep(2)
            SeaOfStarsAW.ut_device.xpath('//Window[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[4]/Button[3]/StaticText[1]').click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
            #         '%H%M%S', time.localtime()) + '.png')

            # 点击发表
            logging.info('点击发表')
            # SeaOfStarsAW.check_status(label="发表")
            # time.sleep(2)
            SeaOfStarsAW.ut_device(label="发表").click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
            #         '%H%M%S', time.localtime()) + '.png')

            # 返回微信主页面
            logging.info('返回微信主页面')
            # SeaOfStarsAW.check_status(label="返回")
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)
            # SeaOfStarsAW.check_status(xpath='//*[@label="标签栏"]/Button[2]/Button[1]')
            # time.sleep(2)
            SeaOfStarsAW.ut_device.xpath('//*[@label="标签栏"]/Button[2]/Button[1]').click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(
            #     self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' + time.strftime(
            #         '%H%M%S', time.localtime()) + '.png')

            # 返回home
            logging.info('返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')