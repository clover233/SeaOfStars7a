"""抖音极速版推荐、热点、作者首个作品与评论。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_douyinjisu_0010(DynamicAppCase):
    PACKAGE = 'com.ss.android.ugc.aweme.lite'
    all_app_package_list = [PACKAGE]

    def on_home(self):
        return self.has(desc='首页，按钮') and self.has(rid='rho')

    def launch(self):
        self.start()
        self.return_to(self.on_home, '未返回抖音极速版主界面', limit=8)

    def channel(self, label):
        if not self.has(rid='rho', text=label) and self.has(rid='r94'):
            self.click(rid='r94')
            self.wait_for(lambda: self.has(text=label), '频道列表未显示{}'.format(label))
            self.click(text=label)
        else:
            self.open_control(lambda: self.has(desc=label + '，已选中，按钮'),
                              '未切换至{}频道'.format(label), rid='rho', text=label)
        self.wait_for(lambda: self.has(desc=label + '，已选中，按钮'),
                      '未进入{}频道，请先将频道添加到顶部'.format(label))

    def recommendation(self):
        self.channel('推荐')
        self.wait_for(lambda: self.has(rid='user_avatar'), '推荐视频未加载', timeout=30)

    def hotspot(self):
        self.channel('热点')
        self.wait_for(lambda: self.has(desc='视频'), '热点首个视频未加载', timeout=30)

    def first_video(self):
        # 热点新版先显示热榜和首个视频卡片，点击实际视频控件展开。
        self.open_control(lambda: self.has(rid='user_avatar'), '热点视频未进入播放页', desc='视频')
        if self.has(desc='播放视频，按钮'):
            self.click(desc='播放视频，按钮')
        self.wait_for(lambda: self.has(desc='暂停视频，按钮'), '热点视频未开始播放', timeout=20)

    def creator(self):
        self.open_control(lambda: self.has(text='作品') and self.has(text='粉丝'),
                          '未进入视频作者主页', rid='user_avatar')

    def author_first(self):
        # 上下浏览后按第一行、第一列选当前作品，不写死作者、作品名或屏幕坐标。
        self.reveal('未找到作者作品页签', text='作品')
        self.click(text='作品')
        width, height = self.d.window_size()
        def cards():
            return [n for n in self.nodes(rid='g_4')
                    if self.bounds(n)[2] - self.bounds(n)[0] < width * .5
                    and self.bounds(n)[3] - self.bounds(n)[1] > height * .08]
        # 恢复作品网格顶部，确保点击的是第一个作品。
        for _ in range(6):
            if self.has(text='粉丝'):
                break
            self.swipe(y1=.35, y2=.8)
            time.sleep(1)
        self.wait_for(lambda: bool(cards()), '作者作品网格未加载', timeout=30)
        first = sorted(cards(), key=lambda n: (self.bounds(n)[1], self.bounds(n)[0]))[0]
        self.click_node(first)
        self.wait_for(lambda: self.has(rid='back_btn') and self.has(rid='user_avatar'),
                      '未打开作者首个作品')
        if self.has(desc='播放视频，按钮'):
            self.click(desc='播放视频，按钮')

    def comments(self):
        self.open_control(lambda: self.has(desc='关闭') and
                          any(n.get('text', '').endswith('条评论') for n in self.nodes(rid='title')),
                          '视频评论面板未打开', rid='comment_container')

    def app_home(self):
        self.return_to(self.on_home, '未返回抖音极速版主界面', limit=8)

    def steps(self):
        return [
            ('启动抖音极速版', self.launch, 3),
            ('点击推荐', self.recommendation, 1),
            ('上下滑动5次浏览推荐页', lambda: self.browse(5, 5), 0),
            ('点击热点', self.hotspot, 1),
            ('点击第一个视频播放', self.first_video, 2),
            ('点击视频的up主', self.creator, 1),
            ('上下滑动5次浏览up主页', lambda: self.browse(5, 5), 0),
            ('点击up主第一个视频播放', self.author_first, 2),
            ('点击查看视频下的评论', self.comments, 1),
            ('返回抖音极速版主界面', self.app_home, 1),
            ('滑动返回Home页', self.home, 1),
        ]
