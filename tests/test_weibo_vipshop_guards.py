"""评论/点赞和购物车身份隔离，不连接实机。"""
import unittest
from unittest.mock import Mock
import xml.etree.ElementTree as ET

from Cases.Top48.shopping_common import StepUnavailable
from Cases.Top48.weibo_common import WeiboDynamicCase
from Cases.Top48.vipshop_common import VipshopDynamicCase


class WeiboVipshopGuardsTest(unittest.TestCase):
    def test_guest_cannot_start_composer_or_like(self):
        case = object.__new__(WeiboDynamicCase)
        case._visitor = True
        case.main_page = Mock()
        case.click_node = Mock()
        with self.assertRaises(StepUnavailable):
            case.compose_menu()
        with self.assertRaises(StepUnavailable):
            case.like()
        case.main_page.assert_not_called()
        case.click_node.assert_not_called()

    def test_original_like_is_preserved(self):
        case = object.__new__(WeiboDynamicCase)
        case._visitor = False
        case.like_node = Mock(return_value=ET.Element('node'))
        case.click_node = Mock()
        with self.assertRaises(StepUnavailable):
            case.like()
        case.click_node.assert_not_called()

    def test_unlike_requires_a_like_from_this_run(self):
        case = object.__new__(WeiboDynamicCase)
        case.click_node = Mock()
        with self.assertRaises(StepUnavailable):
            case.unlike()
        case.click_node.assert_not_called()

    def test_missing_dependency_skips_child_action(self):
        case = object.__new__(WeiboDynamicCase)
        case._groups = {'用户搜索': False}
        action = Mock()
        with self.assertRaises(StepUnavailable):
            case.within('用户搜索', action)
        action.assert_not_called()

    def test_existing_cart_is_not_incremented(self):
        case = object.__new__(VipshopDynamicCase)
        case._product_title = '清风 测试商品'
        case.nodes = Mock(return_value=[ET.Element('node', text='3')])
        case.open_cart = Mock()
        case.label = Mock()
        with self.assertRaises(StepUnavailable):
            case.add_to_cart()
        case.open_cart.assert_not_called()
        case.label.assert_not_called()

    def test_identity_change_prevents_cart_deletion(self):
        case = object.__new__(VipshopDynamicCase)
        case._added_title = '本次商品'
        case._product_title = '其他商品'
        case.label = Mock()
        with self.assertRaises(StepUnavailable):
            case.delete_added_product()
        case.label.assert_not_called()

    def test_checkout_requires_verified_added_product(self):
        case = object.__new__(VipshopDynamicCase)
        case._added_title = None
        case.label = Mock()
        with self.assertRaises(StepUnavailable):
            case.checkout()
        case.label.assert_not_called()


if __name__ == '__main__':
    unittest.main()
