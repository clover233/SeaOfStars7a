"""抖音长视频替代频道、经验和热点浏览（表格第 610～621 行）。"""
from Cases.Top48.douyin_common import DouyinDynamicCase


class PerformanceDynamic_douyin_0060(DouyinDynamicCase):
    all_app_package_list = [DouyinDynamicCase.PACKAGE]

    def long_video(self):
        return self.switch_top('长视频', substitutes=('精选',))

    def hot(self):
        self.return_feed()
        return self.switch_top('热点')

    def steps(self):
        return [
            ('启动抖音', self.launch, 3),
            ('点击长视频', self.long_video, 2),
            ('依次切换关注、团购、推荐，循环3次', self.cycle_channels, 1),
            ('再次点击长视频', self.long_video, 2),
            ('上滑3次、下滑3次浏览长视频', lambda: self.browse(3, 3), 0),
            ('返回推荐页面', lambda: self.switch_top('推荐'), 2),
            ('点击顶部经验', lambda: self.switch_top('经验'), 2),
            ('上滑3次、下滑3次浏览经验', lambda: self.browse(3, 3), 0),
            ('点击热点', self.hot, 2),
            ('上滑3次、下滑3次浏览热点', lambda: self.browse(3, 3), 0),
            ('返回抖音主界面', self.return_feed, 2),
            ('滑动返回Home页', self.home, 1),
        ]
