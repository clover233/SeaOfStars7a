"""微信 0140—0200：小程序只读浏览、测试照片发送、收藏与存储查看。"""
import re
import time

from Cases.Top48.weixin_common import WeixinStepSkipped, optional
from Cases.Top48.weixin_extended import WeixinExtendedCase


class WeixinRemainingCase(WeixinExtendedCase):
    @optional('mini-list')
    def recent_programs(self):
        self.wechat_home()
        for _ in range(2):
            self.swipe(.5, .18, .5, .85, 600)
            time.sleep(.8)
            if self.visible('最近使用', True):
                return
        self.discover()
        self.choose('小程序', region=(0, .12, 1, .9))
        self.content_wait(lambda: self.visible('最近使用', True), '小程序最近使用列表未加载')
        self.adapt('首页下拉未显示最近小程序，改从发现→小程序进入最近使用列表')

    def program_ready(self):
        return self.activity_is('AppBrandUI') and not self.activity_is('AppBrandPluginUI')

    def open_program(self, names):
        self.needs('mini-list')
        # 先查最近使用和我的常用；若缺失，再展开完整最近列表。
        for attempt in range(5):
            for name in names:
                rows = self.find(name, True, (0, .18, 1, .9))
                if rows:
                    row = rows[0]
                    self._locators.add(row['source'])
                    def open_row():
                        self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
                    self.transition(open_row, self.program_ready, '小程序未打开：' + names[0])
                    self._program = names[0]
                    return
            if attempt == 0 and self.visible('最近使用', True):
                self.choose('最近使用', True, index=0)
            else:
                self.swipe()
            time.sleep(.8)
        raise WeixinStepSkipped('最近小程序中没有“{}”，不选用其他商户替代'.format('/'.join(names)))

    def program_content(self, key, labels):
        self.needs(key)
        self.content_wait(lambda: self.program_ready() and any(self.visible(s, True) for s in labels),
                          '小程序内容未加载：' + '/'.join(labels), timeout=35)
        if any(self.visible(s, True) for s in ('同意并', '授权登录', '允许获取', '获取你的', '隐私保护指引')):
            raise WeixinStepSkipped('当前小程序要求登录、授权或协议确认，停在提示页')

    @optional('heytea')
    def heytea(self):
        self.open_program(('喜茶GO', '喜茶'))
        self.program_content('heytea', ('到店取', '门店自取', '到店自取'))

    @optional('heytea-menu')
    def heytea_menu(self):
        self.needs('heytea')
        for label in ('到店取', '门店自取', '到店自取'):
            if self.visible(label, True):
                self.choose(label, True, index=0)
                if label != '到店取':
                    self.adapt('当前入口“{}”替代表中“到店取”'.format(label))
                break
        else:
            raise WeixinStepSkipped('喜茶没有到店取入口')
        self.program_content('heytea', ('时令上新', '推荐榜', '商品', '热销', '人气', '菜单', '当前门店已休息'))
        if self.visible('当前门店已休息'):
            self.adapt('当前门店已休息，继续只读浏览菜单，不修改门店或下单')

    @optional('heytea-menu')
    def browse_heytea(self):
        self.needs('heytea', 'heytea-menu')
        self.program_content('heytea', ('门店', '商品', '菜单', '人气'))
        # 向下浏览内容用上滑手势，再反向回到起始区域。
        self.browse(3, 3)
        self.adapt('按三次反向滑动回到起始区域；自绘列表不导出滚动位置，不能断言已到顶部')

    @optional('meituan')
    def meituan(self):
        self.open_program(('美团',))
        self.program_content('meituan', ('外卖', '美食', '酒店', '美团'))

    @optional('meituan')
    def browse_meituan(self):
        self.program_content('meituan', ('外卖', '美食', '酒店', '美团'))
        self.browse(3, 3)

    @optional('mixue')
    def mixue(self):
        self.open_program(('蜜雪冰城',))
        self.program_content('mixue', ('点餐', '点单', '门店自取', '到店自取', '更快更优惠'))

    @optional('mixue-menu')
    def mixue_menu(self):
        self.needs('mixue')
        self.dismiss_mixue_ad()
        for label in ('点餐', '点单', '门店自取', '到店自取', '更快更优惠'):
            if self.visible(label, True):
                self.choose(label, True, index=0)
                if label != '点餐':
                    self.adapt('当前“{}”替代旧版“点餐”入口'.format(label))
                break
        else:
            raise WeixinStepSkipped('蜜雪冰城没有点餐入口')
        self.program_content('mixue', ('菜单', '商品', '选择门店', '附近门店', '热销', '冰淇淋'))

    def dismiss_mixue_ad(self):
        if self.visible('邀请好友', True) and self.visible('立即邀请', True):
            buttons = self.nodes(desc='关闭')
            if len(buttons) == 1:
                self.click_node(buttons[0])
            else:
                # 已核对“邀请好友得85折券”弹窗，下方圆形 X，不点击邀请按钮。
                self.pct(.5, .742)
            self.content_wait(lambda: not self.visible('得85折券', True)
                              and self.visible('更快更优惠'), '蜜雪广告弹窗未关闭')

    @optional('mixue-menu')
    def browse_mixue(self):
        self.needs('mixue', 'mixue-menu')
        self.dismiss_mixue_ad()
        self.program_content('mixue', ('菜单', '商品', '门店', '冰淇淋'))
        self.browse(3, 3)

    @optional('jd')
    def jd(self):
        self.open_program(('京东购物', '京东'))
        self.program_content('jd', ('京东', '百亿补贴', '购物车', '秒杀'))

    @optional('jd')
    def browse_jd(self):
        self.program_content('jd', ('京东', '购物车', '秒杀'))
        self.browse(3, 3)

    @optional('tongcheng')
    def tongcheng(self):
        self.open_program(('同程旅行',))
        self.program_content('tongcheng', ('火车票', '火车', '机票', '酒店'))

    @optional('train')
    def train(self):
        self.needs('tongcheng')
        if self.visible('火车票查询') and self.departure_date_rows():
            self.adapt('当前同程首页已内置火车票表单，直接浏览该栏目，替代旧版独立火车票页')
        elif self.visible('火车票'):
            self.choose('火车票', index=0)
        elif self.visible('火车'):
            self.choose('火车', index=0)
        else:
            raise WeixinStepSkipped('同程没有火车票表单或入口')
        self.program_content('tongcheng', ('查询', '出发', '到达'))

    def departure_date_rows(self):
        return [r for r in self.screen() if .2 < r['y'] < .85 and r['x'] < .6
                and re.search(r'\d{1,2}月\d{1,2}日', r['text'])]

    @optional('train')
    def browse_train(self):
        self.needs('train')
        self.program_content('tongcheng', ('查询', '出发', '到达'))
        self.browse(3, 3)

    @optional('train-date')
    def train_date(self):
        self.needs('tongcheng', 'train')
        if self.visible('更多日期', True):
            self.choose('更多日期', True)
        else:
            rows = self.departure_date_rows()
            if len(rows) != 1:
                raise WeixinStepSkipped('没有更多日期入口，也未识别到唯一出发日期行')
            row = rows[0]
            self._locators.add(row['source'])
            self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
            self.adapt('点击当前出发日期行，替代旧版右上角“更多日期”')
        self.content_wait(lambda: self.visible('选择日期', True) or self.visible('出发日期', True)
                          or self.visible('日历'), '火车票日期页未打开')

    @optional('train')
    def return_train(self):
        self.needs('tongcheng', 'train')
        self.return_to(lambda: self.visible('查询', True) and self.program_ready(), '未返回火车票页')

    @optional('tongcheng')
    def return_tongcheng(self):
        self.needs('tongcheng')
        self.return_to(lambda: self.visible('酒店') and self.visible('机票'), '未返回同程首页')

    @optional('chat-album')
    def chat_album(self):
        self.require_test_chat()
        self._album_origin_verified = False
        label = '照片' if self.visible('照片') else '相册'
        self.choose(label)
        self.await_text('预览', True, region=(0, .85, .4, 1))
        self.pct(.5, .083)
        self.await_text(self.ALBUM, True)
        self.choose(self.ALBUM, True)
        self.await_text(self.ALBUM, region=(.1, .05, .9, .12))
        self._album_origin_verified = True
        self._album_selected = 0
        self.adapt('仅浏览专用“{}”生成图片；不选个人照片'.format(self.ALBUM))

    def require_fixture_album(self):
        self.needs('test-chat', 'chat-album')
        if (not getattr(self, '_album_origin_verified', False)
                or getattr(self, '_verified_chat', None) != self.TEST_CONTACT
                or not self.visible(self.ALBUM, region=(.1, .05, .9, .12))):
            raise WeixinStepSkipped('未核对授权会话来源和专用测试相册')

    @optional('chat-album')
    def browse_chat_album(self):
        self.require_fixture_album()
        self.browse(3, 3)

    def fixture_grid_top(self):
        width, height = self.d.window_size()
        header = self.find(self.ALBUM, region=(.1, .05, .9, .12))[0]
        return (header['y']+header['h'])*height + width*.035

    @optional('chat-album-selection')
    def select_chat_photos(self):
        self.require_fixture_album()
        width, height = self.d.window_size()
        top = self.fixture_grid_top()
        for col in range(3):
            self.pct((col+.87)/4, (top+width*.03)/height)
        self.await_text('发送3', True, region=(.65, .85, 1, 1))
        self._album_selected = 3
        self.adapt('“多张图片”具体选取三张生成的测试图片')

    @optional('chat-album-selection')
    def send_chat_photos(self):
        self.needs('chat-album', 'chat-album-selection')
        self.require_fixture_album()
        if not self.ALLOW_SEND or self._album_selected != 3 or getattr(self, '_chat', None) != self.TEST_CONTACT:
            raise RuntimeError('测试相册发送前接收人或选图数量校验失败')
        self.require_delivery()
        self.choose('发送3', True, region=(.65, .85, 1, 1))
        # 实发按钮只点一次，页面未返回时停止，不重复发送。
        self.wait_for(lambda: self.chat_ready(self.TEST_CONTACT), '发送照片后未返回授权会话')
        self._album_origin_verified = False
        self._album_selected = 0
        self.require_delivery()

    @optional('chat-album')
    def first_chat_photo(self):
        self.require_fixture_album()
        width, height = self.d.window_size()
        self.pct(.125, (self.fixture_grid_top()+width*.125)/height)
        time.sleep(.7)
        if not self.activity_is('ImagePreviewUI') and self.visible('预览1', True, (0, .85, .4, 1)):
            self.choose('预览1', True, (0, .85, .4, 1))
            self._album_selected = 1
            self.adapt('当前相册点击缩略图先选中，通过“预览(1)”查看第一张大图，不发送该图')
        self.wait_for(lambda: self.activity_is('ImagePreviewUI') and self.visible('发送', True), '未进入照片大图')

    @optional('favorites')
    def favorites_page(self):
        self.favorites()

    @optional('favorites')
    def browse_favorites(self):
        self.needs('favorites')
        self.await_text('收藏', region=(.2, .05, .8, .12))
        self.browse(3, 3)

    @optional('favorite-detail')
    def first_favorite(self):
        self.needs('favorites')
        self.await_text('收藏', region=(.2, .05, .8, .12))
        if self.visible('暂无收藏', True) or self.visible('没有收藏', True):
            raise WeixinStepSkipped('当前收藏为空，没有第一条内容')
        rows = [r for r in self.screen() if .18 < r['y'] < .8 and len(r['text']) >= 3
                and not any(s in r['text'] for s in ('搜索', '图片与视频', '链接', '文件', '音乐', '聊天记录', '标签'))]
        if not rows:
            raise WeixinStepSkipped('收藏列表没有可识别的内容标题')
        row = rows[0]
        self._locators.add(row['source'])
        self.pct(row['x']+row['w']/2, row['y']+row['h']/2, record=False)
        self.wait_for(lambda: not self.activity_is('FavIndexUI'), '第一条收藏未打开')

    @optional('settings')
    def settings(self):
        self.me()
        self.choose('设置', True, region=(0, .15, .8, .9))
        self.await_text('通用')

    @optional('general')
    def general(self):
        self.needs('settings')
        self.choose('通用')
        self.await_text('存储空间')

    @optional('storage')
    def storage(self):
        self.needs('settings', 'general')
        self.choose('存储空间')
        self.content_wait(lambda: self.visible('存储空间', True) and (
            self.visible('缓存', True) or self.visible('聊天记录', True)), '存储空间统计未加载', timeout=45)
        # 只展示统计，不点击清理、管理或删除。
