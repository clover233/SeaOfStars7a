# 这是一个示例 Python 脚本。
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
from case_inst.Weixin_checktext import Weixin_checktext
from case_inst.Weixin_pyq import  Weixin_pyq
from case_inst.Weixin_pyq_video import Weixin_pyq_video
from case_inst.Xhs_scrolld import Xhs_scrolld
from case_inst.Xhs_scrolld_comment import Xhs_scrolld_comment
from case_inst.Xhs_clickfavor import Xhs_clickfavor
from case_inst.Xhs_changeinfo import Xhs_changeinfo
from case_inst.Taobao_search import Taobao_search
from case_inst.Taobao_checkgoods import Taobao_checkgoods
# from case_inst.Taobao_addshop import Taobao_addshop
from case_inst.Taobao_settlement import Taobao_settlement
from case_inst.Txvideo_tab import Txvideo_tab
from case_inst.Txvideo_scroll import Txvideo_scroll
from case_inst.Txvideo_search import Txvideo_search
from case_inst.Xhs_native import Xhs_native
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
Basic1 = [
Weixin_checktext

]

Basics=[Basic1]

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    result_dict = {'case_name':[],'success':[]}
    SeaOfStarsAW.init_device()
    SeaOfStarsAW.start_trace_thread()
    try:
        # for single_case in case_list:
        #     try:
        #         case = single_case(Result_Dir_Path)
        #         case.run_case()
        #         succ_num += 1
        #     except ElementNotFoundError as e:
        #         logging.error(e)
        #         fail_num += 1
        #        SeaOfStarsAW.stop_trace()
        # SeaOfStarsAW.start_21apps()
        for _ in range(1):
            for Basic in Basics:
                for single_case in Basic:
                    try:
                        case = single_case(Result_Dir_Path)
                        result_dict['case_name'].append(case)
                        case.set_up()
                        case.run_case()
                        # SeaOfStarsAW.write_results_to_excel('report.xlsx',str(single_case),'success')
                        time.sleep(8)

                        succ_num += 1
                        result_dict['success'].append('1')

                    except ElementNotFoundError as e:
                        logging.error(e)
                        result_dict['success'].append('0')
                        fail_num += 1
                        time.sleep(5)
                        SeaOfStarsAW.stop_trace()
                        SeaOfStarsAW.ut_device.app_terminate('com.tencent.xin')
                        SeaOfStarsAW.ut_device.app_terminate('com.taobao.taobao4iphone')
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
                        SeaOfStarsAW.ut_device.app_terminate('com.tencent.xin')
                        SeaOfStarsAW.ut_device.app_terminate('com.taobao.taobao4iphone')
                        SeaOfStarsAW.ut_device.app_terminate('com.alipay.iphoneclient')
                        SeaOfStarsAW.ut_device.app_terminate('com.jiangjia.gif')
                        SeaOfStarsAW.ut_device.app_terminate('com.hunantv.imgotv')
                        SeaOfStarsAW.ut_device.app_terminate('com.yueyou.cyreader')
                        SeaOfStarsAW.ut_device.app_terminate('com.tencent.live4iphone')
                        SeaOfStarsAW.ut_device.app_terminate('cn.xuexi.qg')
                    # except:
                        # SeaOfStarsAW.write_results_to_excel('report.xlsx', str(single_case), 'error')
                    finally:
                        SeaOfStarsAW.ut_device.home()
                        SeaOfStarsAW.swipe_to_launcher()
                        SeaOfStarsAW.go_home()
                        df = pd.DataFrame(result_dict)
                        df.to_excel(os.path.join(Result_Dir_Path,'result.xlsx'), index=False)
                        pass

    # except Exception:
    #     pass
    finally:
        logging.info('succ_num - ' + str(succ_num))
        logging.info('fail_num - ' + str(fail_num))
