"""0020 的理财、测试聊天及设置操作。

默认使用用户确认的“测试账号”和相册前5张；可通过
ALIPAY_TEST_CONTACT、ALIPAY_TEST_PHOTOS 覆盖测试收件人和素材。
"""
import logging
import os
import re
import time
import xml.etree.ElementTree as ET

from Cases.Top48.alipay_common import AlipayCase, PACKAGE, PHOTO_ID


def bounds(node):
    return tuple(map(int, re.findall(r'\d+', node.get('bounds', ''))))


class AlipayMessageCase(AlipayCase):
    def set_up(self):
        self.contact = os.environ.get('ALIPAY_TEST_CONTACT', '测试账号').strip()
        raw_photos = os.environ.get('ALIPAY_TEST_PHOTOS', '1,2,3,4,5')
        try:
            self.photo_numbers = [int(value) for value in raw_photos.split(',')]
        except ValueError:
            self.photo_numbers = []
        if not self.contact or len(self.photo_numbers) != 5 or len(set(self.photo_numbers)) != 5 or min(self.photo_numbers) < 1:
            raise RuntimeError('0020 前置条件：配置 ALIPAY_TEST_CONTACT=准确联系人名，'
                               'ALIPAY_TEST_PHOTOS=五张允许发送的照片序号（如 1,2,3,4,5）')
        super().set_up()

    def open_steady(self):
        target = self.d(text='稳健理财', resourceId='com.alipay.android.widget.fortunehome:id/title')
        for _ in range(4):
            if target.exists:
                break
            self.swipe(False)
            time.sleep(1)
        self.tap(text='稳健理财', resource_id='com.alipay.android.widget.fortunehome:id/title')
        self.wait_for(lambda: self.d(text='稳健理财', resourceId='com.alipay.multiplatform.phone.xriver_integration:id/textView_title').exists,
                      '未打开稳健理财页')
        time.sleep(3)
        if not self.d(text='其他产品').exists:
            # 首次“金选·稳健升级”介绍弹层无可访问控件，实机关闭位置。
            for _ in range(2):
                self.relative_click(0.5, 0.814)
                time.sleep(1)
                if self.d(text='其他产品').exists:
                    break
        self.wait_for(lambda: self.d(text='其他产品').exists, '稳健理财内容未加载或首次介绍未关闭')

    def open_first_product(self):
        # 当前版本的热销区叫“大家都在买/一周热门榜”。从卡片容器读取产品名，
        # 避免推荐变化后仍点击旧名称，也排除屏幕右侧预加载的其他榜单。
        for _ in range(8):
            root = ET.fromstring(self.d.dump_hierarchy())
            for section in root.iter('node'):
                if section.get('class') == 'android.view.View' and section.get('text') in ('一周热门榜', '热销'):
                    candidates = [node for node in section.iter('node')
                                  if node.get('class') == 'android.widget.TextView' and node.get('text')]
                    # 实机容器的第一个文本为榜单说明，第二个为第一名产品名称。
                    if len(candidates) > 1:
                        product = candidates[1]
                        box = bounds(product)
                        width, height = self.d.window_size()
                        if len(box) == 4 and box[0] < width * 0.5 and height * 0.14 < box[1] < height * 0.85:
                            logging.info('打开热销第一款产品：%s', product.get('text'))
                            self.tap(text=product.get('text'))
                            self.wait_for(lambda: not self.d(text='稳健理财', resourceId='com.alipay.multiplatform.phone.xriver_integration:id/textView_title').exists,
                                          '点击后未进入理财产品页')
                            return
            self.swipe()
            time.sleep(1)
        raise RuntimeError('未找到热销/一周热门榜第一款理财产品，请检查当前版本布局')

    def message_plus(self):
        if not self.has_tabs():
            raise RuntimeError('点击消息+号前不在消息页')
        self.canvas_tap('+', (0.94, 0.085), 'AlipayLogin')
        self.wait_for(lambda: self.d(text='扫一扫').exists, '消息+号菜单未打开')

    def open_test_chat(self):
        if not self.has_tabs():
            raise RuntimeError('查找测试联系人前不在消息页')
        # 消息列表为 Canvas；通讯录暴露真实好友 id，避免误点全局搜索建议。
        self.canvas_tap('通讯录', (0.825, 0.085), 'AlipayLogin')
        self.wait_for(lambda: 'ContactMainPageActivity' in self.d.app_current()['activity'],
                      '未进入通讯录')
        result = self.d(text=self.contact, resourceId='com.alipay.mobile.socialcontactsdk:id/list_item_title')
        for _ in range(10):
            if result.exists:
                break
            self.swipe()
            time.sleep(0.5)
        if not result.exists or result.count != 1:
            raise RuntimeError('测试联系人未找到或不唯一：{}'.format(self.contact))
        result.click()
        self.wait_for(lambda: 'CSGAPushActivity' in self.d.app_current()['activity'],
                      '未进入已匹配测试账号的资料页')
        time.sleep(1)
        self.canvas_tap('发消息', (0.5, 0.94), 'CSGAPushActivity')
        self.wait_for(self.is_test_chat, '未进入指定测试联系人的聊天页')

    def is_test_chat(self):
        current = self.d.app_current()
        if current['package'] != PACKAGE or 'PersonalChatMsgActivity' not in current['activity']:
            return False
        return self.d(text=self.contact, resourceId='com.alipay.mobile.antui:id/title_text').exists

    def send_test_message(self):
        if not self.is_test_chat():
            raise RuntimeError('收件人校验失败，停止发送')
        edit = self.d(resourceId='com.alipay.mobile.chatapp:id/chat_msg_edit')
        if not edit.wait(timeout=8) or edit.count != 1:
            raise RuntimeError('未找到唯一的聊天输入框，请先完成测试账号聊天预置')
        edit.set_text('动态性能测试')
        self.tap(resource_id='com.alipay.mobile.chatapp:id/sendBtn', description='发送')
        self.wait_for(lambda: self.d(text='动态性能测试', resourceId='com.alipay.mobile.chatapp:id/chat_msg_text').exists,
                      '消息发送后未出现在聊天记录中')

    def chat_album(self):
        if not self.is_test_chat():
            raise RuntimeError('打开聊天图片前收件人校验失败')
        if not self.d(text='图片').exists:
            more = self.d(resourceId='com.alipay.mobile.chatapp:id/chat_stage_control_btn')
            if not more.exists:
                raise RuntimeError('未找到聊天更多按钮，请用测试账号核实当前版本聊天定位')
            more.click()
        self.tap(text='图片')
        self.wait_for(lambda: 'PhotoSelectActivity' in self.d.app_current()['activity'], '未打开聊天相册')

    def send_test_photos(self):
        if 'PhotoSelectActivity' not in self.d.app_current()['activity']:
            raise RuntimeError('当前不是聊天相册')
        initial = ET.fromstring(self.d.dump_hierarchy())
        if any(node.get('checked') == 'true' for node in initial.iter('node')):
            raise RuntimeError('相册已有勾选图片，请清空选择后重跑')
        selected = set()
        photo_order = {}
        for _ in range(15):
            root = ET.fromstring(self.d.dump_hierarchy())
            parents = {child: parent for parent in root.iter() for child in parent}
            for photo in root.iter('node'):
                if photo.get('resource-id') != PHOTO_ID:
                    continue
                match = re.match(r'照片(\d+)[，,]', photo.get('content-desc', ''))
                if not match:
                    continue
                # 相册编号混合视频和照片；按照片出现顺序计数，跳过视频。
                media_number = int(match.group(1))
                if media_number not in photo_order:
                    photo_order[media_number] = len(photo_order) + 1
                number = photo_order[media_number]
                if number not in self.photo_numbers or number in selected:
                    continue
                cell = parents[photo]
                checks = []
                for _ in range(3):
                    checks = [node for node in cell.iter('node') if node.get('checkable') == 'true']
                    if checks:
                        break
                    if cell not in parents:
                        break
                    cell = parents[cell]
                if len(checks) != 1:
                    raise RuntimeError('照片{}未暴露唯一勾选框，停止以避免误发'.format(number))
                checkbox = checks[0]
                if checkbox.get('checked') != 'true':
                    x1, y1, x2, y2 = bounds(checkbox)
                    self.d.click((x1 + x2) // 2, (y1 + y2) // 2)
                    time.sleep(0.3)
                selected.add(number)
            if len(selected) == 5:
                break
            self.swipe()
            time.sleep(0.5)
        if len(selected) != 5:
            raise RuntimeError('相册中未找到全部五张指定测试图片')
        root = ET.fromstring(self.d.dump_hierarchy())
        checked = [node for node in root.iter('node') if node.get('checked') == 'true']
        finish = self.d(resourceId='com.alipay.android.phone.wallet.beephoto:id/bt_finish')
        # 屏幕外勾选框可能不在层级中，完成按钮计数也可核实总选择数量。
        if not finish.exists or not (len(checked) == 5 or re.search(r'[（(]5(?:/\d+)?[）)]', finish.info.get('text', ''))):
            raise RuntimeError('无法确认恰好选择5张图片，停止发送')
        finish.click()
        self.wait_for(self.is_test_chat, '完成图片选择后未返回指定聊天页')

    def settings_entry(self, name):
        title_id = 'com.alipay.mobile.antui:id/title_text'
        if not self.d(text='设置', resourceId=title_id).exists:
            raise RuntimeError('当前不是设置页')
        ratios = {'新消息通知': (0.35, 0.412), '通用': (0.35, 0.652)}
        for _ in range(2):
            self.canvas_tap(name, ratios[name], 'CSPushActivity')
            if not self.d(text='设置', resourceId=title_id).exists:
                break
        self.wait_for(lambda: self.d(text=name, resourceId='com.alipay.multiplatform.phone.xriver_integration:id/textView_title').exists
                      or self.d(text=name, resourceId=title_id).exists, '未打开{}页'.format(name))

    def back_to_settings(self):
        self.d.press('back')
        self.wait_for(lambda: self.d(text='设置', resourceId='com.alipay.mobile.antui:id/title_text').exists,
                      '未返回设置页')
