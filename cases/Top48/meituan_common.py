"""美团 12.67.203 实机定位；步骤来源为用例表 1041～1093 行。"""
import json
import logging
import os
import time

from Cases.Top48.dynamic_apps_common import DynamicAppCase
from aw_new import SeaOfStarsAW


class MeituanStepSkipped(Exception):
    """当前版本缺少功能或服务明确不可用，保留原因而不伪装成功。"""


class MeituanDynamicCase(DynamicAppCase):
    PACKAGE = 'com.sankuai.meituan'
    all_app_package_list = [PACKAGE]

    def point(self, x, y):
        self.foreground()
        result = self.d.shell('input -d 0 swipe {0} {1} {0} {1} 180'.format(round(x), round(y)))
        if result.exit_code:
            raise RuntimeError('美团点击失败：' + result.output)

    def pick(self, *labels):
        for label in labels:
            for key in ('desc', 'text'):
                found = self.nodes(**{key: label})
                if found:
                    self.click_node(found[0])
                    return
        raise RuntimeError('未找到入口：' + '/'.join(labels))

    def main_ready(self):
        return self.has(rid='address_twoLine_name')

    def return_main(self):
        self.return_to(self.main_ready, '未返回美团首页', limit=10)
        self.wait_for(self.main_ready, '首页未就绪')
        # 返回首页保留之前滚动位置；频道节点即便被吸顶搜索栏遮挡仍标为可见。
        # 先恢复频道到搜索栏下方，否则其旧 bounds 会点击到搜索框。
        for _ in range(5):
            channels = self.nodes(desc='外卖')
            searches = self.nodes(rid='search_button')
            if channels and searches and self.bounds(channels[0])[1] >= self.bounds(searches[0])[3]:
                return
            self.swipe(y1=.4, y2=.82)
            time.sleep(.5)
        raise RuntimeError('首页频道仍被吸顶搜索栏遮挡')

    def launch(self):
        self._address_reason = None
        self.start()
        self.return_main()

    def delivery_ready(self):
        return self.has(rid='homepage_search_icon')

    def delivery(self):
        self.return_main()
        def open_delivery():
            # 导航重试前恢复首页，避免页面已切换时点击同名文字。
            if not self.main_ready():
                self.return_main()
            self.click(desc='外卖')
        self.transition(open_delivery, self.delivery_ready, '外卖首页未打开')

    def return_delivery(self):
        self.return_to(self.delivery_ready, '未返回外卖首页', limit=8)

    def food(self):
        self.return_main()
        # 当前版“美食”即餐厅团购频道，有“美食餐厅”商家列表。
        self.transition(lambda: self.pick('美食团购', '美食'),
                        lambda: self.has(text='美食餐厅'), '美食餐厅列表未打开')

    def leisure(self):
        self.return_main()
        self.transition(lambda: self.pick('休闲玩乐'),
                        lambda: self.has(text='台球馆'), '休闲玩乐未打开')

    def search_box(self):
        self.require(rid='homepage_search_icon')
        self.transition(lambda: self.click(rid='homepage_search_icon'),
                        lambda: bool(self.search_editors()), '外卖搜索页未打开')

    def search_editors(self):
        h = self.screen_size()[1]
        return [n for n in self.nodes() if n.get('class') == 'android.widget.EditText'
                and self.bounds(n)[1] < h*.2 and n.get('enabled') == 'true']

    def enter_query(self, query):
        self.wait_for(lambda: len(self.search_editors()) == 1, '搜索页未出现唯一输入框')
        self.d(className='android.widget.EditText', packageName=self.PACKAGE).set_text(query)
        self.wait_for(lambda: any(n.get('text') == query for n in self.search_editors()), '搜索词未输入')
        self._query = query

    def search(self):
        self.click(rid='search_button', text='搜索')
        self.wait_for(lambda: self.has(rid='omj', text=self._query)
                      or bool(self.delivery_titles()), '搜索结果未打开')
        self.wait_for(lambda: bool(self.delivery_titles()), '搜索商家未加载', timeout=25)

    def delivery_titles(self):
        # 两种外卖结果模板均无标题 id；商户标题字号较大，位于月售行上方。
        height = self.screen_size()[1]
        return sorted([n for n in self.nodes() if n.get('text')
                       and not n.get('resource-id') and not n.get('content-desc')
                       and self.bounds(n)[3] - self.bounds(n)[1] >= height * .021
                       and height * .16 < self.bounds(n)[1] < height * .85
                       and self.bounds(n)[0] > self.screen_size()[0] * .16
                       and ('店' in n.get('text', '') or '（' in n.get('text', '')
                            or '汤' in n.get('text', ''))], key=lambda n: self.bounds(n)[1])

    def dismiss_booking_tip(self):
        tips = [n for n in self.nodes() if n.get('text', '').startswith('点击预订，可选购')]
        if tips:
            # 截图核对：提示气泡右侧关闭叉无语义节点，按气泡边界比例换算。
            l, t, r, b = self.bounds(tips[0])
            self.point(r - (r-l)*.09, (t+b)/2)

    def shop(self):
        self.wait_for(lambda: bool(self.delivery_titles()), '无可进入的搜索商家')
        self.click_node(self.delivery_titles()[0])
        time.sleep(2)
        self.dismiss_booking_tip()
        self.wait_for(lambda: self.has(text='点菜') or self.has(rid='tv_shop_name'),
                      '商家详情未打开', timeout=20)

    def local_shop(self):
        width, height = self.screen_size()
        def cards():
            return sorted([n for n in self.nodes() if ', 分' in n.get('content-desc', '')
                           and self.bounds(n)[2]-self.bounds(n)[0] > width*.8
                           and height*.3 < self.bounds(n)[1] < height*.85],
                          key=lambda n: self.bounds(n)[1])
        self.wait_for(lambda: bool(cards()), '餐厅或休闲商家列表未加载')
        card = cards()[0]
        l,t,r,b = self.bounds(card)
        # 卡片内上部为商户标题；下部团购子项会跳到商品详情。
        self.point((l+r)/2, t+(b-t)*.18)
        self.wait_for(lambda: self.has(text='团购') and self.has(text='评价'), '本地商家未打开')

    def comments(self):
        self.pick('评价')
        self.wait_for(lambda: any('已选中' in n.get('content-desc', '')
                                 for n in self.nodes(desc='评价', prefix=True)), '评价未选中')
        self.browse(2, 2, 1)

    def menu(self):
        self.pick('点菜')
        self.wait_for(lambda: self.has(desc='点菜 已选中'), '未返回点菜页')

    def first_food(self):
        self.require(text='点菜')
        for _ in range(4):
            adds = self.nodes(desc='增加，已添加', prefix=True)
            if adds:
                break
            self.swipe(x1=.72, x2=.72)
        if not adds:
            raise MeituanStepSkipped('商家暂无可加购食品')
        add = sorted(adds, key=lambda n:self.bounds(n)[1])[0]
        # 同一行的商品标题，以加号的父卡片内 text 定位，排除左侧分类。
        y = self.bounds(add)[1]
        titles = [n for n in self.nodes() if n.get('text') and not n.get('content-desc')
                  and self.bounds(n)[0] > self.screen_size()[0]*.45
                  and y-self.screen_size()[1]*.15 < self.bounds(n)[1] < y
                  and self.bounds(n)[3]-self.bounds(n)[1] > self.screen_size()[1]*.02]
        if not titles:
            raise RuntimeError('食品加号存在但未定位到同卡片商品标题')
        self.click_node(sorted(titles,key=lambda n:self.bounds(n)[1])[0])
        self.wait_for(lambda:self.has(text='加入购物车'), '食品详情未打开')

    def cart_nodes(self):
        return self.nodes(desc='购物车，已添加', prefix=True)

    def add_food(self):
        if not self.has(text='加入购物车'):
            raise MeituanStepSkipped('无可加购的食品详情')
        self.click(text='加入购物车')
        self.wait_for(lambda: bool(self.cart_nodes()), '加购后购物车未更新')

    def add_again(self):
        if not self.cart_nodes():
            raise MeituanStepSkipped('上一食品未加入购物车')
        # 商品详情加购后只显示无描述图标；购物车面板的“增加”有语义节点。
        self.click_node(self.cart_nodes()[0])
        self.wait_for(lambda:self.has(text='已加购商品'), '购物车未打开')
        self.click(desc='增加')
        self.wait_for(lambda:self.has(desc='已添加2份'), '第二次加购未生效')

    def clear_cart(self):
        if not self.has(text='清空'):
            if self.cart_nodes():
                self.click_node(self.cart_nodes()[0])
            elif self.has(text='购物车'):
                self.click(text='购物车')
            else:
                raise MeituanStepSkipped('购物车没有已加购商品')
        if not self.has(text='清空'):
            raise MeituanStepSkipped('购物车为空，无需清空')
        self.click(text='清空')
        time.sleep(.5)
        if self.has(text='确认清空'):
            self.click(text='确认清空')
        self.wait_for(lambda:not self.cart_nodes() and not self.has(text='已加购商品'), '购物车未清空')

    def group_product(self):
        # 回到团购锚点后取首个商品标题，避免写死商家和商品名称。
        self.pick('团购')
        for _ in range(5):
            nodes = self.nodes()
            titles = [n for n in nodes if len(n.get('text','')) >= 8
                      and not n.get('content-desc') and not n.get('resource-id')
                      and self.bounds(n)[0] > self.screen_size()[0]*.2
                      and self.screen_size()[1]*.55 < self.bounds(n)[1] < self.screen_size()[1]*.9
                      and not any(k in n.get('text','') for k in ('地址','公里','分钟','营业'))]
            if titles:
                self.click_node(sorted(titles,key=lambda n:self.bounds(n)[1])[0])
                self.wait_for(lambda:self.has(text='去下单') or self.has(text='立即抢购')
                              or self.has(text='购买须知') or self.has(text='套餐详情'), '团购商品详情未打开')
                return
            self.swipe()
        raise MeituanStepSkipped('商家没有可展示的团购商品')

    def mine(self):
        self.return_delivery()
        self.click(rid='more', text='我的')
        self.wait_for(lambda:self.has(desc='设置'), '外卖我的页面未打开')

    def addresses(self):
        for _ in range(3):
            for label in ('我的地址','收货地址'):
                if self.has(text=label):
                    self.click(text=label)
                    self.wait_for(lambda:self.has(text='新增收货地址'), '地址列表未打开')
                    return
            time.sleep(1)
        self._address_reason = '当前外卖“我的”页仅显示账号和设置，无我的地址入口（已核对截图）'
        raise MeituanStepSkipped(self._address_reason)

    def first_address(self):
        # 当前设备该入口缺失；其他版本不猜测地址行/编辑图标，避免误改地址。
        raise MeituanStepSkipped(self._address_reason or '未核验本版本地址编辑控件，跳过编辑')

    def save_address(self):
        raise MeituanStepSkipped(self._address_reason or '本次未编辑地址，跳过保存')

    def new_address(self):
        if self._address_reason:
            raise MeituanStepSkipped(self._address_reason)
        self.pick('新增收货地址')
        self.wait_for(lambda:self.has(text='收货人') or self.has(text='联系人'), '新增地址表单未打开')

    def steps(self):
        raise NotImplementedError

    @SeaOfStarsAW.function_log
    def run_case(self):
        if not getattr(self, '_prepared', False):
            self.set_up()
        records = []
        for run in range(self.TEST_TIME):
            for index, (name, action, stay) in enumerate(self.steps(), 1):
                record = dict(run=run+1, step=index, name=name, status='PASS')
                logging.info('%s、%s', index, name)
                SeaOfStarsAW.start_perfetto_trace()
                try:
                    action()
                    time.sleep(stay)
                except MeituanStepSkipped as error:
                    record.update(status='SKIP', reason=str(error))
                    logging.warning('SKIP %s：%s', name, error)
                except Exception as error:
                    record.update(status='FAIL', reason=str(error))
                    logging.exception('步骤失败：%s', name)
                    raise
                finally:
                    records.append(record)
                    with open(os.path.join(self.result_dir_path, 'step_results.json'), 'w', encoding='utf-8') as f:
                        json.dump(records, f, ensure_ascii=False, indent=2)
                    try:
                        SeaOfStarsAW.stop_and_get_perfetto_trace(
                            self.trace_dir_path, self.__class__.__name__,
                            'step_{}、{}_{}'.format(index, name, record['status']), '', self.screenshot_dir_path)
                    except Exception:
                        if record['status'] != 'FAIL':
                            raise
                        logging.exception('失败步骤 trace 导出失败')
