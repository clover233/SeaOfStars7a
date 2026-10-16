"""微博实机定位：weditor 0.7.3 Dump Hierarchy / Android 17，2026-10-16。"""
import time

from Cases.Top48.shopping_common import StepUnavailable, VisualShoppingDynamicCase
from Cases.Top48.weixin_common import WeixinDynamicCase


class WeiboDynamicCase(VisualShoppingDynamicCase):
    PACKAGE = 'com.sina.weibo'
    all_app_package_list = [PACKAGE]
    ALBUM = '微博性能素材'

    def set_up(self):
        super().set_up()
        if getattr(self, 'NEED_IMAGES', False):
            WeixinDynamicCase.prepare_images(self)

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
            if self.find_label('默认分组', '全部关注', '拖动排序') is not None:
                self.back()
                continue
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
        height = self.screen_size()[1]
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
            try:
                activity = self.current_app()['activity']
            except RuntimeError as error:
                if str(error) == '无法识别系统前台应用':
                    return False
                raise
            if any(name in activity for name in ('Login', 'NewRegist', 'SSOLogin')):
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
        # 已选中的“关注”再次点击会展开分组；先核对下划线状态，避免
        # 将分组弹层当作关注信息流，再把后续浏览变成分组拖动。
        if not self.feed_selected(name):
            node = self.find_label(name)
            if node is not None:
                self.click_node(node)
            else:
                self.pct(.413 if name == '推荐' else .565, .08)
            self.await_page(lambda: self.feed_selected(name), '未切换到' + name)
        if name == '关注':
            for _ in range(3):
                if self.find_label('默认分组', '全部关注', '拖动排序') is None:
                    break
                self.back()
        self.await_page(lambda: self.has(rid='contentTextView') or any(
            len(r['text']) > 12 and .2 < r['y'] < .85 for r in self.visual_rows()), name + '内容未加载')

    def feed_selected(self, name):
        # 两个标题的 selected 属性均为 false；用截图中黄色下划线核对。
        shot = self.d.screenshot(display_id=0).convert('RGB')
        width, height = shot.size
        left, right = (.36, .47) if name == '推荐' else (.51, .62)
        pixels = list(shot.crop((round(width*left), round(height*.089),
                                round(width*right), round(height*.104))).getdata())
        return sum(r > 200 and 130 < g < 230 and b < 110 for r, g, b in pixels) > len(pixels)*.01

    def following(self):
        self.require_account()
        self.feed_tab('关注')

    def first_live(self):
        self.require_account()
        height = self.screen_size()[1]
        entries = [n for n in self.nodes() if '直播' in (n.get('content-desc', '') + n.get('text', ''))
                   and self.bounds(n)[1] < height*.45
                   and '发起' not in n.get('content-desc', '')]
        if not entries:
            node = self.find_label('热门直播')
            if node is None:
                raise StepUnavailable('关注页没有正在直播的博主')
            entries = [node]
        # 直播标签在圆形封面下沿；点击同列封面中心，按标签边界换算。
        l, t, r, _ = self.bounds(entries[0])
        self.point((l+r)/2, t-height*.025)
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
        height = self.screen_size()[1]
        if not any(other in (n.get('text'), n.get('content-desc'))
                   and self.bounds(n)[1] < height*.86 for n in self.nodes()):
            raise StepUnavailable('当前版本底栏长按没有“{}”切换菜单'.format(other))

    def bottom_from_menu(self, label):
        height = self.screen_size()[1]
        nodes = [n for n in self.nodes() if label in (n.get('text'), n.get('content-desc'))
                 and self.bounds(n)[1] < height*.86]
        if not nodes:
            raise StepUnavailable('未找到底栏切换菜单：' + label)
        self.click_node(nodes[0])
        self.await_page(lambda: bool(self.nodes(desc=label)), '底栏切换未生效', optional=True)

    def super_topic(self):
        self.main_page()
        node = self.find_label('超话')
        if node is not None:
            self.click_node(node)
        else:
            # 当前版首页左上“超话”图片无文字节点，截图已核对。
            self.pct(.075, .08)
        self.await_page(lambda: self.activity_has('Super', 'super') or self.find_label('超话社区') is not None,
                        '超话页面未打开', optional=True)

    def first_super_topic(self):
        rows = [r for r in self.visual_rows() if r['text'].endswith('超话')
                and len(r['text']) > 3 and .25 < r['y'] < .8]
        if not rows:
            raise StepUnavailable('超话页没有可定位的超话名称')
        before = self.current_app()['activity']
        self.tap_visual(rows[0])
        self.await_page(lambda: self.current_app()['activity'] != before,
                        '超话详情未打开', optional=True)

    def return_super_topic(self):
        self.return_to(lambda: self.find_label('超话社区') is not None, '未返回超话社区', limit=6)

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
        icons = self.footer_icons(footer)
        if len(icons) != 3:
            raise StepUnavailable('正文底栏没有三枚可核对的互动图标')
        self.click_node(icons[part])

    def footer_icons(self, footer):
        width, height = self.screen_size()
        icons = [n for n in footer.iter('node') if n.get('class') == 'android.widget.ImageView'
                 and self.bounds(n)[2]-self.bounds(n)[0] < width*.2
                 and self.bounds(n)[3]-self.bounds(n)[1] > height*.015]
        # 新版在转发、评论、赞之前增加了智搜图标，取右侧三枚互动图标。
        return sorted(icons, key=lambda n: self.bounds(n)[0])[-3:]

    def like_node(self, liked):
        height = self.screen_size()[1]
        labels = ('取消赞', '已赞', '取消点赞') if liked else ('赞', '点赞')
        node = next((n for n in self.nodes() if self.bounds(n)[1] > height*.87
                     and any(n.get(k, '').startswith(labels) for k in ('text', 'content-desc'))), None)
        if node is not None:
            return node
        footers = self.nodes(rid='footerLayout')
        icons = self.footer_icons(footers[0]) if footers else []
        if len(icons) != 3:
            return None
        node = icons[-1]
        # 当前版点赞只导出图标和计数，没有状态描述；截图中未赞为深灰轮廓，
        # 已赞为橙色。仅分析由控件树定位的图标区域，无法核实颜色时跳过。
        pixels = list(self.d.screenshot(display_id=0).convert('RGB').crop(self.bounds(node)).getdata())
        orange = sum(r > 180 and 65 < g < 195 and b < 110 and r-g > 35 for r, g, b in pixels)
        dark = sum(max(r, g, b) < 125 for r, g, b in pixels)
        state = None
        if orange > len(pixels)*.015:
            state = True
        elif len(pixels)*.015 < dark < len(pixels)*.65 and orange == 0:
            state = False
        return node if state is liked else None

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
        def open_box():
            rows = self.nodes(rid='tv_search_keyword')
            if rows:
                self.click_node(rows[0])
            else:
                # 发现页顶部搜索框，原生根偶尔只导出底栏时按截图比例兜底。
                self.pct(.45, .08)
        self.transition(open_box, lambda: bool(self.editors()), '搜索输入页未打开')

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
            width = self.screen_size()[0]
            height = self.screen_size()[1]
            self.swipe(.85, (t+b)/2/height, .2, (t+b)/2/height)
        raise StepUnavailable('当前搜索结果没有用户页签')

    def test_user(self):
        raise StepUnavailable('按用户要求跳过“点击动态测试用户”；依赖的用户微博浏览一并跳过')

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
        self.click(rid='ib_insert_pics')
        self.await_page(lambda: self.activity_has('MediaEditingActivity') or self.find_label('最近项目', '所有图片', '相册', '所有照片') is not None,
                        '相册未打开或未授权', optional=True)

    def select_nine_photos(self):
        if not self.has(rid='bucketTriggerText', text=self.ALBUM):
            self.click(rid='bucketTriggerText')
            self.label(self.ALBUM, optional=True)
        self.await_page(lambda: self.has(rid='bucketTriggerText', text=self.ALBUM),
                        '专用测试相册未打开', optional=True)
        choices = self.nodes(rid='checkView')
        if len(choices) != 9:
            raise StepUnavailable('专用测试相册没有完整暴露9张图片')
        for index in range(9):
            # 每次重新读取状态，不反选已勾选的图片，不使用固定网格坐标。
            choice = self.nodes(rid='checkView')[index]
            if choice.get('content-desc') == '选择':
                self.click_node(choice)
                self.await_page(lambda: len(self.nodes(rid='checkView', desc='取消选择')) >= index+1,
                                '图片选择状态未确认')
        self.await_page(lambda: self.has(rid='next_step_button', text='下一步(9)'),
                        '选中9张图片的计数未确认')

    def photos_next(self):
        self.click(rid='next_step_button', text='下一步(9)')
        self.await_page(lambda: self.has(rid='nextText'), '选图后未进入预览页')

    def preview_next(self):
        if not self.has(rid='nextText'):
            raise StepUnavailable('当前版本选图后直接返回编辑器，没有第二个下一步')
        self.click(rid='nextText')
        self.await_page(lambda: bool(self.editors()), '图片处理后未回到编辑器', optional=True)
