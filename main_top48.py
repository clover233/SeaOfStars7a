import logging
import os
import shutil
import time
import logging
import openpyxl
import pandas as pd

from TraceTool import iTrace
from aw import SeaOfStarsAW
import wda
from aw import ElementNotFoundError

from case48.PerformanceDynamic_58city_0010 import PerformanceDynamic_58city_0010
from case48.PerformanceDynamic_58city_0020 import PerformanceDynamic_58city_0020
from case48.PerformanceDynamic_Alipay_0010 import PerformanceDynamic_Alipay_0010
from case48.PerformanceDynamic_Alipay_0020 import PerformanceDynamic_Alipay_0020
from case48.PerformanceDynamic_Alipay_0070 import PerformanceDynamic_Alipay_0070
# from case48.PerformanceDynamic_Appmarket_0010 import PerformanceDynamic_Appmarket_0010
# from case48.PerformanceDynamic_AttachedScreen_0020 import PerformanceDynamic_AttachedScreen_0020
from case48.PerformanceDynamic_AutoNavi_0010 import PerformanceDynamic_AutoNavi_0010
from case48.PerformanceDynamic_AutoNavi_0030 import PerformanceDynamic_AutoNavi_0030
from case48.PerformanceDynamic_AutoNavi_0040 import PerformanceDynamic_AutoNavi_0040
from case48.PerformanceDynamic_AutoNavi_0050 import PerformanceDynamic_AutoNavi_0050
from case48.PerformanceDynamic_AutoNavi_0060 import PerformanceDynamic_AutoNavi_0060
from case48.PerformanceDynamic_Baidu_0010 import PerformanceDynamic_Baidu_0010
from case48.PerformanceDynamic_Baidumap_0010 import PerformanceDynamic_Baidumap_0010
# from case48.PerformanceDynamic_Beiwanglu_0010 import PerformanceDynamic_Beiwanglu_0010
# from case48.PerformanceDynamic_Beiwanglu_0020 import PerformanceDynamic_Beiwanglu_0020
from case48.PerformanceDynamic_Bilibili_0020 import PerformanceDynamic_Bilibili_0020
from case48.PerformanceDynamic_Bilibili_0030 import PerformanceDynamic_Bilibili_0030
from case48.PerformanceDynamic_Bilibili_0040 import PerformanceDynamic_Bilibili_0040
from case48.PerformanceDynamic_Bilibili_0050 import PerformanceDynamic_Bilibili_0050
# from case48.PerformanceDynamic_Browser_0010 import PerformanceDynamic_Browser_0010
# from case48.PerformanceDynamic_Browser_0020 import PerformanceDynamic_Browser_0020
# from case48.PerformanceDynamic_Call_0010 import PerformanceDynamic_Call_0010
# from case48.PerformanceDynamic_Call_0020 import PerformanceDynamic_Call_0020
# 云闪付
# 大众点评
from case48.PerformanceDynamic_Dingding_0010 import PerformanceDynamic_Dingding_0010
from case48.PerformanceDynamic_Dingding_0020 import PerformanceDynamic_Dingding_0020
from case48.PerformanceDynamic_Dongchedi_0010 import PerformanceDynamic_Dongchedi_0010
from case48.PerformanceDynamic_Dongchedi_0020 import PerformanceDynamic_Dongchedi_0020
from case48.PerformanceDynamic_Douyin_0010 import PerformanceDynamic_Douyin_0010
from case48.PerformanceDynamic_Douyin_0030 import PerformanceDynamic_Douyin_0030
from case48.PerformanceDynamic_Douyin_0040 import PerformanceDynamic_Douyin_0040
from case48.PerformanceDynamic_Douyin_0050 import PerformanceDynamic_Douyin_0050
from case48.PerformanceDynamic_fanqie_0010 import PerformanceDynamic_fanqie_0010
from case48.PerformanceDynamic_fanqie_0020 import PerformanceDynamic_fanqie_0020
from case48.PerformanceDynamic_hanglvzongheng_0010 import PerformanceDynamic_hanglvzongheng_0010
from case48.PerformanceDynamic_hanglvzongheng_0020 import PerformanceDynamic_hanglvzongheng_0020
from case48.PerformanceDynamic_HappyAnimal_0010 import PerformanceDynamic_HappyAnimal_0010
from case48.PerformanceDynamic_hepingjingying_0030 import PerformanceDynamic_hepingjingying_0030
from case48.PerformanceDynamic_jingdong_0010 import PerformanceDynamic_jingdong_0010
from case48.PerformanceDynamic_jingdong_0020 import PerformanceDynamic_jingdong_0020
from case48.PerformanceDynamic_jingdong_0030 import PerformanceDynamic_jingdong_0030
from case48.PerformanceDynamic_jingdong_0040 import PerformanceDynamic_jingdong_0040
from case48.PerformanceDynamic_jrtt_0010 import PerformanceDynamic_jrtt_0010
from case48.PerformanceDynamic_jrtt_0020 import PerformanceDynamic_jrtt_0020
from case48.PerformanceDynamic_kiwi_0010 import PerformanceDynamic_kiwi_0010
from case48.PerformanceDynamic_kiwi_0020 import PerformanceDynamic_kiwi_0020
from case48.PerformanceDynamic_kiwi_0030 import PerformanceDynamic_kiwi_0030
from case48.PerformanceDynamic_Kuaishou_0010 import PerformanceDynamic_Kuaishou_0010
from case48.PerformanceDynamic_Kuaishou_0020 import PerformanceDynamic_Kuaishou_0020
from case48.PerformanceDynamic_mangguoTV_0010 import PerformanceDynamic_mangguoTV_0010
from case48.PerformanceDynamic_meituan_0010 import PerformanceDynamic_meituan_0010
from case48.PerformanceDynamic_pinduoduo_0010 import PerformanceDynamic_pinduoduo_0010
from case48.PerformanceDynamic_qimao_0010 import PerformanceDynamic_qimao_0010
from case48.PerformanceDynamic_qimao_0020 import PerformanceDynamic_qimao_0020
from case48.PerformanceDynamic_qiyi_0010 import PerformanceDynamic_qiyi_0010
from case48.PerformanceDynamic_qiyi_0020 import PerformanceDynamic_qiyi_0020
from case48.PerformanceDynamic_qiyi_0030 import PerformanceDynamic_qiyi_0030
from case48.PerformanceDynamic_qiyi_0060 import PerformanceDynamic_qiyi_0060
from case48.PerformanceDynamic_qiyi_0070 import PerformanceDynamic_qiyi_0070
from case48.PerformanceDynamic_qq_0010 import PerformanceDynamic_qq_0010
from case48.PerformanceDynamic_qq_0020 import PerformanceDynamic_qq_0020
from case48.PerformanceDynamic_qqliulanqi_0010 import PerformanceDynamic_qqliulanqi_0010
from case48.PerformanceDynamic_qqm_0010 import PerformanceDynamic_qqm_0010
from case48.PerformanceDynamic_qqm_0030 import PerformanceDynamic_qqm_0030
from case48.PerformanceDynamic_qunaer_0010 import PerformanceDynamic_qunaer_0010
from case48.PerformanceDynamic_qunaer_0020 import PerformanceDynamic_qunaer_0020
from case48.PerformanceDynamic_sodamusic_0010 import PerformanceDynamic_sodamusic_0010
from case48.PerformanceDynamic_taobao_0010 import PerformanceDynamic_taobao_0010
from case48.PerformanceDynamic_taobao_0020 import PerformanceDynamic_taobao_0020
from case48.PerformanceDynamic_tencentnews_0010 import PerformanceDynamic_tencentnews_0010
from case48.PerformanceDynamic_TencentVideo_0010 import PerformanceDynamic_TencentVideo_0010
from case48.PerformanceDynamic_ths_0040 import  PerformanceDynamic_ths_0040
from case48.PerformanceDynamic_ths_0050 import  PerformanceDynamic_ths_0050
from case48.PerformanceDynamic_tielu12306_0010 import PerformanceDynamic_tielu12306_0010
from case48.PerformanceDynamic_tielu12306_0020 import PerformanceDynamic_tielu12306_0020
from case48.PerformanceDynamic_UC_0010 import PerformanceDynamic_UC_0010
from case48.PerformanceDynamic_UC_0020 import PerformanceDynamic_UC_0020
from case48.PerformanceDynamic_wangzherongyao_0030 import PerformanceDynamic_wangzherongyao_0030
from case48.PerformanceDynamic_Weibo_0010 import PerformanceDynamic_Weibo_0010
from case48.PerformanceDynamic_Weibo_0020 import PerformanceDynamic_Weibo_0020
from case48.PerformanceDynamic_Weibo_0030 import PerformanceDynamic_Weibo_0030
from case48.PerformanceDynamic_Weibo_0040 import PerformanceDynamic_Weibo_0040
from case48.PerformanceDynamic_weipinhui_0010 import PerformanceDynamic_weipinhui_0010
from case48.PerformanceDynamic_weipinhui_0020 import PerformanceDynamic_weipinhui_0020
from case48.PerformanceDynamic_weipinhui_0030 import PerformanceDynamic_weipinhui_0030
# weixin 0010 需要大改，暂时不运行
# from case48.PerformanceDynamic_weixin_0010 import PerformanceDynamic_weixin_0010
from case48.PerformanceDynamic_weixin_0020 import PerformanceDynamic_weixin_0020
from case48.PerformanceDynamic_weixin_0050 import PerformanceDynamic_weixin_0050
from case48.PerformanceDynamic_weixin_0030 import PerformanceDynamic_weixin_0030
from case48.PerformanceDynamic_weixin_0070 import PerformanceDynamic_weixin_0070
from case48.PerformanceDynamic_weixin_0080 import PerformanceDynamic_weixin_0080
from case48.PerformanceDynamic_weixin_0090 import PerformanceDynamic_weixin_0090
from case48.PerformanceDynamic_weixin_0100 import PerformanceDynamic_weixin_0100
from case48.PerformanceDynamic_weixin_0110 import PerformanceDynamic_weixin_0110
from case48.PerformanceDynamic_wpsoffice_0010 import PerformanceDynamic_wpsoffice_0010
from case48.PerformanceDynamic_wpsoffice_0020 import PerformanceDynamic_wpsoffice_0020
from case48.PerformanceDynamic_xhs_0010 import PerformanceDynamic_xhs_0010
from case48.PerformanceDynamic_xhs_0020 import PerformanceDynamic_xhs_0020
from case48.PerformanceDynamic_xhs_0030 import PerformanceDynamic_xhs_0030
from case48.PerformanceDynamic_xhs_0040 import PerformanceDynamic_xhs_0040
from case48.PerformanceDynamic_xhs_0050 import PerformanceDynamic_xhs_0050
from case48.PerformanceDynamic_xianyu_0010 import PerformanceDynamic_xianyu_0010
from case48.PerformanceDynamic_xianyu_0020 import PerformanceDynamic_xianyu_0020
from case48.PerformanceDynamic_xiechengTrip_0010 import PerformanceDynamic_xiechengTrip_0010
from case48.PerformanceDynamic_xiechengTrip_0020 import PerformanceDynamic_xiechengTrip_0020
from case48.PerformanceDynamic_ximalaya_0010 import PerformanceDynamic_ximalaya_0010
from case48.PerformanceDynamic_ximalaya_0020 import PerformanceDynamic_ximalaya_0020
from case48.PerformanceDynamic_xuexiqiangguo_0010 import PerformanceDynamic_xuexiqiangguo_0010
from case48.PerformanceDynamic_xuexiqiangguo_0020 import PerformanceDynamic_xuexiqiangguo_0020
from case48.PerformanceDynamic_youku_0010 import PerformanceDynamic_youku_0010
from case48.PerformanceDynamic_youku_0020 import PerformanceDynamic_youku_0020
from case48.PerformanceDynamic_zhihu_0030 import PerformanceDynamic_zhihu_0030
from case48.PerformanceDynamic_zhongzai_0010 import PerformanceDynamic_zhongzai_0010
from case48.PerformanceDynamic_zhongzai_0020 import PerformanceDynamic_zhongzai_0020
from case48.PerformanceDynamic_zuoyebang_0010 import PerformanceDynamic_zuoyebang_0010
from case48.PerformanceDynamic_zuoyebang_0020 import PerformanceDynamic_zuoyebang_0020






