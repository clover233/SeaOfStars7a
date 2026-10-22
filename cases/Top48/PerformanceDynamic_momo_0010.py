"""陌陌首页、直播浏览和底部导航切换（表格第 1129～1139 行）。"""
import logging
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase
from Cases.Top48.screen_text import ScreenshotText


class PerformanceDynamic_momo_0010(DynamicAppCase):
    PACKAGE = 'com.immomo.momo'
    all_app_package_list = [PACKAGE]
    TABS = ('首页', '直播', '消息', '小宇宙', '更多')

    def dismiss_teen_prompt(self):
        # 列表浏览中会异步出现在线配对邀请，遮住直播卡片；只关闭邀请。
        if self.has(text='拒绝') and any('在线配对' in n.get('text', '')
                                     or '匹配度' in n.get('text', '') for n in self.nodes()):
            self.click(text='拒绝')
            time.sleep(.7)
        if self.has(text='我知道了'):
            self.click(text='我知道了')
            time.sleep(.5)
        elif not self.has(rid='tab_item_tv_label') and not self.has(rid='phone_live_iv_quit'):
            # 首次直播提示会使底栏控件缺失；只关闭截图已核对的青少年提示。
            rows = ScreenshotText().read(self.d)
            if any('在线配对' in r['text'] or '匹配度' in r['text'] for r in rows):
                buttons = [r for r in rows if r['text'].strip() == '拒绝']
                if len(buttons) == 1:
                    r = buttons[0]
                    self.pct(r['x'] + r['w']/2, r['y'] + r['h']/2)
                    time.sleep(.7)
                    return
            if any('青少年模式' in r['text'] for r in rows):
                buttons = [r for r in rows if r['text'] == '我知道了']
                if len(buttons) == 1:
                    r = buttons[0]
                    self.pct(r['x'] + r['w']/2, r['y'] + r['h']/2)
                    time.sleep(.7)

    def live_list(self):
        # 退出挽留层复用了 live_center_layout，必须同时确认已离开直播 Activity。
        return ('LiveActivity' not in self.current_app()['activity']
                and self.has(rid='live_center_layout') and not self.has(rid='phone_live_iv_quit'))

    def tab_ready(self, name):
        self.dismiss_teen_prompt()
        if name == '直播':
            return self.live_list()
        return any(n.get('selected') == 'true'
                   for n in self.nodes(text=name, rid='tab_item_tv_label'))

    def switch_tab(self, name):
        if 'LiveActivity' in self.current_app()['activity']:
            self.exit_live()
        def tap_tab():
            self.dismiss_teen_prompt()
            if self.has(text=name, rid='tab_item_tv_label'):
                self.click(text=name, rid='tab_item_tv_label')
            elif self.live_list():
                # weditor dump + 截图核对：直播列表底栏可见，但控件树缺失底栏。
                # 五个等宽入口；点击屏幕底部 95% 处的图标，随当前分辨率换算。
                logging.info('直播列表底栏未暴露控件，使用比例点击：%s', name)
                self.pct((self.TABS.index(name) + .5) / len(self.TABS), .965)
            else:
                raise RuntimeError('陌陌导航栏不可用：{}'.format(name))
        self.transition(tap_tab, lambda: self.tab_ready(name),
                        '陌陌未切换到{}页'.format(name))

    def launch(self):
        self.start()
        # 启动广告自然结束后再操作，不点击广告或聊天邀请浮层。
        self.wait_for(lambda: self.has(rid='tab_item_tv_label') or self.live_list() or
                      self.has(rid='phone_live_iv_quit') or 'LiveActivity' in self.current_app()['activity'],
                      '陌陌导航未就绪，请确认已登录并关闭启动弹窗', timeout=45)
        if self.has(rid='phone_live_iv_quit') or 'LiveActivity' in self.current_app()['activity']:
            self.exit_live()
        self.switch_tab('首页')
        self.wait_for(lambda: self.has(text='动态', rid='tab_title'), '陌陌首页未加载')

    def open_live(self):
        self.dismiss_teen_prompt()
        self.wait_for(self.live_list, '直播卡片未恢复')
        self.require(rid='live_center_layout')
        # 取当前列表从上到下、从左到右的首个完整卡片，主播名称动态变化。
        width, height = self.screen_size()
        cards = [n for n in self.nodes(rid='live_center_layout')
                 if self.bounds(n)[1] >= height * .1
                 and self.bounds(n)[3] <= height * .92
                 and self.bounds(n)[2] - self.bounds(n)[0] > width * .3
                 and self.bounds(n)[3] - self.bounds(n)[1] > height * .12]
        if not cards:
            raise RuntimeError('直播列表没有可观看的完整卡片')
        first = min(cards, key=lambda n: (self.bounds(n)[1], self.bounds(n)[0]))
        def ready():
            self.dismiss_live_guide()
            return self.has(rid='phone_live_iv_quit') and self.has(rid='live_tv_star_name')
        self.transition(lambda: self.click_node(first), ready,
                        '首个直播间未打开，可能已下播')
        time.sleep(15)
        self.dismiss_live_guide()
        self.wait_for(ready, '直播停留后控制栏未恢复')
        self.require(rid='phone_live_iv_quit')
        self.require(rid='live_tv_star_name')

    def dismiss_live_guide(self):
        if 'LiveActivity' not in self.current_app()['activity'] or self.has(rid='phone_live_iv_quit'):
            return
        rows = ScreenshotText().read(self.d)
        if any('快速切换主播' in r['text'] for r in rows):
            # 首次手势引导没有命名按钮；截图已核对，点击屏幕中央关闭引导。
            self.pct(.5, .5)
            time.sleep(.7)

    def exit_live(self):
        def leave():
            if self.has(text='忽略', rid='dilaog_button1'):
                self.click(text='忽略', rid='dilaog_button1')
            elif self.has(text='暂不使用'):
                self.click(text='暂不使用')
            elif self.has(text='直接退出', rid='dilaog_button1'):
                self.click(text='直接退出', rid='dilaog_button1')
            elif self.has(text='残忍退出'):
                self.click(text='残忍退出')
            elif self.has(rid='phone_live_iv_quit'):
                self.click(rid='phone_live_iv_quit')
            else:
                # 新版挽留推荐/游戏推广只导出 WebView；按截图文字框的比例关闭。
                rows = ScreenshotText().read(self.d)
                labels = [r['text'].replace(' ', '') for r in rows]
                if any('应用外小窗' in s for s in labels):
                    label = '暂不使用'
                elif any('初级门' in s for s in labels):
                    label = '不感兴趣'
                else:
                    label = '残忍退出'
                buttons = [r for r in rows if r['text'].replace(' ', '') == label]
                if len(buttons) == 1:
                    r = buttons[0]
                    self.pct(r['x'] + r['w']/2, r['y'] + r['h']/2)
                else:
                    self.back()
        # 首次退出可能弹“悬浮窗权限”提示，忽略即可，不进入系统授权页。
        for _ in range(8):
            if self.live_list():
                return
            self.dismiss_live_guide()
            leave()
            time.sleep(1)
        self.wait_for(self.live_list, '退出直播后未返回直播列表')

    def steps(self):
        return [
            ('启动陌陌', self.launch, 3),
            ('首页浏览，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击直播，切换到直播页', lambda: self.switch_tab('直播'), 3),
            ('直播页浏览，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击第一个直播观看，等待15s', self.open_live, 0),
            ('返回直播列表页面', self.exit_live, 2),
            ('点击消息tab，切换到消息页', lambda: self.switch_tab('消息'), 2),
            ('点击小宇宙tab，切换到小宇宙tab页', lambda: self.switch_tab('小宇宙'), 2),
            ('点击更多tab，切换到更多tab页', lambda: self.switch_tab('更多'), 2),
            ('点击首页，返回陌陌首页', lambda: self.switch_tab('首页'), 2),
            ('上滑返回home页面', self.home, 1),
        ]
