"""七猫书架阅读；Excel 第 1216～1221 行。"""
from Cases.Top48.qimao_common import QimaoDynamicCase


class PerformanceDynamic_qimao_0010(QimaoDynamicCase):
    def steps(self):
        return [
            ('启动七猫免费小说', self.launch, 2),
            ('点击书架', self.bookshelf, 2),
            ('点击“狂飙”进入阅读', self.open_kuangbiao, 2),
            ('阅读页向左翻5页、向右翻5页', self.turn_pages, 0),
            ('返回七猫主界面', self.return_main, 2),
            ('滑动返回Home页', self.home, 2),
        ]
