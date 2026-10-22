"""米家产品、智能场景与添加设备页浏览（表格第 1113～1122 行）。"""
import logging

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_mihome_0010(DynamicAppCase):
    PACKAGE = 'com.xiaomi.smarthome'
    all_app_package_list = [PACKAGE]

    def selected_tab(self, name):
        return any(n.get('selected') == 'true'
                   for n in self.tab_nodes(name))

    def tab_nodes(self, name):
        # 版本更新会重排混淆 id，以底栏文字和实时边界定位。
        height = self.screen_size()[1]
        return [n for n in self.nodes(text=name) if self.bounds(n)[1] > height * .9]

    def navigation_ready(self):
        return all(self.tab_nodes(name) for name in ('米家', '智能', '产品'))

    def switch_tab(self, name):
        self.transition(lambda: self.click_node(self.tab_nodes(name)[0]),
                        lambda: self.selected_tab(name), '米家未切换到{}页'.format(name))

    def launch(self):
        self.start()
        self.return_to(self.navigation_ready,
                       '米家首页导航未就绪，请确认已登录')
        self.switch_tab('米家')
        self.require(desc='添加设备')

    def product(self):
        self.switch_tab('产品')
        self.wait_for(lambda: self.has(text='搜索更多智能产品'), '产品内容未加载', timeout=30)

    def smart(self):
        self.switch_tab('智能')
        self.wait_for(lambda: self.has(text='我的智能'), '智能页面未加载')

    def return_home_scene(self):
        # 新版“探索”中“手机回家模式”替代旧版“回家”。只浏览，不开启或保存场景。
        for _ in range(7):
            for name in ('回家', '手机回家模式'):
                if self.has(text=name):
                    logging.info('回家场景入口：%s', name)
                    if name != '回家':
                        self._adaptation = '新版米家以手机回家模式替代原回家场景入口，仅浏览不启用场景'
                    self.open_control(lambda: self.has(text=name) and not self.navigation_ready(),
                                      '回家场景详情未打开', text=name)
                    return
            self.swipe()
        # 用户允许版本缺失功能跳过，保留明确日志；不以任意页面冒充回家场景。
        self._last_skip_reason = '当前智能探索页未提供回家/手机回家模式入口'
        logging.warning('SKIP：%s', self._last_skip_reason)
        return False

    def main_page(self):
        self.return_to(self.navigation_ready, '未返回米家导航页')
        self.switch_tab('米家')
        self.require(desc='添加设备')

    def add_device(self):
        # 右上角加号先展开菜单，再进入添加页，避免把菜单误认为添加成功。
        self.open_control(lambda: self.has(text='添加设备'),
                          '添加设备菜单未展开', desc='添加设备')
        self.open_control(lambda: self.has(text='手动添加设备'),
                          '添加设备页面未加载', text='添加设备')

    def steps(self):
        return [
            ('启动米家', self.launch, 3),
            ('点击产品，切换到产品页', self.product, 2),
            ('产品页面上下滑动3次', lambda: self.browse(3, 3), 0),
            ('点击智能，切换到智能页', self.smart, 2),
            ('智能页面上下滑动3次', lambda: self.browse(3, 3), 0),
            ('点击回家，切换到回家页', self.return_home_scene, 3),
            ('点击米家，回到首页', self.main_page, 2),
            ('点击右上角加号，添加设备', self.add_device, 3),
            ('返回米家主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 1),
        ]
