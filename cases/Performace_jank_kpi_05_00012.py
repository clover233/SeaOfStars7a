import logging
import time
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case

class Performance_jank_kpi_05_000012(Case):
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
            logging.info('应用{}启动'.format("com.autonavi.amap"))
            SeaOfStarsAW.trace_thread.add_log('高德地图', '应用启动')
            # SeaOfStarsAW.ut_device.session().app_activate("com.autonavi.amap")
            # pos = SeaOfStarsAW.find_app_from_launcher('高德地图')
            # while str(pos) == ('Point(x=0, y=0)'):
            #     SeaOfStarsAW.ut_device.swipe_left()
            #     pos = SeaOfStarsAW.find_app_from_launcher('高德地图')
            # pos = SeaOfStarsAW.find_app_from_launcher('高德地图')
            # SeaOfStarsAW.click_pos_from_launcher(pos)
            SeaOfStarsAW.ut_device.swipe_left()
            time.sleep(2)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.853, 0.264)


            # 启动应用等待
            time.sleep(15)

            # step2:搜索“西安北站（北进站口）”
            logging.info('搜索“西安北站（北进站口）')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '应用启动')
            # 界面判断
            SeaOfStarsAW.check_status(label="首页")

            # 点击搜索框
            # SeaOfStarsAW.ut_device.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/'
            #                              'Other[1]/Other[2]/Other[1]/Other[2]/Other[1]/Image[1]/Image[1]').click()
            SeaOfStarsAW.ut_device.click(0.426, 0.596)
            time.sleep(2)
            # 界面判断
            SeaOfStarsAW.check_status(label="酒店")
            # 输入文本
            SeaOfStarsAW.ut_device.xpath(
                '//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[2]/Other[1]/Image[1]'
                '/Image[1]/Image[1]/Image[1]/Image[1]/Image[1]/Image[2]').set_text('西安北站（北进站口）')
            time.sleep(2)
            # 点击搜索按钮
            SeaOfStarsAW.ut_device.click(0.911, 0.102)
            time.sleep(5)
            # 界面判断
            SeaOfStarsAW.check_status(label="搜索框，西安北站（北进站口）")
            time.sleep(2)
            # 点击北进站口
            SeaOfStarsAW.ut_device.click(0.213, 0.754)
            time.sleep(2)

            # step3:点击路线，点击导航
            logging.info('点击路线，点击导航')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点击路线，点击导航')
            # 界面判断
            # SeaOfStarsAW.check_status(label="西安北站(北进站口)")
            # time.sleep(2)
            # 点击路线
            SeaOfStarsAW.ut_device.click(0.843, 0.928)
            time.sleep(5)
            SeaOfStarsAW.ut_device.click(0.862, 0.757)
            time.sleep(2)
            # 判断是否在驾车页面
            if not SeaOfStarsAW.ut_device(label="高德推荐").exists:
                SeaOfStarsAW.ut_device.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/'
                                             'Other[1]/Other[1]/Other[2]/Other[1]/Other[1]/Other[3]/ScrollView[1]/'
                                             'Button[1]').click()
                time.sleep(2)
            # SeaOfStarsAW.check_status(label="高德推荐")
            # 点击“开始导航”
            if SeaOfStarsAW.ut_device.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/'
                                            'Other[1]/Other[2]/Other[1]/Image[1]/Image[1]/Image[1]/Image[1]/Image[3]/'
                                            'Image[2]/Image[1]/Image[1]/Image[2]/Image[1]/Image[1]/ScrollView[1]/'
                                            'Image[1]/Image[1]/Image[2]/Image[1]/Image[1]').exists:
                SeaOfStarsAW.ut_device.click(0.071, 0.845)
                time.sleep(2)
            else:
                SeaOfStarsAW.ut_device.click(0.672, 0.904)
                time.sleep(2)

            # step4:停留10s
            logging.info('停留10s')

            time.sleep(10)

            # step5:退出高德地图导航
            SeaOfStarsAW.trace_thread.add_log('高德地图', '退出高德地图导航')
            SeaOfStarsAW.ut_device.click(0.079, 0.922)
            time.sleep(2)
            SeaOfStarsAW.ut_device.click(0.079, 0.922)
            time.sleep(3)
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(2)

            # step6:点周边-美食
            logging.info('点周边-美食')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '点周边-美食')
            # 界面判断
            # SeaOfStarsAW.check_status(label="西安北站(北进站口)")

            SeaOfStarsAW.ut_device.click(0.068, 0.919)
            time.sleep(5)
            SeaOfStarsAW.ut_device.click(0.103, 0.153)
            time.sleep(5)
            # if SeaOfStarsAW.ut_device(label="关闭").exists:
            #     SeaOfStarsAW.ut_device.click(0.5, 0.781)
            #     time.sleep(2)

            # step7: 美食浏览(滑动3次)
            logging.info('美食浏览')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '美食浏览')
            for i in range(0, 3):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            # step8:返回高德首页面
            logging.info('返回高德首页面')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '返回高德首页面')
            for i in range(5):
                SeaOfStarsAW.ut_device.click(0.079, 0.091)
                time.sleep(4)
            # SeaOfStarsAW.ut_device(label="返回").click()
            # SeaOfStarsAW.ut_device.click(0.079, 0.088)

            # step9：返回home
            logging.info('返回home')
            SeaOfStarsAW.trace_thread.add_log('高德地图', '返回home')
            # 界面判断
            # SeaOfStarsAW.check_status(label="tips.route_line")
            SeaOfStarsAW.ut_device.home()
            SeaOfStarsAW.stop_trace()
            SeaOfStarsAW.swipe_to_launcher()
            SeaOfStarsAW.go_home()


        logging.info('用例执行结束')