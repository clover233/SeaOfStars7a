import logging
import os
import platform
import re
import shlex
import shutil
import subprocess
import threading
import time
import json
from functools import wraps
import chardet
from threading import Timer
import uiautomator2 as u2
from enum import Enum
from enum import unique

# 装饰器 - 检测Device.SN是否初始化, 无需修
from uiautomator2 import Device


class SeaOfStarsAW:
    @unique
    class DeviceType(Enum):
        HISI = 0
        EMUI = 1
        XIAOMI = 2

    class PerfettoThread(threading.Thread):

        def __init__(self, ):
            threading.Thread.__init__(self)
            self.isLetPerfettoRun = False
            self.isPerfettoRunning = False

        def start_perfetto(self, trace_dir, trace_name):
            self.save_path = trace_dir
            self.save_name = trace_name
            self.isLetPerfettoRun = True

        def stop_perfetto(self):
            self.isLetPerfettoRun = False
            while self.isPerfettoRunning:
                time.sleep(1)
                logging.info("等待trace抓取结束中...")

        def run(self):
            logging.info("trace线程开始运行")
            while 1:
                while self.isLetPerfettoRun:
                    self.isPerfettoRunning = True
                    # 开始抓取trace
                    logging.info("trace线程开始抓取trace")
                    SeaOfStarsAW.adb_cmd(r'adb shell "setprop persist.traced.enable 1"')
                    SeaOfStarsAW.adb_cmd(r'adb shell "echo 0 > /d/tracing/tracing_on"')
                    time.sleep(1)
                    SeaOfStarsAW.adb_cmd(r'adb shell rm /data/misc/perfetto-traces/trace')
                    SeaOfStarsAW.trace_start_timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                    SeaOfStarsAW.adb_cmd(
                        "adb push {} {}".format(os.path.join("Resources", "perfetto.pbtxt"), "/data/local/tmp/"))
                    SeaOfStarsAW.adb_cmd(
                        'adb shell "cat /data/local/tmp/perfetto.pbtxt | perfetto --txt -c - -o /data/misc/perfetto-traces/trace --detach=perf_debug"')
                    # 抓取15秒的trace
                    for i in range(30):
                        time.sleep(0.5)
                        if not self.isLetPerfettoRun:
                            break
                    # 抓取trace完成,导出trace
                    SeaOfStarsAW.adb_cmd(r'adb shell "perfetto --attach=perf_debug --stop"')
                    time.sleep(1)
                    time_stamp = time.strftime("%H%M%S", time.localtime())
                    trace_name = "{}-{}_{}.trace".format(self.save_name, SeaOfStarsAW.trace_start_timestamp,
                                                            time_stamp)
                    SeaOfStarsAW.adb_cmd(r'adb pull /data/misc/perfetto-traces/trace ' + self.save_path,
                                         is_print_return=False)
                    time.sleep(1)
                    os.rename(os.path.join(self.save_path, "trace"), os.path.join(self.save_path, trace_name))
                    time.sleep(1)
                    logging.info("{}抓取结束,当前温度:{}℃".format(trace_name, SeaOfStarsAW.get_current_tempreture()))
                    self.isPerfettoRunning = False
                time.sleep(0.5)


    SN = '9a08f'
    ut_device:Device = u2.connect(r'9a08f')
    ADB_PROC = None
    shell_temp_path = None
    device_type = DeviceType.HISI
    device_info = {}
    trace_start_timestamp = None
    public_screen_shot_dir = None
    # 用于抓取非关键场景的perfetto trace, 用于统计丢帧数
    perfetto_thread: PerfettoThread = PerfettoThread()


    @staticmethod
    def function_log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.debug("{0:=^40}".format(" " + func.__name__ + " 开始执行 "))
            res = func(*args, **kwargs)
            logging.debug("{0:=^40}".format(" " + func.__name__ + " 执行结束 "))
            return res

        return wrapper

    def Device_Init_Check(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.debug("{0:=^40}".format(" " + func.__name__ + " 开始执行 "))
            if SeaOfStarsAW.SN is None:
                logging.error("{0:!^40}".format(" 需要先初始化SeaOfStarsAW.init_device() "))
                raise AssertionError("需要先初始化SeaOfStarsAW.init_device()")
            res = func(*args, **kwargs)
            logging.debug("{0:=^40}".format(" " + func.__name__ + " 执行结束 "))
            return res
        return wrapper

    def UiAutomatorService_Check(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not SeaOfStarsAW.ut_device.uiautomator.running():
                logging.warning("UiAutomatorService服务未启动,启动中...")
                SeaOfStarsAW.ut_device.uiautomator.start()
                time.sleep(1)
                if not SeaOfStarsAW.ut_device.uiautomator.running():
                    raise AssertionError("UiAutomatorService挂死，服务重启失败")
            res = func(*args, **kwargs)
            return res

        return wrapper

    @staticmethod
    def init_device(result_dir_path=None, serial_no=None):
        SeaOfStarsAW.SN = serial_no
        result = os.popen("adb devices").read()
        devices_list = re.compile(r"(\S+)\s+device\s+").findall(result)
        if len(devices_list) == 0 or (serial_no and serial_no not in devices_list):
            return False
        else:
            if serial_no:
                SeaOfStarsAW.SN = serial_no
            else:
                SeaOfStarsAW.SN = devices_list[0]
        applist = SeaOfStarsAW.get_app_list()
        uiautomator_dir_path = os.path.join(".", "Resources","uiautomator")
        if "com.github.uiautomator.test" not in applist or "com.github.uiautomator" not in applist:
            SeaOfStarsAW.adb_cmd(r"adb install {}".format(os.path.join(uiautomator_dir_path, "app-uiautomator.apk")))
            SeaOfStarsAW.adb_cmd(r"adb install {}".format(os.path.join(uiautomator_dir_path, "app-uiautomator-test.apk")))
        SeaOfStarsAW.adb_cmd(r"adb push {} /data/local/tmp".format(os.path.join(uiautomator_dir_path, "minicap")), is_print_return=False)
        SeaOfStarsAW.adb_cmd(r"adb push {} /data/local/tmp".format(os.path.join(uiautomator_dir_path, "minitouch")), is_print_return=False)
        SeaOfStarsAW.adb_cmd(r"adb push {} /data/local/tmp".format(os.path.join(uiautomator_dir_path, "atx-agent")), is_print_return=False)
        SeaOfStarsAW.adb_cmd(r"adb shell chmod 777 /data/local/tmp/*")
        SeaOfStarsAW.adb_cmd(r"adb shell /data/local/tmp/atx-agent server -d")
        device = u2.connect(SeaOfStarsAW.SN)
        SeaOfStarsAW.ut_device = device
        SeaOfStarsAW.device_info = SeaOfStarsAW.ut_device.info
        if not SeaOfStarsAW.ut_device.uiautomator.running():
            logging.warning("UiAutomatorService服务未启动,启动中...")
            SeaOfStarsAW.ut_device.uiautomator.start()
        # 判断设备类型
        hw_emui_api_level = SeaOfStarsAW.adb_cmd(r"adb shell getprop ro.build.hw_emui_api_level").strip()
        xiaomi_api_level = SeaOfStarsAW.adb_cmd(r"adb shell getprop ro.product.product.brand").strip().lower()
        if hw_emui_api_level != "":
            SeaOfStarsAW.device_type = SeaOfStarsAW.DeviceType.EMUI
            SeaOfStarsAW.skip_emui_guide()
        elif "xiaomi" in xiaomi_api_level:
            SeaOfStarsAW.device_type = SeaOfStarsAW.DeviceType.XIAOMI
        # 初始化温度节点
        thermal_node_list = SeaOfStarsAW.adb_cmd(
            'adb shell "ls /sys/devices/virtual/thermal | grep thermal_zone"').splitlines()
        for thermal_node in thermal_node_list:
            if "thermal_zone" in thermal_node:
                type = SeaOfStarsAW.adb_cmd(
                    'adb shell "cat /sys/devices/virtual/thermal/{}/type"'.format(thermal_node)).strip()
                logging.info(type)
                if type.lower() == "soc_thermal" and (SeaOfStarsAW.device_type == SeaOfStarsAW.DeviceType.HISI):
                    SeaOfStarsAW.shell_temp_path = "/sys/devices/virtual/thermal/{}/temp".format(thermal_node)
                    logging.info("SOC温度节点:{}".format(SeaOfStarsAW.shell_temp_path))
                    break
                if type.lower() == "battery" and (SeaOfStarsAW.device_type == SeaOfStarsAW.DeviceType.XIAOMI or SeaOfStarsAW.device_type == SeaOfStarsAW.DeviceType.EMUI):
                    SeaOfStarsAW.shell_temp_path = "/sys/devices/virtual/thermal/{}/temp".format(thermal_node)
                    logging.info("battery温度节点:{}".format(SeaOfStarsAW.shell_temp_path))
                    break
        # 导出设备信息
        if result_dir_path:
            SeaOfStarsAW.dump_phone_info(result_dir_path)
            SeaOfStarsAW.dump_app_info(result_dir_path)


        logging.info("设备类型："+str(SeaOfStarsAW.device_type))
        # 初始化hizee
        SeaOfStarsAW.adb_cmd(r"adb push {} {}".format(os.path.join(".","Resources","hizee","HiKitsBin"), "/data/local/tmp"), is_print_return=False)
        SeaOfStarsAW.adb_cmd(r"adb push {} {}".format(os.path.join(".","Resources","hizee","platconfig.xml"), "/data/local/tmp"), is_print_return=False)
        SeaOfStarsAW.adb_cmd(r'adb shell "chmod 777 /data/local/tmp/*"')
        # 安装中文输入apk
        SeaOfStarsAW.adb_cmd(r'adb install {}'.format(os.path.join(".", "Resources", "ADBKeyboard.apk")))
        SeaOfStarsAW.adb_cmd(r'adb shell ime enable com.android.adbkeyboard/.AdbIME')
        SeaOfStarsAW.adb_cmd(r'adb shell ime set com.android.adbkeyboard/.AdbIME')
        # 空闲Perfetto线程开始执行,但未开始抓取
        SeaOfStarsAW.perfetto_thread.setDaemon(True)
        SeaOfStarsAW.perfetto_thread.start()
        # 初始化hiperfetto - 抓取温度信息
        SeaOfStarsAW.adb_cmd(
            r"adb push {} {}".format(os.path.join(".", "Resources", "hiperfetto"), "/data/local/tmp"),
            is_print_return=False)
        SeaOfStarsAW.adb_cmd(r'adb shell "chmod 777 /data/local/tmp/*"')
        # 初始化adb窗口供swipe命令复用
        if not SeaOfStarsAW.ADB_PROC:
            SeaOfStarsAW.ADB_PROC = subprocess.Popen("adb -s " + SeaOfStarsAW.SN +" shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        return True

    @staticmethod
    @Device_Init_Check
    def adb_cmd(*cmd, time_out=360, is_check_return=True, is_print_return=True, is_nohup=False):
        """
        向设备发送adb命令执行，并获取返回值，默认执行时间超过360秒会强制结束

        Note:
            默认执行时间超过360秒会强制结束

        :param
            str_cmd:         要执行的adb命令,需要带完整地 adb shell ...命令
            time_out:        执行超时时间(s),默认360s
        :return:
            命令执行返回的字符串,如超时会返回空字符串
        """
        time_count = 0
        cmd_return = ""
        str_cmd = " ".join(cmd)
        str_cmd = str_cmd.replace("adb", "adb -s " + SeaOfStarsAW.SN)
        while time_count < time_out:
            try:
                logging.debug(str_cmd)
                if platform.system() == "Windows":
                    proc = subprocess.Popen(str_cmd, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
                else:
                    proc = subprocess.Popen(shlex.split(str_cmd), stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
                if not is_nohup:
                    kill_proc = lambda p: p.kill()
                    timer = Timer(time_out, kill_proc, [proc])
                    try:
                        timer.start()
                        time_start = time.time()
                        stdout, stderr = proc.communicate()
                        time_end = time.time()
                        if (time_end - time_start) >= time_out:
                            # 命令超时
                            logging.warning("Cmd time out" + str(time_out) + " Seconds")
                            time_count = time_out
                        else:
                            if stdout is not None:
                                if proc.poll() is None:
                                    proc.stdout.readline()
                                    proc.stdout.flush()
                                cmd_return += (
                                    str(stdout) if not stdout else stdout.decode(chardet.detect(stdout)['encoding']))
                            if str(stderr) is not None and ("error: device" in str(stderr) and "not found" in str(stderr)):
                                # 未找到手机等待20s
                                logging.warning("Phone lost,wait for 20 Seconds")
                                time_count += 20
                                time.sleep(20)
                                cmd_return += (
                                    str(stdout) if not stdout else stdout.decode(chardet.detect(stdout)['encoding']))
                            else:
                                stderr = str(stderr, "utf-8")
                                if stdout:
                                    cmd_return += str(stderr)
                                if is_print_return:
                                    logging.debug("执行返回值:\n" + cmd_return)
                                # 正常结束
                                logging.debug("cmd takes %s Seconds.", str(float('%.1f' % (time_end - time_start))))
                                time_count = time_out
                    except Exception as err:
                        logging.error(err)
                    finally:
                        time_count += 60
                        timer.cancel()
                else:
                    break
            except Exception as err:
                # 非法命令
                logging.error("Cmd illegal!Please check." + str(err))
            finally:
                time_count += 60
        if is_check_return and "error" in cmd_return and "closed" in cmd_return:
            logging.error("execute the command %s hava error closed!" % str_cmd)
            SeaOfStarsAW.adb_cmd(cmd)
        else:
            return cmd_return

    @staticmethod
    def hmos_update(*cmd, time_out=60 * 20, is_print_return=True):
        """
        向设备发送adb命令执行，并获取返回值，默认执行时间超过360秒会强制结束

        Note:
            默认执行时间超过360秒会强制结束

        :param
            str_cmd:         要执行的adb命令,需要带完整地 adb shell ...命令
            time_out:        执行超时时间(s),默认360s
        :return:
            命令执行返回的字符串,如超时会返回空字符串
        """
        time_count = 0
        cmd_return = ""
        str_cmd = " ".join(cmd)
        while time_count < time_out:
            try:
                logging.debug(str_cmd)
                if platform.system() == "Windows":
                    proc = subprocess.Popen(str_cmd, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
                else:
                    proc = subprocess.Popen(shlex.split(str_cmd), stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
                kill_proc = lambda p: p.kill()
                timer = Timer(time_out, kill_proc, [proc])
                try:
                    timer.start()
                    time_start = time.time()
                    stdout, stderr = proc.communicate()
                    time_end = time.time()
                    if (time_end - time_start) >= time_out:
                        # 命令超时
                        logging.warning("Cmd time out" + str(time_out) + " Seconds")
                        time_count = time_out
                    else:
                        if stdout is not None:
                            if proc.poll() is None:
                                proc.stdout.readline()
                                proc.stdout.flush()
                            cmd_return += (
                                str(stdout) if not stdout else stdout.decode(chardet.detect(stdout)['encoding']))
                        if str(stderr) is not None and ("error: device" in str(stderr) and "not found" in str(stderr)):
                            # 未找到手机等待20s
                            logging.warning("Phone lost,wait for 20 Seconds")
                            time_count += 20
                            time.sleep(20)
                            cmd_return += (
                                str(stdout) if not stdout else stdout.decode(chardet.detect(stdout)['encoding']))
                        else:
                            stderr = str(stderr, "utf-8")
                            if stdout:
                                cmd_return += str(stderr)
                            if is_print_return:
                                logging.debug("执行返回值:\n" + cmd_return)
                            # 正常结束
                            logging.debug("cmd takes %s Seconds.", str(float('%.1f' % (time_end - time_start))))
                            time_count = time_out
                except Exception as err:
                    logging.error(err)
                finally:
                    time_count += 60
                    timer.cancel()
            except Exception as err:
                # 非法命令
                logging.error("Cmd illegal!Please check." + str(err))
            finally:
                time_count += 60
        else:
            return cmd_return

    @staticmethod
    @Device_Init_Check
    def get_app_list(is_only_system_app=False, is_only_other_app=False):
        """
        读取手机已安装app包名

        :param
            is_only_systemapp:  要执行的adb命令,需要带完整地 adb shell ...命令
            is_only_otherapp:   要执行的adb命令,需要带完整地 adb shell ...命令
        :return:
            包名数组,如["com.netease.nie.yosemite","com.t2ksports.nba2k20and"]
        """
        query_cmd = "pm list packages"
        if is_only_system_app:
            query_cmd += " -s"
        if is_only_other_app:
            query_cmd += " -3"
        pm_list_return = SeaOfStarsAW.adb_cmd("adb shell", query_cmd, is_print_return=False)
        pm_list = pm_list_return.splitlines()
        pm_list = [p.split(":")[1] for p in pm_list if p]
        return pm_list

    @staticmethod
    @Device_Init_Check
    def get_android_sdk():
        """
        获取android sdk版本

        Note:
            SDK对应表如下:
            API 33 - Android 10(T) 2022年8月15日
            API 31,32 - Android 10(S) 2021年10月4日
            API 30 - Android 10(R) 2020年9月9日
            API 29 - Android 10(Q) 2019年9月3日
            API 28 - Android 9(P) 2018年8月6日
            API 27 - Android 8(O) 2017年12月5日
            API 26 - Android 7(M) 2016年8月22日

        :return:
            sdk值,如 26,27...
        """
        return SeaOfStarsAW.adb_cmd("adb shell getprop ro.build.version.sdk").strip()

    @staticmethod
    @Device_Init_Check
    def get_phone_name():
        """
        获取设备代号名

        :return:
            代号名, SEA_AL00_VB
        """
        return SeaOfStarsAW.adb_cmd("adb shell getprop ro.board.boardname").strip()

    @staticmethod
    @Device_Init_Check
    def get_chipname():
        """
        获取芯片代号名_CS/ES

        :return:
            代号名, Baltimore_cs/es
        """
        return SeaOfStarsAW.adb_cmd("adb shell getprop ro.vendor.board.chiptype").strip()

    @staticmethod
    @Device_Init_Check
    def get_phone_version():
        """
        获取系统版本号

        :return:
            代号名, Baltimore_cs/es
        """
        return SeaOfStarsAW.adb_cmd("adb shell getprop ro.build.display.id").strip()

    @staticmethod
    @Device_Init_Check
    def dump_prop_info(dirpath):
        """
        获取芯片代号名_CS/ES

        :return:
            代号名, Baltimore_cs/es
        """
        allprop = SeaOfStarsAW.adb_cmd("adb shell getprop", is_check_return=False)
        with open(os.path.join(dirpath, "getprop.txt"), 'w', encoding='utf-8', newline='') as f:
            f.write(allprop)

    @staticmethod
    @Device_Init_Check
    def is_locked():
        """
        通过 `adb shell dumpsys window policy` 判断设备屏幕是否锁屏

        :raises:
            DeviceError: 锁屏状态结果无法判定

        :return:
            True or False 设备屏幕是否锁屏
        """
        lockScreenRE = re.compile('(?:mShowingLockscreen|isStatusBarKeyguard|showing)=(true|false)')
        m = lockScreenRE.search(SeaOfStarsAW.adb_cmd('adb shell dumpsys window policy', is_print_return=False))
        # if not m:
        #     raise DeviceError("Couldn't determine screen lock state")
        if m.group(1) == 'true':
            logging.info("判断解锁状态:已锁屏.")
            return True
        else:
            cmd_return = SeaOfStarsAW.adb_cmd('adb shell "dumpsys deviceidle | grep mScreenOn"')
            if "false" in cmd_return:
                return True
        return False

    @staticmethod
    @Device_Init_Check
    def unlock_device():
        """
        华为手机通过 `input keyevent` 事件解锁屏幕
        其他手机通过 `swipe` 事件解锁屏幕

        :return:
            None
        """
        if SeaOfStarsAW.device_type == SeaOfStarsAW.DeviceType.HISI or SeaOfStarsAW.device_type == SeaOfStarsAW.DeviceType.EMUI :
            SeaOfStarsAW.adb_cmd('adb shell input keyevent MENU')
            SeaOfStarsAW.adb_cmd('adb shell input keyevent MENU')
            SeaOfStarsAW.adb_cmd('adb shell input keyevent BACK')
        else:
            logging.info("滑动解锁屏幕")
            print(111)
            if not SeaOfStarsAW.ut_device.info['screenOn']:
                SeaOfStarsAW.adb_cmd("adb shell input keyevent POWER")
            SeaOfStarsAW.ut_device.swipe(0.1, 0.9, 0.9, 0.1)

    @staticmethod
    @Device_Init_Check
    def return_launcher():
        """
        通过 `keyevent HOME` 事件返回桌面

        :return:
            None
        """
        SeaOfStarsAW.adb_cmd('adb shell input keyevent HOME')
        time.sleep(2)

    @staticmethod
    @Device_Init_Check
    def return_back():
        """
        通过 `keyevent HOME` 事件返回桌面

        :return:
            None
        """
        SeaOfStarsAW.adb_cmd('adb shell input keyevent BACK')
        time.sleep(2)


    @staticmethod
    @Device_Init_Check
    def set_screen_lock_long_time():
        """
        通过 `settings put system screen_off_timeout` 将屏幕锁定时间改成30分钟

        :return:
            None
        """
        # SeaOfStarsAW.adb_cmd('adb shell settings put system screen_off_timeout 1800000')
        SeaOfStarsAW.adb_cmd('adb shell settings put system screen_off_timeout 6000000')
        SeaOfStarsAW.adb_cmd('adb shell settings get system screen_off_timeout')
        time.sleep(1)

    @staticmethod
    @Device_Init_Check
    def set_system_language_cn():
        """
        通过 `settings put system system_locales zh-Hans-CN` 将系统语言改成中文,过程会重启手机并等待20s

        :return:
            None
        """
        system_language = SeaOfStarsAW.adb_cmd('adb shell "settings get system system_locales"')
        if SeaOfStarsAW.device_type == SeaOfStarsAW.DeviceType.HISI and"zh-Hans-CN" not in system_language:
            SeaOfStarsAW.adb_cmd('adb shell "settings put system system_locales zh-Hans-CN"')
            SeaOfStarsAW.adb_cmd('adb reboot')
            SeaOfStarsAW.adb_cmd('adb wait-for-device')
            time.sleep(20)
        time.sleep(1)

    @staticmethod
    @Device_Init_Check
    def stop_app(package_name):
        """
        通过 `am force-stop` 将指定app强行停止

        :return:
            None
        """
        SeaOfStarsAW.adb_cmd('adb shell am force-stop', package_name)
        time.sleep(2)

    @staticmethod
    @Device_Init_Check
    def stop_apps(app_list):
        """
        通过 `am force-stop` 将指定app列表强行停止

        :return:
            None
        """
        for per_app in app_list:
            SeaOfStarsAW.stop_app(per_app)
            time.sleep(0.5)
        time.sleep(2)

    @staticmethod
    @Device_Init_Check
    # @UiAutomatorService_Check
    def clear_backgroud(save_dir_path=None, case_name=None, time_stamp=None):
        """
        通过android默认的多任务后台,向上滑动,清空所有后台

        :return:
            True,False
        """
        SeaOfStarsAW.return_launcher()
        SeaOfStarsAW.adb_cmd("adb shell input keyevent 187")
        time.sleep(1)
        if SeaOfStarsAW.device_type == SeaOfStarsAW.DeviceType.HISI:
            if SeaOfStarsAW.ut_device.exists(resourceId="com.android.launcher3:id/snapshot"):
                while not SeaOfStarsAW.ut_device.exists(resourceId="com.android.launcher3:id/clear_all"):
                    SeaOfStarsAW.ut_device(scrollable=True).fling.horiz.toBeginning(max_swipes=1000)
                    time.sleep(1)
                SeaOfStarsAW.ut_device(resourceId="com.android.launcher3:id/clear_all").click()
                # SeaOfStarsAW.ut_device.swipe(
                # 600, 2000, 600, 500, 0.05)
                time.sleep(1)
            else:
                SeaOfStarsAW.return_launcher()
        elif SeaOfStarsAW.device_type == SeaOfStarsAW.DeviceType.EMUI:
            if SeaOfStarsAW.ut_device.exists(resourceId="com.huawei.android.launcher:id/clearbox"):
                SeaOfStarsAW.ut_device(resourceId="com.huawei.android.launcher:id/clearbox").click()
            elif SeaOfStarsAW.ut_device.exists(resourceId="com.huawei.android.launcher:id/empty_message"):
                SeaOfStarsAW.return_launcher()
        elif SeaOfStarsAW.device_type == SeaOfStarsAW.DeviceType.XIAOMI:
            if SeaOfStarsAW.ut_device.exists(resourceId="com.miui.home:id/clearAnimView"):
                SeaOfStarsAW.ut_device(resourceId="com.miui.home:id/clearAnimView").click()
        if save_dir_path:
            SeaOfStarsAW.adb_cmd("adb shell input keyevent 187")
            time.sleep(1)
            SeaOfStarsAW.screen_shot(save_dir_path, case_name, "clear_backgroud", time_stamp)
            SeaOfStarsAW.return_launcher()
        time.sleep(2)

    @staticmethod
    @Device_Init_Check
    def is_connected_wifi():
        """
        通过 `getprop wifi.active.interface` 判断手机是否已连接wifi, 如返回非空字符串如wlan0则表示已连接

        :return:
            None
        """
        cmd_return = SeaOfStarsAW.adb_cmd(r'adb shell getprop wifi.active.interface')
        cmd_return = cmd_return.strip()
        if cmd_return != "":
            return True
        else:
            return False

    @staticmethod
    @Device_Init_Check
    def connect_wifi( wifi_name, wifi_passwd):
        """
        通过 wifi.apk 连接指定的热点wifi

        :return:
            None
        """
        SeaOfStarsAW.adb_cmd(r'adb install \\10.163.180.196\ux_share\TestResource\Phone\icekirin\game\wifi.apk')
        SeaOfStarsAW.adb_cmd('adb shell svc wifi enable')
        time.sleep(2)
        SeaOfStarsAW.adb_cmd('adb shell am start -n com.huawei.hisi.connecttowifi/.MainActivity -e ssid %s -e password %s'
                       % (wifi_name, wifi_passwd))
        time.sleep(5)
        SeaOfStarsAW.adb_cmd('adb shell input keyevent HOME')
        time.sleep(2)
        SeaOfStarsAW.stop_app("com.huawei.hisi.connecttowifi")

    @staticmethod
    @Device_Init_Check
    def disconnect_wifi():
        """
        断开 wifi 连接

        :return:
            None
        """
        logging.info("断开wifi")
        SeaOfStarsAW.adb_cmd('adb shell svc wifi disable')
        time.sleep(2)

    @staticmethod
    @Device_Init_Check
    def connect_wifi():
        """
        断开 wifi 连接

        :return:
            None
        """
        SeaOfStarsAW.adb_cmd('adb shell svc wifi enable')
        time.sleep(5)

    @staticmethod
    @Device_Init_Check
    def screen_shot(save_dir_path,
                    case_name, scene_name, time_stamp):
        """
        截图

        :param
            trace_path:     截图保存的目录
            case_name:      用例编号,如heavyLoad_1
            scene_name:     场景名,如douyin_videoSwitch
            time_stamp:     时间戳
        :return:
            None
        """
        save_jpg_name = "{}_{}_{}.jpg".format(case_name, scene_name, time_stamp)
        SeaOfStarsAW.ut_device.screenshot(save_jpg_name)
        shutil.move(save_jpg_name, os.path.join(save_dir_path, save_jpg_name))
        time.sleep(1)

    @staticmethod
    @Device_Init_Check
    def start_perfetto_trace():
        """
        开始抓取perfetto trace

        :return:
            None
        """
        # 停止空闲perfetto抓取
        SeaOfStarsAW.perfetto_thread.stop_perfetto()
        # 初始化trace抓取
        SeaOfStarsAW.adb_cmd(r'adb shell "setprop persist.traced.enable 1"')
        SeaOfStarsAW.adb_cmd(r'adb shell "echo 0 > /d/tracing/tracing_on"')
        time.sleep(1)
        SeaOfStarsAW.adb_cmd(r'adb shell rm /data/misc/perfetto-traces/trace')
        # SeaOfStarsAW.adb_cmd(r'adb push .\Resources\perfetto.pbtxt /data/local/tmp')
        SeaOfStarsAW.trace_start_timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        # with open(os.path.join("Resources", "perfetto.pbtxt")) as trace_config:
        #     cmd_list = ["adb", "-s", SeaOfStarsAW.SN, "shell", "perfetto", "-c", "-", "--txt", "-o",
        #                     "/data/misc/perfetto-traces/trace","--detach=perf_debug"]
        #     logging.info(" ".join(cmd_list))
        #     subprocess.run(cmd_list, stdin=trace_config, check=True)
        SeaOfStarsAW.adb_cmd("adb push {} {}".format(os.path.join("Resources", "perfetto.pbtxt"), "/data/local/tmp/"))
        SeaOfStarsAW.adb_cmd('adb shell "cat /data/local/tmp/perfetto.pbtxt | perfetto --txt -c - -o /data/misc/perfetto-traces/trace --detach=perf_debug"')
        # SeaOfStarsAW.adb_cmd('adb shell "perfetto -c /data/local/tmp/perfetto.pbtxt --txt - -o /data/misc/perfetto-traces/trace --detach=perf_debug"')
        time.sleep(1)

    @staticmethod
    @Device_Init_Check
    def stop_and_get_perfetto_trace(trace_path, case_name, scene_name, next_scene_name, screenshot_dir_path, is_screen_shot=True):
        """
        结束抓取perfetto trace

        :param
            trace_path:     Trace保存的目录
            case_name:      用例编号,如heavyLoad_1
            scene_name:     场景名,如douyin_videoSwitch
            time_stamp:     时间戳
        :return:
            None
        """
        SeaOfStarsAW.adb_cmd(r'adb shell "perfetto --attach=perf_debug --stop"')
        time.sleep(1)
        time_stamp = time.strftime("%H%M%S", time.localtime())
        trace_name = "{}-{}-{}_{}.trace".format(case_name, scene_name, SeaOfStarsAW.trace_start_timestamp, time_stamp)
        SeaOfStarsAW.adb_cmd(r'adb pull /data/misc/perfetto-traces/trace '+trace_path, is_print_return=False)
        time.sleep(1)
        os.rename(os.path.join(trace_path, "trace"), os.path.join(trace_path, trace_name))
        time.sleep(1)
        logging.info("{}抓取结束,当前温度:{}℃".format(trace_name, SeaOfStarsAW.get_current_tempreture()))
        if is_screen_shot and screenshot_dir_path:
            SeaOfStarsAW.screen_shot(screenshot_dir_path, case_name, scene_name, time_stamp)
        # 开始抓取空闲Perfetto thread

        if "-LAST" not in next_scene_name:
            SeaOfStarsAW.perfetto_thread.start_perfetto(trace_path, "{}-{}-PRE".format(case_name, next_scene_name))
        else:
            SeaOfStarsAW.perfetto_thread.start_perfetto(trace_path, "{}-{}".format(case_name, next_scene_name))

    @staticmethod
    @Device_Init_Check
    def stop_perfetto_service():
        """
        结束perfetto 服务

        :param
            trace_path:     Trace保存的目录
            case_name:      用例编号,如heavyLoad_1
            scene_name:     场景名,如douyin_videoSwitch
            time_stamp:     时间戳
        :return:
            None
        """
        SeaOfStarsAW.adb_cmd(r'adb shell "perfetto --attach=perf_debug --stop"')
        time.sleep(2)

    @staticmethod
    @Device_Init_Check
    def stop_and_get_perfetto_trace_test(trace_path):
        """
        结束抓取perfetto trace，测试接口, 正式用例中请勿使用

        :param
            trace_path:     Trace保存的目录
            case_name:      用例编号,如heavyLoad_1
            scene_name:     场景名,如douyin_videoSwitch
            time_stamp:     时间戳
        :return:
            None
        """
        SeaOfStarsAW.adb_cmd(r'adb shell "perfetto --attach=perf_debug --stop"')
        time.sleep(2)
        SeaOfStarsAW.adb_cmd(r'adb pull /data/misc/perfetto-traces/trace ' + trace_path)
        time.sleep(1)

    @staticmethod
    @Device_Init_Check
    def find_app_from_launcher(app_chinese_name, time_out=60):
        """
        在launcher的应用程序抽屉找到app图标，注意: 需要系统语言为中文

        :param
            app_chinese_name:     app在launhcer抽屉上的中文名全名
        :return:
            图标中心点坐标
        """
        # 回到桌面主页
        print(SeaOfStarsAW.ut_device.exists(text=app_chinese_name))
        SeaOfStarsAW.return_launcher()
        SeaOfStarsAW.return_launcher()
        logging.info("桌面启动{}应用".format(app_chinese_name))
        if SeaOfStarsAW.device_type == SeaOfStarsAW.DeviceType.HISI:
            SeaOfStarsAW.ut_device(scrollable=True).fling()
            time_start = time.time()
            while (not SeaOfStarsAW.ut_device.exists(text=app_chinese_name) or
                   SeaOfStarsAW.ut_device(text=app_chinese_name).center()[1] > SeaOfStarsAW.device_info[
                       "displayHeight"] * 0.94) and (time.time() - time_start) < time_out:
                SeaOfStarsAW.ut_device.swipe_ext("up")
            time.sleep(1)
            if SeaOfStarsAW.ut_device.exists(text=app_chinese_name):
                return SeaOfStarsAW.ut_device(text=app_chinese_name).center()
            elif SeaOfStarsAW.ut_device.exists(description=app_chinese_name):
                return SeaOfStarsAW.ut_device(description=app_chinese_name).center()
            else:
                raise AssertionError("未找到app")
                return False
        elif SeaOfStarsAW.device_type == SeaOfStarsAW.DeviceType.EMUI:
            time_start = time.time()
            while not SeaOfStarsAW.ut_device.exists(text=app_chinese_name) and (time.time() - time_start) < time_out:
                SeaOfStarsAW.swipe_right()
                # time_stamp = time.strftime("%H%M%S", time.localtime())
                # SeaOfStarsAW.screen_shot(SeaOfStarsAW.public_screen_shot_dir, app_chinese_name, "find_app_from_launcher", time_stamp)
            time.sleep(1)
            if SeaOfStarsAW.ut_device.exists(text=app_chinese_name):
                return SeaOfStarsAW.ut_device(text=app_chinese_name).center()
            elif SeaOfStarsAW.ut_device.exists(description=app_chinese_name):
                return SeaOfStarsAW.ut_device(description=app_chinese_name).center()
            else:
                raise AssertionError("未找到app")
                return False
        else:
            time_start = time.time()
            while not SeaOfStarsAW.ut_device.exists(text=app_chinese_name) and (time.time() - time_start) < time_out:
                SeaOfStarsAW.swipe_right()
            time.sleep(1)
            if SeaOfStarsAW.ut_device.exists(text=app_chinese_name):
                return SeaOfStarsAW.ut_device(text=app_chinese_name).center()
            elif SeaOfStarsAW.ut_device.exists(description=app_chinese_name):
                return SeaOfStarsAW.ut_device(description=app_chinese_name).center()
            else:
                raise AssertionError("未找到app")
                return False

    @staticmethod
    @Device_Init_Check
    def swipe_left(sleep_time=5):
        logging.info("左滑{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(300, 1500, 600, 1500, 0.03)
        time.sleep(sleep_time)

    @staticmethod
    @Device_Init_Check
    def swipe_right(sleep_time=5):
        logging.info("右滑{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(600, 1500, 300, 1500, 0.03)
        time.sleep(sleep_time)

    @staticmethod
    @Device_Init_Check
    def adb_swipe(x1, y1, x2, y2, speed):
        """
        向设备发送adb swipe命令, 共用一个shell窗口, 避免频繁启动adb

        :param
            x1:        起点坐标x
            y1:        起点坐标y
            x2:        终点坐标x
            y2:        终点坐标y
            speed:     单位:毫秒
        :return:
        """
        cmd = "input swipe {} {} {} {} {} \n".format(x1, y1, x2, y2, speed)
        SeaOfStarsAW.ADB_PROC.stdin.write(cmd.encode())
        SeaOfStarsAW.ADB_PROC.stdin.flush()

    @staticmethod
    @Device_Init_Check
    def scroll_up(sleep_time=5):
        logging.info("上滑{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(550, 500, 550, 2000, 0.04)
        time.sleep(sleep_time)

    @staticmethod
    @Device_Init_Check
    def scroll_down(sleep_time=5):
        logging.info("下滑{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(550, 2000, 550, 500, 0.04)
        time.sleep(sleep_time)

    @staticmethod
    @Device_Init_Check
    def quick_swipe_left(sleep_time=5):
        logging.info("快速左滑{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(300, 1500, 800, 1500, 0.02)
        time.sleep(sleep_time)

    @staticmethod
    @Device_Init_Check
    def quick_swipe_right(sleep_time=5):
        logging.info("快速右滑{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(800, 1500, 300, 1500, 0.02)
        time.sleep(sleep_time)

    @staticmethod
    @Device_Init_Check
    def quick_scroll_up(sleep_time=5):
        logging.info("快速上滑{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(550, 500, 550, 2000, 0.01)
        time.sleep(sleep_time)

    @staticmethod
    @Device_Init_Check
    def quick_scroll_down(sleep_time=5):
        logging.info("快速下滑{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(550, 2000, 550, 200, 0.04)
        time.sleep(sleep_time)

    @staticmethod
    @Device_Init_Check
    def statusbar_pull_down(sleep_time=5):
        logging.info("状态栏下拉{}秒".format(sleep_time))
        SeaOfStarsAW.ut_device.swipe(550, 0, 550, 2100, 0.1)
        time.sleep(sleep_time)

    @staticmethod
    @Device_Init_Check
    def click_pos_from_launcher(pos, sleep_time=15):
        """
        点击坐标，默认等待15秒,用于应用启动

        :param
            pos:     tuple,如(100,100)
        :return:
            None
        """
        if len(pos) > 1:
            logging.info("点击坐标:{},{}".format(pos[0], pos[1]))
            SeaOfStarsAW.ut_device.click(pos[0], pos[1])
            logging.info("等待:{}秒".format(sleep_time))
            time.sleep(sleep_time)
        else:
            logging.info("pos为{}".format(pos))
            raise AssertionError("坐标有误")

    @staticmethod
    @Device_Init_Check
    def get_current_tempreture(temp_node=None):
        temp_node = SeaOfStarsAW.shell_temp_path if not temp_node else temp_node
        if temp_node:
            temp = int(int(SeaOfStarsAW.adb_cmd('adb shell "cat {}"'.format(temp_node)).strip()) / 1000)
        else:
            temp = 0
        logging.info("当前温度:{}℃".format(temp))
        return temp

    @staticmethod
    @Device_Init_Check
    def wait_tempreture_clam_down(dst_tempreture,is_screen_off=True, time_out=60*10):
        """
        等待手机battery温度降到指定温度,会一直sleep阻塞,超时时间60*10秒

        :param
            tempreture:     指定温度
        :return:
            None
        """
        if SeaOfStarsAW.shell_temp_path:
            time_start = time.time()
            if not SeaOfStarsAW.is_locked() and is_screen_off:
                logging.info("灭屏冷却")
                SeaOfStarsAW.adb_cmd("adb shell input keyevent POWER")
                time.sleep(2)
            while SeaOfStarsAW.get_current_tempreture() > dst_tempreture and (time.time() - time_start) < time_out:
                logging.info("等待冷却至{}℃".format(dst_tempreture))
                time.sleep(10)
            if (time.time() - time_start) >= time_out:
                logging.info("冷却等待时长达到{},继续测试".format(time_out))
            else:
                logging.info("已冷却至{}℃".format(dst_tempreture))
            if SeaOfStarsAW.is_locked():
                SeaOfStarsAW.unlock_device()


    @staticmethod
    @Device_Init_Check
    def dump_phone_info(dirpath):
        content = ""
        phone_dict = {
            "chip": SeaOfStarsAW.get_chipname(),
            "phone":SeaOfStarsAW.get_phone_name(),
            "version": SeaOfStarsAW.get_phone_version(),
        }
        for key,val in phone_dict.items():
            content += "{}:{}\n".format(key,val)
        filename = "[{}][{}][{}]_basic_info.txt".format(phone_dict["chip"], phone_dict["phone"], phone_dict["version"])
        with open(os.path.join(dirpath, filename), 'w', encoding='utf-8', newline='') as f:
            f.write(content)

    @staticmethod
    @Device_Init_Check
    def dump_app_info(dirpath):
        app_list = SeaOfStarsAW.get_app_list(is_only_other_app=True)
        content_list = []
        for per_app in app_list:
            content = per_app+":"
            cmd_return = SeaOfStarsAW.adb_cmd('adb shell "dumpsys package {} | grep versionName"'.format(per_app)).strip().split("=")
            if len(cmd_return) > 1:
                content += cmd_return[1]
            content_list.append(content)
        with open(os.path.join(dirpath, "app_info.txt"), 'w', encoding='utf-8', newline='') as f:
            f.write("\n".join(content_list))

    @staticmethod
    @Device_Init_Check
    def skip_emui_guide(sleep_time=5):
        logging.info("跳过EMUI新手流程".format(sleep_time))
        SeaOfStarsAW.adb_cmd("adb shell pm disable com.huawei.hwstartupguide")
        time.sleep(sleep_time)

    @staticmethod
    def start_hiperfetto_monitor(func=None):
        if func:
            @wraps(func)
            def wrapper(*args, **kwargs):
                logging.info("开始hiperfetto注入trace")
                SeaOfStarsAW.adb_cmd('adb remount', is_print_return=False)
                SeaOfStarsAW.adb_cmd('adb shell "pkill hiperfetto"')
                SeaOfStarsAW.adb_cmd(
                    'adb shell "nohup /data/local/tmp/hiperfetto > /sdcard/hiperfetto.log"',
                    is_nohup=True)
                res = func(*args, **kwargs)
                return res
            return wrapper
        else:
            logging.info("开始hiperfetto注入trace")
            SeaOfStarsAW.adb_cmd('adb remount', is_print_return=False)
            SeaOfStarsAW.adb_cmd('adb shell "pkill hiperfetto"')
            SeaOfStarsAW.adb_cmd(
                'adb shell "nohup /data/local/tmp/hiperfetto > /sdcard/hiperfetto.log"',
                is_nohup=True)

    @staticmethod
    def stop_hiperfetto_monitor(func=None):
        if func:
            @wraps(func)
            def wrapper(*args, **kwargs):
                logging.info("停止hiperfetto注入trace")
                SeaOfStarsAW.adb_cmd('adb shell "pkill hiperfetto"')
                res = func(*args, **kwargs)
                return res
            return wrapper
        else:
            logging.info("停止hiperfetto注入trace")
            SeaOfStarsAW.adb_cmd('adb shell "pkill hiperfetto"')

    @staticmethod
    @Device_Init_Check
    def start_hikitsbin_monitor():
        logging.info("开始记录hizee数据")
        time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        SeaOfStarsAW.adb_cmd('adb remount', is_print_return=False)
        SeaOfStarsAW.adb_cmd('adb shell "pkill HiKitsBin"')
        SeaOfStarsAW.adb_cmd('adb shell "rm -rf /sdcard/HiKitsBin"')
        SeaOfStarsAW.adb_cmd('adb shell "mkdir /sdcard/HiKitsBin"')
        SeaOfStarsAW.adb_cmd('adb shell "nohup /data/local/tmp/HiKitsBin > /sdcard/HiKitsBin/HiKitsBin_{}.log"'.format(time_stamp), is_nohup=True)

    @staticmethod
    @Device_Init_Check
    def stop_hikitsbin_monitor(result_dir_path):
        logging.info("停止记录hizee数据")
        time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        SeaOfStarsAW.adb_cmd('adb shell "pkill HiKitsBin"')
        time.sleep(1)
        SeaOfStarsAW.adb_cmd('adb pull /sdcard/HiKitsBin {}'.format(result_dir_path))
        os.rename(os.path.join(result_dir_path,"HiKitsBin","HikitsBin.csv"), os.path.join(result_dir_path,"HiKitsBin","HikitsBin_{}.csv".format(time_stamp)))

    @staticmethod
    @Device_Init_Check
    def start_ddr_monitor():
        logging.info("开始记录ddr数据")
        time_stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        SeaOfStarsAW.adb_cmd('adb remount', is_print_return=False)
        SeaOfStarsAW.adb_cmd('adb shell "pkill sh /data/local/tmp/ddr.sh"')
        SeaOfStarsAW.adb_cmd('adb shell "rm /data/local/tmp/ddr_info.txt"')
        SeaOfStarsAW.adb_cmd(r"adb push {} {}".format(os.path.join(".","Resources","ddr.sh"), "/data/local/tmp"), is_print_return=False)
        SeaOfStarsAW.adb_cmd('adb shell "chmod 777 /data/local/tmp/*"')
        SeaOfStarsAW.adb_cmd('adb shell "nohup sh /data/local/tmp/ddr.sh > /sdcard/test_{}.log"'.format(time_stamp), is_nohup=True)

    @staticmethod
    @Device_Init_Check
    def stop_ddr_monitor(result_dir_path):
        logging.info("停止记录ddr数据")
        SeaOfStarsAW.adb_cmd('adb shell "pkill sh /data/local/tmp/ddr.sh"')
        time.sleep(1)
        SeaOfStarsAW.adb_cmd('adb pull /data/local/tmp/ddr_info.txt {}'.format(result_dir_path))

    @staticmethod
    def check_status(**kw):
        try:
            for i in range(10):
                if SeaOfStarsAW.ut_device(**kw).exists:
                    return True
                time_stamp = time.strftime('%H%M%S', time.localtime())
                SeaOfStarsAW.ut_device.screenshot(
                    SeaOfStarsAW.error_screenshot_path + '/' + SeaOfStarsAW.current_running_class_name + '_' + time_stamp + '.png')
                raise ElementNotFoundError('未找到元素-' + json.dumps(kw, ensure_ascii=False))
        except u2.exceptions.JSONRPCError as e:
            logging.error(e)


class ElementNotFoundError(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.errorInfo = error_info

    def __str__(self):
        return self.errorInfo
