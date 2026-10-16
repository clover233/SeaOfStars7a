"""王者荣耀启动及系统天气浏览；沿用逐步采集与控件/比例定位。"""
import time
from Cases.Top48.travel_shop_common import TravelShopCase
from Cases.Top48.observed_apps_common import StepUnavailable, optional


class HonorLaunchCase(TravelShopCase):
    PACKAGE='com.tencent.tmgp.sgame'
    all_app_package_list=[PACKAGE]
    COMPONENT=PACKAGE+'/.SGameActivity'

    def main_ready(self):
        return self.current_app()['package']==self.PACKAGE and self.activity_is('SGameActivity')

    def main_page(self):
        self.content_wait(self.main_ready,'王者荣耀启动界面未显示')

    def launch_30(self):
        self.launch()
        # 不自动登录、确认协议、下载资源或开始对局；启动运行也是表中场景。
        deadline=time.monotonic()+30
        while time.monotonic()<deadline:
            self.dismiss_system_prompt()
            if self.current_app()['package']!=self.PACKAGE:
                raise StepUnavailable('王者荣耀运行期间离开前台，未完成30秒驻留')
            time.sleep(min(1,max(0,deadline-time.monotonic())))
        if self.visible('登录',True) or self.visible('同意',True) or self.visible('更新',True):
            self.adapt('完成启动前台运行30秒，当前停留登录/协议/资源提示，不代替用户确认')


class WeatherDynamicCase(TravelShopCase):
    PACKAGE='com.miui.weather2'
    all_app_package_list=[PACKAGE]
    COMPONENT=PACKAGE+'/.ActivityWeatherMain'

    def main_ready(self):
        return self.activity_is('ActivityWeatherMain') and self.has(desc='城市管理') and any(
            '第' in n.get('content-desc','') and '页，共' in n.get('content-desc','') for n in self.nodes())

    def main_page(self):
        self.return_to(self.main_ready,'未返回天气主界面')

    def browse_main(self):
        self.main_page();self.browse(5,5)

    @optional('cities')
    def cities(self):
        self.main_page()
        for label in ('管理城市','城市管理','城市列表'):
            if self.has(desc=label):self.native(desc=label);break
            if self.visible(label):self.choose(label);break
        else:raise StepUnavailable('当前天气版本没有导出城市管理入口')
        self.content_wait(lambda:self.has(desc='已添加城市') and self.has(desc='搜索城市'),
                          '天气城市管理页未打开')

    @optional('city_menu')
    def city_menu(self):
        self.needs('cities')
        for label in ('更多设置','更多','菜单','设置'):
            if self.has(desc=label):self.native(desc=label);break
            if self.visible(label):self.choose(label);break
        else:raise StepUnavailable('当前城市管理页没有左上角按钮，保留城市列表，不进入未知入口')
        self.content_wait(lambda:self.visible('设置') or self.visible('编辑') or self.visible('取消'),'城市管理菜单未展开')
        self.pct(.5,.48)
        self.content_wait(lambda:not self.visible('设置') and not self.visible('编辑'),'点击空白后菜单未关闭')
        self.adapt('当前版本城市菜单在右上“更多设置”，点击空白关闭菜单')

    def browse_again(self):
        self.main_page();self.browse(1,1)
        self.adapt('表中“主页浏览”未指定次数，执行上下各一次')

    @optional('switch_city')
    def switch_cities(self):
        self.main_page()
        import re
        def page():
            for n in self.nodes():
                match=re.search(r'第(\d+)页，共(\d+)页',n.get('content-desc',''))
                if match:return tuple(map(int,match.groups()))
            return None
        initial=page()
        if not initial or initial[1]<2:
            raise StepUnavailable('现有城市不足两个，未新增位置或虚报切换城市')
        seen={initial[0]}
        for _ in range(5):
            for a,b in ((.8,.2),(.2,.8)):
                for _ in range(5):
                    self.swipe(a,.45,b,.45);time.sleep(2)
                    current=page()
                    if current:seen.add(current[0])
        if len(seen)<2:raise StepUnavailable('已执行50次横滑，但城市页码未变化，未确认切换成功')
