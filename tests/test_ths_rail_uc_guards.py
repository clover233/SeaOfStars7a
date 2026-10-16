"""自选股归属与失败前置条件保护，无设备连接。"""
import unittest
from unittest.mock import Mock
from Cases.Top48.observed_apps_common import StepUnavailable
from Cases.Top48.ths_common import ThsDynamicCase
from Cases.Top48.railway_common import RailwayDynamicCase

class ObservedGuardsTest(unittest.TestCase):
    def ths(self):
        c=object.__new__(ThsDynamicCase);c.unavailable={};c.click=Mock();c.stock_ready=Mock(return_value=True)
        return c

    def test_original_watch_is_not_removed(self):
        c=self.ths();c._watch_added=True;c._watch_original=True
        with self.assertRaises(StepUnavailable):c.remove_watch()
        c.click.assert_not_called()

    def test_missing_owned_watch_is_not_removed(self):
        c=self.ths();c._watch_added=False;c._watch_original=False
        with self.assertRaises(StepUnavailable):c.remove_watch()
        c.click.assert_not_called()

    def test_existing_watch_is_not_added_again(self):
        c=self.ths();c._watch_original=True
        with self.assertRaises(StepUnavailable):c.add_watch()
        c.click.assert_not_called()

    def test_unconfirmed_stock_is_not_added(self):
        c=self.ths();c._watch_original=False;c.stock_ready.return_value=False
        with self.assertRaises(StepUnavailable):c.add_watch()
        c.click.assert_not_called()

    def test_missing_ticket_results_does_not_sort_other_page(self):
        c=object.__new__(RailwayDynamicCase);c.unavailable={'tickets':'查询失败'};c.choose=Mock()
        with self.assertRaises(StepUnavailable):c.shortest()
        c.choose.assert_not_called()

    def test_duplicate_native_watch_nodes_have_one_state(self):
        c=self.ths();c.nodes=Mock(return_value=[{'text':'删自选'},{'text':'删自选'}])
        self.assertEqual(c.watch_label(),'删自选')

    def test_add_click_is_not_repeated(self):
        c=self.ths();c._watch_original=False;c._locators=set()
        c.watch_label=Mock(return_value='加自选');c.watch_is_added=Mock(return_value=True)
        c.content_wait=lambda predicate,message:self.assertTrue(predicate())
        c.add_watch()
        c.click.assert_called_once_with(rid='ll_add_remove_zixuan')
        self.assertTrue(c._watch_added)

if __name__=='__main__':unittest.main()
