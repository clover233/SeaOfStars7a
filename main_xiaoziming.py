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
from cases.Performace_jank_kpi_05_00000 import Performance_jank_kpi_05_000000
from cases.Performace_jank_kpi_05_00002 import Performance_jank_kpi_05_000002
from cases.Performace_jank_kpi_05_00001 import Performance_jank_kpi_05_000001
from cases.Performace_jank_kpi_05_00003 import Performance_jank_kpi_05_000003
from cases.Performace_jank_kpi_05_00006 import Performance_jank_kpi_05_000006
from cases.Performace_jank_kpi_05_00007 import Performance_jank_kpi_05_000007
from cases.Performace_jank_kpi_05_00010 import Performance_jank_kpi_05_000010
from cases.Performace_jank_kpi_05_00036 import Performance_jank_kpi_05_000036
from cases.Performace_jank_kpi_05_00052 import Performance_jank_kpi_05_000052
from cases.Performace_jank_kpi_05_00049 import Performance_jank_kpi_05_000049
from cases.Performace_jank_kpi_05_00017 import Performance_jank_kpi_05_000017
from cases.Performace_jank_kpi_05_00019 import Performance_jank_kpi_05_000019
from cases.Performace_jank_kpi_05_00039 import Performance_jank_kpi_05_000039
from cases.Performace_jank_kpi_05_00027 import Performance_jank_kpi_05_000027
from cases.Performace_jank_kpi_05_00004 import Performance_jank_kpi_05_000004
from cases.Performace_jank_kpi_05_00012 import Performance_jank_kpi_05_000012
from cases.Performace_jank_kpi_05_00013 import Performance_jank_kpi_05_000013
from cases.Performace_jank_kpi_05_00021 import Performance_jank_kpi_05_000021
from cases.Performace_jank_kpi_05_00022 import Performance_jank_kpi_05_000022
from cases.Performace_jank_kpi_05_00023 import Performance_jank_kpi_05_000023
from cases.Performace_jank_kpi_05_00024 import Performance_jank_kpi_05_000024
from cases.Performace_jank_kpi_05_00025 import Performance_jank_kpi_05_000025
from cases.Performace_jank_kpi_05_00026 import Performance_jank_kpi_05_000026
from cases.Performace_jank_kpi_05_00029 import Performance_jank_kpi_05_000029
from cases.Performace_jank_kpi_05_00030 import Performance_jank_kpi_05_000030
from cases.Performace_jank_kpi_05_00031 import Performance_jank_kpi_05_000031
from cases.Performace_jank_kpi_05_00032 import Performance_jank_kpi_05_000032
from cases.Performace_jank_kpi_05_00033 import Performance_jank_kpi_05_000033
from cases.Performace_jank_kpi_05_00034 import Performance_jank_kpi_05_000034
from cases.Performace_jank_kpi_05_00035 import Performance_jank_kpi_05_000035
from cases.Performace_jank_kpi_05_00037 import Performance_jank_kpi_05_000037
from cases.Performace_jank_kpi_05_00038 import Performance_jank_kpi_05_000038
from cases.Performace_jank_kpi_05_00039 import Performance_jank_kpi_05_000039
from cases.Performace_jank_kpi_05_00040 import Performance_jank_kpi_05_000040
from cases.Performace_jank_kpi_05_00041 import Performance_jank_kpi_05_000041
from cases.Performace_jank_kpi_05_00042 import Performance_jank_kpi_05_000042
from cases.Performace_jank_kpi_05_00043 import Performance_jank_kpi_05_000043
from cases.Performace_jank_kpi_05_00044 import Performance_jank_kpi_05_000044
from cases.Performace_jank_kpi_05_00045 import Performance_jank_kpi_05_000045
from cases.Performace_jank_kpi_05_00046 import Performance_jank_kpi_05_000046
from cases.Performace_jank_kpi_05_00047 import Performance_jank_kpi_05_000047
from cases.Performace_jank_kpi_05_00048 import Performance_jank_kpi_05_000048
from cases.Performace_jank_kpi_05_00049 import Performance_jank_kpi_05_000049
from cases.Performace_jank_kpi_05_00050 import Performance_jank_kpi_05_000050
from cases.Performace_jank_kpi_05_00052 import Performance_jank_kpi_05_000052

