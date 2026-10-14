"""华为运动健康动态用例的运动、健康生活和扫码公共操作。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class HuaweiHealthDynamicCase(DynamicAppCase):
    PACKAGE = 'com.huawei.health'
    all_app_package_list = [PACKAGE]
    PERMISSIONS = (
        'ACCESS_COARSE_LOCATION',
        'ACCESS_FINE_LOCATION',
        'ACTIVITY_RECOGNITION',
        'CAMERA',
        'READ_PHONE_STATE',
    )

    BOTTOM_TAB_ID = 'content'

    def bottom_ready(self):
        return self.has(text='今日', rid=self.BOTTOM_TAB_ID)

    def today_ready(self):
        return self.has(text='今日', rid='action_bar_title')

    def sport_ready(self):
        return self.has(rid='sport_tab_titlebar')

    def device_ready(self):
        return (self.has(text='设备', rid='action_bar_title')
                and self.has(rid='switch_device'))

    def scan_ready(self):
        return ('ScanKitActivity' in self.current_app()['activity']
                and self.has(text='扫描二维码/条码', rid='title_scan'))

    def dismiss_known_popup(self):
        """关闭首次启动/首次进入页面的引导，不依赖固定屏幕坐标。"""
        if self.has(text='稍后', rid='dialog_btn_negative'):
            self.click(text='稍后', rid='dialog_btn_negative')
            time.sleep(.7)
        if self.has(text='知道了', rid='button'):
            self.click(text='知道了', rid='button')
            time.sleep(.7)
        elif self.has(desc='关闭', rid='close_img'):
            self.click(desc='关闭', rid='close_img')
            time.sleep(.7)
        if self.has(text='忽略'):
            self.click(text='忽略')
            time.sleep(.5)

    def main_page(self):
        # 促销页没有关闭按钮；系统返回可回到带底栏的 MainActivity。
        if 'PromotionPolicyActivity' in self.current_app()['activity']:
            self.back()
        self.return_to(self.bottom_ready, '未返回华为运动健康主界面')
        self.dismiss_known_popup()
        self.switch_bottom('今日')

    def launch(self):
        self.start()
        self.main_page()

    def switch_bottom(self, name):
        ready = {
            '今日': self.today_ready,
            '运动': self.sport_ready,
            '设备': self.device_ready,
        }[name]
        if ready():
            return
        self.transition(lambda: self.click(text=name, rid=self.BOTTOM_TAB_ID),
                        ready, '华为运动健康未切换到底部“{}”页'.format(name))
        self.dismiss_known_popup()
        self.wait_for(ready, '华为运动健康“{}”页未加载'.format(name))

    def select_outdoor_running(self):
        self.switch_bottom('运动')
        if self.has(desc='开始运动', rid='section_img_sport_entrance_begin'):
            return
        self.transition(lambda: self.click(text='户外跑步'),
                        lambda: self.has(desc='开始运动',
                                         rid='section_img_sport_entrance_begin'),
                        '户外跑步页面未加载')

    def workout_ready(self):
        return ('TrackMainMapActivity' in self.current_app()['activity']
                and self.has(desc='暂停', rid='track_main_page_btn_pause'))

    def start_workout(self):
        self.select_outdoor_running()
        self.click(desc='开始运动', rid='section_img_sport_entrance_begin')
        # 未完善个人资料时会先弹出提示；选择“稍后”后才真正开始计时。
        deadline = time.monotonic() + 25
        while time.monotonic() < deadline:
            if self.workout_ready():
                return
            if self.has(text='稍后', rid='dialog_btn_negative'):
                self.click(text='稍后', rid='dialog_btn_negative')
            time.sleep(.5)
        raise RuntimeError('户外跑步未进入运动计时页面；当前页面 {}'.format(self.current_app()))

    def long_press_node(self, duration=2.2, **selector):
        node = self.node(**selector)
        left, top, right, bottom = self.bounds(node)
        width, height = self.d.window_size()
        x = min(width - 1, max(0, round((left + right) / 2)))
        y = min(height - 1, max(0, round((top + bottom) / 2)))
        self.foreground()
        # 坐标来自当前控件树的实时 bounds，而非写死分辨率；uiautomator2 的
        # long_click 在此设备上比同点 adb swipe 更稳定。
        self.d.long_click(x, y, duration=duration)

    def wait_and_end_workout(self):
        time.sleep(15)
        self.click(desc='暂停', rid='track_main_page_btn_pause')
        self.wait_for(lambda: self.has(desc='结束运动', rid='track_main_page_btn_stop'),
                      '暂停后未出现结束运动按钮', timeout=6)
        # 原地短时锻炼不会记录数据，当前版本会要求二次确认。长按只在确认框
        # 和主界面都未出现、且结束控件仍存在时重试一次，避免盲目连按。
        confirmed = False
        for _ in range(2):
            self.long_press_node(desc='结束运动', rid='track_main_page_btn_stop')
            deadline = time.monotonic() + 4
            while time.monotonic() < deadline:
                if self.has(text='结束运动', rid='dialog_btn_positive'):
                    self.click(text='结束运动', rid='dialog_btn_positive')
                    confirmed = True
                    break
                if self.bottom_ready():
                    return
                time.sleep(.4)
            if confirmed:
                break
            if not self.has(desc='结束运动', rid='track_main_page_btn_stop'):
                break
        self.wait_for(self.bottom_ready, '结束运动后未返回运动健康主界面', timeout=15)

    def today(self):
        if not self.bottom_ready():
            self.return_to(self.bottom_ready, '点击今日前未返回运动健康主界面')
        self.switch_bottom('今日')

    def open_clover(self):
        # 右侧小三叶草只负责切换首页模型；真正的详情入口是整个健康卡片。
        # 卡片未声明 clickable，但其 bounds 由控件树提供，可避免分辨率相关坐标。
        if not self.has(rid='health_life_clover'):
            self.transition(lambda: self.click(rid='clover_container'),
                            lambda: self.has(rid='health_life_clover'),
                            '首页未切换到三叶草模型')
        self.transition(lambda: self.click(rid='home_item_three_circle_card_layout'),
                        lambda: 'H5ProWebViewActivity' in self.current_app()['activity'],
                        '健康生活（三叶草）详情未打开')

    def return_to_main(self):
        self.return_to(self.bottom_ready, '未返回华为运动健康主界面')
        self.switch_bottom('今日')

    def device(self):
        self.switch_bottom('设备')
        self.dismiss_known_popup()
        self.wait_for(self.device_ready, '华为运动健康设备页未加载')

    def more_ready(self):
        return self.has(text='扫一扫', rid='list_popup_window_item_text')

    def open_more(self):
        self.transition(lambda: self.click(desc='更多选项', rid='hwappbarpattern_ok_icon'),
                        self.more_ready, '设备页更多功能菜单未打开')

    def scan_three_times(self):
        for _ in range(3):
            if not self.more_ready():
                self.open_more()
            self.transition(lambda: self.click(text='扫一扫',
                                                rid='list_popup_window_item_text'),
                            self.scan_ready, '扫一扫页面未打开')
            self.back()
            self.wait_for(self.device_ready, '扫一扫返回后未回到设备页')

    def home(self):
        # H5/扫码 Activity 可能吞掉系统上滑；先回到有底栏的主界面。
        if not self.bottom_ready():
            self.return_to(self.bottom_ready, '返回桌面前未回到运动健康主界面')
        super().home()
