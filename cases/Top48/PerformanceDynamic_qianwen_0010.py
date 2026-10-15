"""通义千问连续问答；Excel 第 1207～1215 行。"""
from Cases.Top48.qianwen_common import QianwenDynamicCase


class PerformanceDynamic_qianwen_0010(QianwenDynamicCase):
    def steps(self):
        return [
            ('启动通义千问', self.launch, 2),
            ('询问“什么是AI”', lambda: self.ask('什么是AI'), 2),
            ('浏览回答，上滑3次、下滑3次', lambda: self.browse(3, 3), 0),
            ('询问“华为终端的主要产品有哪些”',
             lambda: self.ask('华为终端的主要产品有哪些'), 2),
            ('浏览回答，上滑3次、下滑3次', lambda: self.browse(3, 3), 0),
            ('询问“介绍几款市面上主流的手机”',
             lambda: self.ask('介绍几款市面上主流的手机'), 2),
            ('浏览回答，上滑3次、下滑3次', lambda: self.browse(3, 3), 0),
            ('返回通义千问主界面', self.main_page, 2),
            ('滑动返回Home页', self.home, 2),
        ]
