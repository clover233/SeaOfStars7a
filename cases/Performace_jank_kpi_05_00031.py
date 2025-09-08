import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000031(Case):
    all_app_package_list = ['']
    TEST_TIME = 1
    time_out = None

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
        SeaOfStarsAW.clear_background()

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

            # 启动腾讯视频
            logging.info('启动')
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.live4iphone')
            pos = SeaOfStarsAW.find_app_from_launcher('腾讯视频')
            while str(pos) == ('Point(x=0, y=0)'):
                SeaOfStarsAW.ut_device.swipe_left()
                pos = SeaOfStarsAW.find_app_from_launcher('腾讯视频')
            pos = SeaOfStarsAW.find_app_from_launcher('腾讯视频')
            SeaOfStarsAW.click_pos_from_launcher(pos)
            time.sleep(5)
            if SeaOfStarsAW.ut_device(label='我知道了').exists:
                SeaOfStarsAW.ut_device(label='我知道了').click()
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 进入电视剧tab页
            logging.info('进入电视剧tab页')
            SeaOfStarsAW.check_status(label='电视剧')
            SeaOfStarsAW.ut_device(label='电视剧').click()
            time.sleep(2)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 浏览电视剧，上下各滑动一次
            logging.info('浏览电视剧,上滑')
            SeaOfStarsAW.ut_device.swipe(0.341, 0.849, 0.341, 0.486, duration=0.2)
            time.sleep(2)
            logging.info('浏览电视剧,下滑')
            SeaOfStarsAW.ut_device.swipe(0.341, 0.486, 0.341, 0.849, duration=0.2)
            time.sleep(2)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 点击全部剧集
            SeaOfStarsAW.check_status(label='全部剧集')
            logging.info('点击全部剧集')
            SeaOfStarsAW.ut_device(label='全部剧集').click()
            time.sleep(2)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 选择免费
            SeaOfStarsAW.check_status(label='免费')
            logging.info('免费')
            SeaOfStarsAW.ut_device(label='免费').click()
            time.sleep(2)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 点击推荐的第一个视频播放
            logging.info('点击推荐的第一个视频播放')
            SeaOfStarsAW.ut_device.click(0.176, 0.554)
            time.sleep(5)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')
            # 先点击第一集
            SeaOfStarsAW.ut_device.click(0.116, 0.543)
            # 快进、调节音量、调节亮度、播放下一集
            for i in range(2):
                time.sleep(2)
                if SeaOfStarsAW.ut_device(label='VIP可关闭该广告').exists:
                    print(type(SeaOfStarsAW.ut_device(label='VIP可关闭该广告')))
                    print(i)
                    print('1111111111111111111111111')
                    time.sleep(130)
                    # print('1111111111111111111111111')
                if SeaOfStarsAW.ut_device(label='跳过广告').exists:
                    SeaOfStarsAW.ut_device(label='跳过广告').click()
                if SeaOfStarsAW.ut_device(label='夸克全新升级').exists:
                    SeaOfStarsAW.ut_device(label='夸克全新升级').click()

                # 快进
                logging.info('快进')
                time.sleep(20)
                SeaOfStarsAW.ut_device.click(0.394, 0.185)
                time.sleep(1)
                SeaOfStarsAW.ut_device.swipe(0.292, 0.19, 0.679, 0.19, duration=0.3)

                # 调高亮度
                logging.info('调高亮度')
                time.sleep(20)
                SeaOfStarsAW.ut_device.swipe(0.323, 0.235, 0.323, 0.123, duration=0.3)

                # 调低亮度
                logging.info('调低亮度')
                time.sleep(20)
                SeaOfStarsAW.ut_device.swipe(0.323, 0.123, 0.323, 0.235, duration=0.3)

                # 调大音量
                logging.info('调大音量')
                time.sleep(20)
                SeaOfStarsAW.ut_device.swipe(0.651, 0.232, 0.651, 0.125, duration=0.3)

                # 调小音量
                logging.info('调小音量')
                time.sleep(20)
                SeaOfStarsAW.ut_device.swipe(0.651, 0.125, 0.651, 0.232, duration=0.3)

                # 播放下一集
                logging.info('播放下一集')
                time.sleep(20)
                SeaOfStarsAW.ut_device(label='%s' % (i+2)).click()
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + time.strftime('%H%M%S', time.localtime()) + '.png')

            # 返回home
            logging.info('返回home')
            # SeaOfStarsAW.check_status(label='返回')
            # SeaOfStarsAW.check_status(xpath='//*[@label="pread mini back iphone"]')
            SeaOfStarsAW.ut_device.click(0.07, 0.081)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.07, 0.081)
            time.sleep(2)
            # SeaOfStarsAW.ut_device(xpath='//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Button[1]').click()
            # time.sleep(2)
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            step += 1
            SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + time.strftime('%H%M%S', time.localtime()) + '.png')
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')