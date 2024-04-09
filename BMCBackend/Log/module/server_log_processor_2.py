import datetime
import csv
import json
from drain3 import TemplateMiner  # 开源在线日志解析框架
from drain3.file_persistence import FilePersistence
from drain3.template_miner_config import TemplateMinerConfig


def match_template2(msg, template_miner, template_dic):
    cluster = template_miner.match(msg)  # 匹配模板，由开源工具提供
    if cluster and cluster.cluster_id in template_dic:
        return cluster.cluster_id




def number_to_string(num):
    num_str = str(num).zfill(4)
    result = 'AUGG' + num_str
    return result


def match_bmc_log_from_file(input_string, dic_list):  # 配合从文件读取字典使用

    # data2 = pd.read_csv("1.csv")

    config = TemplateMinerConfig()
    config.load('Log/module/drain3.ini')  ## 这个文件在drain3的github仓库里有
    config.profiling_enabled = False

    drain_file = 'comp_a_sellog'
    persistence = FilePersistence(drain_file + '.bin')
    template_miner = TemplateMiner(persistence, config=config)

    # ## 筛选模板
    template_dic = {}
    size_list = []
    for cluster in template_miner.drain.clusters:
        size_list.append(cluster.size)
    size_list = sorted(size_list, reverse=True)[:300]
    min_size = size_list[-1]

    for cluster in template_miner.drain.clusters:
        if cluster.size >= min_size:
            template_dic[cluster.cluster_id] = cluster.size

    #  temp_count_f = len(template_dic)

    collection = set()

    code = match_template2(input_string, template_miner, template_dic)
    collection.add(code)
    ce = dic_list[code - 1]
    code = number_to_string(code)

    return ce, code


def match_bmc_log_component(input_string):  # 获取log对应的部件
    flag_cpu = flag_psu = flag_mem = flag_disk = flag_pcie = flag_fan = 0

    if 'Processor' in input_string:
        flag_cpu = 1
    if 'Power Supply' in input_string:
        flag_psu = 1
    if 'Memory' in input_string:
        flag_mem = 1
    if 'Drive Slot' in input_string:
        flag_disk = 1
    if 'Critical Interrupt' in input_string:
        flag_pcie = 1
    if 'FAN' in input_string:
        flag_fan = 1

    if flag_cpu == 1 and flag_mem != 1:
        component = 'CPU'
    elif flag_cpu == 1 and flag_mem == 1:
        component = 'MEM'
    elif flag_mem == 1:
        component = 'MEM'
    elif flag_psu == 1:
        component = 'PSU'
    elif flag_disk == 1:
        component = 'DISK'
    elif flag_pcie == 1:
        component = 'PCIE'
    elif flag_fan == 1:
        component = 'FAN'
    else:
        component = 'OTHER'

    return component


def server_log_process(csv_file_path, message_column_name='msg', time_column_name='time'):
    # 从dict.txt加载日志模板字典
    file_dict = open('Log/module/dict.txt', 'r', encoding='utf-8')
    js = file_dict.read()
    dic = json.loads(js)
    dic_list = list(dic.values())
    file_dict.close()

    type = []
    message = []
    level = []
    code = []
    time_stamp = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            message.append(row[message_column_name].strip())
            dt = datetime.datetime.fromisoformat(row[time_column_name])
            time_stamp.append(dt)

    for msg in message:
        tmp_judge = match_bmc_log_from_file(msg, dic_list)
        level.append(tmp_judge[0])
        code.append(tmp_judge[1])
        type.append(match_bmc_log_component(msg))

    return type, message, level, code, time_stamp
