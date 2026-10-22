"""只读取主显示屏的前台状态，并容忍页面切换时短暂丢失焦点。"""
import re
import time


class ForegroundNotReady(RuntimeError):
    pass


def display_section(output, pattern):
    sections = list(re.finditer(pattern, output))
    if not sections:
        return output
    for index, match in enumerate(sections):
        if match.group(1) == '0':
            end = sections[index + 1].start() if index + 1 < len(sections) else len(output)
            return output[match.end():end]
    return ''


def component(output, marker):
    match = re.search(marker + r'[^\n]*?\su\d+\s+([\w.]+)/([\w.$]+)', output)
    if match:
        return {'package': match.group(1), 'activity': match.group(2)}


class MainDisplayMixin:
    def screen_size(self):
        """读取 display 0 尺寸，避免副屏 rotation 导致 window_size 宽高互换。"""
        output = self.d.shell('dumpsys window displays').output
        main = display_section(output, r'Display: mDisplayId=(\d+)\b')
        match = re.search(r'\bcur=(\d+)x(\d+)', main)
        if match:
            return tuple(map(int, match.groups()))
        return self.d.screenshot(display_id=0).size

    def current_app(self):
        windows = self.d.shell('dumpsys window displays').output
        main = display_section(windows, r'Display: mDisplayId=(\d+)\b')
        current = component(main, r'mCurrentFocus=Window\{')
        if current:
            return current
        activities = self.d.shell('dumpsys activity activities').output
        main = display_section(activities, r'Display #(\d+)\b')
        current = component(main, r'(?:topResumedActivity=|mResumedActivity:\s*)ActivityRecord\{')
        if current:
            return current
        raise ForegroundNotReady('无法识别主屏前台应用')

    def wait_for(self, predicate, message, timeout=15):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                if predicate():
                    return
            except ForegroundNotReady:
                # 只重试焦点暂缺；定位失败、跨应用和其他异常仍正常上报。
                pass
            time.sleep(.4)
        try:
            current = self.current_app()
        except ForegroundNotReady:
            current = '主屏焦点暂缺'
        raise RuntimeError('{}；当前页面 {}'.format(message, current))
