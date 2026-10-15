"""小米相册 5.4.2.10：控件定位、比例手势及逐步性能采集。"""
import json
import logging
import os
import time
import uuid

from Cases.Top48.dynamic_apps_common import DynamicAppCase
from aw_new import SeaOfStarsAW


class PhotoStepSkipped(Exception):
    pass


class PhotoDynamicCase(DynamicAppCase):
    PACKAGE = 'com.miui.gallery'
    all_app_package_list = [PACKAGE]
    NEED_VIDEO = False

    def shell(self, command):
        result = self.d.shell(command)
        if result.exit_code:
            raise RuntimeError('设备命令失败：' + result.output)
        return result.output

    def foreground(self):
        if self.current_app()['package'] not in (self.PACKAGE, 'com.hyper.gallery.plugin'):
            raise RuntimeError('当前不在相册流程：' + str(self.current_app()))

    def mark(self, reason):
        self._adapted = reason
        logging.info('适配替代：%s', reason)

    def ready(self, predicate, message):
        self.wait_for(predicate, message)
        time.sleep(.5)

    def choose(self, label):
        # 新版 Compose 控件多数将文字放在 content-desc。
        for selector in ({'desc': label}, {'text': label}):
            if self.has(**selector):
                self.click(**selector)
                return
        raise RuntimeError('没有找到控件：' + label)

    def prefix(self, label):
        found = self.nodes(desc=label, prefix=True)
        if not found:
            raise RuntimeError('没有找到入口：' + label)
        self.click_node(found[0])

    def back(self):
        super().back()
        # 相册 Compose 页面切换后层级更新较慢，避免连续返回穿过目标页。
        time.sleep(1.2)

    def launch(self):
        self._album_owned = False
        self._album_reason = None
        self.start()
        time.sleep(1)
        self.photos()

    def photos_ready(self):
        return self.has(desc='点击首页显示设置') and self.has(desc='点击搜索')

    def photos(self):
        # 底部 tab 是语义控件；标题“照片”不能当成 tab 点击。
        for _ in range(8):
            if self.has(desc='未选中, 照片'):
                self.click(desc='未选中, 照片')
                self.ready(self.photos_ready, '照片 tab 未打开')
                return
            if self.photos_ready():
                return
            self.back()
        raise RuntimeError('未返回照片主页')

    def albums(self):
        self.photos()
        self.click(desc='未选中, 影集')
        self.ready(lambda:self.has(desc='全部照片\n', prefix=True), '影集主页未打开')

    def all_photos(self):
        self.albums()
        self.prefix('全部照片\n')
        self.ready(lambda:self.has(desc='全部照片') and self.has(desc='返回'), '全部照片未打开')

    def top(self):
        for _ in range(6):
            self.swipe(y1=.35, y2=.83, duration=180)
            time.sleep(.25)
        time.sleep(1)

    def zoom_cycle(self):
        self.photos()
        scroller = self.d(packageName=self.PACKAGE, className='android.widget.ScrollView')
        if not scroller.exists:
            raise PhotoStepSkipped('照片页没有可执行双指缩放的滚动容器')
        for cycle in range(5):
            for inward in (True, True, False, False):
                self.foreground()
                if inward:
                    scroller.pinch_in(percent=35, steps=40)
                else:
                    scroller.pinch_out(percent=35, steps=40)
                time.sleep(1)
                self.require(desc='点击首页显示设置')
            self.d.screenshot(os.path.join(self.screenshot_dir_path, 'zoom_cycle_{}.png'.format(cycle+1)))
        self.mark('当前版采用连续缩略图密度缩放，按两次捏合、两次捏开执行5轮，日月年层级由截图核对')

    def scroll_grid(self, fling=False):
        for start,end in ((.78,.32),(.32,.78)):
            for _ in range(5):
                self.swipe(y1=start,y2=end,duration=150 if fling else 900)
                time.sleep(1)

    def scrollbar(self):
        raise PhotoStepSkipped('当前版本无可定位的日视图拖动滚动条；保留前两步抛滑与跟手滑，不以普通滑动冒充滚动条')

    def viewer(self):
        return self.has(desc='照片，', prefix=True) or self.has(desc='视频，', prefix=True)

    def first_grid_point(self):
        # 自绘网格没有节点；从截图寻找持续的缩略图色块，排除短小的日期/统计文字。
        # 所有采样位置、连续高度和点击偏移均相对截图尺寸计算。
        image=self.d.screenshot().convert('RGB')
        width,height=image.size
        background=image.getpixel((round(width*.98),round(height*.18)))
        start=None
        for y in range(round(height*.20),round(height*.85),max(1,height//500)):
            occupied=sum(max(abs(a-b) for a,b in zip(
                image.getpixel((round(width*x/60),y)),background))>35 for x in range(1,60))/59
            if occupied>.30:
                if start is None:
                    start=y
            elif start is not None:
                if y-start>height*.04:
                    return width*.1,start+min(width*.08,(y-start)*.4)
                start=None
        raise RuntimeError('截图中未识别到首行缩略图，不点击未知区域')

    def open_first(self, home=True, restore=True):
        if restore:
            self.top()
        if home:
            self.require(desc='点击首页显示设置')
        elif not (self.has(desc='全部照片') or self.has(desc='视频')):
            raise RuntimeError('不在全部照片或视频相册')
        self.transition(lambda:self.point(*self.first_grid_point()),self.viewer,'首个媒体未进入大图')

    def controls(self):
        self.require_viewer()
        if not self.has(desc='返回'):
            self.transition(lambda:self.pct(.5,.45),lambda:self.has(desc='返回'), '未显示大图工具栏')

    def require_viewer(self):
        if not self.viewer():
            raise RuntimeError('当前不是媒体大图页')

    def leave_viewer(self, side=False):
        if side:
            self.swipe(.005,.5,.45,.5,300)
        else:
            self.controls()
            self.click(desc='返回')
        self.ready(lambda:not self.viewer() and (self.photos_ready() or self.has(desc='全部照片')),
                   '退出大图后未返回照片列表')

    def repeat_open(self, side=False):
        for index in range(5):
            self.open_first(restore=index==0)
            self.leave_viewer(side)

    def full_swipes(self, left=0, right=0):
        self.require_viewer()
        for count,x1,x2 in ((left,.8,.2),(right,.2,.8)):
            for _ in range(count):
                self.swipe(x1,.5,x2,.5,400)
                time.sleep(1)
                self.require_viewer()

    def preview_strip(self, right=False):
        self.full_swipes(right=3 if right else 0,left=0 if right else 3)
        self.mark('当前大图页无底部预览条，改为在大图区域同方向滑动3次')

    def album_reentry(self):
        for _ in range(5):
            self.all_photos()
            self.swipe(.005,.5,.45,.5,300)
            self.ready(lambda:self.has(desc='全部照片\n',prefix=True), '侧滑未返回影集主页')

    def prepare_video(self):
        # 只生成和删除本次运行拥有的短录屏，文件名在详情页再次核验。
        self.photos()
        self._video_name = 'SeaOfStars_photo_delete_' + uuid.uuid4().hex + '.mp4'
        self._video_path = '/sdcard/DCIM/SeaOfStarsPhoto/' + self._video_name
        self.shell('mkdir -p /sdcard/DCIM/SeaOfStarsPhoto')
        self.shell('screenrecord --time-limit 1 --size 360x640 ' + self._video_path)
        self.shell('am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://' + self._video_path)
        self.wait_for(lambda:self.d.shell('test -s ' + self._video_path).exit_code == 0, '测试视频未生成')
        time.sleep(2)

    def videos(self):
        self.albums()
        self.prefix('视频\n')
        self.ready(lambda:self.has(desc='视频') and self.has(desc='返回'), '视频相册未打开')

    def first_video(self):
        self.open_first(home=False)
        self.controls()
        self.choose('更多')
        self.ready(lambda:self.has(desc='详情'), '视频更多菜单未打开')
        self.choose('详情')
        self.ready(lambda:self.has(rid='file_info_title',package='com.hyper.gallery.plugin'), '视频详情未打开')
        name = self.node(rid='file_info_title',package='com.hyper.gallery.plugin').get('text')
        self._video_verified = name == getattr(self,'_video_name',None)
        self.back()
        self.ready(self.viewer,'详情返回后未回到视频')
        if not self._video_verified:
            self.mark('第一条视频不是本次测试素材，仅查看，不删除；后续删除步骤将跳过')

    def delete_video(self):
        if not getattr(self,'_video_verified',False):
            raise PhotoStepSkipped('视频详情文件名不等于本次生成的测试文件，跳过删除')
        self.controls()
        self.choose('删除')
        self.ready(lambda:self.has(desc='确认删除这1项内容？',prefix=True), '删除提示未打开')
        buttons=[n for n in self.nodes(desc='删除') if n.get('clickable')=='true']
        if len(buttons)!=1:
            raise RuntimeError('删除确认按钮不唯一')
        self.click_node(buttons[0])
        self.wait_for(lambda:self.d.shell('test -e ' + self._video_path).exit_code != 0,
                      '测试视频未从原路径删除')
        self._video_verified=False
        time.sleep(1)

    def new_album_dialog(self):
        self.albums()
        self.choose('相册')
        self.ready(lambda:self.has(desc='新建相册'), '相册管理页未打开')
        if self.has(desc='动态测试',prefix=True):
            self._album_reason='已存在动态测试相册，本次不覆盖或删除已有相册'
            raise PhotoStepSkipped(self._album_reason)
        self.choose('新建相册')
        self.ready(lambda:self.has(desc='新建共享相册'), '新建菜单未打开')
        self.choose('新建相册')
        self.ready(lambda:bool([n for n in self.nodes() if n.get('class')=='android.widget.EditText']),
                   '相册名称输入框未打开')

    def check_album_flow(self):
        if self._album_reason:
            raise PhotoStepSkipped(self._album_reason)

    def name_album(self):
        self.check_album_flow()
        self.d.send_keys('动态测试',clear=True)
        self.ready(lambda:self.has(text='动态测试'), '相册名称未输入')
        self.choose('确定')
        self.ready(lambda:self.has(desc='请选择项目'), '媒体选择页未打开')
        self._album_owned=True

    def browse_picker(self):
        self.check_album_flow()
        self.require(desc='请选择项目')
        self.scroll_grid()
        # 当前选择器以“照片/影集”分栏，照片列表同时包含图片和视频。
        self.choose('影集')
        self.ready(lambda:self.has(desc='影集'), '选择器影集分栏未打开')
        self.choose('照片')
        self.ready(lambda:self.has(desc='请选择项目'), '未返回媒体选择列表')
        self.mark('图片和视频合并在照片列表，另浏览本版的影集分栏')

    def copy_media(self):
        self.check_album_flow()
        self.require(desc='请选择项目')
        media=self.nodes(desc='照片，',prefix=True)
        if not media:
            raise RuntimeError('选择器没有可复制照片')
        l,t,r,b=self.bounds(media[0])
        # 选择圆圈在缩略图右下角；中心点击会进入预览，不能当成勾选。
        self.point(l+(r-l)*.82,t+(b-t)*.82)
        self.ready(lambda:self.has(desc='显示1项所选内容'), '未勾选一张照片')
        self.choose('确认')
        self.ready(lambda:self.has(desc='选择照片添加方式'), '添加方式面板未打开')
        self.choose('复制')
        self.ready(lambda:self.has(desc='动态测试 , 1'), '复制后未出现含1张照片的动态测试相册')

    def delete_album(self):
        self.check_album_flow()
        if not self._album_owned:
            raise PhotoStepSkipped('本次未创建动态测试相册')
        n=self.node(desc='动态测试 , 1')
        l,t,r,b=self.bounds(n)
        x,y=round((l+r)/2),round(t+(b-t)*.4)
        self.shell('input -d 0 swipe {0} {1} {0} {1} 750'.format(x,y))
        self.ready(lambda:self.has(desc='删除'), '长按相册未出现删除菜单')
        self.choose('删除')
        self.ready(lambda:self.has(desc='删除所选相册？'), '删除相册提示未打开')
        self.choose('全设备删除')
        self.ready(lambda:self.has(desc='新建相册') and not self.has(desc='动态测试',prefix=True),
                   '本次创建的相册未删除')
        self._album_owned=False

    def set_up(self):
        super().set_up()
        if self.NEED_VIDEO:
            self.start()
            self.prepare_video()

    def run_case(self):
        if not getattr(self,'_prepared',False):
            self.set_up()
        records=[]
        for run in range(self.TEST_TIME):
            for number,(name,action,stay) in zip(self.STEP_NUMBERS,self.steps()):
                record=dict(run=run+1,step=number,name=name,status='PASS')
                self._adapted=None
                logging.info('%s、%s',number,name)
                SeaOfStarsAW.start_perfetto_trace()
                try:
                    action()
                    time.sleep(stay)
                    if self._adapted:
                        record.update(status='ADAPTED',reason=self._adapted)
                except PhotoStepSkipped as error:
                    record.update(status='SKIP',reason=str(error))
                    logging.warning('SKIP %s：%s',name,error)
                except Exception as error:
                    record.update(status='FAIL',reason=str(error))
                    logging.exception('步骤失败：%s',name)
                    raise
                finally:
                    records.append(record)
                    with open(os.path.join(self.result_dir_path,'step_results.json'),'w',encoding='utf-8') as f:
                        json.dump(records,f,ensure_ascii=False,indent=2)
                    try:
                        SeaOfStarsAW.stop_and_get_perfetto_trace(
                            self.trace_dir_path,self.__class__.__name__,
                            'step_{}、{}_{}'.format(number,name,record['status']),'',self.screenshot_dir_path)
                    except Exception:
                        if record['status']!='FAIL':
                            raise
                        logging.exception('失败步骤 trace 导出失败')
