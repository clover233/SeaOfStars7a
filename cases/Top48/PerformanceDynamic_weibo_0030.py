"""动态性能场景；Excel「新-7.0.2模型测试步骤」第 1577～1591 行。"""
from Cases.Top48.weibo_common import WeiboDynamicCase


class PerformanceDynamic_weibo_0030(WeiboDynamicCase):
    def launch(self):
        self._liked_by_case = False
        self._draft = False
        self.start()
        def ready():
            if self.has(text='跳过'):
                self.click(text='跳过')
            return self.main_ready() or self.detail_ready() or self.activity_has('MPDialogActivity')
        self.wait_for(ready, '微博启动广告未结束', timeout=30)
        if self.activity_has('MPDialogActivity'):
            self.back()
        self.return_to(self.main_ready, '微博主界面未打开', limit=6)
        self._visitor = self.activity_has('VisitorMainTabActivity')

    def main_page(self):
        # 表中要求返回主界面，并未要求切换首页；底部任一主 tab 均为主界面。
        self.return_to(self.main_ready, '未返回微博主界面', limit=8)

    def steps(self):
        return [
            ('启动微博', self.launch, 3),
            ('点击发现', self.discover, 1),
            ('点击更多热搜', self.hot_list, 2),
            ('热搜界面上滑5次下滑5次', lambda: self.browse(5, 5), 2),
            ('点击微博热搜第一条', self.first_hot, 3),
            ('点击第一条博文查看正文', self.first_post, 3),
            ('正文上滑5次下滑5次', lambda: self.browse(5, 5), 2),
            ('点赞', lambda: self.group('点赞', self.like), 1),
            ('取消本次点赞', lambda: self.within('点赞', self.unlike), 1),
            ('评论框输入评论', lambda: self.group('评论草稿', self.comment_draft), 2),
            ('取消评论返回正文', lambda: self.within('评论草稿', self.cancel_comment), 1),
            ('点击转发微博', lambda: self.group('转发草稿', self.repost_draft), 1),
            ('取消转发', lambda: self.within('转发草稿', self.cancel_repost), 2),
            ('返回微博主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 1),
        ]
