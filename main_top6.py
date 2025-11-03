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

from case6.PerformanceDynamic_Alipay_0010 import PerformanceDynamic_Alipay_0010
from case6.PerformanceDynamic_Bilibili_0040 import PerformanceDynamic_Bilibili_0040
from case6.PerformanceDynamic_Douyin_0010 import PerformanceDynamic_Douyin_0010
from case6.PerformanceDynamic_jingdong_0010 import PerformanceDynamic_jingdong_0010
from case6.PerformanceDynamic_weixin_0090 import PerformanceDynamic_weixin_0090
from case6.PerformanceDynamic_xhs_0030 import PerformanceDynamic_xhs_0030

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
    "PerformanceDynamic_Alipay_0010":'com.alipay.iphoneclient',
    "PerformanceDynamic_Alipay_0020":'com.alipay.iphoneclient',
    "PerformanceDynamic_Alipay_0070":'com.alipay.iphoneclient',
    "PerformanceDynamic_Bilibili_0020":'tv.danmaku.bilianime',
    "PerformanceDynamic_Bilibili_0030":'tv.danmaku.bilianime',
    "PerformanceDynamic_Bilibili_0040":'tv.danmaku.bilianime',
    "PerformanceDynamic_Bilibili_0050":'tv.danmaku.bilianime',
    "PerformanceDynamic_Douyin_0010":"com.ss.iphone.ugc.Aweme",
    "PerformanceDynamic_Douyin_0030":"com.ss.iphone.ugc.Aweme",
    "PerformanceDynamic_Douyin_0040":"com.ss.iphone.ugc.Aweme",
    "PerformanceDynamic_Douyin_0050":"com.ss.iphone.ugc.Aweme",
    "PerformanceDynamic_jingdong_0010":"com.360buy.jdmobile",
    "PerformanceDynamic_jingdong_0020":"com.360buy.jdmobile",
    "PerformanceDynamic_jingdong_0030":"com.360buy.jdmobile",
    "PerformanceDynamic_jingdong_0040":"com.360buy.jdmobile",
    "PerformanceDynamic_jrtt_0010":'com.ss.iphone.article.News',
    "PerformanceDynamic_jrtt_0020":'com.ss.iphone.article.News',
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
}
all_cases = [
    PerformanceDynamic_Alipay_0010,
    PerformanceDynamic_Bilibili_0040,
    PerformanceDynamic_Douyin_0010,
    PerformanceDynamic_jingdong_0010,
    PerformanceDynamic_weixin_0090,
    PerformanceDynamic_xhs_0030,
]

Basics=[all_cases]


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
                        SeaOfStarsAW.ut_device.home()
                        try:
                            for i in range(5):
                                SeaOfStarsAW.ut_device.swipe_right()
                            for i in range(2):
                                SeaOfStarsAW.ut_device.swipe_left()
                        finally:
                            pass

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