Result_Dir_Path = os.path.join(os.getcwd(), 'Result', time.strftime("%Y%m%d_%H%M%S", time.localtime()))
if os.path.exists(Result_Dir_Path):
    shutil.rmtree(Result_Dir_Path)

os.makedirs(Result_Dir_Path)

# 配置log
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger('matplotlib.font_manager').disabled = True
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)
fh = logging.FileHandler(os.path.join(Result_Dir_Path, 'all_log.txt'), encoding='utf-8')
fh.setFormatter(formatter)
logger.addHandler(fh)


succ_num = 0
fail_num = 0
case_name_bundle_name = {
    "PerformanceDynamic_58city_0010":'com.taofang.iphone',
    "PerformanceDynamic_58city_0020":'com.taofang.iphone',
    "PerformanceDynamic_Alipay_0010":'com.alipay.iphoneclient',
    "PerformanceDynamic_Alipay_0020":'com.alipay.iphoneclient',
    "PerformanceDynamic_Alipay_0070":'com.alipay.iphoneclient',
    "PerformanceDynamic_Appmarket_0010":'com.apple.AppStore',
    # "PerformanceDynamic_AttachedScreen_0020":"com.android.systemui",
    "PerformanceDynamic_AutoNavi_0010":'com.autonavi.amap',
    "PerformanceDynamic_AutoNavi_0030":'com.autonavi.amap',
    "PerformanceDynamic_AutoNavi_0040":'com.autonavi.amap',
    "PerformanceDynamic_AutoNavi_0050":'com.autonavi.amap',
    "PerformanceDynamic_AutoNavi_0060":'com.autonavi.amap',
    "PerformanceDynamic_Baidu_0010":'com.baidu.BaiduMobile',
    "PerformanceDynamic_Baidumap_0010":'com.baidu.map',
    "PerformanceDynamic_Beiwanglu_0010":'com.apple.mobilenotes',
    "PerformanceDynamic_Beiwanglu_0020":'com.apple.mobilenotes',
    "PerformanceDynamic_Bilibili_0020":'tv.danmaku.bilianime',
    "PerformanceDynamic_Bilibili_0030":'tv.danmaku.bilianime',
    "PerformanceDynamic_Bilibili_0040":'tv.danmaku.bilianime',
    "PerformanceDynamic_Bilibili_0050":'tv.danmaku.bilianime',
    "PerformanceDynamic_Browser_0010":'com.apple.mobilesafari',
    "PerformanceDynamic_Browser_0020":'com.apple.mobilesafari',
    "PerformanceDynamic_Call_0010":'com.apple.mobilephone',
    "PerformanceDynamic_Call_0020":'com.apple.mobilephone',
    "PerformanceDynamic_Dingding_0010":'com.laiwang.DingTalk',
    "PerformanceDynamic_Dingding_0020":'com.laiwang.DingTalk',
    "PerformanceDynamic_Dongchedi_0010":"com.ss.ios.auto",
    "PerformanceDynamic_Dongchedi_0020":"com.ss.ios.auto",
    "PerformanceDynamic_Douyin_0010":"com.ss.iphone.ugc.Aweme",
    "PerformanceDynamic_Douyin_0030":"com.ss.iphone.ugc.Aweme",
    "PerformanceDynamic_Douyin_0040":"com.ss.iphone.ugc.Aweme",
    "PerformanceDynamic_Douyin_0050":"com.ss.iphone.ugc.Aweme",
    "PerformanceDynamic_fanqie_0010":"com.dragon.read",
    "PerformanceDynamic_fanqie_0020":"com.dragon.read",
    "PerformanceDynamic_hanglvzongheng_0010":'com.travelsky.umetrip',
    "PerformanceDynamic_hanglvzongheng_0020":'com.travelsky.umetrip',
    "PerformanceDynamic_HappyAnimal_0010":'com.happyelements.1OSAnimal',
    "PerformanceDynamic_hepingjingying_0030":'com.tencent.tmgp.pubgmhd',
    "PerformanceDynamic_jingdong_0010":"com.360buy.jdmobile",
    "PerformanceDynamic_jingdong_0020":"com.360buy.jdmobile",
    "PerformanceDynamic_jingdong_0030":"com.360buy.jdmobile",
    "PerformanceDynamic_jingdong_0040":"com.360buy.jdmobile",
    "PerformanceDynamic_jrtt_0010":'com.ss.iphone.article.News',
    "PerformanceDynamic_jrtt_0020":'com.ss.iphone.article.News',
    "PerformanceDynamic_kiwi_0010":"com.yy.kiwi",
    "PerformanceDynamic_kiwi_0020":'com.yy.kiwi',
    "PerformanceDynamic_kiwi_0030":'com.yy.kiwi',
    "PerformanceDynamic_Kuaishou_0010":'com.jiangjia.gif',
    "PerformanceDynamic_Kuaishou_0020":'com.jiangjia.gif',
    "PerformanceDynamic_pinduoduo_0010":"com.xunmeng.pinduoduo",
    "PerformanceDynamic_qimao_0010":"com.yueyou.cyreader",
    "PerformanceDynamic_qimao_0020":"com.yueyou.cyreader",
    "PerformanceDynamic_qiyi_0010":"com.qiyi.iphone",
    "PerformanceDynamic_qiyi_0020":"com.qiyi.iphone",
    "PerformanceDynamic_qiyi_0030":"com.qiyi.iphone",
    "PerformanceDynamic_qiyi_0060":"com.qiyi.iphone",
    "PerformanceDynamic_qiyi_0070":"com.qiyi.iphone",
    "PerformanceDynamic_qq_0010":"com.tencent.mqq",
    "PerformanceDynamic_qq_0020":"com.tencent.mqq",
    "PerformanceDynamic_qqliulanqi_0010":"com.tencent.mtt",
    "PerformanceDynamic_qqm_0010":"com.tencent.QQMusic",
    "PerformanceDynamic_qqm_0030":"com.tencent.QQMusic",
    "PerformanceDynamic_qunaer_0010":"com.qunar.iphoneclient8",
    "PerformanceDynamic_qunaer_0020":"com.qunar.iphoneclient8",
    "PerformanceDynamic_sodamusic_0010":"com.soda.music",
    "PerformanceDynamic_taobao_0010":"com.taobao.taobao4iphone",
    "PerformanceDynamic_taobao_0020":"com.taobao.taobao4iphone",
    "PerformanceDynamic_tencentnews_0010":"com.tencent.info",
    "PerformanceDynamic_TencentVideo_0010":"com.tencent.live4iphone",
    "PerformanceDynamic_ths_0040":"cn.com.10jqka.IHexin",
    "PerformanceDynamic_ths_0050":"cn.com.10jqka.IHexin",
    "PerformanceDynamic_tielu12306_0010":"cn.12306.rails12306",
    "PerformanceDynamic_tielu12306_0020":"cn.12306.rails12306",
    "PerformanceDynamic_UC_0010":"com.ucweb.iphone.lowversion",
    "PerformanceDynamic_UC_0020":"com.ucweb.iphone.lowversion",
    "PerformanceDynamic_wangzherongyao_0030":"com.tencent.smoba",
    "PerformanceDynamic_mangguoTV_0010":"com.hunantv.imgotv",
    "PerformanceDynamic_meituan_0010":'com.meituan.imeituan',
    "PerformanceDynamic_Weibo_0010":"com.sina.weibo",
    "PerformanceDynamic_Weibo_0020":"com.sina.weibo",
    "PerformanceDynamic_Weibo_0030":"com.sina.weibo",
    "PerformanceDynamic_Weibo_0040":"com.sina.weibo",
    "PerformanceDynamic_weipinhui_0010":"com.vipshop.iphone",
    "PerformanceDynamic_weipinhui_0020":"com.vipshop.iphone",
    "PerformanceDynamic_weipinhui_0030":"com.vipshop.iphone",
    "PerformanceDynamic_wpsoffice_0010":"com.kingsoft.www.office.wpsoffice",
    "PerformanceDynamic_wpsoffice_0020":"com.kingsoft.www.office.wpsoffice",
    "PerformanceDynamic_weixin_0010":"com.tencent.xin",
    "PerformanceDynamic_weixin_0020":"com.tencent.xin",
    "PerformanceDynamic_weixin_0050":"com.tencent.xin",
    "PerformanceDynamic_weixin_0030":"com.tencent.xin",
    "PerformanceDynamic_weixin_0070":"com.tencent.xin",
    "PerformanceDynamic_weixin_0080":"com.tencent.xin",
    "PerformanceDynamic_weixin_0090":"com.tencent.xin",
    "PerformanceDynamic_weixin_0100":"com.tencent.xin",
    "PerformanceDynamic_weixin_0110":"com.tencent.xin",
    "PerformanceDynamic_xhs_0010":"com.xingin.discover",
    "PerformanceDynamic_xhs_0020":"com.xingin.discover",
    "PerformanceDynamic_xhs_0030":"com.xingin.discover",
    "PerformanceDynamic_xhs_0040":"com.xingin.discover",
    "PerformanceDynamic_xhs_0050":"com.xingin.discover",
    "PerformanceDynamic_xianyu_0010":"com.taobao.fleamarket",
    "PerformanceDynamic_xianyu_0020":"com.taobao.fleamarket",
    "PerformanceDynamic_xiechengTrip_0010":"ctrip.com",
    "PerformanceDynamic_xiechengTrip_0020":"ctrip.com",
    "PerformanceDynamic_ximalaya_0010":"com.gemd.iting",
    "PerformanceDynamic_ximalaya_0020":"com.gemd.iting",
    "PerformanceDynamic_xuexiqiangguo_0010":"cn.xuexi.qg",
    "PerformanceDynamic_xuexiqiangguo_0020":"cn.xuexi.qg",
    "PerformanceDynamic_youku_0010":"com.youku.YouKu",
    "PerformanceDynamic_youku_0020":"com.youku.YouKu",
    "PerformanceDynamic_zhihu_0030":"com.zhihu.ios",
    "PerformanceDynamic_zhongzai_0010":["com.autonavi.amap","com.tencent.QQMusic","com.qiyi.iphone","com.youku.YouKu"],
    "PerformanceDynamic_zhongzai_0020":["com.autonavi.amap","com.tencent.QQMusic","com.qiyi.iphone","com.youku.YouKu"],
    "PerformanceDynamic_zuoyebang_0010":"com.baidu.homework",
    "PerformanceDynamic_zuoyebang_0020":"com.baidu.homework"
}
all_cases = [
    # PerformanceDynamic_58city_0010,
    # PerformanceDynamic_58city_0020,
    # PerformanceDynamic_Alipay_0010,
    # PerformanceDynamic_Alipay_0020,
    # PerformanceDynamic_Alipay_0070,
    # PerformanceDynamic_AutoNavi_0010,
    # PerformanceDynamic_AutoNavi_0030,
    # PerformanceDynamic_AutoNavi_0040,
    # PerformanceDynamic_AutoNavi_0050,
    # PerformanceDynamic_AutoNavi_0060,
    # PerformanceDynamic_Baidu_0010,
    # PerformanceDynamic_Baidumap_0010,
    # PerformanceDynamic_Bilibili_0020,
    # PerformanceDynamic_Bilibili_0030,
    # PerformanceDynamic_Bilibili_0040,
    PerformanceDynamic_Bilibili_0050,
    # 云闪付用例
    # 大众点评用例
    PerformanceDynamic_Dingding_0010,
    PerformanceDynamic_Dingding_0020,
    PerformanceDynamic_Dongchedi_0010,
    PerformanceDynamic_Dongchedi_0020,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_Douyin_0030,
    PerformanceDynamic_Douyin_0040,
    PerformanceDynamic_Douyin_0050,
    PerformanceDynamic_fanqie_0010,
    PerformanceDynamic_fanqie_0020,
    PerformanceDynamic_hanglvzongheng_0010,
    PerformanceDynamic_hanglvzongheng_0020,
    PerformanceDynamic_HappyAnimal_0010,
    PerformanceDynamic_hepingjingying_0030,
    PerformanceDynamic_jingdong_0010,
    PerformanceDynamic_jingdong_0020,
    PerformanceDynamic_jingdong_0030,
    PerformanceDynamic_jingdong_0040,
    PerformanceDynamic_jrtt_0010,
    PerformanceDynamic_jrtt_0020,
    PerformanceDynamic_kiwi_0010,
    PerformanceDynamic_kiwi_0020,
    PerformanceDynamic_kiwi_0030,
    PerformanceDynamic_Kuaishou_0010,
    PerformanceDynamic_Kuaishou_0020,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_qimao_0010,
    PerformanceDynamic_qimao_0020,
    PerformanceDynamic_qiyi_0010,
    PerformanceDynamic_qiyi_0020,
    PerformanceDynamic_qiyi_0030,
    PerformanceDynamic_qiyi_0060,
    PerformanceDynamic_qiyi_0070,
    PerformanceDynamic_qq_0010,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_qqliulanqi_0010,
    PerformanceDynamic_qqm_0010,
    PerformanceDynamic_qqm_0030,
    PerformanceDynamic_qunaer_0010,
    PerformanceDynamic_qunaer_0020,
    PerformanceDynamic_sodamusic_0010,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_taobao_0020,
    PerformanceDynamic_tencentnews_0010,
    PerformanceDynamic_TencentVideo_0010,
    PerformanceDynamic_ths_0040,
    PerformanceDynamic_ths_0050,
    PerformanceDynamic_tielu12306_0010,
    PerformanceDynamic_tielu12306_0020,
    PerformanceDynamic_UC_0010,
    PerformanceDynamic_UC_0020,
    PerformanceDynamic_wangzherongyao_0030,
    PerformanceDynamic_mangguoTV_0010,
    PerformanceDynamic_meituan_0010,
    PerformanceDynamic_Weibo_0010,
    PerformanceDynamic_Weibo_0020,
    PerformanceDynamic_Weibo_0030,

    PerformanceDynamic_Weibo_0040,
    PerformanceDynamic_weipinhui_0010,
    PerformanceDynamic_weipinhui_0020,
    PerformanceDynamic_weipinhui_0030,
    PerformanceDynamic_wpsoffice_0010,
    PerformanceDynamic_wpsoffice_0020,
    #PerformanceDynamic_weixin_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_weixin_0050,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_weixin_0090,
    PerformanceDynamic_weixin_0100,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_xhs_0010,
    PerformanceDynamic_xhs_0020,
    PerformanceDynamic_xhs_0030,
    PerformanceDynamic_xhs_0040,
    PerformanceDynamic_xhs_0050,
    PerformanceDynamic_xianyu_0010,
    PerformanceDynamic_xianyu_0020,
    PerformanceDynamic_xiechengTrip_0010,
    PerformanceDynamic_xiechengTrip_0020,
    PerformanceDynamic_ximalaya_0010,
    PerformanceDynamic_ximalaya_0020,
    PerformanceDynamic_xuexiqiangguo_0010,
    PerformanceDynamic_xuexiqiangguo_0020,
    PerformanceDynamic_youku_0010,
    PerformanceDynamic_youku_0020,
    PerformanceDynamic_zhihu_0030,
    PerformanceDynamic_zuoyebang_0010,
    PerformanceDynamic_zuoyebang_0020,
    PerformanceDynamic_zhongzai_0010,
    PerformanceDynamic_zhongzai_0020,
]
Basic1 = [
    # 今日头条在苹果17上运行用例卡顿严重
    # PerformanceDynamic_jrtt_0010,
    PerformanceDynamic_UC_0010,
    # PerformanceDynamic_Browser_0010,
    PerformanceDynamic_qqliulanqi_0010,
    PerformanceDynamic_fanqie_0010,
    PerformanceDynamic_qimao_0010,
    PerformanceDynamic_zhihu_0030,
    PerformanceDynamic_jrtt_0020,
    PerformanceDynamic_UC_0020,
    # PerformanceDynamic_Browser_0020,
    PerformanceDynamic_qqliulanqi_0010,
    PerformanceDynamic_fanqie_0020,
    PerformanceDynamic_Baidu_0010,
    PerformanceDynamic_zhihu_0030,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_AutoNavi_0010,
    PerformanceDynamic_ximalaya_0010,
    PerformanceDynamic_qqm_0010,
    PerformanceDynamic_weixin_0100,
    PerformanceDynamic_sodamusic_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_AutoNavi_0040,
    PerformanceDynamic_ximalaya_0020,
    PerformanceDynamic_qqm_0030,
    PerformanceDynamic_Douyin_0050,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_Weibo_0010,
    # PerformanceDynamic_weixin_0060,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_weixin_0090,
    # PerformanceDynamic_Launcher_0010,
    # PerformanceDynamic_AttachedScreen_0020,
    PerformanceDynamic_wpsoffice_0010,
    PerformanceDynamic_Dingding_0010,
    # PerformanceDynamic_Beiwanglu_0010,
    PerformanceDynamic_xuexiqiangguo_0010,
    # PerformanceDynamic_AttachedScreen_0020,
    PerformanceDynamic_wpsoffice_0020,
    PerformanceDynamic_Dingding_0020,
    # PerformanceDynamic_Beiwanglu_0020,
    # PerformanceDynamic_DHSouApp_0010,
    # PerformanceDynamic_baidu_0010,
    PerformanceDynamic_xuexiqiangguo_0020,
    # PerformanceDynamic_Launcher_0030,
    # PerformanceDynamic_splitscreen_0010,
    # PerformanceDynamic_Camera_0020,
    # PerformanceDynamic_Camera_0030,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_qiyi_0020,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_meituan_0010,
    PerformanceDynamic_weixin_0020,
    # PerformanceDynamic_Appmarket_0010,
    PerformanceDynamic_ths_0040,
    PerformanceDynamic_Dongchedi_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_Douyin_0020,
    PerformanceDynamic_zuoyebang_0010,
    PerformanceDynamic_kiwi_0010,
    # PerformanceDynamic_lockscreen_0010,
    PerformanceDynamic_mangguoTV_0010,
    # PerformanceDynamic_Photo_0030,
    PerformanceDynamic_weixin_0090,
    PerformanceDynamic_wangzherongyao_0030,
    PerformanceDynamic_hepingjingying_0030,
    PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_huaweiHealth_0020,
    PerformanceDynamic_tencentnews_0010,
    # PerformanceDynamic_didichuxing_0020,
    PerformanceDynamic_AutoNavi_0030,
    # PerformanceDynamic_Camera_0030,
    # PerformanceDynamic_weixin_0060,
    PerformanceDynamic_qiyi_0030,
    PerformanceDynamic_weixin_0050,
    PerformanceDynamic_weixin_0070,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_ths_0050,
    PerformanceDynamic_weixin_0020,
    # PerformanceDynamic_huaweiHealth_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_AutoNavi_0060,
    PerformanceDynamic_qq_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_zuoyebang_0020,
    # PerformanceDynamic_Camera_0030,
    # PerformanceDynamic_weixin_0060,
    PerformanceDynamic_zhongzai_0010
]
Basic2 = [
    # PerformanceDynamic_Launcher_0020,
    # PerformanceDynamic_Camera_0030,
    # PerformanceDynamic_Photo_0010,
    # PerformanceDynamic_Photo_AI_0010,
    PerformanceDynamic_xhs_0010,
    PerformanceDynamic_Weibo_0010,
    # PerformanceDynamic_DHDouyinjisu_0010,
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_Camera_0030,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_xhs_0030,
    PerformanceDynamic_Weibo_0020,
    PerformanceDynamic_xhs_0040,
    # PerformanceDynamic_Call_AI2_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_splitscreen_0010,
    # PerformanceDynamic_Launcher_0010,
    PerformanceDynamic_AutoNavi_0040,
    # PerformanceDynamic_Call_0020,
    # PerformanceDynamic_DHBaidutieba_0010,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_xhs_0050,
    # PerformanceDynamic_dazhongdianping_0010,
    # PerformanceDynamic_dazhongdianping_0020,
    # PerformanceDynamic_Photo_0030,
    # PerformanceDynamic_CloudFlashPay_0010,
    # PerformanceDynamic_Launcher_0020,
    PerformanceDynamic_weixin_0050,
    # PerformanceDynamic_Beiwanglu_AI_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_DHwukong_0010,
    PerformanceDynamic_Douyin_0050,
    PerformanceDynamic_pinduoduo_0010,
    PerformanceDynamic_taobao_0020,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_weipinhui_0030,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_58city_0020,
    PerformanceDynamic_xiechengTrip_0010,
    PerformanceDynamic_qunaer_0010,
    # PerformanceDynamic_Launcher_0010,
    PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_Beiwanglu_AI_0010,
    # PerformanceDynamic_weather_0010,
    # PerformanceDynamic_huaweiRiLi_0010,
    # PerformanceDynamic_DHshuiyinCamera_0010,
    # PerformanceDynamic_CloudFlashPay_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_qunaer_0020,
    PerformanceDynamic_xiechengTrip_0020,
    PerformanceDynamic_weixin_0050,
    # PerformanceDynamic_baidu_0010,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_weixin_0080,
    # PerformanceDynamic_Launcher_0020,
    # PerformanceDynamic_Photo_AI_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_Douyin_0030,
    PerformanceDynamic_TencentVideo_0010,
    # PerformanceDynamic_DHMiHome_0010,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_youku_0020,
    PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_bilibili_0030,
    PerformanceDynamic_Kuaishou_0020,
    PerformanceDynamic_kiwi_0010,
    PerformanceDynamic_wangzherongyao_0030,
    PerformanceDynamic_hepingjingying_0030,
    PerformanceDynamic_zhongzai_0010,
]
Basic3 = [
    # PerformanceDynamic_Launcher_0010,
    PerformanceDynamic_hanglvzongheng_0010,
    PerformanceDynamic_Alipay_0070,
    PerformanceDynamic_xhs_0010,
    PerformanceDynamic_AutoNavi_0050,
    PerformanceDynamic_weixin_0020,
    # PerformanceDynamic_huaweiRiLi_0020,
    # PerformanceDynamic_DHTesla_0010,
    # PerformanceDynamic_weather_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_tielu12306_0020,
    PerformanceDynamic_qunaer_0010,
    # PerformanceDynamic_weixin_0060,
    # PerformanceDynamic_baidumap_0010,
    PerformanceDynamic_weixin_0080,
    # PerformanceDynamic_Beiwanglu_AI_0030,
    # PerformanceDynamic_Launcher_0020,
    PerformanceDynamic_TencentVideo_0010,
    # PerformanceDynamic_DHwangyiyouxiangdashi_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_youku_0010,
    # PerformanceDynamic_Beiwanglu_AI_0020,
    # PerformanceDynamic_bilibili_0040,
    PerformanceDynamic_Kuaishou_0010,
    PerformanceDynamic_kiwi_0020,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_wangzherongyao_0030,
    PerformanceDynamic_hepingjingying_0030,
    # PerformanceDynamic_Douyin_0060,
    # PerformanceDynamic_Launcher_0010,
    PerformanceDynamic_Weibo_0030,
    PerformanceDynamic_jrtt_0020,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_DHdeepseek_0010,
    PerformanceDynamic_weipinhui_0010,
    PerformanceDynamic_Douyin_0030,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_Beiwanglu_AI_0020,
    PerformanceDynamic_weipinhui_0020,
    PerformanceDynamic_Weibo_0040,
    # PerformanceDynamic_jrtt_0010,
    PerformanceDynamic_jingdong_0040,
    # PerformanceDynamic_Photo_0030,
    # PerformanceDynamic_Launcher_0020,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_Douyin_0040,
    PerformanceDynamic_TencentVideo_0010,
    # PerformanceDynamic_DHcloudmusic_0010,
    PerformanceDynamic_mangguoTV_0010,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_youku_0020,
    # PerformanceDynamic_Photo_AI_0010,
    PerformanceDynamic_weixin_0050,
    # PerformanceDynamic_bilibili_0050,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_Kuaishou_0020,
    PerformanceDynamic_wangzherongyao_0030,
    PerformanceDynamic_hepingjingying_0030,
    # PerformanceDynamic_Launcher_0030,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_Douyin_0030,
    # PerformanceDynamic_DHSouApp_0010,
    PerformanceDynamic_TencentVideo_0010,
    PerformanceDynamic_youku_0010,
    # PerformanceDynamic_Beiwanglu_AI_0030,
    # PerformanceDynamic_bilibili_0020,
    PerformanceDynamic_TencentVideo_0010,
    # PerformanceDynamic_hwmovie_0020,
    # PerformanceDynamic_DHDouyinjisu_0010,
    PerformanceDynamic_mangguoTV_0010,
    PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_hwmovie_0010,
    PerformanceDynamic_Kuaishou_0020,
    PerformanceDynamic_zhongzai_0010,
]
Basic4 = [
    # PerformanceDynamic_Launcher_0010,
    PerformanceDynamic_xhs_0020,
    PerformanceDynamic_AutoNavi_0060,
    # PerformanceDynamic_Beiwanglu_AI_0040,
    # PerformanceDynamic_weixin_0060,
    # PerformanceDynamic_DHBaidutieba_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_didichuxing_0020,
    PerformanceDynamic_Douyin_0040,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_weixin_0110,
    PerformanceDynamic_qunaer_0010,
    PerformanceDynamic_tielu12306_0010,
    PerformanceDynamic_hanglvzongheng_0020,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_baidu_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_DHwukong_0010,
    PerformanceDynamic_jingdong_0010,
    # PerformanceDynamic_hwvmall_0010,
    PerformanceDynamic_Douyin_0040,
    PerformanceDynamic_taobao_0020,
    PerformanceDynamic_jingdong_0020,
    PerformanceDynamic_Alipay_0020,
    # PerformanceDynamic_Camera_0030,
    # PerformanceDynamic_Photo_0010,
    # PerformanceDynamic_meituxiuxiu_0010,
    PerformanceDynamic_xhs_0030,
    # PerformanceDynamic_DHshuiyinCamera_0010,
    # PerformanceDynamic_weixin_0010,
    # PerformanceDynamic_Camera_0030,
    PerformanceDynamic_Alipay_0070,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_Kuaishou_0010,
    # PerformanceDynamic_meituxiuxiu_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_Camera_0030,
    PerformanceDynamic_weixin_0080,
    # PerformanceDynamic_weixin_0060,
    # PerformanceDynamic_lockscreen_0010,
    # PerformanceDynamic_bilibili_0030,
    PerformanceDynamic_Kuaishou_0020,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_bilibili_0040,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_qiyi_0060,
    PerformanceDynamic_Kuaishou_0010,
    # PerformanceDynamic_DHMiHome_0010,
    # PerformanceDynamic_weixin_0060,
    PerformanceDynamic_Douyin_0030,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_Douyin_0020,
    PerformanceDynamic_weixin_0020,
    # PerformanceDynamic_weixin_0060,
    # PerformanceDynamic_DHTesla_0010,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_Call_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_qq_0020,
    PerformanceDynamic_weixin_0090,
    # PerformanceDynamic_Beiwanglu_AI_0010,
    # PerformanceDynamic_hwireader_0010,
    # PerformanceDynamic_Setting_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_weixin_0060,
    PerformanceDynamic_Alipay_0020,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_pinduoduo_0010,
    # PerformanceDynamic_DHwangyiyouxiangdashi_0010,
    PerformanceDynamic_taobao_0010,
    # PerformanceDynamic_Beiwanglu_AI_0020,
    PerformanceDynamic_Douyin_0050,
    # PerformanceDynamic_lockscreen_0010,
    PerformanceDynamic_Alipay_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_baidu_0010,
    PerformanceDynamic_jrtt_0020,
    PerformanceDynamic_Dongchedi_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_DHdeepseek_0010,
    # PerformanceDynamic_jrtt_0010,
    # PerformanceDynamic_Photo_AI_0010,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_Dongchedi_0020,
    # PerformanceDynamic_baidu_0010,
    PerformanceDynamic_weixin_0080,
    PerformanceDynamic_wangzherongyao_0030,
    PerformanceDynamic_Weibo_0020,
    PerformanceDynamic_hepingjingying_0030,
    PerformanceDynamic_weixin_0100,
    PerformanceDynamic_jrtt_0020,
    PerformanceDynamic_Douyin_0030,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_weixin_0060,
    # PerformanceDynamic_Beiwanglu_AI_0010,
    PerformanceDynamic_HappyAnimal_0010,
    PerformanceDynamic_Douyin_0040,
    PerformanceDynamic_qqm_0030,
    PerformanceDynamic_HappyAnimal_0010,
    # PerformanceDynamic_Douyin_0060,
    PerformanceDynamic_qimao_0020,
    PerformanceDynamic_Weibo_0030,
    PerformanceDynamic_mangguoTV_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_didichuxing_0020,
    # PerformanceDynamic_DHcloudmusic_0010,
    PerformanceDynamic_weixin_0050,
    # PerformanceDynamic_Launcher_0010,
    # PerformanceDynamic_mms_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_meituan_0090,
    # PerformanceDynamic_baidumap_0010,
    PerformanceDynamic_qunaer_0010,
    # PerformanceDynamic_Photo_0010,
    # PerformanceDynamic_Launcher_0020,
    PerformanceDynamic_zhongzai_0020,
]
Basic5 = [
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_qiyi_0070,
    PerformanceDynamic_Kuaishou_0020,
    # PerformanceDynamic_Beiwanglu_AI_0010,
    # PerformanceDynamic_DHSouApp_0010,
    # PerformanceDynamic_DHDouyinjisu_0010,
    PerformanceDynamic_Douyin_0040,
    PerformanceDynamic_qiyi_0010,
    # PerformanceDynamic_DHBaidutieba_0010,
    PerformanceDynamic_Kuaishou_0010,
    # PerformanceDynamic_DHwukong_0010,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_DHshuiyinCamera_0010,
    # PerformanceDynamic_Call_AI2_0010,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_jingdong_0030,
    # PerformanceDynamic_hwvmall_0020,
    # PerformanceDynamic_Douyin_0060,
    PerformanceDynamic_xianyu_0020,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_weixin_0050,
    PerformanceDynamic_jingdong_0040,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_Alipay_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_DHMiHome_0010,
    # PerformanceDynamic_Beiwanglu_AI_0030,
    # PerformanceDynamic_DHTesla_0010,
    # PerformanceDynamic_Appmarket_0010,
    # PerformanceDynamic_Photo_AI_0010,
    # PerformanceDynamic_Douyin_0070,
    # PerformanceDynamic_Launcher_0020,
    # PerformanceDynamic_DHwangyiyouxiangdashi_0010,
    PerformanceDynamic_qqm_0030,
    PerformanceDynamic_weixin_0070,
    # PerformanceDynamic_DHdeepseek_0010,
    PerformanceDynamic_tencentnews_0010,
    PerformanceDynamic_kiwi_0020,
    PerformanceDynamic_weixin_0100,
    PerformanceDynamic_xuexiqiangguo_0010,
    # PerformanceDynamic_hwireader_0010,
    # PerformanceDynamic_DHcloudmusic_0010,
    # PerformanceDynamic_Setting_0010,
    # PerformanceDynamic_DHSouApp_0010,
    # PerformanceDynamic_mms_0010,
    PerformanceDynamic_weixin_0020,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_Weibo_0040,
    PerformanceDynamic_weixin_0030,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_weixin_0050,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_Beiwanglu_AI_0020,
    # PerformanceDynamic_meituan_0080,
    PerformanceDynamic_Douyin_0040,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_Alipay_0010,
    # PerformanceDynamic_meituan_0080,
    # PerformanceDynamic_Beiwanglu_AI_0030,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_Camera_0030,
    # PerformanceDynamic_DHDouyinjisu_0010,
    # PerformanceDynamic_DHBaidutieba_0010,
    PerformanceDynamic_xhs_0040,
    # PerformanceDynamic_DHwukong_0010,
    # PerformanceDynamic_DHshuiyinCamera_0010,
    # PerformanceDynamic_DHMiHome_0010,
    # PerformanceDynamic_DHTesla_0010,
    PerformanceDynamic_Kuaishou_0020,
    # PerformanceDynamic_DHwangyiyouxiangdashi_0010,
    # PerformanceDynamic_DHdeepseek_0010,
    # PerformanceDynamic_DHcloudmusic_0010,
    # PerformanceDynamic_DHSouApp_0010,
    # PerformanceDynamic_theme_0010,
    PerformanceDynamic_Douyin_0010,
    # PerformanceDynamic_DHDouyinjisu_0010,
    # PerformanceDynamic_DHBaidutieba_0010,
    # PerformanceDynamic_Camera_0030,
    # PerformanceDynamic_DHwukong_0010,
    PerformanceDynamic_weixin_0080,
    # PerformanceDynamic_Setting_0010,
    # PerformanceDynamic_Photo_0010,
    # PerformanceDynamic_theme_0010,
    # PerformanceDynamic_Launcher_0020,
    # PerformanceDynamic_Beiwanglu_AI_0010,
    # PerformanceDynamic_DHshuiyinCamera_0010,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_weixin_0070,
    PerformanceDynamic_Douyin_0030,
    # PerformanceDynamic_weixin_0010,
    PerformanceDynamic_Kuaishou_0010,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_kiwi_0030,
    # PerformanceDynamic_Photo_0010,
    PerformanceDynamic_qqm_0030,
    # PerformanceDynamic_lockscreen_0010,
    # PerformanceDynamic_Beiwanglu_AI_0010,
    # PerformanceDynamic_Launcher_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_weixin_0050,
    # PerformanceDynamic_DHMiHome_0010,
    # PerformanceDynamic_Douyin_0020,
    PerformanceDynamic_taobao_0010,
    PerformanceDynamic_xianyu_0010,
    PerformanceDynamic_Alipay_0010,
    PerformanceDynamic_weixin_0030,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_meituan_0010,
    PerformanceDynamic_58city_0010,
    PerformanceDynamic_zhongzai_0020,
]
# Basics=[Basic1,Basic2,Basic3,Basic4,Basic5]
Basics=[Basic5,Basic4,Basic3,Basic2,Basic1]
# Basics=[Basic1]
test = [all_cases,]

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    result_dict = {'case_name':[],'success':[]}
    SeaOfStarsAW.init_device()
    SeaOfStarsAW.start_trace_thread()
    try:
        for _ in range(1):
            # for Basic in Basics:
            for Basic in Basics:
                print(Basic)
                # i = 1
                # print(f'basic{i}')
                # i =+ 1
                for single_case in Basic:
                    try:
                        case = single_case(Result_Dir_Path)
                        result_dict['case_name'].append(case)
                        case.set_up()
                        case.run_case()
                        time.sleep(3)

                        succ_num += 1
                        result_dict['success'].append('1')
                    except ElementNotFoundError as e:
                        logging.error(e)
                        result_dict['success'].append('0')
                        fail_num += 1
                        time.sleep(5)
                        SeaOfStarsAW.stop_trace()
                    except TypeError:
                        result_dict['success'].append('0')
                        time.sleep(5)
                        case = single_case(Result_Dir_Path)
                        case.set_up()
                        case.run_case()
                    except Exception as err:
                        result_dict['success'].append('0')
                        logging.error(err)
                        fail_num += 1
                        time.sleep(5)
                        SeaOfStarsAW.stop_trace()
                    finally:
                        # 初始化
                        try:
                            for i in range(5):
                                SeaOfStarsAW.ut_device.swipe_right()
                            for i in range(2):
                                SeaOfStarsAW.ut_device.swipe_left()
                        finally:
                            pass
                        SeaOfStarsAW.ut_device.home()

                        try:
                            bundle_name = case_name_bundle_name[single_case.__name__]
                            if type(bundle_name) == list:
                                for name in bundle_name:
                                    SeaOfStarsAW.ut_device.app_terminate(name)
                            else:
                                SeaOfStarsAW.ut_device.app_terminate(bundle_name)
                        except KeyError:
                            pass
                        finally:
                            pass
                        #SeaOfStarsAW.swipe_to_launcher()
                        #SeaOfStarsAW.go_home()
                        df = pd.DataFrame(result_dict)
                        df.to_excel(os.path.join(Result_Dir_Path,'result.xlsx'), index=False)
                        pass

    finally:
        logging.info('succ_num - ' + str(succ_num))
        logging.info('fail_num - ' + str(fail_num))
