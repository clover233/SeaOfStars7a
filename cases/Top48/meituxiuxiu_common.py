"""美图秀秀动态性能用例的页面操作。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class MeituXiuxiuDynamicCase(DynamicAppCase):
    PACKAGE = 'com.mt.mtxx.mtxx'
    PERMISSIONS = ('CAMERA',)

    def dismiss_popups(self):
        for selector in ({'text': '取消'}, {'desc': 'pop_close'}):
            if self.has(**selector):
                self.click(**selector)
                time.sleep(1)

    def main_ready(self):
        return self.has(text='图片美化') and self.has(text='相机')

    def picker_ready(self):
        return self.has(text='图片视频')

    def editor_ready(self):
        return self.has(text='保存') and self.has(text='滤镜') and self.has(text='调色')

    def saved_ready(self):
        return self.has(text='图片已保存') and self.has(text='再修一张')

    def camera_ready(self):
        return self.has(text='滤镜调色') and self.has(text='拍摄')

    def launch(self):
        self.start()
        self.dismiss_popups()
        if not self.main_ready():
            self.main_page()
        self.wait_for(self.main_ready, '美图秀秀首页未加载')

    def import_page(self):
        self.transition(lambda: self.click(text='图片美化'), self.picker_ready,
                        '未进入美图秀秀图片页面')

    def first_image_and_filter(self):
        def select_first():
            images = self.nodes(rid='D`')
            if not images:
                raise RuntimeError('图片页面没有可编辑的图片')
            self.click_node(images[0])
        self.transition(select_first,
                        lambda: self.editor_ready() or self.has(text='进入图片美化'),
                        '第一张图片未进入预览页')
        if not self.editor_ready():
            self.transition(lambda: self.click(text='进入图片美化'), self.editor_ready,
                            '图片预览确认后未进入编辑页')
        self.click(text='滤镜')
        time.sleep(1)

    def first_filter(self):
        width, height = self.d.window_size()
        choices = [node for node in self.nodes()
                   if node.get('clickable') == 'true'
                   and height * .77 < self.bounds(node)[1] < height * .86
                   and self.bounds(node)[0] > width * .15
                   and width * .10 < self.bounds(node)[2] - self.bounds(node)[0] < width * .25]
        if choices:
            self.click_node(min(choices, key=lambda node: self.bounds(node)[0]))
        # 12.20.1 的滤镜面板选择后即时生效，没有独立“确认”按钮。
        time.sleep(1)

    def brightness_100(self):
        if not self.has(text='调色'):
            raise RuntimeError('编辑页没有调色入口')
        self.click(text='调色')
        def sliders():
            return self.nodes(rid='BDy') or self.nodes(rid='BF5')
        self.wait_for(lambda: self.has(text='亮度') and bool(sliders()),
                      '调色亮度滑杆未显示')
        slider = sliders()[0]
        left, top, right, bottom = self.bounds(slider)
        self.d.swipe((left + right) // 2, (top + bottom) // 2,
                     right - 8, (top + bottom) // 2, duration=.35)
        self.wait_for(lambda: self.has(text='100') or self.has(text='+100'), '亮度未设置为100')
        confirm = self.nodes(rid='O=') or self.nodes(rid='PH')
        if confirm:
            self.click_node(confirm[0])
        elif self.has(text='确认'):
            self.click(text='确认')
        else:
            self.back()
        self.wait_for(self.editor_ready, '调色确认后未返回编辑页')

    def save(self):
        self.transition(lambda: self.click(text='保存'), self.saved_ready,
                        '图片保存页未出现')
        self.dismiss_popups()

    def edit_another(self):
        self.transition(lambda: self.click(text='再修一张'), self.picker_ready,
                        '未返回图片页面')

    def main_page(self):
        self.return_to(self.main_ready, '未返回美图秀秀主界面', limit=7)
        self.dismiss_popups()

    def camera(self):
        self.main_page()
        self.transition(lambda: self.click(text='相机'), self.camera_ready,
                        '相机页面未打开')

    def camera_filter(self):
        self.transition(lambda: self.click(text='滤镜调色'),
                        lambda: bool(self.nodes(rid='tv_title')),
                        '相机滤镜面板未打开')

    def switch_camera_filter(self):
        height = self.d.window_size()[1]
        titles = [node for node in self.nodes(rid='tv_title')
                  if self.bounds(node)[1] > height * .72]
        if not titles:
            raise RuntimeError('相机滤镜面板没有可选滤镜')
        self.click_node(titles[0])

    def collapse_camera_filter(self):
        arrows = self.nodes(rid='mS')
        if arrows:
            self.click_node(arrows[0])
            time.sleep(1)
        if self.has(rid='mS'):
            self.back()
        self.wait_for(self.camera_ready, '未收起相机滤镜面板')

    def shutter(self):
        # 快门是相机自绘控件，层级树没有节点；在相机状态成立后按屏幕比例定位。
        self.transition(lambda: self.pct(.50, .844),
                        lambda: self.has(text='去修图') or self.has(text='编辑'),
                        '拍照后未出现编辑入口')

    def edit_photo(self):
        label = '编辑' if self.has(text='编辑') else '去修图'
        self.transition(lambda: self.click(text=label), self.editor_ready,
                        '照片未进入编辑页')
