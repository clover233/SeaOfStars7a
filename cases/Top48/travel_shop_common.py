"""去哪儿、汽水音乐、淘宝：主屏控件/截图定位和逐步采集。"""
import os
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from Cases.Top48.tencent_media_common import TencentObservedCase
from Cases.Top48.observed_apps_common import StepUnavailable, optional


class TravelShopCase(TencentObservedCase):
    TAP_MS = 250
    INPUT_SOURCE = ''

    def launch(self):
        self.unavailable={}
        self._recording=self._call_active=self._live_started=self._owned_draft=False
        for attempt in range(2):
            result=self.d.shell(['am','start','-W','--display','0','-n',self.COMPONENT])
            if result.exit_code:raise RuntimeError('应用启动失败：'+result.output)
            time.sleep(2);self.invalidate()
            self.dismiss_system_prompt()
            if self.current_app()['package']==self.PACKAGE:break
        self.wait_for(lambda:self.current_app()['package']==self.PACKAGE,'应用未进入前台')
        self.dismiss_ads();self.main_page()

    def return_to(self, ready, message, limit=6):
        for _ in range(limit):
            self.dismiss_ads()
            if ready():return
            self.back()
        self.wait_for(ready,message,timeout=3)

    def ad_matches(self, rows, label, contains=False):
        query=self.normalized(label)
        return [r for r in rows if (query in self.normalized(r['text']) if contains
                                    else query==self.normalized(r['text']))]

    def tap_row(self,row):
        self._locators.add(row['source'])
        self.pct(row['x']+row['w']/2,row['y']+row['h']/2,record=False)

    def dismiss_ads(self):
        self.dismiss_system_prompt()
        for _ in range(3):
            rows=self.screen()
            for label in ('跳过广告','跳过','关闭广告','以后再说','暂不升级','暂不更新','下次再说'):
                matches=self.ad_matches(rows,label,True)
                if len(matches)==1:
                    self.tap_row(matches[0]);time.sleep(.5);break
            else:return rows
        return self.screen()

    def nodes(self, rid=None, **kwargs):
        rows=super().nodes(**kwargs)
        if rid:
            rows=[n for n in rows if n.get('resource-id')==rid or (':id/' not in rid
                    and n.get('resource-id','').split(':id/')[-1]==rid)]
        return rows

    def dismiss_system_prompt(self):
        # 本机权限窗出现时 mCurrentFocus 偶尔仍指向底下应用，以实际控件树为准。
        system=('com.miui.securitycenter','com.android.permissioncontroller','com.google.android.permissioncontroller')
        nodes=list(ET.fromstring(self.d.dump_hierarchy()).iter('node'))
        for n in nodes:
            if n.get('package') in system and n.get('text') in ('拒绝','不允许','不同意','取消'):
                box=self.bounds(n)
                if len(box)!=4:continue
                a,b,z,y=box
                self._locators.add('tree')
                self.d.shell('input -d 0 tap {} {}'.format(round((a+z)/2),round((b+y)/2)))
                time.sleep(.5);self.invalidate()
                if any(x.get('package') in system and x.get('text') in ('拒绝','不允许','不同意','取消')
                       for x in ET.fromstring(self.d.dump_hierarchy()).iter('node')):
                    self.d.press('back');time.sleep(.5);self.invalidate()
                return
        super().dismiss_system_prompt()

    def input_text(self, text):
        edits=self.input_nodes()
        if not edits:
            raise StepUnavailable('输入框尚未显示，未向其他控件输入文字')
        if not any(n.get('focused')=='true' for n in edits):
            self.click_node(edits[0])
        self.content_wait(lambda:any(n.get('focused')=='true' for n in self.input_nodes()),'输入框未获得焦点',timeout=8)
        time.sleep(.4)
        self.foreground()
        super().input_text(text)

    def input_nodes(self):
        return [n for n in self.nodes() if n.get('class') in ('android.widget.EditText',
                'android.widget.AutoCompleteTextView','android.widget.MultiAutoCompleteTextView')]

    def point(self, x, y):
        self.foreground()
        source=getattr(self,'_tap_source',self.INPUT_SOURCE)
        duration=200 if source=='mouse' else self.TAP_MS
        r = self.d.shell('input {3} -d 0 swipe {0} {1} {0} {1} {2}'.format(round(x), round(y), duration, source))
        if r.exit_code:
            raise RuntimeError('主屏点击失败：'+r.output)
        self.invalidate()

    def swipe(self, x1=.5, y1=.78, x2=.5, y2=.32, duration=400):
        self.foreground()
        w, h = self.d.window_size()
        r = self.d.shell('input -d 0 swipe {} {} {} {} {}'.format(
            round(w*x1), round(h*y1), round(w*x2), round(h*y2), duration))
        if r.exit_code:
            raise RuntimeError('主屏滑动失败：'+r.output)
        self.invalidate()

    def entry(self, *labels, region=None):
        self.dismiss_ads()
        for label in labels:
            if self.visible(label, region=region):
                self.choose(label, region=region)
                return
        raise StepUnavailable('当前页面没有可核对的入口：'+'/'.join(labels))

    def go(self, action, ready, message):
        # 仅供可重复的页面导航；发送、加购等动作不使用此重试入口。
        self.dismiss_ads()
        original=getattr(self,'_tap_source',self.INPUT_SOURCE)
        try:
            for source in (original,'mouse' if original!='mouse' else ''):
                if ready():return
                self._tap_source=source
                action()
                try:
                    self.content_wait(ready,message,timeout=6)
                    return
                except StepUnavailable:
                    pass
        finally:self._tap_source=original
        raise StepUnavailable(message+'；两次导航均未确认目标页面')

    def horizontal(self, left, right, y=.5):
        for count, a, b in ((left,.8,.2),(right,.2,.8)):
            for _ in range(count):
                self.dismiss_ads()
                self.swipe(a,y,b,y)
                time.sleep(2)

    def first_row(self, pattern, region=(0,.2,1,.85)):
        rows = [r for r in self.screen() if re.search(pattern,r['text'])
                and region[0] < r['x']+r['w']/2 < region[2]
                and region[1] < r['y']+r['h']/2 < region[3]]
        if not rows:
            raise StepUnavailable('没有可核对的首条结果，未点击广告或旧位置')
        r=rows[0]; self._locators.add(r['source'])
        self.pct(r['x']+r['w']/2,r['y']+r['h']/2,record=False)


