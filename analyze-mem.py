import re
import xml.etree.ElementTree as ET
import os
import logging
import csv
import time

logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

logging.getLogger("matplotlib.font_manager").disabled = True
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

def parse_hitches_tick(tick_xml_path):
    total_time = 0
    if os.path.exists(tick_xml_path):
        dom = ET.parse(tick_xml_path)
        root = dom.getroot()
        row = root.findall(".//row")
        last_row = row[-1]
        total_time = last_row.findall("sample-time")[0].text
    else:
        logging.error("Trace有问题,{}未生成".format(tick_xml_path))
    return total_time

def parse_hitches_ca_commit(ca_commit_xml_path):
    ca_commit_result = []
    if os.path.exists(ca_commit_xml_path):
        dom = ET.parse(ca_commit_xml_path)
        root = dom.getroot()
        id_map = {}
        all_id = root.findall(".//*[@id]")
        for per_id in all_id:
            id_map[per_id.get("id")] = per_id
        row = root.findall(".//row")
        for per_row in row:
            result = {"start_time": "None", "start_time_value": -1, "process": ""}
            start_obj = per_row.findall("start-time")[0] if "id" in per_row.findall("start-time")[0].attrib.keys() else \
                id_map[per_row.findall("start-time")[0].attrib["ref"]]
            process_obj = per_row.findall("process")[0] if "id" in per_row.findall("process")[0].attrib.keys() else \
                id_map[per_row.findall("process")[0].attrib["ref"]]

            result["start_time"] = start_obj.attrib["fmt"]
            result["start_time_value"] = int(start_obj.text)

            result["process"] = "".join(process_obj.attrib["fmt"].split()[:-1])
            ca_commit_result.append(result)
    else:
        logging.error("Trace有问题,{}未生成".format(ca_commit_xml_path))
    return ca_commit_result

def parse_hitches_lifetime(hitches_life_time_xml_path):
    all_result = []
    if os.path.exists(hitches_life_time_xml_path):
        # 整理丢帧耗时
        dom = ET.parse(hitches_life_time_xml_path)
        root = dom.getroot()
        id_map = {}
        all_id = root.findall(".//*[@id]")
        for per_id in all_id:
            id_map[per_id.get("id")] = per_id
        row = root.findall(".//row")
        for per_row in row:
            result = {"start_time": "None", "start_time_value": -1, "end_time": "None", "end_time_value": -1,
                      "framelife_timeduration": -1}
            start_obj = per_row.findall("start-time")[0] if "id" in per_row.findall("start-time")[0].attrib.keys() else \
            id_map[per_row.findall("start-time")[0].attrib["ref"]]
            end_obj = per_row.findall("event-time")[-1] if "id" in per_row.findall("event-time")[-1].attrib.keys() else \
            id_map[per_row.findall("event-time")[-1].attrib["ref"]]

            result["start_time"] = start_obj.attrib["fmt"]
            result["start_time_value"] = int(start_obj.text)

            result["end_time"] = end_obj.attrib["fmt"]
            result["end_time_value"] = int(end_obj.text)

            result["framelife_timeduration"] = result["end_time_value"] - result["start_time_value"]
            all_result.append(result)
    else:
        logging.error("Trace有问题,{}未生成".format(hitches_life_time_xml_path))
    return all_result

def parse_all_xml(hitches_lifetime_xml_path, ca_commit_xml_path, tick_xml_path, log_txt_path):
    # 整理丢帧耗时
    all_result = parse_hitches_lifetime(hitches_lifetime_xml_path)
    ca_commit_result = parse_hitches_ca_commit(ca_commit_xml_path)
    tick_result = parse_hitches_tick(tick_xml_path)
    scene_result = parse_scene_log(log_txt_path)
    # 汇总
    for per_hitch in all_result:
        hitch_process = []
        for per_ca_commit in ca_commit_result:
            if per_hitch["start_time_value"] < per_ca_commit["start_time_value"] < per_hitch["end_time_value"]:
                if per_ca_commit["process"] not in hitch_process:
                    hitch_process.append(per_ca_commit["process"])
        per_hitch["process"] = hitch_process
        per_hitch["scene"] = ('None', 'None')
        for per_scene_tick in scene_result:
            per_scene_tick_float = float(per_scene_tick)
            if per_hitch["start_time_value"]/1e9 >= per_scene_tick_float:
                per_hitch["scene"] = scene_result[per_scene_tick]
        # if len(per_hitch["scene"]) < 2:
        #     print("per_hitch scene len < 2 :",hitches_lifetime_xml_path)
        #     print(per_hitch)
    return all_result, tick_result


