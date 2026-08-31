# -*- coding: utf-8 -*-
import logging
import os
import shutil
import time
from enum import Enum
from enum import unique
from uiautomator2 import Device
from aw import SeaOfStarsAW
from aw_new import SeaOfStarsAW

""" ----------------------------- 该文件无特殊情况，请不要修改！ -----------------------------
#!+======================================================================================
# 版权 (C) 海思半导体有限公司 2022 海思Kirin解决方案集成与验证部用户体验组
# Copyright (C) Hisilicon Technologies Co., Ltd. 2022. All rights reserved.
#========================================================================================
#   @FileName:      CaseBase.py
#   @Description:   该文件仅作为父类模块进行导入继承，不能直接使用，请在其子类中实现必要的接口！
#                   1、(必须实现)set_up      : 测试环境准备
#                   2、(必须实现)run_case    : 测试用例执行
#                   3、(必须实现)clean_up    : 测试环境恢复
#                   4、(选择实现)run_top20_backgroud    : 后台运行TOP20应用
#   @Author:        q00355607
#   @Date:          2023-04-28
#   @History:       created by q00355607 at 2023-04-28
#   @Environment:   Python3.7+
#!!======================================================================================
"""


class Case(object):
    """
    #====================================================================================
    #   @ClassName:     Case
    #   @Function:      星辰大海项目用例接口基类，为子类提供公共变量和方法
    #   @Author:        q00355607
    #   @History:       create at 2023-04-28
    #====================================================================================
    """
    CASE_SCENE_MAP =\
    {
        # "heavyLoad_1": ["meituan_coldlaunch", "pinduoduo_coldlaunch", "zhifubao_coldlaunch", "taobao_coldlaunch",
        #             "douyin_coldlaunch", "amap_coldlaunch", "qqbrow_coldlaunch", "wechat_coldlaunch", "kugou_coldlaunch",
        #             "jingdong_coldlaunch", "kuaishou_coldlaunch", "weibo_coldlaunch", "baidu_coldlaunch", "cloudmusic_coldlaunch",
        #             "aiqiyi_coldlaunch", "camera_coldlaunch", "tecentnews_coldlaunch", "icbc_coldlaunch", "chinamworld_coldlaunch",
        #             "huoshan_coldlaunch", "karaoke_coldlaunch", "autohome_coldlaunch", "anjuke_coldlaunch",
        #             "ctrip_coldlaunch", "qqlive_coldlaunch", "douyu_coldlaunch", "bili_coldlaunch", "youku_coldlaunch", "toutiao_coldlaunch"],
        "heavyLoad_1": ["meituan_coldlaunch", "pinduoduo_coldlaunch", "zhifubao_coldlaunch", "taobao_coldlaunch",
                        "douyin_coldlaunch", "amap_coldlaunch", "qqbrow_coldlaunch", "wechat_coldlaunch",
                        "kugou_coldlaunch",
                        "jingdong_coldlaunch", "kuaishou_coldlaunch", "weibo_coldlaunch", "baidu_coldlaunch",
                        "cloudmusic_coldlaunch",
                        "aiqiyi_coldlaunch", "camera_coldlaunch", "tecentnews_coldlaunch",
                        "chinamworld_coldlaunch",
                        "huoshan_coldlaunch", "karaoke_coldlaunch", "autohome_coldlaunch", "anjuke_coldlaunch",
                        "ctrip_coldlaunch", "qqlive_coldlaunch", "douyu_coldlaunch", "bili_coldlaunch",
                        "youku_coldlaunch", "toutiao_coldlaunch"],
        #1是应用冷启动的集合
        "heavyLoad_2": ["wechat_videoChat", "taobao_startup", "taobao_browse", "taobao_click_juhuasuan",
                        "xiaohongshu_startup", "xiaohongshu_browse", "xiaohongshu_click_focus", "jingdong_startup",
                        "jingdong_browse", "jingdong_click_buy"],
        #2是静态页面浏览类app动作的集合，包括滑动、视频通话、启动等
        "heavyLoad_3": ["douyin_startup", "douyin_browe_video", "toutiao_startup", "toutiao_browe_recommend",
                        "zhihu_startup", "zhihu_browe", "zhihu_click_hot", "wechat_startup",
                        "wechat_clickin_moments", "wechat_browe_moments"],
        "heavyLoad_4": ["amap_startup", "amap_search", "amap_navigation", "wechat_videoChat",
                        "amap_navigation", "wechat_search", "wechat_broweChat", "alipay_startup",
                        "alipay_openScan"],
        "heavyLoad_5": ["tecentVideo_startup", "tecentVideo_browe", "tecentVideo_click_fullScreen", "tecentVideo_play",
                        "bilibili_startup", "bilibili_click_live", "bilibili_livePlay", "aiqiyi_startup",
                        "aiqiyi_browe", "aiqiyi_click_search", "aiqiyi_click_fullScreen", "aiqiyi_play",
                        "youku_startup", "youku_browe", "youku_click_fullScreen", "youku_play"],
        "heavyLoad_6": [],
        "heavyLoad_10": ["douyin_videoSwitch", "douyin_browe_video", "douyin_browe_comment", "douyin_click_shoppingCart",
                        "qq_startup", "qq_browe_msg", "qq_click_Qzone", "qq_browe_Qzone",
                        "cloudMusic_startup", "cloudMusic_click_recommend", "weibo_startup", "weibo_browe",
                        "meituan_startup", "meituan_browe", "meituan_click_foods", "meituan_browe_foods",
                        "alipay_startup", "alipay_browe_reputation", "wechat_click_videoChannels", "wechat_browe_videoChannels"],
        # NPS测试用例涉及的app动作集合
        "NPS_scene_01": ["android_unlock", "android_desktop_browe", "taobao_startup", "taobao_click_maochao",  "taobao_browe"],
        "NPS_scene_02": ["wechat_coldlaunch", "douyin_coldlaunch", "toutiao_coldlaunch", "taobao_coldlaunch",
                         "meituan_coldlaunch", "camera_coldlaunch", "photos_coldlaunch", "telephone_coldlaunch",
                         "huaweibrower_coldlaunch", "huaweimusic_coldlaunch", "general"],
        "NPS_scene_03": ["cloudmusic_coldlaunch", "cloudmusic_click_playout", "cloudmusic_browe_back", "cloudmusic_warmstart",
                         "wechat_coldlaunch", "wechat_click_photo", "wechat_browe_photo", "wechat_browe_pyq", "general"],
        "NPS_scene_04": ["douyin_coldlaunch", "douyin_click_search", "douyin_browe", "douyin_warmstart",
                         "douyin_browe_back", "launch_unlock", "general"],
        "NPS_scene_05": ["camera_start_locked", "camera_click_front", "camera_click_takephoto", "camera_click_back", "general"],
        "NPS_scene_06": ["desktop_coldlaunch", "setup_click_level2", "setup_browe_wifi", "setup_click_hotspot", "setup_click_traffic",
                         "douyin_coldlaunch", "douyin_click_search", "douyin_browe", "douyin_browe_back", "general"],
        "NPS_scene_07": ["desktop_browe_globalresearch", "globalresearch_browe", "douyin_coldlaunch", "douyin_search",
                         "douyin_browe", "douyin_back", "general"],
        "NPS_scene_08": ["manager_coldlaunch", "manager_browe", "setup_coldlaunch", "setup_browe_storage", "general"],
        "NPS_scene_09": ["toutiao_coldlaunch", "toutiao_browe", "taobao_coldlaunch", "taobao_browe", "bilibili_coldlaunch",
                         "bilibili_browe", "general"],
        "NPS_scene_10": ["desktop_browe_multitask", "multitask_browe", "general"],
        "NPS_scene_11": ["toutiao_coldlaunch", "toutiao_click_search", "toutiao_browe_russia", "toutiao_click_zhuanti",
                         "toutiao_browe_news", "toutiao_click_videos", "toutiao_browe_videos", "baidu_coldlaunch", "baidu_click_up",
                         "baidu_browe_up", "baidu_click_videos", "baidu_browe_videos", "douyin_coldlaunch", "douyin_click_search",
                         "douyin_browe"],
        "NPS_scene_12": ["wechat_coldlaunch", "wechat_click_search", "wechat_click_account", "wechatmeituan_click_search",
                         "wechatmeituan_click_ui", "wechatxiecheng_click_search", "wechatxiecheng_click_account", "wechatxiecheng_click_follow",
                         "wechatxiecheng_click_ui", "wechatdidi_click_search", "wechatdidi_click_account", "wechatdidi_click_follow",
                         "wechatdidi_click_ui", "wechatfurong_click_search", "wechatfurong_click_account", "wechatfurong_click_follow", "wechatfurong_click_ui",
                         "wechatems_click_search", "wechatems_click_account", "wechatems_click_follow", "wechatems_click_ui",
                         "wechathosp_click_search", "wechathosp_click_account", "wechathosp_click_ui", "wechatpolic_click_search",
                         "wechatpolic_click_account", "wechatpolic_click_follow", "wechatpolic_click_ui", "wechatpolic_browe", "wechatcaijing_click_search",
                         "wechatcaijing_click_account", "wechatcaijing_browe"],
        "NPS_scene_13": ["tengxunnews_coldlaunch", "tengxunnews_browe", "tengxunnews_click_search", "tengxunnews_click_news",
                         "tengxunnews_browe_news", "tengxunnews_click_video", "tengxunnews_browe_video", "jingdong_coldlaunch",
                         "jingdong_browe", "jingdong_click_search", "jingdong_browe_search", "jingdong_click_commodity",
                         "jingdong_browe_commodity"],
        "NPS_scene_14": ["douyin_1_coldlaunch", "douyin_1_browe_blogger", "douyin_1_click_firstvideo", "douyin_2_coldlaunch",
                         "douyin_2_click_search", "douyin_3_coldlaunch", "douyin_3_click_search", "douyin_3_click_videolab",
                         "douyin_3_click_firstvideo", "douyin_3_click_review"],
        "NPS_scene_15": ["wechat_coldlaunch", "douyin_coldlaunch", "qq_coldlaunch", "taobao_coldlaunch",
                         "alipay_coldlaunch", "meituan_coldlaunch", "jingdong_coldlaunch", "weibo_coldlaunch",
                         "xhs_coldlaunch", "toutiao_coldlaunch"],
        "NPS_scene_16": ["wechat_warmstart", "douyin_warmstart", "qq_warmstart", "taobao_warmstart", "alipay_warmstart",
                         "meituan_warmstart", "jingdong_warmstart", "weibo_warmstart", "xhs_warmstart", "toutiao_warmstart"],
        "NPS_scene_17": ["wechat_coldlaunch", "wechat_click_search", "wechat_click_game", "wechat_click_joinsheep",
                         "douyin_coldlaunch", "douyin_click_search", "change_click_applet", "change_click_douyin"],
        "NPS_scene_18": ["wechat1_coldlaunch", "wechat1_click_chatting", "wechat1_click_send", "wechat1_click_photo",
                         "wechat1_click_sendphoto", "wechat2_warmstart", "wechat2_click_search", "wechat2_click_game",
                         "wechat2_click_relay", "wechat2_click_send"],
        "NPS_scene_19": ["douyin1_coldlaunch", "douyin1_click_search", "douyin1_click_video", "douyin1_click_play",
                         "douyin2_coldlaunch", "douyin2_click_search", "douyin2_click_play",  "douyin3_coldlaunch",
                         "douyin3_click_search", "douyin3_click_enter", "douyin3_click_share1", "douyin3_click_share2",
                         "douyin3_click_share3"],
        "NPS_scene_20": ["setting1_coldlaunch", "setting1_click_wlan", "setting2_coldlaunch", "setting2_click_wlan",
                         "setting3_coldlaunch", "setting3_click_web", "setting3_click_data", "setting4_coldlaunch",
                         "setting4_click_web", "setting4_click_data", "douyin_coldlaunch", "douyin_click_search"],
        "NPS_scene_21": ["systemUI_click_music", "douyin_coldlaunch", "douyin_click_search"],
        "NPS_scene_22": ["xhs1_coldlaunch", "xhs1_click_search", "xhs1_click_video", "xhs1_click_review",
                         "xhs1_click_blogger", "xhs1_click_livelab", "xhs1_click_livestudio", "xhs2_coldlaunch",
                         "xhs2_click_search", "xhs2_click_vedio", "xhs2_click_share", "xhs2_click_return"],
        "NPS_scene_23": ["kuaishou1_coldlaunch", "kuaishou1_click_search", "kuaishou1_click_video1", "kuaishou1_click_jingxuan",
                         "kuaishou1_click_find", "kuaishou1_click_me", "kuaishou1_click_follow", "kuaishou1_click_news",
                         "kuaishou1_click_video2", "kuaishou2_coldlaunch", "kuaishou2_click_search", "kuaishou2_click_friend",
                         "kuaishou2_click_return"],
        "NPS_scene_24": ["wechat1_coldlaunch", "wechat1_click_live", "wechat1_click_return", "wechat1_click_return",
                         "wechat2_coldlaunch", "wechat2_click_find", "wechat2_click_live", "wechat2_click_more",
                         "wechat2_click_search", "wechat2_click_count", "w echat2_click_video", "wechat2_click_return"],
        "NPS_scene_25": ["douyin1_coldlaunch", "douyin1_click_search", "douyin1_click_livetab", "douyin1_click_live",
                         "douyin2_coldlaunch", "douyin2_click_search", "douyin2_click_live"],
        "NPS_scene_26": ["bili1_coldlaunch", "bili1_click_livetab", "bili1_click_live", "wechat_coldlaunch",
                         "wechat1_click_chatting", "wechat1_click_send", "wechat1_click_photo", "wechat1_click_sendphoto",
                         "bili2_warmstart", "bili2_recomlab"],
        "NPS_scene_27": ["douyin1_coldlaunch", "douyin1_click_search", "douyin1_click_livetab", "douyin1_click_live",
                         "douyin2_coldlaunch", "douyin2_click_mall", "douyin2_click_search", "douyin2_click_commodity"],
        "NPS_scene_28": ["aqy1_coldlaunch", "aqy1_click_TV", "aqy1_click_all", "aqy1_click_free", "aqy1_click_play",
                         "aqy1_click_share", "aqy1_click_return", "wechat1_coldlaunch", "wechat1_click_chatting",
                         "wechat1_click_send", "wechat1_click_photo", "wechat1_click_sendphoto", "wechat2_coldlaunch",
                         "wechat2_click_chat", "wechat2_click_link", "aqy2_warmstart", "aqy2_click_videotab", "aqy2_click_hometab"],
        "NPS_scene_30": ["appstore1_coldlaunch", "appstore1_click_searchbox", "appstore1_click_search1", "appstore1_click_search2",
                         "appstore1_click_search3", "appstore1_click_search4", "appstore1_click_search5", "tomato1_coldlaunch",
                         "tomato1_click_searchbox", "tomato1_click_search", "tomato1_click_tab", "tomato1_click_green",
                         "tomato1_click_play", "wechat2_click_link", "camera_coldlaunch", "tomato2_warmstart",
                         "appstore2_warmstart", "appstore2_click_my", "appstore2_click_manage", "appstore3_warmstart",
                         "appstore3_click_my", "appstore3_click_manage", "appstore4_coldlaunch", "appstore4_click_my",
                         "appstore4_click_manage", "appstore4_click_searchbox"],
        "NPS_scene_31": ["jingdong1_coldlaunch", "jingdong1_click_searchbox", "jingdong1_click_search", "jingdong1_click_commodity",
                         "jingdong2_coldlaunch", "jingdong2_click_searchbox", "jingdong2_click_search", "jingdong2_click_commodity",
                         "jingdong2_click_review", "jingdong3_coldlaunch", "jingdong3_click_searchbox", "jingdong3_click_search",
                         "jingdong3_click_commodity", "jingdong3_click_shoppingcart", "jingdong3_click_account", "jingdong3_click_submit",],
        "NPS_scene_32": ["tengxun1_coldlaunch", "tengxun1_click_searchbox", "tengxun1_click_search", "tengxun1_click_play",
                         "tengxun1_click_fullscreen", "taobao_coldlaunch", "tengxun2_warmstart"]
    }

    # TOP20应用清单
    TOP20APP_LIST = ['com.baidu.searchbox',
                    'com.xunmeng.pinduoduo',
                    'com.tencent.mtt',
                    'com.tencent.mobileqq',
                    'com.sankuai.meituan',
                    'com.smile.gifmaker',
                    'com.eg.android.AlipayGphone',
                    'com.kugou.android',
                    'com.sina.weibo',
                    'com.tencent.news',
                    'com.youku.phone',
                    'com.alibaba.android.rimet',
                    'com.tencent.qqmusic',
                    'com.baidu.BaiduMap',
                    'com.achievo.vipshop',
                    'com.ss.android.article.lite',
                    'com.mt.mtxx.mtxx',
                    'com.ss.android.ugc.live',
                    'com.tmall.wireless',
                    'com.meitu.meiyancamera'
                     ]

    # TOP10应用清单
    # 微信，抖音，淘宝，支付宝，王者荣耀，今日头条，哔哩哔哩，快手，百度，小红书
    TOP10APP_LIST = ['com.tencent.mm',
                     'com.ss.android.ugc.aweme',
                     'com.taobao.taobao',
                     'com.eg.android.AlipayGphone',
                     'com.tencent.tmgp.sgame',
                     'com.ss.android.article.news',
                     'tv.danmaku.bili',
                     'com.smile.gifmaker',
                     'com.baidu.searchbox',
                     'com.xingin.xhs',
                     ]

    # TOP5应用清单
    # 微信，抖音，淘宝，支付宝，王者荣耀
    TOP5APP_LIST = ["com.tencent.mm",
                 "com.ss.android.ugc.aweme",
                 "com.taobao.taobao",
                 "com.eg.android.AlipayGphone",
                 "com.tencent.tmgp.sgame"]


    @SeaOfStarsAW.function_log
    def __init__(self,  result_path):
        time_stamp = time.strftime("%H%M%S", time.localtime())
        self.result_dir_path = os.path.join(result_path, self.__class__.__name__+'_'+time_stamp)
        self.trace_dir_path = os.path.join(self.result_dir_path, "Traces")
        self.screenshot_dir_path = os.path.join(self.result_dir_path, "Screenshots")
        SeaOfStarsAW.error_screen_shot_dir = os.path.join(result_path, "error_screenshots")
        SeaOfStarsAW.public_screen_shot_dir = os.path.join(result_path, "public_screenshots")
        if not os.path.exists(self.trace_dir_path):
            os.makedirs(self.trace_dir_path)
        if not os.path.exists(self.screenshot_dir_path):
            os.makedirs(self.screenshot_dir_path)
        if not os.path.exists(SeaOfStarsAW.public_screen_shot_dir):
            os.makedirs(SeaOfStarsAW.public_screen_shot_dir)
        if not os.path.exists(SeaOfStarsAW.error_screen_shot_dir):
            os.makedirs(SeaOfStarsAW.error_screen_shot_dir)
        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.fh = logging.FileHandler(os.path.join(self.result_dir_path, "log.txt"), encoding='utf-8')
        self.fh.setFormatter(formatter)
        logger.addHandler(self.fh)
        self.case_index = 0
    def set_up(self):
        raise NotImplementedError('请在子类中重写同名 set_up 方法')

    def run_case(self):
        raise NotImplementedError('请在子类中重写同名 run_case 方法')

    def clean_up(self):
        raise NotImplementedError('请在子类中重写同名 clean_up 方法')

    @SeaOfStarsAW.function_log
    def run_top20_backgroud(self):
        phone_app_list = SeaOfStarsAW.get_app_list()
        for per_app in self.TOP20APP_LIST:
            if per_app not in phone_app_list:
                return False
        for per_app in self.TOP20APP_LIST:
            logging.info("启动{}中".format(per_app))
            SeaOfStarsAW.ut_device.app_start(per_app, use_monkey=True)
            logging.info("间隔20s")
            time.sleep(20)
            SeaOfStarsAW.return_launcher()
            time.sleep(5)
        time.sleep(30)

    def get_perfetto_param(self, case_index=None, is_case_index_autoadd=True):
        if case_index is not None:
            self.case_index = case_index
        caseindex = self.case_index
        if is_case_index_autoadd:
            self.case_index += 1
        if caseindex + 1 < len(Case.CASE_SCENE_MAP[self.__class__.__name__]):
            next_scene = Case.CASE_SCENE_MAP[self.__class__.__name__][caseindex + 1]
        else:
            next_scene = Case.CASE_SCENE_MAP[self.__class__.__name__][-1]+"-LAST"
        return (self.trace_dir_path, self.__class__.__name__, Case.CASE_SCENE_MAP[self.__class__.__name__][caseindex],
                next_scene, self.screenshot_dir_path)

    @SeaOfStarsAW.function_log
    def run_top10_backgroud(self):
        phone_app_list = SeaOfStarsAW.get_app_list()
        for per_app in self.TOP10APP_LIST:
            if per_app not in phone_app_list:
                return False
        for per_app in self.TOP10APP_LIST:
            logging.info("启动{}中".format(per_app))
            SeaOfStarsAW.ut_device.app_start(per_app, use_monkey=True)
            logging.info("间隔20s")
            time.sleep(20)
            SeaOfStarsAW.return_launcher()
            time.sleep(5)
        time.sleep(30)

    @SeaOfStarsAW.function_log
    def run_top5_backgroud(self):
        phone_app_list = SeaOfStarsAW.get_app_list()
        for per_app in self.TOP5APP_LIST:
            if per_app not in phone_app_list:
                return False
        for per_app in self.TOP5APP_LIST:
            logging.info("启动{}中".format(per_app))
            SeaOfStarsAW.ut_device.app_start(per_app, use_monkey=True)
            logging.info("间隔20s")
            time.sleep(20)
            SeaOfStarsAW.return_launcher()
            time.sleep(5)
        time.sleep(30)