"""番茄畅听搜索、短剧和听歌浏览场景；步骤对应 Excel 第 686–696 行。"""
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_fanqiechangting_0010(DynamicAppCase):
    PACKAGE = 'com.xs.fm'
    all_app_package_list = [PACKAGE]
    HOME_ID = 'amr'
    MUSIC_ID = 'g7d'

    def home_ready(self):
        # 听歌页也保留同一套底部导航和“推荐”文案；首页顶部搜索框才是稳定区分项。
        return self.has(rid=self.HOME_ID) and bool(self.home_search_boxes())

    def home_search_boxes(self):
        height = self.screen_size()[1]
        return [node for node in self.nodes(rid='title')
                if self.bounds(node)[1] < height * .12]

    def return_home_tab(self):
        if not self.has(rid=self.HOME_ID):
            # 听歌页使用自绘界面，控件树可能只有根节点。先关闭弹窗，再按比例点首页。
            self.back()
            if not self.has(rid=self.HOME_ID):
                self.pct(.1, .94)
                time.sleep(2)
        self.wait_for(lambda: self.has(rid=self.HOME_ID), '未显示番茄畅听底部导航')
        # 底部首页在短剧频道也存在；仍实际点击，以恢复首页并滚回顶部。
        self.click(rid=self.HOME_ID)
        self.wait_for(self.home_ready, '番茄畅听未切换到首页')

    def launch(self):
        self.start()
        if 'SearchActivity' in self.current_app()['activity']:
            self.side_return()
        self.return_home_tab()

    def search_box(self):
        nodes = self.home_search_boxes()
        if not nodes:
            raise RuntimeError('未找到番茄畅听顶部搜索框')
        return sorted(nodes, key=lambda node: self.bounds(node)[1])[0]

    def search_olympics(self):
        # 浏览/播放器返回后先恢复首页，不能假定先前的顶部搜索框仍在当前页。
        self.return_home_tab()
        self.transition(lambda: self.click_node(self.search_box()),
                        lambda: self.has(rid='fpw') and self.has(text='搜索', rid='io'),
                        '番茄畅听搜索页未打开')
        self.d(resourceId=self.PACKAGE + ':id/fpw', packageName=self.PACKAGE).set_text('奥运会')
        # 等软键盘和应用窗口边界稳定，避免输入完成瞬间取到过渡态可视区域。
        time.sleep(1)
        self.click(text='搜索', rid='io')
        self.wait_for(lambda: any('奥运会' in node.get('text', '')
                                  for node in self.nodes() if node.get('resource-id') !=
                                  self.PACKAGE + ':id/fpw'),
                      '“奥运会”搜索结果未加载', timeout=20)

    def side_return(self):
        self.swipe(.005, .5, .45, .5, 350)
        self.wait_for(lambda: self.has(rid=self.HOME_ID), '侧滑后未返回番茄畅听首页')

    def short_drama(self):
        self.transition(lambda: self.click(text='短剧'),
                        lambda: any(node.get('selected') == 'true'
                                    for node in self.nodes(text='短剧')),
                        '番茄畅听未进入短剧推荐页')

    def listen_music(self):
        self.click(rid=self.MUSIC_ID)
        # 当前版本听歌页为自绘页面，进入后常只暴露根节点。
        self.wait_for(lambda: not self.home_ready(), '番茄畅听未进入听歌页')

    def steps(self):
        return [
            ('启动番茄畅听', self.launch, 3),
            ('首页滑动，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击上方搜索框，输入奥运会，点击搜索', self.search_olympics, 2),
            ('在搜索界面，上滑5次', lambda: self.browse(5, 0), 0),
            ('侧滑返回到首页', self.side_return, 2),
            ('点击短剧，进入短剧推荐页面', self.short_drama, 2),
            ('短剧推荐页面滑动，上滑10次', lambda: self.browse(10, 0), 0),
            ('点击底部首页', self.return_home_tab, 2),
            ('首页上滑3次，下滑3次', lambda: self.browse(3, 3), 0),
            ('点击底部音乐（听歌）', self.listen_music, 3),
            ('滑动返回Home页', self.home, 1),
        ]
