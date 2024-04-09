import copy
import datetime
import json
import csv
import tqdm
from Log.models import MemoryLog, PCIELog
from Log.module.server_log_processor_2 import match_bmc_log_component
from Log.module.util import match_bmc_log_from_file


# from django.utils.timezone import make_aware

# def server_log_process(csv_file_path, message_column_name='msg', time_column_name='time'):
#     message = []
#     level = []
#     time_stamp = []
#     with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             tmp = row[message_column_name].strip()
#             message.append(tmp)
#             # dt = make_aware(datetime.datetime.fromisoformat(row[time_column_name])) 不再使用时区
#             dt = datetime.datetime.fromisoformat(row[time_column_name])
#             time_stamp.append(dt)
#
#     for msg in message:
#         level.append(match_bmc_log(msg))
#
#     # with open('output.txt', 'w') as file:
#     #     for item in data_new:
#     #         file.write("%s\n" % item)
#     return time_stamp, message, level

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

    for msg in tqdm.tqdm(message):
        tmp_judge = match_bmc_log_from_file(msg, dic_list)
        level.append(tmp_judge[0])
        code.append(tmp_judge[1])
        type.append(match_bmc_log_component(msg))

    return type, message, level, code, time_stamp


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def memory_log_process(csv_file_path):
    record = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            t = copy.deepcopy(row)
            for k in t:
                if k == 'time':
                    continue
                t[k] = round(float(t[k]))
            t['datetime'] = datetime.datetime.fromisoformat(t['time'])
            del t['time']
            obj = MemoryLog(**t)
            record.append(obj)
    return record


def pcie_log_process(csv_file_path):
    record = []
    with (open(csv_file_path, newline='', encoding='utf-8') as csvfile):
        reader = csv.DictReader(csvfile)
        for row in reader:
            t = {}
            t["error_severity"] = row["Error Severity"]
            t["pcie_bus_error_type"] = row["PCIE Bus Error type"]
            t["receiver_id"] = row["Receiver ID"]
            t["vendor_id"] = row["VendorID"]
            t["device_id"] = row["DeviceID"]
            t["bus"] = row["Bus"]
            t["device"] = row["Device"]
            t["function"] = row["Function"]
            t['datetime'] = datetime.datetime.fromisoformat(row['time'])
            obj = PCIELog(**t)
            record.append(obj)
    return record