class QunarDynamicCase(TravelShopCase):
    PACKAGE = 'com.Qunar'
    all_app_package_list = [PACKAGE]
    COMPONENT = PACKAGE + '/com.mqunar.splash.SplashActivity'

    def dismiss_ads(self):
        rows=super().dismiss_ads()
        matches=self.ad_matches(rows,'放弃权益')
        if len(matches)==1:
            self.tap_row(matches[0])
            time.sleep(.6);self.invalidate()
            return
        if self.has(text='刮刮卡弹窗', prefix=True) or (self.ad_matches(rows,'获得一张新喜国庆刮刮卡',True)
                and self.ad_matches(rows,'双节限时加赠',True)) or self.ad_matches(rows,'刮奖区',True):
            self.back()
            return
        if self.ad_matches(rows,'上滑或点击跳转广告详情页面',True) and self.ad_matches(rows,'关闭',True):
            self.tap_row(self.ad_matches(rows,'关闭',True)[0])
            time.sleep(.7)

    def native(self, **selector):
        self.dismiss_ads()
        super().native(**selector)

    def content_wait(self, predicate, message, timeout=25):
        def ready():
            self.dismiss_ads()
            return predicate()
        return super().content_wait(ready,message,timeout)

    def main_ready(self):
        return self.activity_is('alexhome.ui.activity.MainActivity') and self.visible('看世界',region=(0,.9,1,1))

    def main_page(self):
        self.dismiss_ads()
        self.return_to(self.main_ready,'未返回去哪儿旅行首页',limit=10)
        self.native(rid='atom_alexhome_mod_home')
        self.dismiss_ads()

    def flight_ready(self):
        return self.activity_is('flight.modules.home') and self.has(rid='atom_flight_tv_search_text')

    @optional('flight_page')
    def flight_page(self):
        self.main_page()
        self.native(rid='atom_alexhome_youth_mod_flight')
        self.content_wait(self.flight_ready,'机票搜索页未打开')
        self.dismiss_ads()

    @optional('flights')
    def flight_search(self):
        self.needs('flight_page')
        self.dismiss_ads()
        if not self.flight_ready():
            raise StepUnavailable('当前不在机票搜索页')
        self.native(rid='atom_flight_tv_search_text')
        self.content_wait(self.flight_results_ready,'已点击机票搜索，但搜索结果未加载',timeout=30)

    def flight_results_ready(self):
        return not self.flight_ready() and any(self.visible(s,True) for s in ('起飞时间','低价优先','出发时间','筛选','无直飞航班'))

    @optional('flights')
    def tomorrow(self):
        self.needs('flights')
        self.entry('明天')
        self.content_wait(self.flight_results_ready,'明天的航班结果未显示')

    @optional('flights')
    def browse_flights(self):
        self.needs('flights')
        self.browse_checked(self.flight_results_ready,5,5,'机票结果不可用')

    def flight_detail_ready(self):
        return not self.flight_ready() and (self.visible('预订') or self.visible('订',region=(.7,.2,1,.9)))

    @optional('flight_detail')
    def first_flight(self):
        self.needs('flights')
        if not self.flight_results_ready():
            raise StepUnavailable('机票结果不可用')
        for _ in range(3):self.swipe(.5,.35,.5,.8)
        def open_first():
            cards=self.nodes(desc='flight_module_search|QunarFlightList|Flights_',prefix=True)
            if not cards:raise StepUnavailable('未找到首条航班卡片')
            self._locators.add('tree');self.click_node(sorted(cards,key=lambda n:self.bounds(n)[1])[0])
        self.go(open_first,self.flight_detail_ready,'首条机票方案未打开')

    @optional('flight_detail')
    def browse_flight(self):
        self.needs('flight_detail')
        self.browse_checked(self.flight_detail_ready,1,1,'机票方案不可用')

    @optional('booking')
    def booking(self):
        self.needs('flight_detail')
        def open_booking():
            for label in ('预订','订'):
                matches=self.find(label,region=(.7,.25,1,.9))
                if matches:self.tap_row(matches[0]);return
            raise StepUnavailable('当前航班没有可核对的预订按钮')
        self.go(open_booking,lambda:self.visible('登录',True) or self.booking_ready(),
                '订票填写页未显示')
        if self.visible('登录',True):
            raise StepUnavailable('预订需要登录，停在登录页，未提交订单')

    def booking_ready(self):
        return (self.has(desc='f_major_bundle_rn|QunarBooking|NavBar')
                and self.visible('填单页',True,region=(0,.04,1,.14)))

    @optional('booking')
    def browse_booking(self):
        self.needs('booking')
        if not self.booking_ready():raise StepUnavailable('订票填写页不可用')
        self.browse(2,2)

    def return_flight(self):
        self.dismiss_ads()
        self.return_to(self.flight_ready,'未返回机票首页',limit=8)

    @optional('checkin')
    def checkin(self):
        self.return_flight()
        for _ in range(3):
            if self.visible('值机选座') or self.visible('航班服务'):break
            self.swipe();time.sleep(.7)
        if self.visible('值机选座'):
            self.entry('值机选座')
        else:
            self.entry('航班服务')
            self.content_wait(lambda:self.visible('值机选座'),'航班服务中没有值机选座')
            self.entry('值机选座')
        self.content_wait(lambda:self.visible('值机',True) or self.visible('选座',True),'值机页面未打开')

    @optional('checkin')
    def browse_checkin(self):
        self.needs('checkin')
        self.browse(1,1)

    def hotel_ready(self):
        return not self.main_ready() and self.visible('开始搜索')

    @optional('hotel_page')
    def hotel_page(self):
        self.main_page()
        self.native(rid='atom_alexhome_youth_mod_hotel')
        self.content_wait(self.hotel_ready,'酒店搜索页未打开')

    @optional('hotel_page')
    def xian(self):
        self.needs('hotel_page')
        if not self.hotel_ready():raise StepUnavailable('酒店搜索页不可用')
        if self.has(rid='atom_hotel_tv_city_name',text='西安') or self.visible('西安'):
            self.adapt('目的地已是西安，保留当前城市')
            return
        nodes=self.nodes(rid='atom_hotel_tv_city_name')
        if not nodes:raise StepUnavailable('酒店目的地未导出可核对的城市控件')
        self._locators.add('tree'); self.click_node(nodes[0])
        self.content_wait(lambda:self.has(rid='qd_placeholder') or self.visible('西安')
                          or any(n.get('class')=='android.widget.EditText' for n in self.nodes()),'城市选择页未显示')
        if self.has(rid='qd_common_tv_cityname',text='西安'):
            self.go(lambda:self.native(rid='qd_common_tv_cityname',text='西安'),
                    lambda:self.hotel_ready() and self.has(rid='atom_hotel_tv_city_name',text='西安'),
                    '历史/热门城市西安未选中')
            return
        if not self.visible('西安'):
            if self.has(rid='qd_placeholder'):self.native(rid='qd_placeholder')
            self.content_wait(lambda:any(n.get('class')=='android.widget.EditText' for n in self.nodes()),'城市搜索输入框未显示')
            edits=[n for n in self.nodes() if n.get('class')=='android.widget.EditText']
            self.click_node(edits[0]);self.input_text('西安')
            self.content_wait(lambda:self.visible('西安'),'西安城市结果未显示')
        def select_city():
            height=self.d.window_size()[1]
            matches=[n for n in self.nodes(text='西安') if n.get('class')!='android.widget.EditText'
                     and self.bounds(n)[1]<height*.3]
            if not matches:raise StepUnavailable('未找到“城市 西安/陕西”的城市结果')
            self._locators.add('tree');self.click_node(sorted(matches,key=lambda n:self.bounds(n)[1])[0])
        self.go(select_city,lambda:self.hotel_ready() and self.visible('西安'),'酒店目的地未切换到西安')

    @optional('hotel_orders')
    def hotel_orders(self):
        self.needs('hotel_page')
        self.entry('酒店订单','我的订单')
        self.content_wait(lambda:not self.hotel_ready() and any(self.visible(s,True) for s in
                          ('搜索订单','待入住','登录')),'酒店订单页未显示')
        if self.visible('登录',True):self.adapt('当前未登录，酒店订单验证到登录入口')

    def return_hotel(self):
        self.needs('hotel_page')
        self.return_to(self.hotel_ready,'未返回酒店搜索页')

    @optional('hotels')
    def hotel_search(self):
        self.needs('hotel_page')
        self.return_hotel();self.entry('开始搜索')
        self.content_wait(self.hotel_results_ready,'酒店搜索结果未加载',timeout=35)

    def hotel_results_ready(self):
        return (self.has(desc='home_rn|listPage|filter') and
                self.has(desc='home_rn|listPage|hotel_',prefix=True) and
                any(self.visible(s,True,region=(0,.05,1,.5)) for s in ('智能排序','星级/价格','位置区域')))

    @optional('hotels')
    def browse_hotels(self):
        self.needs('hotels');self.browse_checked(self.hotel_results_ready,3,3,'酒店列表不可用')

    @optional('hotel_detail')
    def first_hotel(self):
        self.needs('hotels')
        for _ in range(3):self.swipe(.5,.35,.5,.8)
        def open_first():
            cards=self.nodes(desc='home_rn|listPage|hotel_',prefix=True)
            if not cards:raise StepUnavailable('当前列表没有可核对的酒店卡片')
            self._locators.add('tree');self.click_node(sorted(cards,key=lambda n:self.bounds(n)[1])[0])
        self.go(open_first,lambda:not self.hotel_results_ready() and
                (self.visible('房型',True) or self.visible('设施',True)),'酒店详情未打开')

    @optional('hotel_pictures')
    def hotel_pictures(self):
        self.needs('hotel_detail')
        for name in ('查看全部图片','相册','图片'):
            if self.visible(name,True):
                self.choose(name,True,index=0);break
        else:raise StepUnavailable('酒店详情没有可核对的图片/相册入口')
        self.content_wait(lambda:self.visible('相册',True) or self.visible('全部',True),'酒店图片详情未打开')
        width,height=self.d.window_size()
        def open_photo():
            tiles=[n for n in self.nodes() if n.get('content-desc') in ('房间','客房','外观','公共区域')
                   and self.bounds(n)[2]-self.bounds(n)[0]>width*.3
                   and self.bounds(n)[3]-self.bounds(n)[1]>height*.1]
            if not tiles:raise StepUnavailable('图片总览没有可核对的照片缩略图')
            self._locators.add('tree');self.click_node(sorted(tiles,key=lambda n:self.bounds(n)[1])[0])
        self.go(open_photo,lambda:any(re.search(r'\d+\s*/\s*\d+|第\d+张',r['text']) for r in self.screen()),
                '酒店照片大图未打开')
        self.adapt('当前版本先进入图片总览，再打开首张照片大图')

    @optional('hotel_pictures')
    def browse_pictures(self):
        self.needs('hotel_pictures');self.horizontal(3,3)

    @optional('train_page')
    def train_page(self):
        self.main_page();self.native(rid='atom_alexhome_youth_mod_train')
        self.dismiss_ads()
        self.content_wait(lambda:self.visible('搜索') or self.visible('搜索车票'),'火车高铁查询页未打开')

    @optional('trains')
    def train_search(self):
        self.needs('train_page');self.entry('搜索','搜索车票','查询')
        self.content_wait(lambda:self.visible('出发时间',True) or self.visible('耗时',True)
                          or self.visible('暂无车次',True),'车次结果未加载',timeout=35)


