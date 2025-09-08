import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000023(Case):
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
            logging.info('应用{}启动'.format("com.ss.iphone.article.News"))
            # SeaOfStarsAW.ut_device.session().app_activate("com.ss.iphone.article.News")
            # pos = SeaOfStarsAW.find_app_from_launcher('今日头条')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('今日头条')
            # pos = SeaOfStarsAW.find_app_from_launcher('今日头条')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.607, 0.375)
            # 启动应用等待
            time.sleep(15)

            # step2:推荐页滑动，重复三次
            logging.info('进入收藏-图片的链接）')
            SeaOfStarsAW.check_status(label="已选中，推荐")

            # 滑动3次
            for i in range(0, 3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(0, 4):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            # step3:进入第一条
            logging.info('进入第一条')

            SeaOfStarsAW.ut_device.xpath('//Table/Cell[1]/Other[1]/Other[3]/Other[1]/StaticText[1]').click()
            time.sleep(2)

            # step4:阅读浏览新闻详情
            logging.info('阅读浏览新闻详情')
            # 界面判断
            # SeaOfStarsAW.check_status(label="搜索栏")
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)
            # 上滑一次浏览
            SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(5)

            # step5：查看评论
            logging.info('查看评论')
            # 进入评论区查看评论

            SeaOfStarsAW.ut_device.click(0.347, 0.934)
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(label="写评论")

            # step6：点击分享到微信好友
            logging.info('点击分享到微信好友')

            SeaOfStarsAW.ut_device(label="分享").click()
            time.sleep(2)


            # step7：返回头条首页，返回home
            logging.info('返回头条首页，返回home')
            # 界面判断

            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()

        logging.info('用例执行结束')