"""哔哩哔哩动态性能场景：实机 hierarchy 定位及按实时尺寸换算的手势。"""
import re
import time
import xml.etree.ElementTree as ET

from Cases.Top48.baidu_common import BaiduDynamicCase


class BilibiliDynamicCase(BaiduDynamicCase):
    PACKAGE = 'tv.danmaku.bili'
    PREFIX = PACKAGE + ':id/'
    all_app_package_list = [PACKAGE]

    def shell(self, command):
        result = self.d.shell(command)
        if result.exit_code:
            raise RuntimeError('设备命令失败：{} {}'.format(command, result.output))
        return result.output

    def nodes(self, **selector):
        keys = {'resourceId': 'resource-id', 'description': 'content-desc',
                'text': 'text', 'className': 'class'}
        return [n for n in ET.fromstring(self.d.dump_hierarchy()).iter('node')
                if n.get('package') == self.PACKAGE
                and n.get('display-id', '0') == '0'
                and n.get('visible-to-user') != 'false'
                and all(n.get(keys[k]) == v for k, v in selector.items())]

    def has(self, rid=None, **selector):
        if rid:
            selector['resourceId'] = self.PREFIX + rid
        return bool(self.nodes(**selector))

    @staticmethod
    def bounds(node):
        return tuple(map(int, re.findall(r'\d+', node.get('bounds'))))

    def click_point(self, x, y):
        self.foreground()
        # 此 Android 17 实机过滤 u2 短按；100ms 系统注入手势可正常响应。
        self.shell('input mouse -d 0 tap {} {}'.format(round(x), round(y)))

    def click_node(self, node, x=.5, y=.5):
        l, t, r, b = self.bounds(node)
        self.click_point(l + (r-l)*x, t + (b-t)*y)

    def click(self, rid=None, **selector):
        if rid:
            selector['resourceId'] = self.PREFIX + rid
        ns = self.nodes(**selector)
        if len(ns) != 1:
            raise RuntimeError('控件不存在或不唯一：{}'.format(selector))
        self.click_node(ns[0])

    def swipe(self, x1, y1, x2, y2, duration=400):
        self.foreground()
        w, h = self.screen_size()
        self.shell('input swipe {} {} {} {} {}'.format(
            round(w*x1), round(h*y1), round(w*x2), round(h*y2), duration))

    def browse(self, up=5, down=5):
        for count, start, end in ((up, .78, .32), (down, .32, .78)):
            for _ in range(count):
                self.swipe(.5, start, .5, end)
                time.sleep(2)

    def is_home(self):
        return self.has('expand_search') and self.has('tab_title', text='推荐')

    def home(self):
        for _ in range(8):
            if self.is_home():
                return
            self.foreground()
            self.shell('input keyevent 4')
            time.sleep(.8)
        self.wait_for(self.is_home, '未返回哔哩哔哩首页')

    def launch(self):
        self.d.app_start(self.PACKAGE, use_monkey=True)
        self.wait_for(lambda: self.current_app()['package'] == self.PACKAGE, '哔哩哔哩未启动')
        if self.has(text='不再提醒'):
            self.click(text='不再提醒')
        self.home()

    def channel(self, title):
        self.click('tab_title', text=title)
        time.sleep(1)
        if not any(n.get('selected') == 'true' for n in
                   self.nodes(resourceId=self.PREFIX+'tab_title', text=title)):
            # 直播频道的新版标签会过滤鼠标源 tap；仍按原生节点边界触屏点击。
            node = self.nodes(resourceId=self.PREFIX+'tab_title', text=title)[0]
            l, t, r, b = self.bounds(node)
            w, h = self.screen_size()
            self.d.click((l+r)/2/w, (t+b)/2/h)
        self.wait_for(lambda: any(n.get('selected') == 'true' for n in
                      self.nodes(resourceId=self.PREFIX+'tab_title', text=title)),
                      '未切换频道：'+title)

    def is_video(self):
        return self.has('video_area_float_layer_container')

    def video(self, min_seconds=0):
        # 排除广告子树，按页面从上到下、从左到右选择首个可见视频标题。
        root = ET.fromstring(self.d.dump_hierarchy())
        candidates = []
        parents = {child: parent for parent in root.iter() for child in parent}
        def long_enough(node):
            if not min_seconds:
                return True
            parent = parents.get(node)
            for _ in range(4):
                if parent is None:
                    break
                durations = [n.get('text', '') for n in parent.iter()
                             if n.get('resource-id') == self.PREFIX+'duration']
                if durations:
                    for duration in durations:
                        parts = duration.split(':')
                        if len(parts) in (2, 3) and all(p.isdigit() for p in parts):
                            seconds = 0
                            for part in parts:
                                seconds = seconds*60 + int(part)
                            if seconds >= min_seconds:
                                return True
                    return False
                parent = parents.get(parent)
            return False
        def visit(node):
            if node.get('resource-id') == self.PREFIX + 'ad_tint_frame':
                return
            if node.get('package') == self.PACKAGE and node.get('resource-id') == self.PREFIX+'title' and node.get('text'):
                l, t, r, b = self.bounds(node)
                if r > l and b > t and long_enough(node):
                    candidates.append(node)
            for child in node:
                visit(child)
        visit(root)
        if not candidates:
            raise RuntimeError('没有可见且时长满足要求的视频条目：{}秒'.format(min_seconds))
        self.click_node(min(candidates, key=lambda n: (self.bounds(n)[1], self.bounds(n)[0])))
        self.wait_for(lambda: self.is_video() and self.has('avatar'), '未进入视频播放页')

    def up_page(self):
        self.wait_for(lambda: self.has('avatar'), '视频UP主头像未加载')
        self.transition(lambda: self.click('avatar'),
                        lambda: 'space' in self.current_app()['activity'].lower()
                        or self.has(text='空间页') or self.has(text='投稿') and not self.is_video(),
                        '未进入UP主空间')
        time.sleep(2)

    def up_video(self):
        # 新版空间页 WebView 未暴露视频卡片。先固定投稿页，再在视频列表首行换算点击。
        self.click(text='投稿')
        time.sleep(1)
        # 投稿页顶部标签下为首条视频；滚动使空间头部折叠，避免误点关注等按钮。
        self.swipe(.5, .75, .5, .30)
        time.sleep(1)
        tabs = self.nodes(text='投稿')
        if len(tabs) != 1:
            raise RuntimeError('UP主投稿页标签不可定位')
        _, _, _, bottom = self.bounds(tabs[0])
        w, h = self.screen_size()
        self.click_point(w*.20, bottom + h*.10)
        self.wait_for(lambda: self.is_video() and self.has('avatar'), '比例点击未打开UP主首个视频')

    def comments(self):
        self.wait_for(lambda: self.has('tab_title', text='评论'), '视频评论入口未加载')
        self.click('tab_title', text='评论')
        self.wait_for(lambda: any(n.get('selected') == 'true' for n in
                      self.nodes(resourceId=self.PREFIX+'tab_title', text='评论')),
                      '未切换评论页')

    def search_box(self):
        self.click('expand_search')
        self.wait_for(lambda: self.has('search_src_text'), '未打开搜索框')

    def search_huawei(self):
        self.d(resourceId=self.PREFIX+'search_src_text').set_text('华为终端')
        self.wait_for(lambda: self.has('search_src_text', text='华为终端'), '搜索词未写入')
        self.click('action_search')
        self.wait_for(lambda: self.has('search_fake_text', text='华为终端'), '未显示华为终端搜索结果')
        time.sleep(2)

    def landscape(self):
        w, h = self.screen_size()
        return w > h

    def show_video_controls(self):
        if self.landscape():
            if not self.has('bbplayer_fullscreen_play'):
                self.relative_click(.5, .5)
        elif not self.has('gemini_halfscreen_expand'):
            self.click('video_area_float_layer_container')
        time.sleep(.3)

    def playing_video(self):
        self.show_video_controls()
        rid = 'bbplayer_fullscreen_play' if self.landscape() else 'gemini_halfscreen_play'
        self.wait_for(lambda: self.has(rid, description='暂停'), '视频未处于播放状态')

    def watching_live(self):
        self.foreground()
        self.wait_for(lambda: self.has('roomid') and self.has('live_send_danmaku'), '直播间未加载')

    def fullscreen(self):
        self.show_video_controls()
        self.click('gemini_halfscreen_expand')
        self.wait_for(self.landscape, '视频未进入横屏全屏')

    def double_player(self):
        if not self.landscape():
            raise RuntimeError('双击播放操作要求横屏全屏')
        self.foreground()
        w, h = self.screen_size()
        # 短于80ms的按下在此机可能被过滤；连续两次80ms原地手势构成双击。
        self.shell('input swipe {0} {1} {0} {1} 80; input swipe {0} {1} {0} {1} 80'.format(
            round(w*.5), round(h*.5)))
        time.sleep(.3)

    def pause_and_type(self):
        self.double_player()
        self.show_video_controls()
        self.wait_for(lambda: self.has('bbplayer_fullscreen_play', description='播放'), '双击未暂停视频')
        self.click('bbplayer_fullscreen_dminput')
        self.wait_for(lambda: self.has('player_input_edit'), '未打开弹幕输入框（请检查登录状态）')
        self.d(resourceId=self.PREFIX+'player_input_edit').set_text('还行')
        self.wait_for(lambda: self.has('player_input_edit', text='还行'), '弹幕未输入还行')

    def send_danmaku(self):
        if not self.has('player_input_edit', text='还行'):
            raise RuntimeError('弹幕内容不正确，停止发送')
        self.click('player_input_send')  # 对外发送只执行一次，禁止重试造成重复弹幕。
        self.wait_for(lambda: not self.has('player_input_edit'), '弹幕发送后输入框未关闭')

    def resume_video(self):
        self.double_player()
        self.show_video_controls()
        self.wait_for(lambda: self.has('bbplayer_fullscreen_play', description='暂停'), '双击未继续播放')

    def exit_fullscreen(self):
        if not self.landscape():
            raise RuntimeError('侧滑前视频已退出全屏，可能已播放结束')
        self.swipe(.005, .5, .4, .5, 250)
        self.wait_for(lambda: not self.landscape() and self.is_video(), '侧滑未退出全屏')

    def live_room(self):
        cards = self.nodes(resourceId=self.PREFIX+'tvTitle')
        if not cards:
            raise RuntimeError('直播列表没有可见直播卡片')
        self.click_node(min(cards, key=lambda n: (self.bounds(n)[1], self.bounds(n)[0])))
        self.wait_for(lambda: self.has('live_room_enter_guide_primary') or self.has('roomid'),
                      '直播卡片未打开直播间或预览')
        if self.has('live_room_enter_guide_primary'):
            self.click('live_room_enter_guide_primary')
        self.wait_for(lambda: self.has('live_send_danmaku') and self.has('roomid'), '未进入直播间')

    def live_fullscreen(self):
        self.click('controller_underlay')
        # 直播旋转按钮没有 ID/描述；相对播放器实时边界右下角定位，已实机验证。
        self.click_node(self.nodes(resourceId=self.PREFIX+'controller_underlay')[0], .94, .90)
        # 新版横屏会自动隐藏输入栏，不能用弹幕输入框判断播放器方向。
        def ready():
            self.dismiss_live_prompt()
            return self.landscape() and self.has('roomid')
        self.wait_for(lambda: ready()
                      and self.has('controller_underlay')
                      and 'LiveRoomActivity' in self.current_app()['activity'],
                      '直播未切换横屏')

    def dismiss_live_prompt(self):
        # 横屏后延迟出现的关注弹窗有独立 close 节点，不点击关注按钮。
        if self.has('follow_text') and self.has('close'):
            self.click('close')
            self.wait_for(lambda: not self.has('follow_text'), '直播关注提示未关闭')

    def watch_live_fullscreen(self):
        self.live_fullscreen()
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            self.dismiss_live_prompt()
            if not self.landscape() or 'LiveRoomActivity' not in self.current_app()['activity']:
                raise RuntimeError('横屏观看期间离开直播播放器')
            time.sleep(.8)
        self.dismiss_live_prompt()
        self.wait_for(lambda: self.landscape() and self.has('roomid')
                      and self.has('controller_underlay'), '横屏观看结束时直播播放器不可用')

    def launcher_gesture(self):
        self.swipe(.5, .995, .5, .62, 250)
        self.wait_for(lambda: 'launcher' in self.current_app()['activity'].lower(), '上滑未返回桌面')
