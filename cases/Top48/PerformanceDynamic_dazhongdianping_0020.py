"""推荐分类浏览；新版缺少推荐频道时使用同名分类入口。"""
import logging
import time

from Cases.Top48.PerformanceDynamic_dazhongdianping_0010 import PerformanceDynamic_dazhongdianping_0010


class PerformanceDynamic_dazhongdianping_0020(PerformanceDynamic_dazhongdianping_0010):
    def channel(self, label, marker):
        markers = (marker,) if isinstance(marker, str) else marker
        ready = lambda: all(self.has(text=m) for m in markers) and not self.on_home()
        message = '未进入{}频道'.format(label)
        # 优先使用推荐旁频道。用户允许新版缺失时替换为首页同名分类。
        candidates = [n for n in self.nodes(text=label)
                      if n.get('resource-id') != self.PACKAGE + ':id/tv_category_name']
        if self.has(text='推荐') and candidates:
            self.transition(lambda: self.click_node(candidates[0]), ready, message)
        else:
            logging.info('当前版本无推荐旁%s频道，替代为首页%s分类', label, label)
            self.return_to(self.on_home, '未回到大众点评首页')
            # 下滑恢复首页分类，不能把信息流里的同名文本当入口。
            for _ in range(6):
                if self.has(rid='tv_category_name', text=label):
                    break
                self.swipe(y1=.32, y2=.78)
                time.sleep(1)
            self.open_control(ready, message, rid='tv_category_name', text=label)
        self.wait_for(ready, message)

    def steps(self):
        return [
            ('启动大众点评', self.launch, 3),
            ('主页浏览，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击推荐旁边的美食', lambda: self.channel('美食', '美食餐厅'), 1),
            ('滑动浏览美食，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击推荐旁边的景点游玩', lambda: self.channel('景点游玩', '全部景点'), 1),
            ('滑动浏览出行，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击推荐旁边的休闲玩乐',
             lambda: self.channel('休闲玩乐', ('按摩足疗', '洗浴汗蒸', 'KTV')), 1),
            ('滑动浏览玩乐，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('返回大众点评主界面', self.app_home, 1),
            ('滑动返回Home页', self.home, 1),
        ]
