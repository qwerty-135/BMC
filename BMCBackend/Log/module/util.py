import datetime
from time import sleep

import pandas as pd
import numpy as np
import paramiko
from django.conf import settings

from drain3 import TemplateMiner  # 开源在线日志解析框架
from drain3.file_persistence import FilePersistence
from drain3.template_miner_config import TemplateMinerConfig


def match_template(df, template_miner, template_dic):
    msg = df.msg
    cluster = template_miner.match(msg)  # 匹配模板，由开源工具提供
    if cluster and cluster.cluster_id in template_dic:
        df['template_id'] = cluster.cluster_id  # 模板id
        df['template'] = cluster.get_template()  # 具体模板
    else:
        df['template_id'] = 'None'  # 没有匹配到模板的数据也会记录下来，之后也会用作一种特征。
        df['template'] = 'None'
    return df


def feature_generation(df_data, gap_list, model_name, log_source, win_list, func_list, len_template_dic):
    gap_list = gap_list.split(',')

    arr = np.arange(1, len_template_dic)

    dummy_col = ['template_id_' + str(x) for x in arr]

    for gap in gap_list:
        df_data['collect_time_gap'] = pd.to_datetime(df_data.collect_time).dt.ceil(gap)
        df_data = template_dummy(df_data)

        df_data = df_data.reset_index(drop=True)
        df_data = df_data.groupby(['sn', 'collect_time_gap']).agg(sum).reset_index()
        df_data = feature_win_fun(df_data, dummy_col, win_list, func_list, gap)
        df_data.to_pickle(
            'cpu_diag_comp_sel_log_all_feature_' + gap + '_' + win_list + '_' + func_list + '.pkl')  # 将构造好的特征数据存下来
        return df_data


def feature_generation_for_short(df_data, gap_list, model_name, log_source, win_list, func_list, len_template_dic):
    gap_list = gap_list.split(',')

    arr = np.arange(1, len_template_dic)

    dummy_col = ['template_id_' + str(x) for x in arr]

    for gap in gap_list:
        df_data['collect_time_gap'] = pd.to_datetime(df_data.collect_time).dt.ceil(gap)
        df_data = template_dummy_for_short(df_data, dummy_col)

        df_data = df_data.reset_index(drop=True)
        df_data = df_data.groupby(['sn', 'collect_time_gap']).agg(sum).reset_index()
        df_data = feature_win_fun(df_data, dummy_col, win_list, func_list, gap)
        df_data.to_pickle(
            'cpu_diag_comp_sel_log_all_feature_' + gap + '_' + win_list + '_' + func_list + '.pkl')  # 将构造好的特征数据存下来
        return df_data


def template_dummy_for_short(df, dummy_col):
    dfe = pd.DataFrame(0, index=range(len(df)), columns=dummy_col)

    for i in range(0, len(df)):
        dfe.loc[i, 'template_id_' + str(df['template_id'][i])] = 1

    df = pd.concat([df[['sn', 'collect_time_gap']], dfe], axis=1)
    return df


def template_dummy(df):
    df_dummy = pd.get_dummies(df['template_id'], prefix='template_id')
    df = pd.concat([df[['sn', 'collect_time_gap']], df_dummy], axis=1)
    return df


def feature_win_fun(df, dummy_col, win_list, func_list, gap):
    win_list = win_list.split(',')
    func_list = func_list.split(',')
    drop_col = ['sn']
    merge_col = ['collect_time_gap']
    df_out = df[drop_col + merge_col]

    for win in win_list:
        for func in func_list:
            df_feature = df.groupby(drop_col).apply(rolling_funcs, win, func, dummy_col)
            df_feature = df_feature.reset_index(drop=True).rename(columns=dict(zip(dummy_col, map(lambda x: x + '_' +
                                                                                                            func + '_' + win,
                                                                                                  dummy_col))))
            df_out = pd.concat([df_out, df_feature], axis=1)
    return df_out


def rolling_funcs(df, window, func, fea_col):
    df = df.sort_values('collect_time_gap')
    df = df.set_index('collect_time_gap')
    df = df[fea_col]

    df2 = df.rolling(str(window) + 'h')

    if func in ['sum']:
        df3 = df2.apply(sum_func)
    else:
        print('func not existed')
    return df3


def sum_func(series):
    return sum(series)


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

    persistence = FilePersistence('Log/module/comp_a_sellog.bin')
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

    flag_cpu = flag_psu = flag_mem = flag_disk = flag_pcie = flag_fan = flag_intrusion = flag_os = flag_acpi = flag_boot = flag_lan = 0

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
    if 'Intrusion' in input_string:
        flag_intrusion = 1
    if 'OS Status' in input_string:
        flag_os = 1
    if 'ACPI' in input_string:
        flag_acpi = 1
    if 'Boot' in input_string:
        flag_boot = 1
    if 'LAN' in input_string:
        flag_lan = 1

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
    elif flag_intrusion == 1:
        component = 'INTRUSION'
    elif flag_os == 1:
        component = 'OS'
    elif flag_acpi == 1:
        component = 'ACPI'
    elif flag_boot == 1:
        component = 'BOOT'
    elif flag_lan == 1:
        component = 'LAN'



    else:
        component = 'ANOTHER'

    return component


def server_query():
    host = settings.SERVER_HOST
    port = settings.SERVER_PORT
    username = settings.SERVER_USER_NAME
    password = settings.SERVER_PASSWORD
    data_path = "./data/server_log/query/"

    file = open(data_path + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt", "w", encoding="utf-8")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        t = paramiko.Transport((host, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)

        # Rasdaemon
        file.write("Rasdaemon\n")
        ssh.connect(hostname=host, port=port, username=username, password=password)
        result = ssh.exec_command("ras-mc-ctl --summary")
        file.write(result[1].read().decode('utf-8') + "\n")
        # Smartmontools
        file.write("Smartmontools\n")
        result = ssh.exec_command("sudo smartctl -s on -a /dev/sda", get_pty=True)
        result[0].write("ssm010407" + '\n')
        file.write(result[1].read().decode('utf-8') + "\n")
        # MCELog
        file.write("MCELog\n")
        result = ssh.exec_command("mcelog")
        file.write(result[1].read().decode('utf-8') + "\n")
        # IPMITools
        file.write("IPMITools\n")
        result = ssh.exec_command("ipmitool")
        file.write(result[1].read().decode('utf-8') + "\n")

        # Rasdaemon CSV file downloading
        stdin, stdout, stderr = ssh.exec_command("sqlite3")
        stdin.write(".open /var/lib/rasdaemon/ras-mc_event.db" + "\n")
        for table in ["aer_event", "extlog_event", "mc_event", "mce_record"]:
            stdin.write(".output " + str(table) + ".csv\n")
            stdin.write(".mode csv\n")
            stdin.write("SELECT * FROM " + str(table) + ";\n")
            sleep(1)
            sftp.get(str(table) + ".csv",
                     data_path + str(table) + "_" + datetime.datetime.now().isoformat().split(".")[0].
                     replace(":", "-").replace("T", "-") + ".csv")
        stdin.write(".quit\n")
        ssh.close()
        sftp.close()
    except Exception as e:
         raise e

