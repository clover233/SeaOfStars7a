# -*- coding: utf-8 -*-

import logging
import os
import shutil
import time
import uiautomator2 as u2
from uiautomator2 import Device
from Cases.CaseBase import Case
from aw_new import SeaOfStarsAW

class PerformanceDynamic_fuzai(Case):

    all_app_package_list = [
        "com.tencent.qqgame.xq",
        "com.guandan.mi",
        "com.tuyoo.doudizhu.android3d.mi",
        "com.qmzg2.mi",
        "com.k7k7.goujihd.mi",
        "com.xiaomi.gamecenter",
        "com.mipay.wallet",
        "com.qidian.QDReader",
        "news.cnr.cn",
        "com.kugou.android",
        "com.sina.news",
        "com.tencent.peng",
        "com.ifeng.news2",
        "com.sohu.newsclient",
        "com.miui.fm",
        "bubei.tingshu",
        "com.duowan.mobile",
        "com.kiloo.subwaysurf",
    ]

    def __init__(self, result_path):
        super().__init__(result_path)

    @SeaOfStarsAW.function_log
    def set_up(self):
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
        # 清空后台
        SeaOfStarsAW.stop_apps(phone_app_list)
        SeaOfStarsAW.clear_backgroud()
        logging.info("测试环境准备完成!")


    @SeaOfStarsAW.function_log
    def run_case(self):
        """
        测试用例执行
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("用例开始执行!")
        # SeaOfStarsAW.init_device()
        #  todo
        SeaOfStarsAW.start_perfetto_trace()
        logging.info("依次拉起18个负载应用")

        # 1、天天象棋
        SeaOfStarsAW.ut_device.app_start('com.tencent.qqgame.xq', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 2、掼蛋
        SeaOfStarsAW.ut_device.app_start('com.guandan.mi', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 3、途游斗地主（比赛版）
        SeaOfStarsAW.ut_device.app_start('com.tuyoo.doudizhu.android3d.mi', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 4、全民主公Ⅱ
        SeaOfStarsAW.ut_device.app_start('com.qmzg2.mi', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 5、多乐够级
        SeaOfStarsAW.ut_device.app_start('com.k7k7.goujihd.mi', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 6、游戏中心
        SeaOfStarsAW.ut_device.app_start('com.xiaomi.gamecenter', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 7、钱包
        SeaOfStarsAW.ut_device.app_start('com.mipay.wallet', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 8、起点读书
        SeaOfStarsAW.ut_device.app_start('com.qidian.QDReader', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 9、央广网
        SeaOfStarsAW.ut_device.app_start('news.cnr.cn', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 10、酷狗音乐
        SeaOfStarsAW.ut_device.app_start('com.kugou.android', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 11、新浪新闻
        SeaOfStarsAW.ut_device.app_start('com.sina.news', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 12、天天爱消除
        SeaOfStarsAW.ut_device.app_start('com.tencent.peng', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 13、凤凰新闻
        SeaOfStarsAW.ut_device.app_start('com.ifeng.news2', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 14、搜狐新闻
        SeaOfStarsAW.ut_device.app_start('com.sohu.newsclient', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 15、蜻蜓FM
        SeaOfStarsAW.ut_device.app_start('com.miui.fm', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 16、懒人听书
        SeaOfStarsAW.ut_device.app_start('bubei.tingshu', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 17、YY
        SeaOfStarsAW.ut_device.app_start('com.duowan.mobile', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        # 18、地铁跑酷
        SeaOfStarsAW.ut_device.app_start('com.kiloo.subwaysurf', use_monkey=True)
        time.sleep(2)
        SeaOfStarsAW.return_launcher()

        SeaOfStarsAW.stop_and_get_perfetto_trace(self.trace_dir_path, self.__class__.__name__,
                                                 'step_' + "1、依次拉起18个负载应用", "",
                                                 self.screenshot_dir_path)
        logging.info("用例执行结束!")

    @SeaOfStarsAW.function_log
    def clean_up(self):
        """
        测试环境恢复
        """
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ 请在下方添加自己的代码！↓ ↓ ↓ ↓
        # ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
        logging.info("开始恢复环境!")
        SeaOfStarsAW.stop_apps(self.all_app_package_list)
        SeaOfStarsAW.clear_backgroud()
        logger = logging.getLogger()
        logger.removeHandler(self.fh)