class SodaMusicDynamicCase(TravelShopCase):
    PACKAGE='com.luna.music'
    all_app_package_list=[PACKAGE]
    COMPONENT=PACKAGE+'/com.luna.biz.main.main.MainActivity'
    TAP_MS=200
    INPUT_SOURCE='mouse'

    def dismiss_ads(self):
        rows=super().dismiss_ads()
        if self.ad_matches(rows,'签到7天领',True) and self.ad_matches(rows,'打开签到提醒',True):
            # 已核对签到弹窗底部 X；不触碰领取或提醒开关。
            self.pct(.5,.721)
            self.invalidate()
        if self.ad_matches(rows,'选择最近的听歌偏好') and len(self.ad_matches(rows,'完成'))==1:
            self.tap_row(self.ad_matches(rows,'完成')[0])
            self.adapt('关闭首次听歌偏好引导，不选择新的偏好')

    def main_ready(self):
        return (self.activity_is('main.main.MainActivity') and self.has(rid='czr')
                and self.has(rid='b6j',text='我的') and self.has(rid='b6j',text='发现')
                and self.visible('我的',region=(.75,.9,1,.99)))

    def main_page(self):
        self.dismiss_ads()
        self.return_to(self.main_ready,'未返回汽水音乐底部导航',limit=8)

    def search_ready(self):
        return self.has(rid='ddz') and bool(self.input_nodes())

    @optional('search')
    def search_page(self):
        self.main_page()
        def open_search():
            if self.has(rid='czr'):self.native(rid='czr')
            elif self.has(desc='搜索'):self.native(desc='搜索')
            else:raise StepUnavailable('当前首页未导出可核对的搜索图标')
        self.go(open_search,self.search_ready,'汽水音乐搜索输入页未打开')

    def results_ready(self):
        return self.visible('国歌',True,region=(0,.15,1,.85)) and any(self.visible(s) for s in ('综合','歌曲','单曲'))

    @optional('search')
    def search_anthem(self):
        self.needs('search')
        self.input_text('国歌')
        if self.visible('搜索',region=(.75,.03,1,.16)):
            self.choose('搜索',region=(.75,.03,1,.16))
        else:self.d.press('enter');self.invalidate()
        self.content_wait(self.results_ready,'国歌搜索结果未显示')

    @optional('search')
    def browse_search(self):
        self.needs('search');self.browse_checked(self.results_ready,2,2,'国歌搜索结果不可用')

    @optional('playback')
    def play_pause(self):
        self.main_page()
        if self.media_state()!=3:
            self.play_control(False)
            self.content_wait(lambda:self.media_state()==3,'汽水音乐未开始播放')
        time.sleep(15)
        if self.media_state()!=3:
            raise StepUnavailable('播放中断，未完成15秒连续播放')
        self.play_control(True)
        self.content_wait(lambda:self.media_state()==2,'汽水音乐暂停未生效')

    def play_control(self, pause):
        labels=('暂停','暂停播放') if pause else ('播放','继续播放')
        for label in labels:
            if self.has(desc=label):self.native(desc=label);return
            if self.visible(label):self.choose(label);return
        if self.main_ready() and self.has(rid='b6a'):
            self.native(rid='b6a')
            return
        # 播放/暂停状态有时使用不同原生图标ID，底部中央按钮的位置已经截图核对。
        if not self.main_ready():raise StepUnavailable('当前不在汽水音乐播放器')
        self.pct(.5,.936)
        self.adapt('底部播放图标未导出描述，按主界面中央按钮比例切换，以本包媒体会话校验')

    def my_page(self):
        self.return_to(self.main_ready,'未返回汽水音乐主界面')
        self.entry('我的',region=(.75,.9,1,.99))
        self.content_wait(lambda:self.visible('我喜欢',True) or self.visible('登录',True),'我的页面未显示')

    @optional('favorites')
    def favorites(self):
        if self.visible('登录',True):raise StepUnavailable('我喜欢的音乐需要登录')
        self.entry('我喜欢的音乐','我喜欢')
        self.content_wait(lambda:self.visible('我喜欢',True) and not self.visible('模式选择'),'我喜欢列表未打开')

    @optional('header_menu')
    def header_menu(self):
        self.main_page()
        # 本机21.2.0的三横线在左上，右上为搜索。按已核对的实际三横线打开侧栏。
        if not self.has(rid='c+o'):raise StepUnavailable('当前首页没有三横线模式入口')
        self.go(lambda:self.pct(.08,.081),lambda:self.visible('听歌模式') and self.visible('默认模式',True),
                '三横线侧栏未打开')
        self.adapt('本版本三横线位于左上，打开“听歌模式”侧栏；未切换模式或开通会员')


