# -*- coding: utf-8 -*-
"""百度问答与百科浏览；步骤来自动态性能模型测试用例7.xlsx。"""
import re
import time
import xml.etree.ElementTree as ET

from Cases.Top48.dynamic_apps_common import DynamicAppCase


class PerformanceDynamic_baidu_0010(DynamicAppCase):
    PACKAGE = 'com.baidu.searchbox'
    all_app_package_list = [PACKAGE]
    QUESTION = '西安三天旅行攻略'
    QUERY = '西安百度百科'

    def is_home(self):
        current = self.current_app()
        height = self.d.window_size()[1]
        return (current['package'] == self.PACKAGE
                and current['activity'].endswith('.MainActivity')
                and all(any(self.bounds(n)[1] > height * .9 for n in self.nodes(text=label))
                        for label in ('百度', '我的')))

    def dismiss_splash_ad(self):
        height = self.d.window_size()[1]
        skip = [n for n in self.nodes(text='跳过') if self.bounds(n)[3] < height * .16]
        if len(skip) == 1:
            self.click_node(skip[0])
            return True
        return False

    def launch_ready(self):
        if self.dismiss_splash_ad():
            return False
        if self.is_home():
            return True
        activity = self.current_app()['activity']
        if activity.endswith('.LightSearchActivity') or 'SwanAppActivity' in activity:
            # 热启动会恢复上次搜索/百科页面；仅对已识别的内容页返回，
            # Splash 等启动中页面仍只等待，避免返回退出应用。
            self.return_home()
            return self.is_home()
        return False

    def return_home(self):
        for _ in range(10):
            self.foreground()
            if self.dismiss_splash_ad():
                self.wait_for(self.is_home, '百度开屏结束后首页未加载', timeout=30)
                return
            if self.is_home():
                return
            self.d.press('back')
            time.sleep(0.8)
        raise RuntimeError('未返回百度主界面')

    def launch(self):
        self.start()
        # 开屏时不能用 Back 探测首页，否则会退出百度回到桌面。
        self.wait_for(self.launch_ready, '百度启动后首页未加载', timeout=35)

    def is_ai(self):
        return self.d(description='newChat', packageName=self.PACKAGE).exists and (
            self.d(text='文心助手').exists or self.d(text='文心一言').exists)

    def open_ai(self):
        if not self.is_home():
            raise RuntimeError('打开文心前不在百度首页')
        def click_entry():
            entry = self.d(text='文心一言', className='android.widget.TextView')
            if entry.exists:
                self.tap(text='文心一言', className='android.widget.TextView')
            else:
                # 15.78 版底部中间为无文字图标，实机截图核实。
                self.relative_click(0.5, 0.953)
        self.transition(click_entry, self.is_ai, '未打开文心问答页')

    def edit(self):
        return self.d(className='android.widget.EditText', packageName=self.PACKAGE)

    def ask_question(self):
        if not self.is_ai():
            raise RuntimeError('当前不是文心问答页')
        if not self.edit().wait(timeout=6):
            self.transition(lambda: self.relative_click(0.4, 0.92),
                            lambda: self.edit().exists, '未找到文心输入框，请关闭首次介绍或完成登录')
        edit = self.edit()
        if edit.count != 1:
            raise RuntimeError('文心输入框不唯一')
        # 任务模式和快速问答的负载不同，明确使用普通快速问答。
        if self.d(text='任务', className='android.widget.TextView').exists:
            self.transition(lambda: self.tap(text='任务', className='android.widget.TextView'),
                            lambda: self.d(text='快速回答').exists, '未展开问答模式菜单')
            self.tap(text='快速', className='android.widget.TextView')
            self.wait_for(lambda: not self.d(text='快速回答').exists, '未关闭问答模式菜单')
        edit.set_text(self.QUESTION)
        time.sleep(1)
        def submit():
            if not self.is_ai() or edit.get_text() != self.QUESTION:
                raise RuntimeError('文心提交前输入内容或页面发生变化')
            root = ET.fromstring(self.d.dump_hierarchy())
            parents = {child: parent for parent in root.iter() for child in parent}
            width = self.d.window_size()[0]
            for node in root.iter('node'):
                if node.get('class') != 'android.widget.EditText' or node.get('text') != self.QUESTION:
                    continue
                box = list(map(int, re.findall(r'\d+', node.get('bounds', ''))))
                icons = []
                # 输入框直属容器中右下角的可点击 ImageView 是发送箭头；
                # 读取实时 bounds，适配键盘高度，排除右上角清空按钮。
                for child in parents[node]:
                    if child.get('class') != 'android.widget.ImageView' or child.get('clickable') != 'true':
                        continue
                    b = list(map(int, re.findall(r'\d+', child.get('bounds', ''))))
                    if len(b) == 4 and b[1] > box[3] and b[0] > width * 0.75:
                        icons.append(b)
                if len(icons) == 1:
                    x1, y1, x2, y2 = icons[0]
                    self.click_point((x1+x2)//2, (y1+y2)//2)
                    return
            raise RuntimeError('未找到唯一文心发送箭头')
        self.transition(submit, lambda: not edit.exists or edit.get_text() != self.QUESTION,
                        '文心问题未提交')
        time.sleep(8)  # 回答主体为 Canvas；预留生成时间，截图随该步骤导出。
        if not self.is_ai():
            raise RuntimeError('问答提交后离开文心页面，请检查登录状态')

    def open_search(self):
        if not self.is_home():
            raise RuntimeError('打开搜索框前不在百度首页')
        self.transition(lambda: self.relative_click(0.4, 0.085),
                        lambda: self.edit().exists, '搜索输入框未打开')

    def search_encyclopedia(self):
        edit = self.edit()
        if not edit.exists or edit.count != 1:
            raise RuntimeError('当前不是百度搜索输入页')
        edit.set_text(self.QUERY)
        # 输入页背后的旧结果可能仍留在 UiSelector 查询中；必须实际提交，
        # 再只用主屏当前节点确认结果，不能让旧结果令 transition 提前返回。
        height = self.d.window_size()[1]
        buttons = [n for n in self.nodes(text='搜索') if self.bounds(n)[3] < height * .18]
        if len(buttons) != 1:
            raise RuntimeError('百度搜索提交入口不唯一')
        self.click_node(buttons[0])
        self.wait_for(self.is_results, '百科搜索结果未加载', timeout=25)
        time.sleep(3)

    def is_results(self):
        nodes = self.nodes()
        height = self.d.window_size()[1]
        return (any(n.get('text') == self.QUERY and self.bounds(n)[3] < height * .18 for n in nodes)
                and any(n.get('text') == '综合' and self.bounds(n)[3] < height * .3 for n in nodes)
                and not any(n.get('class') == 'android.widget.EditText' for n in nodes))

    def open_first_result(self):
        if not self.is_results():
            raise RuntimeError('当前不是西安百度百科搜索结果页')
        def click_result():
            result = self.d(textMatches='^西安(?:市)?[_－-]百度百科$', className='android.widget.TextView')
            if result.exists and result.count == 1:
                box = result.info['bounds']
                self.click_point((box['left']+box['right'])//2, (box['top']+box['bottom'])//2)
            else:
                # 当前首条为“百度AI·百度百科解答”卡片，正文前百科标识进入详情。
                self.relative_click(0.115, 0.484)
        self.transition(click_result,
                        lambda: 'SwanAppActivity' in self.current_app()['activity'],
                        '首个百科结果未进入详情')
        time.sleep(3)

    def steps(self):
        return [
            ('启动百度浏览器', self.launch, 2),
            ('点击底部文心一言', self.open_ai, 2),
            ('输入西安三天旅行攻略进行问答', self.ask_question, 2),
            ('返回百度主界面', self.return_home, 2),
            ('点击搜索框，拉起输入法', self.open_search, 2),
            ('输入西安百度百科点击搜索', self.search_encyclopedia, 2),
            ('浏览搜索结果，上滑5次，下滑5次', self.browse, 0),
            ('点击第一个搜索结果查看详情', self.open_first_result, 2),
            ('上滑5次，下滑5次，查看搜索结果', self.browse, 0),
            ('返回百度主界面', self.return_home, 2),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
