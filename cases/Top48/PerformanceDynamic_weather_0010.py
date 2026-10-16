"""天气应用浏览；用例表1550～1557行。"""
from Cases.Top48.game_weather_common import WeatherDynamicCase


class PerformanceDynamic_weather_0010(WeatherDynamicCase):
    def steps(self):
        return [
            ('启动天气',self.launch,2),
            ('主页浏览，上下各滑动5次',self.browse_main,2),
            ('点击天气主页面左下方三点三线',self.cities,2),
            ('点击左上按钮，再返回（单击空白）',self.city_menu,2),
            ('主页浏览',self.browse_again,2),
            ('滑动切换不同城市，左滑5次，右滑5次，重复操作5次',self.switch_cities,2),
            ('返回天气主界面',self.main_page,2),
            ('滑动返回Home页',self.home,2),
        ]
