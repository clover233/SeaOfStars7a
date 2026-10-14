"""番茄免费小说书架阅读场景；步骤对应 Excel 第 666–672 行。"""
import logging
import time

from Cases.Top48.fanqie_common import FanqieDynamicCase


class PerformanceDynamic_fanqie_0010(FanqieDynamicCase):
    BOOK_NAME = '长生不死'
    BOOK_TITLE_ID = 'jm4'

    def bookshelf(self):
        self.switch_bottom('书架')
        self.wait_for(lambda: bool(self.nodes(rid=self.BOOK_TITLE_ID)), '番茄书架未加载')

    def book_node(self):
        exact = self.nodes(text=self.BOOK_NAME, rid=self.BOOK_TITLE_ID)
        if exact:
            return exact[0]
        books = sorted(self.nodes(rid=self.BOOK_TITLE_ID), key=lambda node: self.bounds(node)[1])
        if not books:
            raise RuntimeError('书架没有可阅读的书籍')
        logging.warning('书架没有《%s》，改用《%s》完成阅读步骤', self.BOOK_NAME,
                        books[0].get('text'))
        return books[0]

    def open_book(self):
        book = self.book_node()
        title = book.get('text')
        self.transition(lambda: self.click_node(book),
                        lambda: self.has(text=title, rid='j9d') or self.has(rid='h21'),
                        '未进入《{}》阅读页'.format(title))

    def turn_pages(self):
        # 阅读页没有稳定的左右翻页控件，按屏幕比例执行横向翻页手势。
        for start, end in ((.82, .18), (.18, .82)):
            for _ in range(5):
                self.swipe(start, .5, end, .5, 320)
                time.sleep(1)

    def return_to_bookshelf(self):
        self.return_to(lambda: self.bottom_selected('书架') and
                       bool(self.nodes(rid=self.BOOK_TITLE_ID)),
                       '未返回番茄书架')

    def repeat_reading_twice(self):
        self.return_to_bookshelf()
        for index in range(2):
            self.open_book()
            self.turn_pages()
            if index == 0:
                self.return_to_bookshelf()

    def steps(self):
        return [
            ('启动番茄免费小说', self.launch, 3),
            ('首页浏览，上滑5次，下滑5次', lambda: self.browse(5, 5), 0),
            ('点击书架', self.bookshelf, 2),
            ('点击长生不死书籍，进入阅读书籍页面', self.open_book, 2),
            ('滑动阅读书籍，左翻页5次，右翻页5次', self.turn_pages, 0),
            ('返回主界面，步骤4和5重复执行2次', self.repeat_reading_twice, 1),
            ('滑动返回Home页', self.home, 1),
        ]
