"""微博实机定位：weditor 0.7.3 Dump Hierarchy / Android 17，2026-10-16。"""
import re
import time

from Cases.Top48.shopping_common import ShoppingDynamicCase, StepUnavailable
from Cases.Top48.weibo_vip_common import WeiboVipDynamicCase


class WeiboDynamicCase(WeiboVipDynamicCase):
    PACKAGE = 'com.sina.weibo'
    all_app_package_list = [PACKAGE]

    def main_ready(self):
        return self.activity_has('MainTabActivity') and self.has(desc='首页')

    def launch(self):
        self._liked_by_case = False
        self._draft = False
        self.start()
        if self.activity_has('MPDialogActivity'):
            self.back()  # 游客签到广告；不点击领取。
        self.main_page()
        self._visitor = self.activity_has('VisitorMainTabActivity')

    def main_page(self):
        for _ in range(12):
            if self.main_ready():
                self.bottom('首页')
                self.wait_for(lambda: self.find_label('推荐') is not None, '微博首页未加载')
                return
            if getattr(self, '_draft', False):
                node = self.find_label('不保存', '不保留', '放弃编辑')
                if node is not None:
                    self.click_node(node)
                    self._draft = False
                    continue
            self.back()
        raise RuntimeError('未能返回微博主界面')

    def bottom_node(self, label):
        height = self.d.window_size()[1]
        nodes = [n for n in self.nodes() if self.bounds(n)[1] > height*.86
                 and label in (n.get('text'), n.get('content-desc'))]
        if not nodes:
            raise StepUnavailable('当前微博没有底栏入口：' + label)
        return nodes[0]

    def bottom(self, label):
        self.click_node(self.bottom_node(label))

    def require_account(self):
        if getattr(self, '_visitor', False):
            raise StepUnavailable('当前微博为游客模式，此功能需要登录')

    def await_page(self, ready, message, optional=False):
        def check():
            if self.activity_has('Login', 'NewRegist', 'SSOLogin'):
                self.back()
                raise StepUnavailable('微博要求登录：' + message)
            return ready()
        try:
            self.wait_for(check, message, timeout=12)
        except RuntimeError:
            if optional:
                raise StepUnavailable(message)
            raise

    def feed_tab(self, name):
        self.main_page()
        self.label(name)
        self.await_page(lambda: self.has(rid='contentTextView') or any(
            len(r['text']) > 12 and .2 < r['y'] < .85 for r in self.visual_rows()), name + '内容未加载')

    def following(self):
        self.require_account()
        self.feed_tab('关注')

    def first_live(self):
        self.require_account()
        height = self.d.window_size()[1]
        entries = [n for n in self.nodes() if '直播' in (n.get('content-desc', '') + n.get('text', ''))
                   and self.bounds(n)[1] < height*.45
                   and '发起' not in n.get('content-desc', '')]
        if not entries:
            node = self.find_label('热门直播')
            if node is None:
                raise StepUnavailable('关注页没有正在直播的博主')
            entries = [node]
        self.click_node(entries[0])
        self.await_page(lambda: self.activity_has('Live', 'live'), '直播未打开', optional=True)

    def return_following(self):
        self.main_page()
        self.following()

    def hold(self, node):
        l, t, r, b = self.bounds(node)
        self.foreground()
        x, y = round((l+r)/2), round((t+b)/2)
        result = self.d.shell('input -d 0 swipe {0} {1} {0} {1} 900'.format(x, y))
        if result.exit_code:
            raise RuntimeError('长按失败：' + result.output)
        time.sleep(1)

    def tab_menu(self, tab):
        self.main_page()
        self.hold(self.bottom_node(tab))
        other = '超话' if tab == '视频' else '视频'
        height = self.d.window_size()[1]
        if not any(other in (n.get('text'), n.get('content-desc'))
                   and self.bounds(n)[1] < height*.86 for n in self.nodes()):
            raise StepUnavailable('当前版本/游客底栏长按没有“{}”切换菜单'.format(other))

    def bottom_from_menu(self, label):
        height = self.d.window_size()[1]
        nodes = [n for n in self.nodes() if label in (n.get('text'), n.get('content-desc'))
                 and self.bounds(n)[1] < height*.86]
        if not nodes:
            raise StepUnavailable('未找到底栏切换菜单：' + label)
        self.click_node(nodes[0])
        self.await_page(lambda: bool(self.nodes(desc=label)), '底栏切换未生效', optional=True)

    def super_topic(self):
        self.bottom_from_menu('超话')
        self.bottom('超话')
        self.await_page(lambda: self.activity_has('Super', 'super') or self.has(text='超话'),
                        '超话页面未打开', optional=True)

    def first_super_topic(self):
        width, height = self.d.window_size()
        cards = [n for n in self.nodes() if '超话' in n.get('content-desc', '')
                 and n.get('clickable') == 'true'
                 and height*.2 < self.bounds(n)[1] < height*.8
                 and self.bounds(n)[2]-self.bounds(n)[0] > width*.3]
        if not cards:
            raise StepUnavailable('超话页没有可定位的超话卡片')
        self.click_node(cards[0])
        self.await_page(lambda: self.has(rid='contentTextView'), '超话内容未加载', optional=True)

    def return_super_topic(self):
        self.return_to(lambda: self.main_ready(), '未返回微博底栏')
        self.bottom('超话')

    def discover(self):
        self.main_page()
        self.bottom('发现')
        self.await_page(lambda: self.has(rid='tv_search_keyword'), '发现页面未加载')

    def hot_list(self):
        node = self.find_label('更多热搜')
        if node is not None:
            self.click_node(node)
        else:
            self.wait_for(lambda: any('更多热搜' in n.get('content-desc', '') for n in self.nodes()),
                          '未找到发现页热搜区域')
            node = next(n for n in self.nodes() if '更多热搜' in n.get('content-desc', ''))
            # weditor 显示整块热搜被合并：入口位于区域的右列、末行。
            l, t, r, b = self.bounds(node)
            self.point(l+(r-l)*.65, t+(b-t)*.92)
        self.await_page(lambda: self.activity_has('RankPageActivity'), '热搜榜未打开')

    def first_hot(self):
        self.require(rid='tv_coupon_des')
        cards = sorted(self.nodes(rid='tv_coupon_des'), key=lambda n: self.bounds(n)[1])
        self.click_node(cards[0])
        self.await_page(lambda: self.activity_has('SearchActivity'), '热搜词结果未打开')
        self.await_page(lambda: self.has(rid='contentTextView'), '热搜词没有博文结果')

    def first_post(self):
        self.click(rid='contentTextView')
        self.await_page(lambda: self.activity_has('DetailPageActivity'), '博文正文未打开')

    def detail_ready(self):
        return self.activity_has('DetailPageActivity') and self.has(rid='footerLayout')

    def detail_action(self, part):
        self.require_account()
        if not self.detail_ready():
            raise RuntimeError('当前不是博文正文页')
        footer = self.node(rid='footerLayout')
        l, t, r, b = self.bounds(footer)
        self.point(l+(r-l)*(part+.5)/3, (t+b)/2)

    def like_node(self, liked):
        height = self.d.window_size()[1]
        labels = ('取消赞', '已赞', '取消点赞') if liked else ('赞', '点赞')
        return next((n for n in self.nodes() if self.bounds(n)[1] > height*.87
                     and any(n.get(k, '').startswith(labels) for k in ('text', 'content-desc'))), None)

    def like(self):
        self.require_account()
        if self.like_node(True) is not None:
            raise StepUnavailable('当前博文原已点赞，保留原状态')
        node = self.like_node(False)
        if node is None:
            raise StepUnavailable('当前正文未暴露可核实状态的点赞控件')
        self.click_node(node)
        self.await_page(lambda: self.like_node(True) is not None, '点赞状态未确认')
        self._liked_by_case = True

    def unlike(self):
        if not getattr(self, '_liked_by_case', False):
            raise StepUnavailable('本次用例未产生点赞')
        node = self.like_node(True)
        if node is None:
            raise RuntimeError('无法确认本次点赞状态')
        self.click_node(node)
        self.await_page(lambda: self.like_node(False) is not None, '取消赞状态未确认')
        self._liked_by_case = False

    def editors(self):
        return [n for n in self.nodes() if n.get('class') == 'android.widget.EditText'
                and n.get('enabled') != 'false']

    def input_text(self, text):
        self.await_page(lambda: bool(self.editors()), '未找到可输入的文本框')
        editors = self.editors()
        node = next((n for n in editors if n.get('focused') == 'true'), editors[0])
        self.click_node(node)
        rid = node.get('resource-id')
        if rid:
            self.d(resourceId=rid).set_text(text)
        else:
            self.d.send_keys(text, clear=True)
        self.await_page(lambda: any(n.get('text') == text for n in self.editors()), '输入内容未确认')

    def comment_draft(self):
        self.detail_action(1)
        self.input_text('评论')
        self._draft = True

    def cancel_comment(self):
        self.discard_editor()
        self.await_page(self.detail_ready, '取消评论后未返回正文')

    def repost_draft(self):
        self.detail_action(0)
        self.await_page(lambda: bool(self.editors()), '转发编辑器未打开', optional=True)
        self._draft = True

    def cancel_repost(self):
        self.discard_editor()
        self.await_page(self.detail_ready, '取消转发后未返回正文')

    def discard_editor(self):
        # 只取消当前用例打开的编辑器，绝不点击发送/发布。
        for _ in range(4):
            node = self.find_label('取消', '不保存', '不保留', '放弃编辑')
            if node is not None:
                self.click_node(node)
            else:
                self.back()
            time.sleep(.5)
            if not self.editors():
                self._draft = False
                return
        raise RuntimeError('编辑器未关闭')

    def open_search(self):
        self.click(rid='tv_search_keyword')
        self.await_page(lambda: bool(self.editors()), '搜索输入页未打开')

    def submit_search(self):
        self.label('搜索')
        self.await_page(lambda: self.activity_has('SearchActivity'), '搜索结果未打开')

    def users_tab(self):
        # 横向结果栏有时需要左滑一次才显示“用户”。
        for _ in range(3):
            node = self.find_label('用户')
            if node is not None:
                self.click_node(node)
                time.sleep(1)
                return
            tabs = self.nodes(rid='search_item_text')
            if not tabs:
                break
            _, t, _, b = self.bounds(tabs[0])
            width = self.d.window_size()[0]
            height = self.d.window_size()[1]
            self.swipe(.85, (t+b)/2/height, .2, (t+b)/2/height)
        raise StepUnavailable('当前搜索结果没有用户页签')

    def test_user(self):
        nodes = [n for n in self.nodes(text='动态测试') if n.get('class') != 'android.widget.EditText'
                 and self.bounds(n)[1] > self.d.window_size()[1]*.2]
        if not nodes:
            raise StepUnavailable('没有名为“动态测试”的用户，跳过指定用户浏览')
        self.click_node(nodes[0])
        self.await_page(lambda: self.activity_has('Profile', 'UserInfo'), '用户主页未打开', optional=True)

    def user_first_post(self):
        for _ in range(4):
            if self.has(rid='contentTextView'):
                self.first_post()
                return
            self.swipe()
        raise StepUnavailable('指定用户没有可浏览的微博')

    def compose_menu(self):
        self.require_account()
        self.main_page()
        node = self.find_label('发布', '更多', '加号')
        if node is None:
            # 首页右上 +，已用 weditor 截图核对；按实时分辨率换算。
            self.pct(.932, .08)
        else:
            self.click_node(node)
        self.await_page(lambda: self.find_label('写微博') is not None, '写微博菜单不可用', optional=True)

    def write_post(self):
        self.label('写微博', optional=True)
        self.await_page(lambda: bool(self.editors()), '写微博编辑器未打开', optional=True)
        self._draft = True

    def open_photos(self):
        self.label('图片', '相册', '照片', optional=True)
        self.await_page(lambda: self.find_label('最近项目', '所有图片', '相册') is not None,
                        '相册未打开或未授权', optional=True)

    def select_nine_photos(self):
        chosen = set()
        for _ in range(5):
            choices = [n for n in self.nodes() if re.search(r'未选中.*(图片|照片)|(图片|照片).*未选中', n.get('content-desc', ''))]
            for n in choices:
                key = n.get('content-desc')
                if key in chosen:
                    continue
                self.click_node(n)
                chosen.add(key)
                if len(chosen) == 9:
                    self.await_page(lambda: self.find_label('下一步(9)', '下一步（9）', '完成(9)', '完成（9）') is not None,
                                    '选中9张图片的计数未确认', optional=True)
                    return
            self.swipe()
        raise StepUnavailable('相册不足9张可定位图片或当前版本未提供图片选择状态')

    def photos_next(self):
        self.label('下一步(9)', '下一步（9）', '完成(9)', '完成（9）', optional=True)
        time.sleep(1)

    def preview_next(self):
        node = self.find_label('下一步')
        if node is None:
            raise StepUnavailable('当前版本选图后直接返回编辑器，没有第二个下一步')
        self.click_node(node)
        self.await_page(lambda: bool(self.editors()), '图片处理后未回到编辑器', optional=True)
