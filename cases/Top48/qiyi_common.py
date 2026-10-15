"""爱奇艺动态性能用例的页面操作。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class QiyiDynamicCase(DynamicAppCase):
    PACKAGE = 'com.qiyi.video'

    def point(self, x, y):
        self.foreground()
        # 爱奇艺 17.9.5 会过滤普通短点击，450ms 能稳定触发且未达到长按菜单阈值。
        self.d.long_click(round(x), round(y), duration=.45)

    def swipe(self, x1=.5, y1=.78, x2=.5, y2=.32, duration=400):
        self.foreground()
        width, height = self.d.window_size()
        self.d.swipe(round(width * x1), round(height * y1),
                     round(width * x2), round(height * y2),
                     duration=duration / 1000)

    def home_ready(self):
        return (self.has(desc='搜索')
                and any(node.get('selected') == 'true'
                        for node in self.nodes(rid='navi0')))

    def launch(self):
        self.start()
        if not self.home_ready():
            self.main_page()
        self.wait_for(self.home_ready, '爱奇艺首页未加载', timeout=30)

    def selected_channel(self, name):
        return any(node.get('selected') == 'true'
                   and node.get('class') == 'android.widget.RadioButton'
                   for node in self.nodes(text=name))

    def channel_nodes(self, name):
        return [node for node in self.nodes(text=name)
                if node.get('class') == 'android.widget.RadioButton']

    def channel(self, name):
        if not self.channel_nodes(name):
            if name == '首页':
                width, height = self.d.window_size()
                for _ in range(3):
                    self.d.swipe(round(width * .20), round(height * .125),
                                 round(width * .85), round(height * .125), duration=.4)
                    time.sleep(.5)
                    if self.channel_nodes(name):
                        break
            else:
                self.click(desc='更多频道')
            self.wait_for(lambda: bool(self.channel_nodes(name)),
                          '爱奇艺没有{}频道'.format(name))
        channel_nodes = self.channel_nodes(name)
        if not channel_nodes:
            raise RuntimeError('爱奇艺{}频道入口不可用'.format(name))
        target = channel_nodes[0]
        self.transition(lambda: self.click_node(target),
                        lambda: self.selected_channel(name),
                        '爱奇艺未切换到{}频道'.format(name))

    def tv(self):
        self.channel('电视剧')

    def movie(self):
        self.channel('电影')

    def main_page(self):
        self.return_to(self.home_ready, '未返回爱奇艺主界面', limit=7)
        if not self.selected_channel('首页'):
            self.channel('首页')

    def search_ready(self):
        return bool(self.d(className='android.widget.EditText').count)

    def open_search(self):
        self.main_page()
        self.transition(lambda: self.click(desc='搜索'), self.search_ready,
                        '爱奇艺搜索页未打开')

    def input_movie(self):
        if not self.search_ready():
            raise RuntimeError('爱奇艺搜索输入框不可用')
        edit = self.d(className='android.widget.EditText')
        edit.click()
        edit.set_text('大话天仙')

    def results_ready(self):
        edit = self.d(className='android.widget.EditText')
        return (edit.exists and edit.get_text() == '大话天仙'
                and self.has(rid='video_area')
                and self.has(text='大话天仙'))

    def submit_once(self):
        buttons = self.nodes(rid='btn_search')
        if not buttons:
            buttons = [node for node in self.nodes(text='搜索')
                       if node.get('clickable') == 'true']
        if buttons:
            self.click_node(buttons[-1])
        else:
            raise RuntimeError('爱奇艺搜索按钮不可用')
        self.wait_for(self.results_ready,
                      '爱奇艺“大话天仙”搜索结果未加载', timeout=25)

    def search_twice(self):
        for _ in range(2):
            edits = self.d(className='android.widget.EditText')
            if not edits.exists:
                raise RuntimeError('爱奇艺搜索输入框不可用')
            edits.click()
            edits.set_text('大话天仙')
            self.submit_once()
            time.sleep(2)

    def player_ready(self):
        activity = self.current_app()['activity'].lower()
        return ('player' in activity or 'video' in activity
                or self.has(desc='暂停') or self.has(desc='播放'))

    def play_movie(self):
        all_nodes = self.nodes()
        targets = [node for node in all_nodes
                   if node.get('text') == '大话天仙'
                   and node.get('class') != 'android.widget.EditText']
        if not targets:
            raise RuntimeError('爱奇艺搜索结果没有“大话天仙”')
        target = targets[-1]
        containers = [node for node in all_nodes
                      if node.get('clickable') == 'true' and target in list(node.iter('node'))]
        if containers:
            target = min(containers, key=lambda node: (
                self.bounds(node)[2] - self.bounds(node)[0])
                * (self.bounds(node)[3] - self.bounds(node)[1]))
        self.transition(lambda: self.click_node(target), self.player_ready,
                        '“大话天仙”未开始播放')
