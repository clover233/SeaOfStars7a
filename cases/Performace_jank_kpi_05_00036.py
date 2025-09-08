import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000036(Case):
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
            SeaOfStarsAW.ut_device.click(337, 322)
            # SeaOfStarsAW.ut_device.session().app_activate('com.tencent.xin')
            # pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # pos = SeaOfStarsAW.find_app_from_launcher('微信')
            # SeaOfStarsAW.click_pos_from_launcher(pos)

            time.sleep(2)

            # 返回主页
            # SeaOfStarsAW.trace_thread.add_log('微信', '返回主页')
            # SeaOfStarsAW.ut_device.click(0.076, 0.089)

            # 主页滑动
            SeaOfStarsAW.trace_thread.add_log('微信', '主页滑动')
            logging.info('主页滑动')
            SeaOfStarsAW.ut_device.swipe(0.5, 0.5, 0.5, 0.3)
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe(0.5, 0.3, 0.5, 0.5)
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')


            # 进入群聊
            logging.info('进入群聊')
            SeaOfStarsAW.trace_thread.add_log('微信', '进入群聊')
            # SeaOfStarsAW.check_status(label='测试群聊')
            SeaOfStarsAW.ut_device(label="测试用例36").click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')
            #

            # 查看图片
            logging.info('查看图片')
            SeaOfStarsAW.trace_thread.add_log('微信', '查看图片')
            for i in range(5):
                SeaOfStarsAW.ut_device.click(0.699, 0.258)
                time.sleep(2)
                for _ in range(3):
                    SeaOfStarsAW.ut_device.swipe(0.7, 0.5, 0.3, 0.5)
                    time.sleep(2)
                SeaOfStarsAW.ut_device.swipe(0.5, 0.2, 0.5, 0.5)
                time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')
            #

            # 查看视频
            logging.info('查看视频')
            SeaOfStarsAW.trace_thread.add_log('微信', '查看视频')
            for _ in range(5):
                SeaOfStarsAW.ut_device.click(0.7, 0.7)
                time.sleep(10)
                SeaOfStarsAW.ut_device.click(0.5, 0.5)
                time.sleep(2)
                SeaOfStarsAW.ut_device(label="关闭").click()
                time.sleep(2)

            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 转发给朋友
            logging.info('转发给朋友')
            SeaOfStarsAW.trace_thread.add_log('微信', '转发给朋友')
            SeaOfStarsAW.ut_device.tap_hold(0.7, 0.7, 3)
            time.sleep(2)
            # 点击转发
            # SeaOfStarsAW.ut_device.tap_hold(0.367, 0.556, 1)
            SeaOfStarsAW.ut_device.click(0.48, 0.495)

            time.sleep(2)
            # SeaOfStarsAW.check_status(label='永不被封')
            SeaOfStarsAW.ut_device(label="用例36转发").click()
            time.sleep(2)
            SeaOfStarsAW.check_status(label='发送')
            SeaOfStarsAW.ut_device(label="发送").click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 返回微信主页面
            SeaOfStarsAW.trace_thread.add_log('微信', '返回微信主页面')
            SeaOfStarsAW.ut_device.click(0.077, 0.082)
            time.sleep(1)
            SeaOfStarsAW.ut_device(label="测试用例36聊天").click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 播放语音留言
            SeaOfStarsAW.trace_thread.add_log('微信', '播放语音留言')
            # SeaOfStarsAW.ut_device.click(0.712, 0.295)
            SeaOfStarsAW.ut_device.click(0.733, 0.3)
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 发送文字消息"哈哈哈"
            SeaOfStarsAW.trace_thread.add_log('微信', '发送文字消息"哈哈哈"')
            SeaOfStarsAW.ut_device.click(0.933, 0.925)
            time.sleep(2)
            SeaOfStarsAW.ut_device(xpath='//TextView').set_text('哈哈哈哈哈')
            time.sleep(2)
            if SeaOfStarsAW.ut_device(label='send').exists:
                SeaOfStarsAW.ut_device(label='send').click()
            else:
                SeaOfStarsAW.ut_device(label='发送').click()
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 发送语音
            SeaOfStarsAW.trace_thread.add_log('微信', '发送语音')
            # SeaOfStarsAW.check_status(label='语音')
            SeaOfStarsAW.ut_device(label="语音").click()
            time.sleep(2)
            SeaOfStarsAW.ut_device.tap_hold(0.44, 0.928, 3)
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 发送图片
            SeaOfStarsAW.trace_thread.add_log('微信', '发送图片')
            for i in range(3):
                SeaOfStarsAW.ut_device.click(0.929, 0.925)
                time.sleep(2)
                SeaOfStarsAW.ut_device(label="照片").click()
                time.sleep(2)
                SeaOfStarsAW.ut_device.click(0.19, 0.803)
                time.sleep(2)
                SeaOfStarsAW.ut_device(label='发送(1)').click()
                time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 返回主页面
            SeaOfStarsAW.trace_thread.add_log('微信', '返回主页面')
            logging.info('返回主页面')
            SeaOfStarsAW.ut_device(labelContains="返回").click()
            time.sleep(2)
            step += 1
            # SeaOfStarsAW.ut_device.screenshot(self.screenshot_dir_path + '/' + self.__class__.__name__ + 'step_' + str(step) + '_' +time.strftime('%H%M%S', time.localtime()) + '.png')

            # 返回home
            SeaOfStarsAW.trace_thread.add_log('微信', '返回home')
            logging.info('返回home')
            SeaOfStarsAW.ut_device.home()
            time.sleep(2)
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')