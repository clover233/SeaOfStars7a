"""图库浏览照片；用例表1140～1158行（原表无第10步）。"""
from Cases.Top48.photo_common import PhotoDynamicCase


class PerformanceDynamic_photo_0010(PhotoDynamicCase):
    STEP_NUMBERS = tuple(range(1,10)) + tuple(range(11,18))

    def steps(self):
        return [
            ('启动相册',self.launch,3),
            ('点击照片进入照片tab',self.photos,1),
            ('双指捏合捏开切换视图重复5次',self.zoom_cycle,1),
            ('日视图上抛5次下抛5次',lambda:self.scroll_grid(fling=True),0),
            ('日视图向上跟手滑5次向下跟手滑5次',self.scroll_grid,0),
            ('日视图上下滚动条滑动各5次',self.scrollbar,0),
            ('点击第一张照片进入大图',self.open_first,1),
            ('底部预览条向右滑动3次',lambda:self.preview_strip(right=True),1),
            ('底部预览条向左滑动3次',self.preview_strip,1),
            ('点击左上角退出照片页',self.leave_viewer,1),
            ('第一张照片大图与左上角返回重复5次',self.repeat_open,1),
            ('第一张照片大图与侧滑退出重复5次',lambda:self.repeat_open(side=True),1),
            ('点击第一张照片查看大图',self.open_first,1),
            ('左滑5次右滑5次查看大图',lambda:self.full_swipes(left=5,right=5),1),
            ('返回相册主界面',self.photos,1),
            ('滑动返回Home页',self.home,1),
        ]
