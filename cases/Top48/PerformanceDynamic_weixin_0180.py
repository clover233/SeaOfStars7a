"""同程旅行微信小程序浏览；用例表1844～1853行。"""
from Cases.Top48.weixin_remaining import WeixinRemainingCase


class PerformanceDynamic_weixin_0180(WeixinRemainingCase):
    def steps(self):
        return [
            ('启动微信', self.launch, 2),
            ('下滑调出最近小程序页面', self.recent_programs, 2),
            ('点击同程旅行订酒店机票火车汽车门票小程序，切换到同程旅行页面', self.tongcheng, 2),
            ('点击火车票查询，切换到火车票页面', self.train, 2),
            ('火车票页面浏览，上滑3次，下滑3次', self.browse_train, 2),
            ('点击右上角更多日期，切换到日期界面', self.train_date, 2),
            ('返回火车票页面', self.return_train, 2),
            ('返回同程旅行页面', self.return_tongcheng, 2),
            ('返回微信主界面', self.wechat_home, 2),
            ('滑动返回Home页', self.home, 2),
        ]
