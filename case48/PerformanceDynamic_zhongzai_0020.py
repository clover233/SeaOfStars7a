import logging
import time
import openpyxl
from threading import Timer
from aw import SeaOfStarsAW
from cases.CaseBase import Case


class PerformanceDynamic_zhongzai_0020(Case):
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
            # todo 后续放开log
            # SeaOfStarsAW.start_trace(self.trace_dir_path, self.__class__.__name__, 'step_' + str(step),
            #                          self.screenshot_dir_path)
            app_name ="重载"

            step1 = "'1、打开qq音乐,等待10s'"
            logging.info('启动qq音乐')
            SeaOfStarsAW.trace_thread.add_log(app_name, step1)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.847, 0.135)
            time.sleep(10)

            step2 = "2、浏览首页 上滑2次 下滑2次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step3 = "3、点击第一个音乐卡片 进行播放  停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step3)
            SeaOfStarsAW.ut_device.click(0.552, 0.794)
            time.sleep(1)

            step4 = "4、上滑qq音乐进入后台 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step4)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step5 = "5、启动高德地图 停留3s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step5)
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device.click(0.602, 0.128)
            time.sleep(3)

            step6 = "6、点击搜索框 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step6)
            SeaOfStarsAW.ut_device.click(0.656, 0.623)
            time.sleep(1)

            step7 = "7、输入 西安北站 并搜索 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step7)
            SeaOfStarsAW.ut_device().set_text("西安北站")

            time.sleep(1)

            step8 = "8、点击第一个结果 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step8)
            SeaOfStarsAW.ut_device(label="西安北站").click()
            time.sleep(1)

            step9 = "9、点击 开始导航 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step9)
            SeaOfStarsAW.ut_device.click(0.648, 0.927)
            time.sleep(10)
            time.sleep(1)

            step10 = "10、上滑 将高德放入后台 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step10)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)


            step11 = "11、启动携程旅行 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step11)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.626, 0.717)
            time.sleep(10)

            step12 = "12、向上抛滑1次 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)

            step13 = "13、向下抛滑2次 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            for i in range(1):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

            step14 = "14、点击民宿 客栈 停留1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step14)
            SeaOfStarsAW.ut_device(label="民宿/客栈").click()

            step15 = "15、向上抛滑2次  每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step15)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step16 = "16、向下抛滑3次  每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step16)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step17 = "17、点击查询按钮"
            SeaOfStarsAW.trace_thread.add_log(app_name, step17)
            SeaOfStarsAW.ut_device.click(0.512, 0.505)

            step18 = "18、输入 臻选民宿 点击搜索"
            SeaOfStarsAW.trace_thread.add_log(app_name, step18)
            SeaOfStarsAW.ut_device.click(0.476, 0.088)
            SeaOfStarsAW.ut_device().set_text("臻选民宿")
            SeaOfStarsAW.ut_device(label="搜索").click()

            step19 = "19、点击第一个民宿"
            SeaOfStarsAW.trace_thread.add_log(app_name, step19)
            SeaOfStarsAW.ut_device.click(0.53, 0.464)


            step20 = "20、向上抛滑2次"
            SeaOfStarsAW.trace_thread.add_log(app_name, step20)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)

            step21 = "21、点击评论 "
            SeaOfStarsAW.trace_thread.add_log(app_name, step21)
            SeaOfStarsAW.ut_device(label="评价").click()

            step12 = "22、点击查看75条评论"
            SeaOfStarsAW.trace_thread.add_log(app_name, step12)
            SeaOfStarsAW.ut_device.click(0.72, 0.337)

            step13 = "23、上滑2次 下滑3次 每次停留2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step13)
            for i in range(2):
                SeaOfStarsAW.ut_device.swipe_up()
                time.sleep(2)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()
                time.sleep(2)

            step14 = "24、左滑1次 返回"
            SeaOfStarsAW.trace_thread.add_log(app_name, step14)
            SeaOfStarsAW.ut_device.click(0.074, 0.081)

            step15 = "25、点击全部设施"
            SeaOfStarsAW.trace_thread.add_log(app_name, step15)
            SeaOfStarsAW.ut_device(label="设施").click()

            step16 = "26、向下 抛滑3次"
            SeaOfStarsAW.trace_thread.add_log(app_name, step16)
            for i in range(3):
                SeaOfStarsAW.ut_device.swipe_down()

            # 因为无x，较原本应用删减掉2个步骤
            step17 = "27、返回首页"
            SeaOfStarsAW.trace_thread.add_log(app_name, step17)
            SeaOfStarsAW.ut_device.click(0.074, 0.081)
            SeaOfStarsAW.ut_device.click(0.074, 0.081)
            SeaOfStarsAW.ut_device.click(0.074, 0.081)

            step18 = "28、返回home"
            SeaOfStarsAW.trace_thread.add_log(app_name, step18)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)


            step31 = "31、打开微信 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step31)
            SeaOfStarsAW.ut_device.click(0.605, 0.606)
            time.sleep(1)

            step32 = "32、点击发现 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step32)
            SeaOfStarsAW.ut_device.click(0.626, 0.921)
            time.sleep(1)

            step33 = "33、点击 朋友圈 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step33)
            SeaOfStarsAW.ut_device(label="朋友圈").click()
            time.sleep(1)

            step34 = "34、朋友圈 上滑6次 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step34)
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)


            step35 = "35、朋友圈 下滑6次 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step35)
            for i in range(6):
                SeaOfStarsAW.ut_device.swipe_down()
            time.sleep(1)

            step36 = "36、点击右上角 相机的图标 2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step36)
            SeaOfStarsAW.ut_device(label="拍照").click()
            time.sleep(2)

            step37 = "37、点击拍摄 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step37)
            SeaOfStarsAW.ut_device.click(0.48, 0.789)
            time.sleep(1)

            step38 = "38、点击拍照按钮 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step38)
            SeaOfStarsAW.ut_device.click(0.488, 0.898)
            time.sleep(1)

            step39 = "39、点击取消按钮 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step39)
            SeaOfStarsAW.ut_device(label="取消").click()
            time.sleep(1)

            step40 = "40、点击拍照按钮 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device.click(0.488, 0.898)
            time.sleep(1)

            step41 = "41、点击取消按钮 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step41)
            SeaOfStarsAW.ut_device(label="取消").click()
            time.sleep(1)

            step42 = "42、返回至 微信首页 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step42)
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(1)

            step40 = "43、上滑退出微信 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step40 = "44、打开支付宝 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device.click(0.382, 0.137)
            time.sleep(1)

            step40 = "45、点击扫一扫 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device.swipe_right()
            SeaOfStarsAW.ut_device(label="扫一扫").click()
            time.sleep(1)

            step40 = "46、返回首页 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device(label="返回").click()
            time.sleep(1)

            step40 = "47、点击视频 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device(label="视频").click()
            time.sleep(1)

            step40 = "48、向上滑动视频8次 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            for i in range(8):
                SeaOfStarsAW.ut_device.swipe_up()
            time.sleep(1)

            step40 = "49、返回支付宝首页 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device.click(0.038, 0.074)
            time.sleep(1)

            step40 = "50、退出支付宝 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step40 = "51、启动高德地图 2s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device.click(0.602, 0.128)
            time.sleep(2)

            step40 = "52、退出导航 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device(label="退出导航按钮").click()
            time.sleep(1)

            step40 = "52、启动qq音乐 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device.swipe_left()
            SeaOfStarsAW.ut_device.click(0.847, 0.135)
            time.sleep(1)

            step40 = "53、点击暂停 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device(label="播放").click()
            time.sleep(1)

            step40 = "54、返回首页 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)

            step40 = "55、退出qq音乐 1s"
            SeaOfStarsAW.trace_thread.add_log(app_name, step40)
            SeaOfStarsAW.ut_device.home()
            time.sleep(1)
            SeaOfStarsAW.ut_device.swipe_left()

        logging.info('用例执行结束')