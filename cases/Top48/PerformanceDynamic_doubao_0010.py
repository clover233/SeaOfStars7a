"""豆包连续提问与答案浏览（表格第 492～499 行）。"""
from Cases.Top48.doubao_common import DoubaoDynamicCase


class PerformanceDynamic_doubao_0010(DoubaoDynamicCase):
    all_app_package_list = [DoubaoDynamicCase.PACKAGE]
    QUESTIONS = (
        '什么是AI',
        '华为终端的主要产品有哪些',
        '介绍几款市面上主流的手机',
    )

    def ask_question(self, question):
        self.ask(question)

    def steps(self):
        return [
            ('启动豆包', self.launch, 3),
            ('点击对话框，输入什么是AI', lambda: self.ask_question(self.QUESTIONS[0]), 3),
            ('浏览搜索结果，上滑3次、下滑3次', lambda: self.browse(3, 3), 0),
            ('点击对话框，输入华为终端的主要产品有哪些', lambda: self.ask_question(self.QUESTIONS[1]), 3),
            ('浏览搜索结果，上滑3次、下滑3次', lambda: self.browse(3, 3), 0),
            ('点击对话框，输入介绍几款市面上主流的手机', lambda: self.ask_question(self.QUESTIONS[2]), 3),
            ('浏览搜索结果，上滑3次、下滑3次', lambda: self.browse(3, 3), 0),
            ('滑动返回Home页', self.home, 1),
        ]