def parse_scene_log(log_txt_path):
    all_result_dict = {}
    if os.path.exists(log_txt_path):
        with open(log_txt_path) as f:
            lines = f.read()
            re_result = re.findall("(\d+\.\d+)\s+:\s+\[(\S+)\]\[(\S+)\]", lines)
            for per_result in re_result:
                all_result_dict[per_result[0]] = per_result[1:]
    else:
        print(log_txt_path," not exit")
    return all_result_dict


# is_regen_xml 强制重新生成xml
def gen_xml(trace_file, is_regen_xml=False):
    """
    根据正则表达式，生成xml格式的文件
    :param trace_file:
    :param is_regen_xml:
    :return:
    """
    dir_name, full_file_name = os.path.split(trace_file)
    file_base_name, file_ext = os.path.splitext(full_file_name)

    input_file_path = trace_file
    #
    xpath_str = "'/trace-toc/run[@number=\"1\"]/data/table[@schema=\"hitches-lifetime-interval\"]'"
    # 
    output_hitches_lifetime_file_path = os.path.join(dir_name, file_base_name)+"_hitches_lifetime.xml"
    if os.path.exists(output_hitches_lifetime_file_path):
        logging.debug("xml文件已存在：{}".format(output_hitches_lifetime_file_path))
    if is_regen_xml or not os.path.exists(output_hitches_lifetime_file_path):
        xctrace_cmd = r"xctrace export --input {} --xpath {} --output {}".format(input_file_path, xpath_str, output_hitches_lifetime_file_path)
        xctrace_cmd = xctrace_cmd.replace("(","\\(")
        xctrace_cmd = xctrace_cmd.replace(")","\\)")
        logging.info("生成xml中...\n{}".format(xctrace_cmd))
        os.system(xctrace_cmd)


    xpath_str = "'/trace-toc/run[@number=\"1\"]/data/table[@schema=\"hitches-lifetime-interval\"]'"
    output_hitches_lifetime_file_path = os.path.join(dir_name, file_base_name)+"_hitches_lifetime.xml"
    if os.path.exists(output_hitches_lifetime_file_path):
        logging.debug("xml文件已存在：{}".format(output_hitches_lifetime_file_path))
    if is_regen_xml or not os.path.exists(output_hitches_lifetime_file_path):
        xctrace_cmd = r"xctrace export --input {} --xpath {} --output {}".format(input_file_path, xpath_str, output_hitches_lifetime_file_path)
        xctrace_cmd = xctrace_cmd.replace("(","\\(")
        xctrace_cmd = xctrace_cmd.replace(")","\\)")
        logging.info("生成xml中...\n{}".format(xctrace_cmd))
        os.system(xctrace_cmd)

    xpath_str = "'/trace-toc/run[@number=\"1\"]/data/table[@schema=\"hitches-ca-commit-interval\"]'"
    output_ca_commit_file_path = os.path.join(dir_name, file_base_name) + "_hitches_ca_commit.xml"
    if os.path.exists(output_ca_commit_file_path):
        logging.debug("xml文件已存在：{}".format(output_ca_commit_file_path))
    if is_regen_xml or not os.path.exists(output_ca_commit_file_path):
        xctrace_cmd = r"xctrace export --input {} --xpath {} --output {}".format(input_file_path, xpath_str,
                                                                                 output_ca_commit_file_path)
        xctrace_cmd = xctrace_cmd.replace("(", "\\(")
        xctrace_cmd = xctrace_cmd.replace(")", "\\)")
        logging.info("生成xml中...\n{}".format(xctrace_cmd))
        os.system(xctrace_cmd)

    xpath_str = "'/trace-toc/run[@number=\"1\"]/data/table[@schema=\"tick\"]'"
    tick_file_path = os.path.join(dir_name, file_base_name) + "_hitches_tick.xml"
    if os.path.exists(tick_file_path):
        logging.debug("xml文件已存在：{}".format(tick_file_path))
    if is_regen_xml or not os.path.exists(tick_file_path):
        xctrace_cmd = r"xctrace export --input {} --xpath {} --output {}".format(input_file_path, xpath_str,
                                                                                 tick_file_path)
        xctrace_cmd = xctrace_cmd.replace("(", "\\(")
        xctrace_cmd = xctrace_cmd.replace(")", "\\)")
        logging.info("生成xml中...\n{}".format(xctrace_cmd))
        os.system(xctrace_cmd)
    return full_file_name, output_hitches_lifetime_file_path, output_ca_commit_file_path, tick_file_path

