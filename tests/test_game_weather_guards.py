"""王者30秒驻留、天气城市切换和步骤结构的设备外检查。"""
import unittest
from unittest.mock import Mock, PropertyMock, patch
from importlib import import_module
from Cases.Top48.game_weather_common import HonorLaunchCase, WeatherDynamicCase
from Cases.Top48.travel_shop_common import TravelShopCase, StepUnavailable

class GameWeatherGuardsTest(unittest.TestCase):
    def setUp(self):
        p=patch.object(TravelShopCase,'d',new_callable=PropertyMock,return_value=Mock());p.start();self.addCleanup(p.stop)

    def test_game_launch_rejects_foreground_loss(self):
        c=object.__new__(HonorLaunchCase);c.launch=Mock();c.dismiss_system_prompt=Mock()
        c.current_app=Mock(return_value={'package':'other.app'})
        with self.assertRaises(StepUnavailable):c.launch_30()

    def test_game_runs_for_full_thirty_seconds(self):
        c=object.__new__(HonorLaunchCase);c.launch=Mock();c.dismiss_system_prompt=Mock()
        c.current_app=Mock(return_value={'package':c.PACKAGE});c.visible=Mock(return_value=False)
        now=[100.0]
        def advance(seconds):now[0]+=seconds
        with patch('Cases.Top48.game_weather_common.time.monotonic',side_effect=lambda:now[0]),patch('Cases.Top48.game_weather_common.time.sleep',side_effect=advance):
            c.launch_30()
        self.assertEqual(now[0]-100,30)

    def weather(self,count):
        c=object.__new__(WeatherDynamicCase);c.unavailable={};c.main_page=Mock();c.swipe=Mock()
        import xml.etree.ElementTree as E
        c.nodes=Mock(return_value=[E.Element('node',{'content-desc':f'北京，第1页，共{count}页'})])
        return c

    def test_single_city_does_not_pretend_switching(self):
        c=self.weather(1)
        with self.assertRaises(StepUnavailable):c.switch_cities()
        c.swipe.assert_not_called()

    def test_fifty_swipes_require_city_index_change(self):
        c=self.weather(6)
        with patch('Cases.Top48.game_weather_common.time.sleep'),self.assertRaises(StepUnavailable):c.switch_cities()
        self.assertEqual(c.swipe.call_count,50)

    def test_weather_home_requires_page_indicator_not_list_title(self):
        c=self.weather(6);c.activity_is=Mock(return_value=True);c.has=Mock(return_value=True)
        self.assertTrue(c.main_ready());c.nodes.return_value=[];self.assertFalse(c.main_ready())

    def test_all_requested_cases_have_expected_step_counts(self):
        for name,count in [('qunaer_0010',19),('qunaer_0020',14),('sodamusic_0010',12),('taobao_0010',17),('taobao_0020',15),('wangzherongyao_0030',2),('weather_0010',8)]:
            cls=getattr(import_module('Cases.Top48.PerformanceDynamic_'+name),'PerformanceDynamic_'+name)
            self.assertEqual(len(cls.steps(object.__new__(cls))),count,name)

if __name__=='__main__':unittest.main()
