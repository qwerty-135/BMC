import pandas as pd
from sklearn.model_selection import  train_test_split
import torch
import torch.nn as nn
import numpy as np
from torch import optim


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




def feature_generation(df_data, gap_list,  win_list, func_list,len_template_dic):
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

def feature_generation_for_short(df_data, gap_list, win_list, func_list,len_template_dic):
    gap_list = gap_list.split(',')

    arr = np.arange(1, len_template_dic)

    dummy_col = ['template_id_' + str(x) for x in arr]

    for gap in gap_list:
        df_data['collect_time_gap'] = pd.to_datetime(df_data.collect_time).dt.ceil(gap)
        df_data = template_dummy_for_short(df_data,dummy_col)

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