def gen_result(all_trace_file):
    success_trace_count = 0
    all_hitches_result = []
    all_time_result = []
    for per_trace_file in all_trace_file:
        # 解析XML对应的Trace
        full_file_name, hitches_lifetime_xml_file, ca_commit_xml, tick_commit_xml = gen_xml(per_trace_file)
        scene_log_patch = os.path.join(os.path.split(per_trace_file)[0], os.path.splitext(full_file_name)[0]+".log")
        hitches_result, time_result = parse_all_xml(hitches_lifetime_xml_file, ca_commit_xml, tick_commit_xml, scene_log_patch)
        all_hitches_result.append({"file_name":full_file_name,"file_path":per_trace_file, "result":hitches_result})
        all_time_result.append({"file_name":full_file_name,"file_path":per_trace_file, "result":time_result})
        if len(hitches_result) > 0:
            success_trace_count += 1

    time_stamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    result_dir = os.path.join(os.getcwd(), "Result", "result_" + time_stamp)
    os.makedirs(result_dir)

    result_filename = os.path.join(result_dir, "result_all_hitches({}-{}).csv".format(success_trace_count, len(all_trace_file)))
    with open(result_filename, 'w', encoding='utf-8-sig') as f:
        csv_writer = csv.writer(f)
        # title = ["文件名", "帧耗时(ns)", "起始时间(相对值)", "结束时间(相对值)", "起始时间(绝对值)", "结束时间(绝对值)"]
        title = ["file_name", "scene_1", "scene_2", "process", "framelife_time(ns)", "start_time(relative)", "end_time(relative)", "start_time(absolute)", "end_time(absolute)", "file_path"]
        csv_writer.writerow(title)
        for per_trace in all_hitches_result:
            for per_hitch in per_trace["result"]:
                process_name = "".join(["["+i+"]" for i in per_hitch["process"]]) if len(per_hitch["process"]) > 0 else "None"
                csv_writer.writerow([per_trace["file_name"], per_hitch['scene'][0], per_hitch['scene'][1],
                                     process_name, per_hitch["framelife_timeduration"], per_hitch["start_time"],
                                     per_hitch["end_time"], per_hitch["start_time_value"], per_hitch["end_time_value"],
                                     "/".join(per_trace["file_path"].split("/")[-4:])])

    result_filename = os.path.join(result_dir, "time.csv")
    with open(result_filename, 'w', encoding='utf-8-sig') as f:
        csv_writer = csv.writer(f)
        total_time = 0
        title = ["file_name", "time(s)", "file_path"]
        csv_writer.writerow(title)
        for per_trace in all_time_result:
            total_time += int(per_trace["result"])
            csv_writer.writerow([per_trace["file_name"], format(int(per_trace["result"])/1e9, ".3f"), per_trace["file_path"]])
        csv_writer.writerow([])
        csv_writer.writerow(["total(min)", format(total_time/1e9/60, ".1f")])

    result_filename = os.path.join(result_dir, "result_hitches_ca_commit_filt.csv")
    with open(result_filename, 'w', encoding='utf-8-sig') as f:
        csv_writer = csv.writer(f)
        total_100ms_hitch = 0
        app_100ms_hitch = 0
        title = ["appname", "hitches_count","hitches_ratio"]
        csv_writer.writerow(title)
        app_100ms_map = {"None": 0, "AutomationModeUI": 0, "SpringBoard": 0}
        for per_trace in all_hitches_result:
            for per_hitch in per_trace["result"]:
                if per_hitch["framelife_timeduration"] >= 100*1e6:
                    total_100ms_hitch += 1
                    if len(per_hitch["process"]) > 0:
                        for per_process in per_hitch["process"]:
                            # SpringBoard单独 或者 仅SpringBoard、AutomationModeUI两个时计数
                            if per_process == "SpringBoard":
                                if ("AutomationModeUI" in per_hitch["process"] and len(per_hitch["process"]) == 2) or len(per_hitch["process"]) == 1:
                                    app_100ms_map["SpringBoard"] += 1
                                    app_100ms_hitch += 1
                                continue
                            # 仅AutomationModeUI单独
                            if per_process == "AutomationModeUI":
                                if len(per_hitch["process"]) == 1:
                                    app_100ms_map["AutomationModeUI"] += 1
                                    app_100ms_hitch += 1
                                continue
                            app_100ms_hitch += 1
                            if per_process in app_100ms_map.keys():
                                app_100ms_map[per_process] += 1
                            else:
                                app_100ms_map[per_process] = 1

                    else:
                        app_100ms_hitch += 1
                        app_100ms_map["None"] += 1
        app_100ms_list = sorted(app_100ms_map.items(), key=lambda x: x[1], reverse=True)
        for per_app in app_100ms_list:
            csv_writer.writerow([per_app[0], per_app[1], format(per_app[1]/app_100ms_hitch,".3f")])
        csv_writer.writerow([])
        csv_writer.writerow(["total_hitches", total_100ms_hitch])
        csv_writer.writerow(["app_total_hitches", app_100ms_hitch])

    result_filename = os.path.join(result_dir, "result_hitches_ca_commit_filt_repair.csv")
    with open(result_filename, 'w', encoding='utf-8-sig') as f:
        csv_writer = csv.writer(f)
        total_100ms_hitch = 0
        app_100ms_hitch = 0
        title = ["appname", "hitches_count", "hitches_ratio"]
        csv_writer.writerow(title)
        app_100ms_map = {"None": 0, "AutomationModeUI": 0, "SpringBoard": 0}
        for per_trace in all_hitches_result:
            pre_hitch = None
            for cur_hitch in per_trace["result"]:
                if cur_hitch["framelife_timeduration"] >= 100 * 1e6:
                    if pre_hitch is None or (cur_hitch["end_time_value"] - pre_hitch["end_time_value"]) >= 100*1e6:
                        pre_hitch = cur_hitch
                        total_100ms_hitch += 1
                        if len(cur_hitch["process"]) > 0:
                            for per_process in cur_hitch["process"]:
                                # SpringBoard单独 或者 仅SpringBoard、AutomationModeUI两个时计数
                                if per_process == "SpringBoard":
                                    if ("AutomationModeUI" in cur_hitch["process"] and len(
                                            cur_hitch["process"]) == 2) or len(cur_hitch["process"]) == 1:
                                        app_100ms_map["SpringBoard"] += 1
                                        app_100ms_hitch += 1
                                    continue
                                # 仅AutomationModeUI单独
                                if per_process == "AutomationModeUI":
                                    if len(cur_hitch["process"]) == 1:
                                        app_100ms_map["AutomationModeUI"] += 1
                                        app_100ms_hitch += 1
                                    continue
                                app_100ms_hitch += 1
                                if per_process in app_100ms_map.keys():
                                    app_100ms_map[per_process] += 1
                                else:
                                    app_100ms_map[per_process] = 1
                        else:
                            app_100ms_hitch += 1
                            app_100ms_map["None"] += 1
        app_100ms_list = sorted(app_100ms_map.items(), key=lambda x: x[1], reverse=True)
        for per_app in app_100ms_list:
            csv_writer.writerow([per_app[0], per_app[1], format(per_app[1] / app_100ms_hitch, ".3f")])
        csv_writer.writerow([])
        csv_writer.writerow(["total_hitches", total_100ms_hitch])
        csv_writer.writerow(["app_total_hitches", app_100ms_hitch])

    result_filename = os.path.join(result_dir, "result_hitches_scene_filt.csv")
    with open(result_filename, 'w', encoding='utf-8-sig') as f:
        csv_writer = csv.writer(f)
        total_100ms_hitch = 0
        title = ["scene_1", "scene_2", "hitches_count","hitches_ratio"]
        csv_writer.writerow(title)
        scene_100ms_map = {}
        for per_trace in all_hitches_result:
            pre_hitch = None
            for cur_hitch in per_trace["result"]:
                if cur_hitch["framelife_timeduration"] >= 100*1e6:
                    if pre_hitch is None or (cur_hitch["end_time_value"] - pre_hitch["end_time_value"]) >= 100 * 1e6:
                        pre_hitch = cur_hitch
                        total_100ms_hitch += 1
                        scene_key_name = ",".join(cur_hitch['scene'])
                        if scene_key_name in scene_100ms_map.keys():
                            scene_100ms_map[scene_key_name] += 1
                        else:
                            scene_100ms_map[scene_key_name] = 1
        scene_100ms_list = sorted(scene_100ms_map.items(), key=lambda x: x[1], reverse=True)
        for per_scene in scene_100ms_list:
            scene_name = per_scene[0].split(",")
            csv_writer.writerow([scene_name[0], scene_name[1], per_scene[1], format(per_scene[1]/total_100ms_hitch, ".3f")])
        csv_writer.writerow([])
        csv_writer.writerow(["total_hitches", total_100ms_hitch])

    logging.info("执行完成.")


def run(result_dir_path):
    all_trace_file = []
    for main_dir, dirs, file_name_list in os.walk(result_dir_path):
        if main_dir[-6:] == ".trace":
            all_trace_file.append(main_dir)
    all_trace_file.sort()
    gen_result(all_trace_file)

# run("/Users/kirintest/Documents/DynamicTraces/")
run("/Users/kirintest/Documents/PythonProject/SeaOfStar_IOS_Analyze_new/trace_test")