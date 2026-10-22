"""优酷频道浏览、搜索与播放；用例表 2019～2031 行。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_youku_0020(DynamicAppCase):
    PACKAGE = 'com.youku.phone'
    all_app_package_list = [PACKAGE]
    QUERY = '大话天仙'

    def dismiss_prompts(self):
        if self.has(rid='splash_ad_txt_skip'):
            self.click(rid='splash_ad_txt_skip')
        if self.has(text='您当前的ip可能变更', prefix=True):
            self.click(text='关闭', rid='android:id/button2')
            time.sleep(.5)

    def main_ready(self):
        return self.has(rid='home_logo_img') and self.has(desc='搜索框', prefix=True)

    def launch(self):
        self.start()
        time.sleep(5)
        self.dismiss_prompts()
        self.main_page()

    def channel_selected(self, name):
        return any(n.get('selected') == 'true' for n in self.nodes(desc=name)
                   if n.get('class') == 'android.widget.Button')

    def channel(self, name):
        self.wait_for(self.main_ready, '优酷首页频道栏未加载')
        for _ in range(4):
            if self.has(desc=name):
                break
            # 选中电影后频道栏自动左移，先把首页标签滑回可见区域。
            self.swipe(.2, .137, .8, .137, 400)
            time.sleep(.4)
        self.open_control(lambda: self.channel_selected(name),
                          '优酷未切换到{}频道'.format(name), desc=name)

    def main_page(self):
        self.dismiss_prompts()
        self.return_to(self.main_ready, '未返回优酷主界面', limit=8)
        self.channel('首页')

    def search_ready(self):
        return self.has(rid='et_widget_search_text_soku')

    def open_search(self):
        self.main_page()
        # 点击当前控件树中的 TextSwitcher，避免旧版搜索框比例落到其他入口。
        self.open_control(self.search_ready, '优酷搜索输入页未打开', desc='搜索框', prefix=True)

    def input_movie(self):
        self.wait_for(self.search_ready, '优酷搜索输入框未出现')
        self.click(rid='et_widget_search_text_soku')
        self.d(resourceId=self.PACKAGE + ':id/et_widget_search_text_soku').set_text(self.QUERY)
        self.wait_for(lambda: self.has(text=self.QUERY, rid='et_widget_search_text_soku'),
                      '优酷搜索词未写入')

    def results_ready(self):
        return self.has(text=self.QUERY, rid='item_b_program_info_title')

    def search_twice(self):
        for _ in range(2):
            self.input_movie()
            self.click(text='搜索', rid='tv_right')
            self.wait_for(self.results_ready, '优酷大话天仙搜索结果未加载', timeout=25)
            time.sleep(1)

    def player_ready(self):
        return any(name in self.current_app()['activity'] for name in (
            'PlayerActivity', 'SmallVideoNcrActivity'))

    def play_movie(self):
        self.wait_for(self.results_ready, '播放前未找到大话天仙搜索结果')
        external_only = self.has(text='外站播放')
        self.open_control(self.player_ready, '大话天仙播放页未打开',
                          text=self.QUERY, rid='item_b_program_info_title')
        if external_only:
            self._adaptation = '当前大话天仙正片仅提供外站播放，改为搜索结果关联的站内短片播放30秒'

    def browse_player(self):
        self.wait_for(self.player_ready, '视频播放页未打开')
        self.browse(5, 5)

    def steps(self):
        return [
            ('启动优酷', self.launch, 2),
            ('首页浏览上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击动漫tab页', lambda: self.channel('动漫'), 1),
            ('动漫tab页浏览上滑3次，下滑3次', lambda: self.browse(3, 3), 0),
            ('点击电影tab页', lambda: self.channel('电影'), 1),
            ('电影tab页浏览上滑3次，下滑3次', lambda: self.browse(3, 3), 0),
            ('返回推荐页点击搜索框，切换到搜索页面', self.open_search, 1),
            ('输入大话天仙', self.input_movie, 1),
            ('搜索视频大话天仙，重复搜索2次', self.search_twice, 1),
            ('点击播放大话天仙，观看30秒', self.play_movie, 30),
            ('视频播放页浏览上滑5次，下滑5次', self.browse_player, 0),
            ('返回优酷主界面', self.main_page, 2),
            ('上滑返回桌面', self.home, 2),
        ]