from cases.Performace_jank_kpi_05_00053 import Performance_jank_kpi_05_000053
from cases.Performace_jank_kpi_05_00054 import Performance_jank_kpi_05_000054
from cases.Performace_jank_kpi_05_00055 import Performance_jank_kpi_05_000055
from cases.Performace_jank_kpi_05_00056 import Performance_jank_kpi_05_000056
from cases.Performace_jank_kpi_05_00057 import Performance_jank_kpi_05_000057
from cases.Performace_jank_kpi_05_00058 import Performance_jank_kpi_05_000058
from cases.Performace_jank_kpi_05_00059 import Performance_jank_kpi_05_000059
from cases.Performace_jank_kpi_05_00062 import Performance_jank_kpi_05_000062



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
Basic0 = [
# Performance_jank_kpi_05_000000,
# Performance_jank_kpi_05_000001,
# Performance_jank_kpi_05_000002,
# Performance_jank_kpi_05_000003,
# Performance_jank_kpi_05_000004,
# Performance_jank_kpi_05_000006,
# Performance_jank_kpi_05_000007,
# Performance_jank_kpi_05_000010,
# Performance_jank_kpi_05_000012,
# Performance_jank_kpi_05_000013,
# Performance_jank_kpi_05_000017,
# Performance_jank_kpi_05_000019,
# Performance_jank_kpi_05_000021,
# Performance_jank_kpi_05_000022,
# Performance_jank_kpi_05_000029,
# Performance_jank_kpi_05_000032,
# Performance_jank_kpi_05_000033,
# Performance_jank_kpi_05_000034,
# Performance_jank_kpi_05_000035,
# Performance_jank_kpi_05_000036,
# Performance_jank_kpi_05_000037,
# Performance_jank_kpi_05_000038,
# Performance_jank_kpi_05_000039,
# Performance_jank_kpi_05_000040,
# Performance_jank_kpi_05_000041,
# Performance_jank_kpi_05_000042,
# Performance_jank_kpi_05_000045,
# Performance_jank_kpi_05_000046,
# Performance_jank_kpi_05_000047,
# Performance_jank_kpi_05_000049,
# Performance_jank_kpi_05_000050,
# Performance_jank_kpi_05_000052,
# Performance_jank_kpi_05_000054,
# Performance_jank_kpi_05_000055,
# Performance_jank_kpi_05_000056,
# Performance_jank_kpi_05_000057,
# Performance_jank_kpi_05_000058,
]
Basic1 = [
Performance_jank_kpi_05_000036,
Performance_jank_kpi_05_000038,
Performance_jank_kpi_05_000037,
Performance_jank_kpi_05_000021,
Performance_jank_kpi_05_000052,
Performance_jank_kpi_05_000052,
Performance_jank_kpi_05_000055,
Performance_jank_kpi_05_000054,
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000013,
Performance_jank_kpi_05_000041,
Performance_jank_kpi_05_000046,
Performance_jank_kpi_05_000042,
Performance_jank_kpi_05_000047,
Performance_jank_kpi_05_000037,
Performance_jank_kpi_05_000045,
Performance_jank_kpi_05_000046,
Performance_jank_kpi_05_000013,
Performance_jank_kpi_05_000033,
Performance_jank_kpi_05_000017,
Performance_jank_kpi_05_000034,
Performance_jank_kpi_05_000035,
Performance_jank_kpi_05_000052,
Performance_jank_kpi_05_000052,
]
Basic2=[
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000019,
Performance_jank_kpi_05_000010,
Performance_jank_kpi_05_000010,
Performance_jank_kpi_05_000010,
Performance_jank_kpi_05_000039,
Performance_jank_kpi_05_000036,
Performance_jank_kpi_05_000040,
Performance_jank_kpi_05_000042,
Performance_jank_kpi_05_000038,
Performance_jank_kpi_05_000042,
Performance_jank_kpi_05_000046,
Performance_jank_kpi_05_000047,
Performance_jank_kpi_05_000047,
Performance_jank_kpi_05_000042,
Performance_jank_kpi_05_000037,
Performance_jank_kpi_05_000037,
Performance_jank_kpi_05_000050,
Performance_jank_kpi_05_000058,
Performance_jank_kpi_05_000037,
Performance_jank_kpi_05_000037,
Performance_jank_kpi_05_000017,
Performance_jank_kpi_05_000021,
Performance_jank_kpi_05_000021,
Performance_jank_kpi_05_000022,
Performance_jank_kpi_05_000021,
Performance_jank_kpi_05_000021,
Performance_jank_kpi_05_000052,
Performance_jank_kpi_05_000055,
Performance_jank_kpi_05_000054,
]
Basic3=[

Performance_jank_kpi_05_000038,
Performance_jank_kpi_05_000036,
Performance_jank_kpi_05_000040,
Performance_jank_kpi_05_000037,
Performance_jank_kpi_05_000038,
Performance_jank_kpi_05_000036,
Performance_jank_kpi_05_000038,
Performance_jank_kpi_05_000040,
Performance_jank_kpi_05_000042,
Performance_jank_kpi_05_000047,
Performance_jank_kpi_05_000037,
Performance_jank_kpi_05_000042,
Performance_jank_kpi_05_000036,
Performance_jank_kpi_05_000038,
Performance_jank_kpi_05_000040,
Performance_jank_kpi_05_000019,
Performance_jank_kpi_05_000039,
Performance_jank_kpi_05_000052,
Performance_jank_kpi_05_000052,
Performance_jank_kpi_05_000017,
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000000,
Performance_jank_kpi_05_000001,
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000012,
# Performance_jank_kpi_05_000033,
# Performance_jank_kpi_05_000017,
# Performance_jank_kpi_05_000034,
# Performance_jank_kpi_05_000035,
# Performance_jank_kpi_05_000019,
# Performance_jank_kpi_05_000039,


]
Basic4=[
Performance_jank_kpi_05_000004,
Performance_jank_kpi_05_000002,
Performance_jank_kpi_05_000003,
Performance_jank_kpi_05_000036,
Performance_jank_kpi_05_000037,
Performance_jank_kpi_05_000038,
Performance_jank_kpi_05_000042,
Performance_jank_kpi_05_000045,
Performance_jank_kpi_05_000047,
Performance_jank_kpi_05_000004,
Performance_jank_kpi_05_000002,
Performance_jank_kpi_05_000002,
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000000,
Performance_jank_kpi_05_000002,
Performance_jank_kpi_05_000004,
Performance_jank_kpi_05_000004,
Performance_jank_kpi_05_000002,
Performance_jank_kpi_05_000056,
Performance_jank_kpi_05_000002,
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000003,
Performance_jank_kpi_05_000002,
Performance_jank_kpi_05_000002,
Performance_jank_kpi_05_000002,
Performance_jank_kpi_05_000003,
Performance_jank_kpi_05_000007,
Performance_jank_kpi_05_000002,
]
Basic5=[
Performance_jank_kpi_05_000036,
Performance_jank_kpi_05_000037,
Performance_jank_kpi_05_000038,
Performance_jank_kpi_05_000040,
Performance_jank_kpi_05_000042,
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000056,
Performance_jank_kpi_05_000057,
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000032,
Performance_jank_kpi_05_000058,
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000029,
Performance_jank_kpi_05_000006,
Performance_jank_kpi_05_000034,
Performance_jank_kpi_05_000056,
Performance_jank_kpi_05_000057,
Performance_jank_kpi_05_000049,
Performance_jank_kpi_05_000056,
Performance_jank_kpi_05_000057,
Performance_jank_kpi_05_000006,
Performance_jank_kpi_05_000007,
Performance_jank_kpi_05_000006,
]
Basics=[Basic1,Basic2,Basic3,Basic4,Basic5]
# Basics=[Basic0]
# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    """
    
    """
    result_dict = {'case_name':[],'success':[]}
    SeaOfStarsAW.init_device()
    # 抓trace
    # SeaOfStarsAW.start_trace_thread()
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
        for _ in range(1):
            for Basic in Basics:
                SeaOfStarsAW.start_21apps()
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
