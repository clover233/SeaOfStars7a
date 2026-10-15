"""图库管理相册；用例表1159～1175行。"""
from Cases.Top48.photo_common import PhotoDynamicCase


class PerformanceDynamic_photo_0030(PhotoDynamicCase):
    NEED_VIDEO = True
    STEP_NUMBERS = tuple(range(1,18))

    def steps(self):
        return [
            ('启动相册',self.launch,3),
            ('点击影集',self.albums,1),
            ('点击图片进入全部照片',self.all_photos,1),
            ('全部照片上抛5次下抛5次',lambda:self.scroll_grid(fling=True),0),
            ('全部照片向上跟手滑5次向下跟手滑5次',self.scroll_grid,0),
            ('进入全部照片并侧滑返回影集重复5次',self.album_reentry,1),
            ('点击视频进入视频相册',self.videos,1),
            ('点击第一个视频查看详情',self.first_video,1),
            ('删除本次生成的测试视频并确认',self.delete_video,1),
            ('返回影集界面',self.albums,1),
            ('点击相册及加号新建相册',self.new_album_dialog,1),
            ('设置相册名称为动态测试并确认',self.name_album,1),
            ('浏览图片视频选择器上下各滑动5次',self.browse_picker,1),
            ('选择一个文件确认并复制',self.copy_media,1),
            ('长按动态测试相册删除并全设备删除',self.delete_album,1),
            ('返回相册照片主界面',self.photos,1),
            ('滑动返回Home页',self.home,1),
        ]