class TaobaoDynamicCase(TravelShopCase):
    PACKAGE='com.taobao.taobao'
    all_app_package_list=[PACKAGE]
    COMPONENT=PACKAGE+'/com.taobao.tao.welcome.Welcome'
    ALBUM='淘宝性能素材'
    NEED_IMAGES=True
    TAP_MS=200
    INPUT_SOURCE='mouse'
    # 本次人工授权仅覆盖此关键词选出的商品客服；后续批跑需显式启用实发。
    SEND_ENV='TAOBAO_ALLOW_CUSTOMER_MESSAGES'

    def verification_active(self):
        app=self.current_app()
        return app['package']==self.PACKAGE and '.security.open.middletier.fc.ui.' in app['activity']

    def foreground(self):
        super().foreground()
        if self.verification_active():
            raise StepUnavailable('淘宝要求滑块/安全验证，停止交互，待用户在应用内处理后复测')

    def native(self, **selector):
        self.foreground()
        super().native(**selector)

    def home(self):
        if self.verification_active():
            self.d.press('home')
            self.wait_for(lambda:'launcher' in self.current_app()['activity'].lower(),'未返回Home')
            self.adapt('出现淘宝验证页，按Home离开，未操作验证控件')
            return
        super().home()

    def launch(self):
        self._verified_product=False
        self._customer_header=''
        super().launch()

    def prepare_images(self):
        import struct, zlib, tempfile
        def chunk(kind,data):
            return struct.pack('!I',len(data))+kind+data+struct.pack('!I',zlib.crc32(kind+data))
        raw=b''.join(b'\x00'+bytes((35,165,210))*320 for _ in range(320))
        png=(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!2I5B',320,320,8,2,0,0,0))
             +chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
        remote='/sdcard/Pictures/'+self.ALBUM
        self.d.shell(['mkdir','-p',remote])
        with tempfile.TemporaryDirectory(prefix='taobao-fixture-') as folder:
            local=Path(folder)/'SeaOfStars_Taobao_Test.png';local.write_bytes(png)
            self.d.push(str(local),remote+'/'+local.name)
            self.d.shell(['am','broadcast','-a','android.intent.action.MEDIA_SCANNER_SCAN_FILE',
                          '-d','file://'+remote+'/'+local.name])

    def dismiss_ads(self):
        if self.verification_active():
            raise StepUnavailable('淘宝要求滑块/安全验证，停止交互，待用户在应用内处理后复测')
        rows=super().dismiss_ads()
        if self.ad_matches(rows,'点击推荐可切换模式',True):
            self.pct(.5,.42)
            return
        if self.has(desc='限时福利砸中你') and self.has(desc='关闭按钮'):
            self.native(desc='关闭按钮')
            time.sleep(.8);self.invalidate()
        # 原生首页券条，只点该条右端关闭区域，不领取优惠券。
        banners=self.nodes(rid='homepage_pop_view')
        if banners and self.ad_matches(rows,'待领取',True):
            a,b,z,y=self.bounds(banners[0]);w,h=self.d.window_size()
            self.pct((a+(z-a)*.96)/w,(b+y)/2/h)

    def main_ready(self):
        return (self.activity_is('tao.welcome.Welcome','tao.TBMainActivity') and self.has(desc='搜索栏')
                and self.visible('购物车',region=(.5,.9,.8,1))
                and not self.has(desc='限时福利砸中你'))

    def main_page(self):
        self.dismiss_ads()
        if not self.main_ready() and self.has(desc='首页') and self.visible('购物车',region=(.5,.9,.8,1)):
            self.go(lambda:self.native(desc='首页'),self.main_ready,'淘宝首页底栏未切换')
        self.return_to(self.main_ready,'未返回淘宝首页',limit=10)

    def search_ready(self):
        return self.activity_is('search.uniform.SearchActivity') and self.has(rid='searchEdit')

    def results_ready(self):
        return self.search_ready() and self.has(desc='销量,',prefix=True)

    @optional('search')
    def search_tissue(self):
        self.main_page()
        self.go(lambda:self.native(desc='搜索栏'),self.search_ready,'淘宝搜索输入页未打开')
        self.input_text('清风卫生纸')
        self.go(lambda:self.native(rid='searchbtn'),self.results_ready,'清风卫生纸搜索结果未显示')
        self._tissue_search=True

    @optional('search')
    def browse_results(self):
        self.needs('search');self.browse_checked(self.results_ready,5,6,'商品结果不可用')

    def product_ready(self):
        return (self.current_app()['activity'].rsplit('.',1)[-1] in ('TTDetailActivity','DetailActivity') and
                (self.has(desc='客服,按钮') or self.visible('客服',region=(0,.85,.5,1))))

    @optional('product')
    def sales_first(self):
        self.needs('search')
        for _ in range(5):
            if self.has(desc='销量,',prefix=True):break
            self.swipe(.5,.35,.5,.8)
        self.go(lambda:self.native(desc='销量,',prefix=True),
                lambda:self.has(desc='销量,已选中'),'销量排序未选中')
        w,h=self.d.window_size()
        cards=[n for n in self.nodes() if '清风' in n.get('content-desc','')
               and re.search(r'(元|付款)',n.get('content-desc',''))
               and (self.bounds(n)[3]-self.bounds(n)[1])>h*.12
               and self.bounds(n)[1]>h*.15 and self.bounds(n)[3]<h*.98]
        if not cards:raise StepUnavailable('销量排序后没有可核对的清风商品卡片')
        cards=sorted(cards,key=lambda n:(self.bounds(n)[1],self.bounds(n)[0]))
        organic=[n for n in cards if not any(s in n.get('content-desc','') for s in ('下拉补贴','下拉详情','广告'))]
        card=(organic or cards)[0]
        if card is not cards[0]:self.adapt('首条为补贴广告卡，改为销量结果中首条普通清风商品')
        self._selected_product=card.get('content-desc','')
        def open_product():
            if not self.results_ready():raise StepUnavailable('已离开商品列表，未重复点击旧卡片位置')
            fresh=self.nodes(desc=self._selected_product)
            if not fresh:raise StepUnavailable('本次清风商品卡片已变化，未点击旧位置')
            self._locators.add('tree');self.click_node(fresh[0])
        self.go(open_product,self.product_ready,'首条清风商品详情未打开')
        self._verified_product='清风' in self._selected_product

    @optional('product')
    def browse_product(self):
        self.needs('product');self.browse_checked(self.product_ready,5,5,'商品详情不可用')

    @optional('reviews')
    def reviews(self):
        self.needs('product');self.return_product()
        height=self.d.window_size()[1]
        tabs=[n for n in self.nodes(text='评价') if self.bounds(n)[1]<height*.2]
        if tabs:self._locators.add('tree');self.click_node(tabs[0]);time.sleep(.7);self.invalidate()
        if not self.product_ready() and any(self.visible(x,True) for x in ('全部评价','有图','追评')):
            self.adapt('当前版本通过顶部“评价”直接打开完整评价页')
            return
        for _ in range(5):
            # “问大家”也有查看更多；必须限定到评价标题所在的原生行。
            headers=[n for n in self.nodes() if re.match(r'^(宝贝|用户|商品)?评价',n.get('content-desc',''))
                     and any(x in n.get('content-desc','') for x in ('查看更多','查看全部'))]
            if headers:
                header=headers[0]
                buttons=[n for n in header.iter('node') if any(t in (n.get('text','')+' '+n.get('content-desc',''))
                         for t in ('查看更多','查看全部')) and n is not header]
                if buttons:
                    self._locators.add('tree');self.click_node(sorted(buttons,key=lambda n:self.bounds(n)[2]-self.bounds(n)[0])[0]);break
                # 某些版本只导出整行；限定评价行右侧，不能点击整行中心或问大家。
                a,b,z,y=self.bounds(header);w,h=self.d.window_size()
                if y-b<h*.15:
                    self.pct((a+(z-a)*.92)/w,(b+y)/2/h);break
            if self.visible('查看全部评价',True):self.choose('查看全部评价',True,index=0);break
            labels=[r for r in self.screen() if re.match(r'^(宝贝|用户|商品)?评价',r['text'])]
            more=self.find('查看更多')
            matches=[r for r in more if any(abs(r['y']-title['y'])<.025 for title in labels)]
            if matches:self.tap_row(matches[0]);break
            self.swipe();time.sleep(.7)
        else:raise StepUnavailable('当前商品未找到评价区域的查看更多入口，未点击问大家')
        self.content_wait(lambda:not self.product_ready() and any(self.visible(x,True) for x in ('全部评价','有图','追评')),
                          '宝贝评价页未打开')

    @optional('reviews')
    def browse_reviews(self):
        self.needs('reviews');self.browse(5,5)

    @optional('product_return')
    def return_product(self):
        self.needs('product')
        self.return_to(self.product_ready,'未返回本次商品详情',limit=6)

    def chat_ready(self):
        return (self.activity_is('chat', 'conversation') and
                any(n.get('class')=='android.widget.EditText' for n in self.nodes()))

    @optional('customer')
    def customer_service(self):
        self.needs('product');self.return_product()
        if not getattr(self,'_verified_product',False):raise StepUnavailable('未确认本次清风商品，停止打开客服')
        def open_customer():
            if self.has(desc='客服,按钮'):self.native(desc='客服,按钮')
            else:self.entry('客服',region=(0,.85,.55,1))
        self.go(open_customer,lambda:self.chat_ready() or self.visible('登录',True),'商品客服未打开')
        if not self.chat_ready():raise StepUnavailable('商品客服需要登录，未进入聊天')
        # 商品详情直接打开的客服仍须展示同一品牌/商品，再保存当前会话顶部身份。
        self.content_wait(lambda:self.visible('清风',True),'客服页面未显示清风商品或店铺，未授权当前会话',timeout=15)
        last=['']
        def stable_header():
            title=self.chat_header()
            ready=bool(title) and title==last[0]
            last[0]=title
            return ready
        self.content_wait(stable_header,'客服标题尚未稳定，未授权当前会话',timeout=12)
        self._customer_header=self.chat_header()
        if not self._customer_header:raise StepUnavailable('无法核对客服会话标题')

    def chat_header(self):
        # 只取店名标题，排除下方会变化的星级/评分与加载时的通用“消息”。
        labels=[self.normalized(r['text']) for r in self.screen()
                if .04<r['y']+r['h']/2<.085 and .12<r['x']+r['w']/2<.7
                and re.search(r'[\u4e00-\u9fff]',r['text'])]
        return '|'.join(t for t in labels if t not in ('消息','客服'))

    def require_customer_send(self):
        self.needs('customer')
        if os.environ.get(self.SEND_ENV)!='1':raise StepUnavailable('客服实发未启用；设置 '+self.SEND_ENV+'=1 后运行')
        if not (getattr(self,'_verified_product',False) and self.chat_ready()
                and getattr(self,'_customer_header','') and self.chat_header()==self._customer_header):
            raise StepUnavailable('当前客服会话与本次清风商品身份不一致，未发送')

    @optional('hello')
    def send_hello(self):
        self.require_customer_send()
        if getattr(self,'_hello_attempted',False):raise StepUnavailable('已执行过本次文字发送，不重复发送')
        self.input_text('你好')
        edits=[n for n in self.nodes() if n.get('class')=='android.widget.EditText']
        if not any(n.get('text')=='你好' for n in edits):raise StepUnavailable('待发文字不是“你好”，未点击发送')
        self.require_customer_send()
        self._hello_attempted=True
        self.entry('发送',region=(.7,.45,1,1))
        self.content_wait(lambda:self.chat_ready() and self.visible('你好') and
                          not any(n.get('text')=='你好' and n.get('class')=='android.widget.EditText' for n in self.nodes()),
                          '文字发送结果未确认；不自动重发')

    @optional('picture')
    def send_picture(self):
        original=getattr(self,'_tap_source',self.INPUT_SOURCE)
        self._tap_source=''
        try:return self._send_picture()
        finally:self._tap_source=original

    def _send_picture(self):
        self.require_customer_send()
        if getattr(self,'_picture_attempted',False):raise StepUnavailable('已执行过本次图片发送，不重复发送')
        def open_drawer():
            if self.has(desc='抽屉菜单按钮'):self.native(desc='抽屉菜单按钮')
            elif self.has(desc='更多功能'):self.native(desc='更多功能')
            elif self.has(desc='添加'):self.native(desc='添加')
            elif self.visible('+'):self.choose('+',region=(.7,.6,1,1))
            else:raise StepUnavailable('客服聊天未导出可核对的加号入口')
        self.go(open_drawer,lambda:self.visible('相册'),'相册入口未展开')
        titles=('所有照片','全部照片','最近照片','最近项目')
        def open_album():
            items=[n for n in self.nodes(desc='相册') if n.get('clickable')=='true']
            if items:self._locators.add('tree');self.click_node(items[0])
            else:self.entry('相册')
        self.go(open_album,lambda:any(self.visible(t,True,region=(0,.03,1,.18)) for t in titles+(self.ALBUM,)),
                '未进入可核对的相册选择页')
        if not self.visible(self.ALBUM,region=(.1,.03,.9,.15)):
            for title in titles:
                if self.visible(title,True,region=(0,.03,1,.18)):
                    self.choose(title,True,region=(0,.03,1,.18),index=0);break
            self.content_wait(lambda:self.visible(self.ALBUM,True,region=(0,.15,1,1)),
                              '专用测试相册未显示，未选个人图片')
            self.choose(self.ALBUM,True,region=(0,.15,1,1),index=0)
        self.content_wait(lambda:self.visible(self.ALBUM,region=(.1,.03,.9,.15)),
                          '专用测试相册标题未显示，未选择图片')
        # 该相册只创建一张纯色测试图；必须有图片/选中控件才可选择。
        choices=[n for n in self.nodes() if re.search(r'(未选中|选择图片|选择照片)',n.get('content-desc',''))]
        if not choices:raise StepUnavailable('专用相册未导出图片选择控件，未猜测点击个人照片')
        self.click_node(choices[0]);time.sleep(.5);self.invalidate()
        if not self.visible('发送',True):raise StepUnavailable('选择测试图后未出现发送按钮')
        buttons=[r for r in self.find('发送',True) if r['x']+r['w']/2>.6
                 and (r['y']+r['h']/2<.18 or r['y']+r['h']/2>.82)]
        if not buttons:raise StepUnavailable('未找到当前测试图的发送按钮')
        self._picture_attempted=True
        self.tap_row(buttons[0])
        self.content_wait(self.chat_ready,'图片发送后未回到客服会话；不自动重发')
        self.adapt('仅发送专用纯色测试图；返回同一客服会话，具体送达状态以聊天截图核对')

    @optional('shop')
    def shop(self):
        self.needs('product');self.return_product();self.swipe()
        def open_shop():
            if self.has(desc='店铺,按钮'):self.native(desc='店铺,按钮')
            else:self.entry('店铺','进店逛逛',region=(0,.1,1,1))
        self.go(open_shop,lambda:self.has(desc='llShopInfoPart') or
                (not self.product_ready() and any(self.visible(x,True) for x in
                ('全部宝贝','全部商品','店铺首页','店铺推荐'))),'商品店铺未打开')
        self.browse(3,3)

    @optional('cart')
    def add_cart(self):
        self.needs('product');self.return_product()
        if not getattr(self,'_verified_product',False):raise StepUnavailable('未确认清风商品，未加购')
        if getattr(self,'_cart_attempted',False):raise StepUnavailable('本次已尝试加购，不自动重复增加数量')
        if self.has(desc='加入购物车,不可选') or self.visible('此地区暂不可购买',True):
            raise StepUnavailable('当前商品所在地区不可购买，加购按钮不可选，未更改收货地址')
        def success():
            return any(self.visible(t,True) for t in ('加入购物车成功','添加成功','已加入购物车','加购成功','加入成功'))
        self._cart_attempted=True
        self.entry('加入购物车',region=(.3,.85,1,1))
        self.content_wait(lambda:success() or self.visible('套餐类型',True) or self.visible('请选择',True),
                          '加购结果或规格选择页未显示')
        if success():return
        # 原生状态未导出时保留当前默认规格，只确认加购，不进入购买或支付。
        if not self.visible('加入购物车',region=(0,.85,1,1)):
            raise StepUnavailable('规格页没有明确的加购确认按钮')
        self.choose('加入购物车',region=(0,.85,1,1))
        self.content_wait(success,'加购成功未确认；不自动重试，避免重复增加数量')

    def selected_channel(self, name):
        return self.has(desc=name+',已选中') or self.has(desc=name+'已选中')

    def channel(self,name):
        self.main_page()
        def select():
            for desc in (name+',未选中',name+',已选中',name+'未选中',name+'已选中',name):
                if self.has(desc=desc):self.native(desc=desc);return
            self.entry(name,region=(0,.045,1,.11))
        self.go(select,lambda:self.selected_channel(name),'首页'+name+'频道未选中')

    def recommend(self):self.channel('推荐')

    @optional('third')
    def third_tab(self):
        self.channel('闪购')
        self.adapt('当前首页第三个频道为“闪购”，按实际第三个频道浏览')

    @optional('third')
    def browse_third(self):
        self.needs('third');self.browse_checked(lambda:self.selected_channel('闪购'),5,5,'第三频道不可用')

    def browse_recommend(self):
        self.recommend();self.browse(5,5)

    @optional('following')
    def following(self):self.channel('关注')

    @optional('following')
    def browse_following(self):
        self.needs('following');self.browse_checked(lambda:self.selected_channel('关注'),5,5,'关注页不可用')

    @optional('explore')
    def explore(self):
        self.main_page()
        label='逛逛' if self.visible('逛逛',region=(0,.9,1,1)) else '视频'
        self.bottom_node(label)
        self.content_wait(lambda:not self.has(desc='搜索栏') and
                (self.has(desc='已选中，推荐，按钮') or self.has(desc='已选中，关注，按钮')
                 or self.visible('发现')),'逛逛/视频内容未打开')
        if label=='视频':self.adapt('当前底栏“逛逛”已改为“视频”，改为浏览视频内容')

    @optional('explore')
    def browse_explore(self):
        self.needs('explore');self.browse(5,5);self.horizontal(3,3)

    def my_taobao(self):
        # 先恢复主屏，避免点在商品或视频里的同名字样。
        self.main_page();self.bottom_node('我的淘宝')
        self.content_wait(lambda:self.visible('我的订单',True) or self.visible('待付款'),'我的淘宝未打开')

    @optional('orders')
    def orders(self):
        self.entry('我的订单','全部订单','查看全部订单')
        self.content_wait(lambda:self.visible('全部') and self.visible('待付款'),'我的订单页未打开')

    @optional('orders')
    def browse_orders(self):
        self.needs('orders');self.horizontal(5,5)
