import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000037(Case):
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
            SeaOfStarsAW.trace_thread.add_log('微信', '应用启动')
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

            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            for _ in range(5):
                # 进入发现
                SeaOfStarsAW.trace_thread.add_log('微信', '进入发现')
                logging.info('进入发现')
                # SeaOfStarsAW.check_status(label='发现')
                SeaOfStarsAW.ut_device.click(0.625, 0.923)
                time.sleep(2)
                # SeaOfStarsAW.check_status(label='朋友圈')
                SeaOfStarsAW.ut_device.xpath('//Table/Cell[1]').click()
                time.sleep(2)

                # 浏览朋友圈

                logging.info('浏览朋友圈')
                SeaOfStarsAW.trace_thread.add_log('微信', '浏览朋友圈')
                SeaOfStarsAW.ut_device.swipe(0.7, 0.8, 0.7, 0.5)
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe(0.7, 0.4, 0.7, 0.9)
                time.sleep(2)
                step -= 1
                if _ < 4:
                    SeaOfStarsAW.ut_device(label='返回').click()
            step += 2
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 查看朋友圈动态图片
            logging.info('查看朋友圈动态图片')
            SeaOfStarsAW.trace_thread.add_log('微信', '查看朋友圈动态图片')

            for i in range(6):
                SeaOfStarsAW.ut_device.click(0.287, 0.575)
                time.sleep(2)
                for j in range(3):
                    SeaOfStarsAW.ut_device.swipe(0.9, 0.5, 0.3, 0.5, 0.05)
                    time.sleep(2)
                time.sleep(2)
                SeaOfStarsAW.ut_device.swipe(0.5, 0.1, 0.5, 0.2, 0.05)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 点击朋友圈发布的视频
            logging.info('点击朋友圈发布的视频')
            SeaOfStarsAW.trace_thread.add_log('微信', '点击朋友圈发布的视频')
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.498, 0.982)
            time.sleep(5)
            SeaOfStarsAW.ut_device.swipe(0.6, 0.1, 0.6, 0.2, 0.05)

            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 朋友圈发表文字评论"哈哈哈哈哈哈哈哈"
            # 点击两点按钮
            logging.info('点击两点按钮')
            SeaOfStarsAW.trace_thread.add_log('微信', '点击两点按钮')
            SeaOfStarsAW.ut_device.swipe(0.6, 0.1, 0.6, 0.2, 0.05)
            time.sleep(2)
            # SeaOfStarsAW.ut_device.click(0.9, 0.737)
            SeaOfStarsAW.ut_device(name='Moments_OperationButton').click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 点击评论
            logging.info('点击评论')
            SeaOfStarsAW.trace_thread.add_log('微信', '点击评论')
            SeaOfStarsAW.check_status(label='评论')
            SeaOfStarsAW.ut_device(label='评论').click()
            time.sleep(2)
            # 发送 哈哈哈哈哈哈哈哈
            logging.info('发送 哈哈哈哈哈哈哈哈')
            SeaOfStarsAW.ut_device().set_text('哈哈哈哈哈哈哈哈')
            time.sleep(2)
            # 点击发送
            logging.info('点击发送')
            SeaOfStarsAW.trace_thread.add_log('微信', '点击发送')
            if SeaOfStarsAW.ut_device(label='send').exists:
                SeaOfStarsAW.ut_device(label='send').click()
            else:
                SeaOfStarsAW.ut_device(label='发送').click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 点击返回到上一层
            logging.info('点击返回到上一层')
            SeaOfStarsAW.trace_thread.add_log('微信', '点击返回到上一层')
            SeaOfStarsAW.ut_device(label='返回').click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.124, 0.92)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 返回到home页面
            logging.info('返回到home页面')
            SeaOfStarsAW.trace_thread.add_log('微信', '返回到home页面')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')