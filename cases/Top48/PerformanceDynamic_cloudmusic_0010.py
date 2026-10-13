"""网易云雷达播放场景；步骤对应 Excel 第 382–388 行。"""
import logging
import re
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_cloudmusic_0010(DynamicAppCase):
    PACKAGE = 'com.netease.cloudmusic'
    all_app_package_list = [PACKAGE]

    def dismiss_promotion(self):
        # 仅关闭已识别的推广，不把开通会员当作播放前提。
        if self.has(rid='skipBtn'):
            self.click(rid='skipBtn')
        if (self.has(text='立即开通') or
                any('听有声书即可领取' in n.get('text', '') for n in self.nodes())):
            self.back()
            time.sleep(1)

    def launch(self):
        self.start()
        time.sleep(5)  # 等开屏广告结束，避免点穿广告。
        self.dismiss_promotion()
        self.return_to(lambda: self.has(desc='首页') and self.has(desc='推荐'),
                       '未回到网易云首页')
        self.click(desc='首页')
        self.click(desc='推荐')
        time.sleep(1)
        self.dismiss_promotion()
        self.wait_for(lambda: self.has(text='雷达歌单') or self.has(text='推荐歌单'),
                      '网易云推荐首页未加载')

    def radar_playlist(self):
        self.reveal('未找到雷达歌单', text='雷达歌单')
        self.open_control(lambda: self.has(text='私人雷达') or self.has(text='播放全部'),
                          '未打开首个雷达歌单', text='雷达歌单')
        # 当前版本此入口直接打开首个“私人雷达”；旧版本先显示歌单集合。
        if not self.has(text='播放全部'):
            self.open_control(lambda: self.has(text='播放全部'),
                              '未打开私人雷达播放列表', text='私人雷达')

    def media_state(self):
        output = self.d.shell('dumpsys media_session').output
        session = re.search(r'package=' + re.escape(self.PACKAGE) +
                            r'\s.*?state=PlaybackState\s*\{state=(?:[A-Z_]+\()?([0-9]+)',
                            output, re.S)
        return int(session.group(1)) if session else None

    def play_all(self):
        self.click(text='播放全部')
        time.sleep(2)
        self.dismiss_promotion()
        self.wait_for(lambda: self.media_state() == 3, '播放全部后未开始播放', timeout=20)
        if not self.has(rid='nextBtn'):
            self.open_control(lambda: self.has(rid='nextBtn'), '未打开完整播放器', rid='tv_music')

    def next_five(self):
        for index in range(5):
            previous = self.node(rid='songName').get('text')
            def changed():
                self.dismiss_promotion()
                names = self.nodes(rid='songName')
                return bool(names and names[0].get('text') != previous)
            self.transition(lambda: self.click(rid='nextBtn'), changed, '下一首后歌曲未切换')
            self.wait_for(lambda: self.media_state() == 3, '切歌后未播放', timeout=20)
            logging.info('切歌 %s/5：%s -> %s', index + 1, previous,
                         self.node(rid='songName').get('text'))
            time.sleep(1)

    def pause(self):
        self.wait_for(lambda: self.media_state() == 3, '暂停前歌曲未播放')
        self.transition(lambda: self.click(rid='playBtn'), lambda: self.media_state() == 2,
                        '歌曲未暂停')

    def steps(self):
        return [
            ('启动网易云音乐', self.launch, 3),
            ('首页浏览，上滑2次，下滑2次，重复2次',
             lambda: [self.browse(2, 2) for _ in range(2)], 0),
            ('点击雷达歌单下的第一个歌单', self.radar_playlist, 1),
            ('播放全部', self.play_all, 2),
            ('点击下一首，重复5次', self.next_five, 0),
            ('暂停播放', self.pause, 1),
            ('滑动返回Home页', self.home, 1),
        ]
