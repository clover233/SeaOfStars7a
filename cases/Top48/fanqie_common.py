"""番茄免费小说动态用例的首页、书架和榜单公共操作。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class FanqieDynamicCase(DynamicAppCase):
    PACKAGE = 'com.dragon.read'
    all_app_package_list = [PACKAGE]
    BOTTOM_TAB_ID = 'g_r'
    CHANNEL_ID = 'cp'
    RANK_TAB_ID = 'g_q'
    RANK_TABS = {'推荐榜', '完本榜', '巅峰榜', '新书榜', '漫剧榜'}

    def bottom_selected(self, name):
        return any(node.get('selected') == 'true'
                   for node in self.nodes(text=name, rid=self.BOTTOM_TAB_ID))

    def switch_bottom(self, name):
        if self.bottom_selected(name):
            return
        self.transition(lambda: self.click(text=name, rid=self.BOTTOM_TAB_ID),
                        lambda: self.bottom_selected(name),
                        '番茄免费小说未切换到底部“{}”页'.format(name))

    def close_pendant(self):
        if self.has(desc='Close Button'):
            self.click(desc='Close Button')
            time.sleep(.5)

    def main_page(self):
        self.return_to(lambda: self.has(text='书城', rid=self.BOTTOM_TAB_ID),
                       '未返回番茄免费小说主界面')
        self.switch_bottom('书城')
        self.close_pendant()

    def launch(self):
        self.start()
        self.main_page()

    def home(self):
        # 阅读器会吞掉底部上滑手势；先退回带底栏的主界面，再执行系统手势。
        self.return_to(lambda: self.has(text='书城', rid=self.BOTTOM_TAB_ID),
                       '返回桌面前未退出番茄阅读/榜单页')
        super().home()

    def channel_selected(self, name):
        # 当前版本不设置 selected 属性，而是把选中项字体区域加高约 7 px。
        target = self.nodes(text=name, rid=self.CHANNEL_ID)
        channels = self.nodes(rid=self.CHANNEL_ID)
        if not target or not channels:
            return False
        heights = [self.bounds(node)[3] - self.bounds(node)[1] for node in channels]
        target_height = self.bounds(target[0])[3] - self.bounds(target[0])[1]
        return target_height == max(heights) and max(heights) > min(heights)

    def reveal_channel(self, name):
        if self.has(text=name, rid=self.CHANNEL_ID):
            return
        # 顶部频道是横向列表；先向右拖动以找回左侧“推荐”，再反向兜底。
        for start, end in ((.2, .8), (.2, .8), (.8, .2), (.8, .2)):
            self.swipe(start, .125, end, .125, 350)
            time.sleep(.8)
            if self.has(text=name, rid=self.CHANNEL_ID):
                return
        raise RuntimeError('未找到番茄免费小说频道：' + name)

    def select_channel(self, name):
        self.reveal_channel(name)
        if self.channel_selected(name):
            return
        self.transition(lambda: self.click(text=name, rid=self.CHANNEL_ID),
                        lambda: self.channel_selected(name),
                        '番茄免费小说未切换到“{}”频道'.format(name))

    def rank_signature(self):
        height = self.d.window_size()[1]
        titles = []
        for node in self.nodes(rid=self.RANK_TAB_ID):
            text = node.get('text', '')
            top = self.bounds(node)[1]
            if text and text not in self.RANK_TABS and height * .2 < top < height * .62:
                titles.append(text)
        return tuple(titles)

    def select_rank(self, name):
        self.click(text=name, rid=self.RANK_TAB_ID)
        # 榜单不暴露 selected/checked，且会记住上次选择；重复点击时内容不变化是正常状态。
        self.wait_for(lambda: bool(self.rank_signature()),
                      '“{}”榜单内容未加载'.format(name))
        time.sleep(1)

    def swipe_rank(self, left=True):
        start, end = ((.82, .18) if left else (.18, .82))
        self.swipe(start, .4, end, .4, 450)
        self.wait_for(lambda: bool(self.rank_signature()), '榜单左右滑动后内容丢失', timeout=6)
        time.sleep(1)

    def browse_rank(self):
        for _ in range(2):
            self.swipe_rank(left=True)
        for _ in range(2):
            self.swipe_rank(left=False)
