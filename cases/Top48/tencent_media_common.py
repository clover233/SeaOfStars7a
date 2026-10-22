"""QQ 音乐、腾讯新闻和腾讯视频的实机定位及媒体状态检查。"""
import re
import time
import xml.etree.ElementTree as ET

from Cases.Top48.observed_apps_common import ObservedAppCase, StepUnavailable, optional


class TencentObservedCase(ObservedAppCase):
    def point(self, x, y):
        self.foreground()
        # QQ 音乐的自绘卡片不响应鼠标源点击；实机核对改用主屏触屏短按。
        result = self.d.shell('input touchscreen -d 0 swipe {0} {1} {0} {1} 100'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('主屏点击失败：' + result.output)
        self.invalidate()

    def native(self, **selector):
        self._locators.add('tree')
        self.click(**selector)

    def label_node(self, label):
        """点击文字所属的可点击父控件，避免点到标签底部的空白。"""
        root = ET.fromstring(self.d.dump_hierarchy())
        parents = {child: parent for parent in root.iter() for child in parent}
        rows = self.find(label)
        width, height = self.screen_size()
        for row in rows:
            for n in root.iter('node'):
                if n.get('package') != self.PACKAGE or n.get('text') != label:
                    continue
                box = self.bounds(n)
                if len(box) != 4 or abs((box[1]+box[3])/2/height-(row['y']+row['h']/2)) > .025:
                    continue
                while n.get('clickable') != 'true' and n in parents:
                    parent = parents[n]
                    if parent.tag != 'node' or parent.get('package') != self.PACKAGE:
                        break
                    n = parent
                if n.get('clickable') == 'true':
                    parent_box = self.bounds(n)
                    # 标签栏有时仅整页容器标记 clickable，不能改点整页中心的广告。
                    if len(parent_box) == 4 and (parent_box[3]-parent_box[1])/height <= .22:
                        self._locators.add('tree')
                        self.click_node(n)
                        return
        self.choose(label)

    def media_state(self):
        """只读取目标包名自己的会话，不能用其他后台播放器的状态判成功。"""
        output = self.d.shell('dumpsys media_session').output
        for block in output.split('package=')[1:]:
            if block.splitlines()[0].strip() != self.PACKAGE:
                continue
            state = re.search(r'state=PlaybackState \{state=(?:[A-Z_]+\()?(\d+)', block)
            if state:
                return int(state.group(1))
        return None

    def media_description(self):
        for block in self.d.shell('dumpsys media_session').output.split('package=')[1:]:
            if block.splitlines()[0].strip() == self.PACKAGE:
                found = re.search(r'metadata:.*?description=(.*)', block)
                if found:
                    return found.group(1).strip()
        return ''

    def browse_checked(self, ready, up, down, message):
        self.dismiss_ads()
        if not ready():
            raise StepUnavailable(message)
        self.browse(up, down)


class QqMusicDynamicCase(TencentObservedCase):
    PACKAGE = 'com.tencent.qqmusic'
    all_app_package_list = [PACKAGE]
    COMPONENT = PACKAGE + '/.activity.AppStarterActivity'

    def launch(self):
        super().launch()
        self.home_page()

    def dismiss_ads(self):
        super().dismiss_ads()
        if self.has(text='歌曲同步') and self.has(rid='il_', text='知道了'):
            self.native(rid='il_', text='知道了')
            time.sleep(.5)
        if self.activity_is('TMECoreActivity'):
            # 全屏互动广告与启动页广告不同，优先使用明确的关闭属性。
            for selector in ({'desc': '关闭'}, {'text': '关闭'}, {'text': '跳过'}):
                if self.has(**selector):
                    self.native(**selector)
                    break
            else:
                # 该广告的 X 不导出节点；已核对截图右上“广告”胶囊旁关闭位置。
                if self.visible('广告', True, (.7, .05, 1, .17)):
                    self.pct(.938, .106)
            time.sleep(.8)
            self.invalidate()
        # 实机弹窗原生树仅有广告标签和此说明，关闭 X 位于广告标签右侧。
        # 只有这两个弹窗特征同时出现才使用截图核对过的比例，防止点穿到登录。
        if self.has(text='点击上方按钮/素材跳转详情页或第三方应用') and self.has(text='广告'):
            self.pct(.855, .236)
            time.sleep(.6)
            self.invalidate()

    def main_ready(self):
        return (not self.activity_is('NewPlayerActivity', 'LoginActivity', 'TMECoreActivity')
                and self.visible('首页', region=(0, .9, .25, .99))
                and self.visible('我的', region=(.75, .9, 1, .99)))

    def main_page(self):
        for _ in range(6):
            self.dismiss_ads()
            if self.main_ready():
                break
            if self.activity_is('TMECoreActivity'):
                time.sleep(1)
                self.invalidate()
                continue
            self.back()
        self.content_wait(self.main_ready, '未返回QQ音乐主界面')
        self.collapse_player()

    def collapse_player(self):
        # 返回页面后播放器有时自动展开，遮住新歌榜；按原生“收起”恢复迷你条。
        if self.has(rid='cd0', desc='收起'):
            self.native(rid='cd0', desc='收起')
            self.content_wait(lambda:not self.has(rid='cd0', desc='收起'), '底部展开播放器未收起')

    def my_ready(self):
        return self.main_ready() and self.visible('本地') and self.visible('收藏')

    def my_page(self):
        self.main_page()
        self.go(lambda: self.bottom_node('我的'), self.my_ready, 'QQ音乐我的页未打开')
        self.dismiss_ads()
        self._music_logged_in = not self.visible('立即登录')

    def home_page(self):
        self.main_page()
        self.go(lambda: self.bottom_node('首页'),
                lambda: self.main_ready() and any(n.get('selected') == 'true' for n in self.nodes(rid='jbk', desc='首页')),
                'QQ音乐首页未打开')
        # ln0 的 selected 是跑马灯状态，多个标签会同时为 true，不能作为选中依据。
        self.native(rid='ln0', text='推荐')
        time.sleep(.7)
        self.invalidate()
        self.content_wait(lambda:self.main_ready() and not self.visible('Staff Picks', True),
                          'QQ音乐推荐页面未打开')

    def recent_ready(self):
        return self.visible('最近播放', True, (0, .05, 1, .2)) and not self.main_ready()

    @optional('recent')
    def recent(self):
        self.my_page()
        for name in ('最近', '最近播放'):
            if self.visible(name):
                def ready():
                    self.dismiss_ads()
                    return self.recent_ready()
                self.go(lambda: self.label_node(name), ready, '最近播放页面未打开')
                return
        raise StepUnavailable('20.9.5.8未登录的我的页没有“最近/最近播放”入口')

    @optional('recent')
    def browse_recent(self):
        self.needs('recent')
        self.browse_checked(self.recent_ready, 2, 2, '最近播放页不可用')

    @optional('local')
    def local(self):
        self.my_page()
        self.go(lambda: self.label_node('本地'),
                lambda: not self.main_ready() and (self.visible('没有本地歌曲') or self.visible('本地歌曲', True)),
                '本地音乐页未打开')
        self.dismiss_system_prompt()
        if self.visible('没有本地歌曲'):
            self.adapt('当前设备本地歌曲为空，验证本地音乐空态，不扫描或导入个人文件')

    def search_ready(self):
        return self.has(rid='searchItem')

    @optional('search')
    def search_page(self):
        self.home_page()
        self.go(lambda: self.native(rid='c3j'), self.search_ready, 'QQ音乐搜索输入页未打开')

    def results_ready(self):
        return self.search_ready() and self.has(desc='综合 按钮') and self.has(desc='歌手 按钮')

    @optional('search')
    def search_song(self):
        self.needs('search')
        if not self.search_ready():
            raise StepUnavailable('当前不在QQ音乐搜索页')
        self.input_text('红旗飘飘')
        self.d.press('enter')
        self.invalidate()
        self.content_wait(self.results_ready, '红旗飘飘搜索结果未显示')

    def search_tab(self, name):
        self.needs('search')
        if not self.results_ready():
            raise StepUnavailable('搜索结果不可用')
        self.go(lambda: self.native(desc=name+' 按钮'),
                lambda: any(n.get('selected') == 'true' for n in self.nodes(desc=name+' 按钮')),
                name+'搜索分类未选中')

    @optional('search')
    def singers(self):
        self.search_tab('歌手')

    @optional('search')
    def comprehensive(self):
        self.search_tab('综合')

    @optional('search')
    def browse_results(self):
        self.needs('search')
        self.browse_checked(self.results_ready, 2, 2, '综合搜索结果不可用')

    def player_ready(self):
        return self.activity_is('NewPlayerActivity') and self.has(rid='kog')

    def hold_music(self, seconds):
        self.content_wait(lambda: self.media_state() == 3, '音乐未开始播放')
        # 播放计时从本包媒体会话 PLAYING 后开始，结束时再次确认没有暂停/失败。
        time.sleep(seconds)
        if self.media_state() != 3:
            raise StepUnavailable('播放期间媒体会话已停止，未完成{}秒播放'.format(seconds))

    @optional('song')
    def first_song(self):
        self.needs('search')
        self.comprehensive()
        # 上下浏览后恢复顶部；按歌名控件和结果顺序选择首条单曲，排除 AI 摘要。
        for _ in range(4):
            if self.has(rid='kog', text='红旗飘飘'):
                break
            self.swipe(.5, .35, .5, .8)
        if not self.has(rid='kog', text='红旗飘飘'):
            raise StepUnavailable('综合结果没有可见的首条“红旗飘飘”单曲')
        self.native(rid='kog', text='红旗飘飘')
        self.content_wait(lambda: self.media_state() == 3 and self.media_description().startswith('红旗飘飘,'),
                          '首条红旗飘飘未开始播放')
        self.hold_music(20)

    @optional('song')
    def player(self):
        self.needs('song')
        if self.player_ready():
            self.adapt('当前版本选择单曲后自动进入播放详情，保留详情页核验')
            return
        if not self.has(rid='gfo'):
            raise StepUnavailable('底部播放器没有歌曲详情入口')
        self.go(lambda: self.native(rid='gfo'), self.player_ready, '播放详情未打开')

    def pause(self):
        self.dismiss_ads()
        state = self.media_state()
        if state == 2:
            self.adapt('目标歌曲已经暂停，保持暂停状态，避免切换成播放')
            return
        if state != 3:
            raise StepUnavailable('当前没有正在播放的QQ音乐媒体会话')
        def stop():
            candidates = self.nodes(desc='暂停')
            if not candidates:
                raise StepUnavailable('没有可核对的暂停控件')
            self._locators.add('tree')
            self.click_node(candidates[0])
        self.go(stop, lambda: self.media_state() == 2, 'QQ音乐暂停未生效')

    @optional('song')
    def pause_song(self):
        self.needs('song')
        self.player()
        self.pause()

    @optional('favorite')
    def favorite_roundtrip(self):
        self.needs('song')
        self.player()
        if not getattr(self, '_music_logged_in', False):
            raise StepUnavailable('当前QQ音乐未登录，收藏需要登录；未改变收藏状态')
        def state():
            nodes = self.nodes(rid='ic5')
            if len(nodes) != 1:
                return None
            desc = nodes[0].get('content-desc', '')
            if any(s in desc for s in ('已收藏', '取消收藏', '取消喜欢')):
                return True
            if desc.startswith('收藏') or desc == '添加到我喜欢':
                return False
            return None
        original = state()
        if original is True:
            raise StepUnavailable('歌曲原已收藏，保留用户收藏，不执行取消')
        if original is None:
            raise StepUnavailable('收藏状态未导出，未执行不可核对的切换')
        self.native(rid='ic5')
        try:
            self.content_wait(lambda: state() is True, '收藏状态未确认')
        finally:
            if state() is True:
                self.native(rid='ic5')
                self.wait_for(lambda: state() is False, '本用例新增收藏未恢复')

    @optional('song')
    def lyrics_roundtrip(self):
        self.needs('song')
        self.player()
        self.go(lambda: self.swipe(.8, .4, .2, .4), lambda: self.has(rid='jr_'), '歌词页未打开')
        self.go(lambda: self.swipe(.2, .4, .8, .4), lambda: self.has(desc='专辑封面'), '未返回专辑播放界面')

    def rank_ready(self):
        # 榜单列表滑动后 Charts 大标题会移出屏幕；多个榜卡仍能确认列表。
        cards = sum(self.visible(name) for name in ('巅峰潮流榜', '飙升榜', '热歌榜', '新歌榜'))
        return (self.visible('Charts', region=(0, .04, 1, .2))
                or self.visible('排行榜', region=(0, .04, 1, .2)) or cards >= 2) and not self.main_ready()

    @optional('rank')
    def ranks(self):
        self.home_page()
        self.native(rid='ln0', text='乐馆')
        time.sleep(1)
        self.invalidate()
        for _ in range(3):
            if self.visible('排行榜') or self.visible('排行'):
                break
            self.swipe(.5, .35, .5, .8)
        label = '排行榜' if self.visible('排行榜') else '排行'
        if not self.visible(label):
            raise StepUnavailable('当前首页/乐馆没有可核对的排行榜入口')
        def open_rank():
            if label == '排行' and self.has(desc='排行。双击选择，左右滑动翻页'):
                self.native(desc='排行。双击选择，左右滑动翻页')
            else:
                self.choose(label)
        self.go(open_rank, self.rank_ready, '排行榜未打开')
        if label == '排行':
            self.adapt('当前版本从乐馆的“排行”进入 Charts 排行榜')

    @optional('rank')
    def browse_ranks(self):
        self.needs('rank')
        self.collapse_player()
        self.browse_checked(self.rank_ready, 2, 2, '排行榜不可用')

    def rank_detail(self, name):
        self.needs('rank')
        self.return_to(self.rank_ready, '未返回排行榜')
        self.collapse_player()
        for _ in range(5):
            if self.visible(name):
                break
            self.swipe()
        if not self.visible(name):
            raise StepUnavailable('排行榜中没有'+name+'入口')
        self.go(lambda: self.choose(name),
                lambda: not self.rank_ready() and self.visible(name, True), name+'未打开')

    @optional('hot_rank')
    def hot_rank(self):
        self.rank_detail('热歌榜')

    @optional('rank')
    def back_ranks(self):
        self.needs('rank')
        self.return_to(self.rank_ready, '未返回排行榜')
        self.collapse_player()

    @optional('new_rank')
    def new_rank(self):
        self.rank_detail('新歌榜')

    @optional('share')
    def rank_share(self):
        self.needs('new_rank')
        if not self.visible('新歌榜', True, (0, .08, .6, .25)):
            raise StepUnavailable('当前不在已核对的新歌榜详情')
        def share():
            width, height = self.screen_size()
            rows = [n for n in self.nodes(desc='分享')
                    if .8 < (self.bounds(n)[0]+self.bounds(n)[2])/2/width < .91
                    and self.bounds(n)[3] < height*.13]
            if len(rows) == 1:
                self._locators.add('tree')
                self.click_node(rows[0])
            else:
                # 新歌榜右上分享图标无文案，已按当前详情截图核对。
                self.pct(.865, .082)
        self.go(share, lambda:self.visible('音乐卡片'), '分享面板未打开')

    @optional('share')
    def music_card(self):
        self.needs('share')
        self.go(lambda: self.label_node('音乐卡片'),
                lambda: self.visible('保存图片') or self.visible('保存到相册') or self.visible('分享卡片', True),
                '音乐卡片预览未打开')

    def browse_home(self):
        self.home_page()
        self.browse(2, 2)

    @optional('home_music')
    def home_music(self):
        self.home_page()
        for _ in range(4):
            rows = [n for n in self.nodes(rid='glr') if n.get('clickable') == 'true'
                    and self.bounds(n)[0] < self.d.window_size()[0]*.5]
            if rows:
                break
            self.swipe()
        if not rows:
            raise StepUnavailable('首页没有可核对的音乐单曲卡片')
        self._locators.add('tree')
        title = rows[0].get('content-desc', '').split('音频')[0].strip()
        if not title:
            raise StepUnavailable('音乐卡片没有可核对的单曲名称')
        self.click_node(rows[0])
        self.content_wait(lambda: self.media_state() == 3 and self.media_description().startswith(title+','),
                          '首页音乐卡片未播放对应歌曲')


class TencentNewsDynamicCase(TencentObservedCase):
    PACKAGE = 'com.tencent.news'
    all_app_package_list = [PACKAGE]
    COMPONENT = PACKAGE + '/.activity.SplashActivity'

    def main_ready(self):
        # 未登录版本底栏文字为“未登录”，其入口语义仍是“我的”。
        # 不要求截图出现旧文案；以原生新闻底栏和频道栏确认首页。
        return (self.has(rid='news_tab_button', desc='新闻')
                and self.has(desc='我的') and self.has(rid='channelbar_text'))

    def main_page(self):
        self.dismiss_ads()
        self.return_to(self.main_ready, '未返回腾讯新闻首页')

    def browse_home(self):
        self.main_page()
        self.browse(5, 5)

    def channels(self):
        self.main_page()
        # 在首页频道内容区左右切换，各五次；不横滑热点精选轮播广告卡。
        for left in (True, False):
            for _ in range(5):
                self.swipe(.85 if left else .15, .42, .15 if left else .85, .42)
                time.sleep(1)
                self.dismiss_ads()
                if not self.main_ready():
                    self.main_page()
                    self.adapt('当前频道打开独立页面，返回首页后继续横滑')

    def article_ready(self):
        return not self.main_ready() and self.has(rid='news_detail_title') and (self.has(rid='action_bar_input')
            or self.has(rid='action_bar_comment')
            or self.visible('写评论', True) or self.visible('说两句', True)
            or self.visible('说点什么', True))

    @optional('article')
    def first_news(self):
        self.main_page()
        # 切回要闻，避免横滑后进入直播或付费栏目；按真实新闻标题 ID，排除信息流广告。
        if self.visible('要闻'):
            self.label_node('要闻')
            time.sleep(1)
            self.invalidate()
        for _ in range(4):
            # 同一个 title_text 也用于视频卡片；图文语义可避免误入视频播放页。
            rows = self.nodes(rid='title_text', desc='图文：', prefix=True)
            if rows:
                break
            self.swipe(.5, .35, .5, .8)
        if not rows:
            raise StepUnavailable('首页没有可核对的图文新闻标题')
        self._locators.add('tree')
        self.click_node(rows[0])
        def ready():
            self.dismiss_ads()
            return self.article_ready()
        self.content_wait(ready, '新闻正文未打开')

    @optional('article')
    def browse_article(self):
        self.needs('article')
        self.browse_checked(self.article_ready, 2, 2, '腾讯新闻正文不可用')


class TencentVideoDynamicCase(TencentObservedCase):
    PACKAGE = 'com.tencent.qqlive'
    all_app_package_list = [PACKAGE]
    COMPONENT = PACKAGE + '/.ona.activity.SplashHomeActivity'
    PREROLL_TIMEOUT = 180

    def swipe(self, x1=.5, y1=.78, x2=.5, y2=.32, duration=400):
        self.foreground()
        width, height = self.d.window_size()
        # 腾讯视频广告卡将鼠标拖动当成点击；触屏源才能形成正常的内容滚动。
        result = self.d.shell('input touchscreen -d 0 swipe {} {} {} {} {}'.format(
            round(width*x1), round(height*y1), round(width*x2), round(height*y2), duration))
        if result.exit_code:
            raise RuntimeError('腾讯视频主屏滑动失败：' + result.output)
        self.invalidate()

    def main_ready(self):
        return (self.visible('个人中心', region=(.7, .9, 1, .99))
                and (self.visible('首页', region=(0, .9, .25, .99))
                     or self.visible('返回顶部', region=(0, .9, .25, .99))))

    def main_page(self):
        self.dismiss_ads()
        # VIP 套餐面板用系统返回关闭，不触碰确认协议/开通按钮。
        self.return_to(self.main_ready, '未返回腾讯视频首页', limit=8)

    def browse_home(self):
        self.main_page()
        self.browse(2, 2)

    def video_ready(self):
        return self.activity_is('VideoDetail', 'VideoActivity') and not self.main_ready()

    def preroll(self):
        return self.has(desc='qad_fullscreen_button') or self.visible('VIP可关闭该广告', True)

    def paywall(self):
        return self.visible('开通VIP会员，观看完整内容', True) or self.visible('确认协议并开通', True)

    def require_video(self):
        self.needs('video')
        if not self.video_ready() or self.paywall() or self.preroll():
            raise StepUnavailable('当前视频受会员或广告限制，未操作播放器')

    @optional('video')
    def first_video(self):
        self.main_page()
        # 首个推荐海报，排除顶部广告/会员卡；运行时取控件边界，不固定标题或像素。
        for _ in range(5):
            rows = self.nodes(desc='poster_top_pic_container')
            if rows:
                break
            self.swipe(.5, .35, .5, .8)
        if not rows:
            raise StepUnavailable('首页未导出可核对的推荐视频海报')
        def open_video():
            if not self.main_ready():
                raise StepUnavailable('未进入视频详情且已离开首页，未重复点击旧位置')
            self.native(desc='poster_top_pic_container')
        self.go(open_video, self.video_ready, '推荐视频详情未打开')
        def playing():
            self.dismiss_ads()
            if self.paywall():
                raise StepUnavailable('首个推荐视频要求开通VIP观看完整内容，未购买')
            return not self.preroll() and self.media_state() == 3
        self.content_wait(playing, '广告未结束或视频未开始播放', timeout=self.PREROLL_TIMEOUT)
        for _ in range(6):
            time.sleep(5)
            self.invalidate()
            if not playing():
                raise StepUnavailable('未完成连续30秒正片播放，当前为广告、暂停或会员限制')

    def show_controls(self):
        self.require_video()
        rows = self.nodes(desc='播放器，播放控件未显示，单指双击可显示')
        if rows:
            self._locators.add('tree')
            self.click_node(rows[0])
            self.invalidate()
        # 播放器异步挂载无障碍子节点；截图中已出现的按钮可能晚于点击数百毫秒导出。
        self.content_wait(lambda:self.has(desc='全屏按钮', prefix=True) or self.has(desc='全屏'),
                          '播放器全屏控件尚未显示', timeout=6)

    @optional('fullscreen')
    def fullscreen(self):
        self.require_video()
        self.show_controls()
        rows = [n for n in self.nodes() if n.get('content-desc') in ('全屏', '全屏按钮', '进入全屏')
                or n.get('content-desc', '').startswith('全屏按钮，双击可全屏')]
        if not rows:
            raise StepUnavailable('正片播放器没有可核对的全屏按钮')
        self._locators.add('tree')
        self.click_node(rows[0])
        self.content_wait(lambda:self.d.window_size()[0] > self.d.window_size()[1], '未切换横屏全屏')

    @optional('fullscreen')
    def exit_fullscreen(self):
        self.needs('video', 'fullscreen')
        if self.d.window_size()[0] < self.d.window_size()[1]:
            self.adapt('播放器已返回竖屏，保持竖屏状态')
            return
        self.back()
        self.content_wait(lambda:self.d.window_size()[0] < self.d.window_size()[1], '未退出横屏全屏')

    @optional('video')
    def browse_recommendations(self):
        self.require_video()
        # 下方内容区滚动，避开固定播放器，保持上/下各三次。
        for up in (True, False):
            for _ in range(3):
                self.swipe(.5, .86 if up else .48, .5, .48 if up else .86)
                time.sleep(2)
        self.adapt('当前详情底部为选集、推荐等混合内容，按底部内容区上下各三次浏览')

    def search_ready(self):
        return self.activity_is('SearchPagerActivity') and any(n.get('class') == 'android.widget.EditText' for n in self.nodes())

    @optional('search')
    def search_page(self):
        self.main_page()
        self.go(lambda:self.native(desc='搜索框'), self.search_ready, '腾讯视频搜索页未打开')

    def results_ready(self):
        return (self.activity_is('SearchPagerActivity') and self.has(desc='搜索结果页')
                and self.has(desc='斗破苍穹', prefix=True))

    @optional('search')
    def search_drama(self):
        self.needs('search')
        if not self.search_ready():
            raise StepUnavailable('当前不在腾讯视频搜索输入页')
        self.input_text('斗破苍穹')
        self.choose('搜索', region=(.85, .05, 1, .12))
        self.content_wait(self.results_ready, '斗破苍穹搜索结果未显示')

    @optional('search')
    def browse_results(self):
        self.needs('search')
        self.browse_checked(self.results_ready, 3, 3, '腾讯视频搜索结果不可用')

    @optional('film')
    def film_tab(self):
        self.needs('search')
        if not self.results_ready():
            raise StepUnavailable('腾讯视频搜索结果不可用')
        if not self.visible('影视', region=(0, .09, 1, .2)):
            raise StepUnavailable('当前版本搜索分类没有“影视”入口')
        self.go(lambda:self.native(desc='影视未选中'),
                lambda:self.has(desc='影视已选中'), '影视分类未选中')

    @optional('film')
    def browse_films(self):
        self.needs('film')
        self.browse_checked(self.results_ready, 1, 1, '影视搜索结果不可用')
