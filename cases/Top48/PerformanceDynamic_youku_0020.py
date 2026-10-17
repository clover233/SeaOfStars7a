import logging
import time
from Cases.CaseBase import Case
from aw_new import SeaOfStarsAW


class PerformanceDynamic_youku_0020(Case):
    all_app_package_list = [""]

    def __init__(self, result_path):
        super().__init__(result_path)

    @SeaOfStarsAW.function_log
    def set_up(self):
        """
        测试环境准备
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("测试环境开始准备!")
        # 判断手机上是否已安装好TOP30应用,未安装则用例失败
        phone_app_list = SeaOfStarsAW.get_app_list()
        for per_app in self.all_app_package_list:
            if per_app not in phone_app_list:
                return False
        # 设置系统语言为中文
        SeaOfStarsAW.set_system_language_cn()
        # 解锁屏幕
        if SeaOfStarsAW.is_locked():
            SeaOfStarsAW.unlock_device()
        # 设置屏幕锁定时间为10min
        SeaOfStarsAW.set_screen_lock_long_time()
        # 保留已有应用后台
        logging.info("测试环境准备完成!")

    def _enter_search_text(self, query):
        device = SeaOfStarsAW.ut_device
        search_input = device(resourceId='com.youku.phone:id/et_widget_search_text_soku')
        if not search_input.wait(timeout=10):
            raise RuntimeError('优酷搜索输入框未出现')
        search_input.click()
        focused_input = device(resourceId='com.youku.phone:id/et_widget_search_text_soku', focused=True)
        if not focused_input.wait(timeout=5):
            raise RuntimeError('优酷搜索输入框未获得焦点')
        # 直接替换控件文本，避免 AdbKeyboard.clearText 的空指针异常。
        focused_input.set_text(query)
        if not device(resourceId='com.youku.phone:id/et_widget_search_text_soku',
                      text=query).wait(timeout=5):
            raise RuntimeError('优酷搜索词未写入：' + query)

    def _search_video(self, query):
        self._enter_search_text(query)
        search_button = SeaOfStarsAW.ut_device(resourceId='com.youku.phone:id/tv_right', text='搜索')
        if not search_button.wait(timeout=5):
            raise RuntimeError('优酷搜索按钮未出现')
        search_button.click()
        if not SeaOfStarsAW.ut_device(resourceId='com.youku.phone:id/item_b_program_info_title',
                                      text=query).wait(timeout=15):
            raise RuntimeError('优酷搜索结果未出现：' + query)

    @SeaOfStarsAW.function_log
    def run_case(self):
        """
        测试用例执行
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("用例开始执行!")
        steps_num = 1

        app = 'com.youku.phone'
        step = "1、打开优酷（停留5s）"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info("启动{}中".format("优酷"))
        SeaOfStarsAW.ut_device.app_start(app, use_monkey=True)
        time.sleep(5)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "2、首页浏览上滑5次，下滑5次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(5):
            SeaOfStarsAW.scroll_down(0.5)
            time.sleep(2)
        for _ in range(5):
            SeaOfStarsAW.scroll_up(0.5)
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "3、点击动漫tab页"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='动漫')[0].click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "4、动漫tab页浏览上滑3次，下滑3次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(3):
            SeaOfStarsAW.scroll_down(0.5)
            time.sleep(2)
        for _ in range(3):
            SeaOfStarsAW.scroll_up(0.5)
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "5、点击电影tab页"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='电影')[0].click()
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "6、电影tab页浏览上滑3次，下滑3次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(3):
            SeaOfStarsAW.scroll_down(0.5)
            time.sleep(2)
        for _ in range(3):
            SeaOfStarsAW.scroll_up(0.5)
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "7、返回推荐页点击搜索框，切换到搜索页面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.ut_device(text='剧集')[0].click()
        time.sleep(1)
        SeaOfStarsAW.ut_device(text='首页')[0].click()
        time.sleep(1)
        SeaOfStarsAW.ut_device.click(0.466, 0.084)
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "8、输入大话天仙"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        self._enter_search_text("大话天仙")
        time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "9、搜索视频大话天仙，重复搜索2次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(2):
            self._search_video("大话天仙")
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "10、点击播放大话天仙，观看30秒"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)

        SeaOfStarsAW.ut_device.click(0.408, 0.551)
        time.sleep(30)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "11、视频播放页浏览上滑5次，下滑5次"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(5):
            SeaOfStarsAW.scroll_down()
            time.sleep(2)
        for _ in range(5):
            SeaOfStarsAW.scroll_up()
            time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "12、返回优酷主界面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        for _ in range(5):
            SeaOfStarsAW.ut_device.swipe(0.99, 0.423, 0.636, 0.423)
            time.sleep(1)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        step = "13、上滑返回桌面"
        SeaOfStarsAW.start_perfetto_trace()
        logging.info(step)
        SeaOfStarsAW.return_launcher()
        time.sleep(2)
        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + str(steps_num) + "-" + step, "", self.screenshot_dir_path)
        steps_num += 1

        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        """
        清理日志，保留应用后台
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("用例结束，保留应用后台，仅清理日志处理器。")
        logger = logging.getLogger()
        logger.removeHandler(self.fh)
