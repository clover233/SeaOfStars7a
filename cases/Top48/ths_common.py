"""同花顺自选浏览与格力电器自选管理，不进入交易流程。"""
from Cases.Top48.observed_apps_common import ObservedAppCase, StepUnavailable, optional


class ThsDynamicCase(ObservedAppCase):
    PACKAGE = 'com.hexin.plat.android'
    all_app_package_list = [PACKAGE]
    COMPONENT = PACKAGE + '/.LogoEmptyActivity'

    def dismiss_ads(self):
        super().dismiss_ads()
        if self.has(rid='bubble_layout') and self.has(rid='close_btn'):
            self.click(rid='close_btn')

    def selected_bottom(self, label):
        return any(n.get('selected') == 'true' for n in self.nodes(desc=label))

    def main_ready(self):
        return self.has(desc='首页') and self.has(desc='自选')

    def main_page(self):
        self.return_to(self.main_ready, '未返回同花顺主界面', limit=10)
        self.go(lambda: self.bottom_node('首页'), lambda: self.selected_bottom('首页'), '未切换同花顺首页')

    @optional('watchlist')
    def watchlist(self):
        self.main_page()
        self.go(lambda: self.bottom_node('自选'), lambda: self.selected_bottom('自选'), '自选列表未打开')

    @optional('watchlist')
    def watch_up(self):
        self.needs('watchlist')
        if not self.selected_bottom('自选'):
            raise StepUnavailable('当前不在自选列表')
        self.browse(2, 0)

    @optional('watchlist')
    def watch_down(self):
        self.needs('watchlist')
        if not self.selected_bottom('自选'):
            raise StepUnavailable('当前不在自选列表')
        self.browse(0, 2)

    @optional('stock-search')
    def stock_search(self):
        self.needs('watchlist')
        if self.has(desc='股票搜索'):
            self._locators.add('tree')
            self.click(desc='股票搜索')
        elif self.has(rid='new_title_search'):
            self._locators.add('tree')
            self.click(rid='new_title_search')
        else:
            self.choose('搜索', True, region=(0, .04, 1, .16), index=0)
        self.content_wait(lambda: any(n.get('class') == 'android.widget.EditText' for n in self.nodes()),
                          '股票搜索输入框未打开')

    @optional('stock-search')
    def stock_query(self):
        self.needs('stock-search')
        fields = [n for n in self.nodes() if n.get('class') == 'android.widget.EditText']
        if len(fields) != 1:
            raise StepUnavailable('股票搜索框不唯一或不存在')
        self.click_node(fields[0])
        self.input_text('格力电器')
        self.content_wait(lambda: self.visible('格力电器', region=(0, .13, 1, .85))
                          and self.visible('000651', True), '格力电器股票搜索结果未显示')

    @optional('stock-detail')
    def stock_detail(self):
        self.needs('stock-search')
        self.choose('格力电器', region=(0, .13, 1, .85), index=0)
        self.content_wait(self.stock_ready, '格力电器股票详情未打开')
        self._watch_added = False
        self._watch_original = self.watch_is_added()

    def watch_label(self):
        rows = self.nodes(rid='tv_add_remove_zixuan')
        labels = {row.get('text', '') for row in rows if row.get('text')}
        if len(labels) == 1:
            return labels.pop()
        for label in ('删自选', '已加自选', '已自选', '删除自选', '移出自选', '加自选', '添加自选'):
            if self.visible(label, region=(.5, .87, .9, 1)):
                return label
        return ''

    def watch_is_added(self):
        return self.watch_label() in ('删自选', '已加自选', '已自选', '删除自选', '移出自选')

    def stock_ready(self):
        return self.visible('格力电器', True, (0, .04, 1, .18)) and (
            self.visible('分时') or self.visible('日K') or self.visible('加自选', True)
            or self.visible('删自选', True))

    @optional('watch-add')
    def add_watch(self):
        self.needs('stock-detail')
        if not self.stock_ready():
            raise StepUnavailable('当前不是格力电器详情')
        if getattr(self, '_watch_original', False):
            raise StepUnavailable('格力电器原本已在自选中，保留原有状态，不重复添加')
        if self.watch_label() not in ('加自选', '添加自选'):
            raise StepUnavailable('未识别到可确认未加入自选的按钮状态')
        self._locators.add('tree')
        self.click(rid='ll_add_remove_zixuan')
        try:
            self.content_wait(self.watch_is_added, '加入自选后未看到状态确认')
        finally:
            self._watch_added = self.watch_is_added()

    @optional('stock-detail')
    def browse_stock(self):
        self.needs('stock-detail')
        self.browse(3, 0)

    def remove_watch(self):
        self.needs('stock-detail')
        if not getattr(self, '_watch_added', False) or getattr(self, '_watch_original', False):
            raise StepUnavailable('本次用例没有新增格力电器，不删除原有自选')
        if not self.stock_ready():
            raise StepUnavailable('当前不是格力电器详情，不操作其他股票自选')
        for _ in range(4):
            if self.watch_is_added():
                break
            self.swipe(y1=.3, y2=.8)
        if not self.watch_is_added():
            raise StepUnavailable('没有识别到本次新增自选的删除入口')
        self._locators.add('tree')
        self.click(rid='ll_add_remove_zixuan')
        if self.visible('确定') and self.visible('删除', True):
            self.choose('确定')
        self.content_wait(lambda: self.watch_label() in ('加自选', '添加自选'),
                          '移除本次新增自选后未看到状态确认')
        self._watch_added = False

    def clean_up(self):
        try:
            if getattr(self, '_watch_added', False) and not getattr(self, '_watch_original', False):
                was_home = 'launcher' in self.current_app()['activity'].lower()
                if self.current_app()['package'] != self.PACKAGE:
                    self.d.app_start(self.PACKAGE)
                    self.invalidate()
                if not self.stock_ready():
                    self.watchlist()
                    self.stock_search()
                    self.stock_query()
                    self.stock_detail()
                    self._watch_added = True
                    self._watch_original = False
                self.remove_watch()
                if was_home:
                    self.home()
        finally:
            super().clean_up()
