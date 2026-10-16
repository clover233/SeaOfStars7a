"""动态性能场景；Excel「新-7.0.2模型测试步骤」第 1592～1609 行。"""
from Cases.Top48.weibo_common import WeiboDynamicCase


class PerformanceDynamic_weibo_0040(WeiboDynamicCase):
    def steps(self):
        return [
            ('启动微博', self.launch, 3),
            ('点击发现', self.discover, 1),
            ('点击搜索框', self.open_search, 1),
            ('输入动态测试', lambda: self.input_text('动态测试'), 2),
            ('点击搜索', self.submit_search, 2),
            ('点击用户', lambda: self.group('用户搜索', self.users_tab), 1),
            ('打开动态测试用户', lambda: self.group('目标用户', lambda: self.within('用户搜索', self.test_user)), 2),
            ('浏览第一条微博', lambda: self.within('目标用户', self.user_first_post), 2),
            ('返回微博首页', self.main_page, 2),
            ('点击右上角加号', lambda: self.group('发布菜单', self.compose_menu), 1),
            ('点击写微博', lambda: self.group('微博草稿', lambda: self.within('发布菜单', self.write_post)), 1),
            ('输入今天天气很好', lambda: self.within('微博草稿', lambda: self.input_text('今天天气很好')), 2),
            ('点击图片图标', lambda: self.group('选图', lambda: self.within('微博草稿', self.open_photos)), 1),
            ('选择9张图片', lambda: self.group('九张图片', lambda: self.within('选图', self.select_nine_photos)), 1),
            ('选图后点击下一步', lambda: self.group('图片预览', lambda: self.within('九张图片', self.photos_next)), 1),
            ('预览后点击下一步', lambda: self.within('图片预览', self.preview_next), 1),
            ('返回微博主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 1),
        ]
