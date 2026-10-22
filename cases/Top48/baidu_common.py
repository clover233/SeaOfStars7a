"""百度系列动态用例的等待、比例手势和逐步性能采集。"""
import logging
import time

from Cases.CaseBase import Case
from Cases.Top48.main_display import ForegroundNotReady, MainDisplayMixin
from aw_new import SeaOfStarsAW


class BaiduDynamicCase(Case):
    PACKAGE = ''
    TEST_TIME = 1
    PERMISSIONS = ()

    @property
    def d(self):
        return SeaOfStarsAW.ut_device

    @SeaOfStarsAW.function_log
    def set_up(self):
        if not self.d.app_info(self.PACKAGE):
            raise RuntimeError('未安装应用：{}'.format(self.PACKAGE))
        if SeaOfStarsAW.is_locked():
            SeaOfStarsAW.unlock_device()
        for permission in self.PERMISSIONS:
            result = self.d.shell('pm grant {} android.permission.{}'.format(self.PACKAGE, permission))
            if result.exit_code or 'Exception' in result.output or 'Error' in result.output:
                raise RuntimeError('授权失败 {}: {}'.format(permission, result.output))
        self._prepared = True

    def current_app(self):
        # 小米副屏也有 resumed activity；只读取 display 0。
        # 播放器挂载/页面切换会短暂丢失焦点，直接查询时也给出有限重试。
        for attempt in range(3):
            try:
                return MainDisplayMixin.current_app(self)
            except ForegroundNotReady:
                if attempt == 2:
                    raise
                time.sleep(.2)

    def foreground(self):
        current = self.current_app()
        if current['package'] != self.PACKAGE:
            raise RuntimeError('前台不是目标应用，停止操作：{}'.format(current))

    wait_for = MainDisplayMixin.wait_for
    screen_size = MainDisplayMixin.screen_size

    def tap(self, **selector):
        self.foreground()
        obj = self.d(**selector)
        if not obj.wait(timeout=8):
            raise RuntimeError('未找到控件：{}'.format(selector))
        if obj.count != 1:
            raise RuntimeError('控件不唯一：{}'.format(selector))
        box = obj.info['bounds']
        self.click_point((box['left'] + box['right']) // 2, (box['top'] + box['bottom']) // 2)

    def click_point(self, x, y):
        self.foreground()
        # 当前 Android 17 测试机过滤过短的点击；200ms 单次按下可正常响应，
        # 仍低于长按阈值，避免以双击方式重试发送/导航按钮。
        self.d.long_click(x, y, duration=0.2)

    def transition(self, action, ready, message):
        # 部分页面第一次点击未响应；仅在目标状态未出现时重试，禁止盲目双击。
        for _ in range(2):
            if ready():
                return
            action()
            deadline = time.monotonic() + 4
            while time.monotonic() < deadline:
                if ready():
                    return
                time.sleep(0.4)
        self.wait_for(ready, message)

    def relative_click(self, x, y):
        if not (0 < x < 1 and 0 < y < 1):
            raise ValueError('点击坐标必须为 (0, 1) 内的屏幕比例')
        self.foreground()
        width, height = self.screen_size()
        self.click_point(round(width * x), round(height * y))

    def browse(self, up=5, down=5):
        self.foreground()
        width, height = self.screen_size()
        for upward, count in ((True, up), (False, down)):
            for _ in range(count):
                self.foreground()
                start, end = (0.78, 0.3) if upward else (0.3, 0.78)
                self.d.swipe(round(width * 0.5), round(height * start),
                             round(width * 0.5), round(height * end), duration=0.4)
                time.sleep(2)

    def launcher_gesture(self):
        self.foreground()
        width, height = self.screen_size()
        self.d.swipe(round(width * 0.5), round(height * 0.995),
                     round(width * 0.5), round(height * 0.62), duration=0.25)
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(), '上滑后未返回桌面')

    @SeaOfStarsAW.function_log
    def run_case(self):
        if hasattr(self, 'RECOVERY_CHECKPOINTS'):
            from Cases.Top48.step_recovery import run_recoverable_case
            return run_recoverable_case(self)
        # main.py 当前注释了 set_up，直接运行用例时仍保证前置准备。
        if not getattr(self, '_prepared', False):
            self.set_up()
        for _ in range(self.TEST_TIME):
            for index, (name, action, stay) in enumerate(self.steps(), 1):
                logging.info('%s、%s', index, name)
                SeaOfStarsAW.start_perfetto_trace()
                failed = False
                try:
                    action()
                    time.sleep(stay)
                except Exception:
                    failed = True
                    logging.exception('步骤 %s、%s 失败', index, name)
                    raise
                finally:
                    try:
                        SeaOfStarsAW.stop_and_get_perfetto_trace(
                            self.trace_dir_path, self.__class__.__name__,
                            'step_{}、{}'.format(index, name), '', self.screenshot_dir_path)
                    except Exception:
                        if not failed:
                            raise
                        logging.exception('失败步骤的 trace 导出失败')

    @SeaOfStarsAW.function_log
    def clean_up(self):
        logging.getLogger().removeHandler(self.fh)
        self.fh.close()
        logging.info('用例结束，保留应用后台')
