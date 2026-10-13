"""对应动态性能模型测试用例7.xlsx：哔哩哔哩 0030。"""
from Cases.Top48.bilibili_common import BilibiliDynamicCase


class PerformanceDynamic_bilibili_0030(BilibiliDynamicCase):
    def steps(self):
        return [
            ('启动哔哩哔哩', self.launch, 3),
            ('点击热门', lambda: self.channel('热门'), 1),
            ('上滑5次浏览热门页面', lambda: self.browse(up=5, down=0), 1),
            ('下滑5次浏览热门页面', lambda: self.browse(up=0, down=5), 1),
            ('点击一个视频播放', lambda: self.video(min_seconds=180), 1),
            ('点击屏幕调出菜单，点击全屏按钮', self.fullscreen, 1),
            ('观看10秒视频', self.playing_video, 10),
            ('双击暂停并输入弹幕还行', self.pause_and_type, 1),
            ('点击发送弹幕', self.send_danmaku, 1),
            ('双击继续观看5秒视频', self.resume_video, 5),
            ('侧滑退出全屏', self.exit_fullscreen, 1),
            ('点击评论', self.comments, 1),
            ('上滑5次浏览评论页面', lambda: self.browse(up=5, down=0), 1),
            ('下滑5次浏览评论页面', lambda: self.browse(up=0, down=5), 1),
            ('返回哔哩哔哩主界面', self.home, 1),
            ('滑动返回Home页', self.launcher_gesture, 1),
        ]
