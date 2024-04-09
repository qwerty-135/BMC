import pandas as pd
from sklearn.model_selection import  train_test_split
import torch
import torch.nn as nn
import numpy as np
from torch import optim
from torch.utils.data import Dataset, DataLoader
import os
from util import match_template,feature_generation_for_short
import torch.utils.data as Data

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(DEVICE)

data2=pd.read_csv("t1.csv")
from drain3 import TemplateMiner  # 开源在线日志解析框架
from drain3.file_persistence import FilePersistence
from drain3.template_miner_config import TemplateMinerConfig

config = TemplateMinerConfig()
config.load('drain3.ini')  ## 这个文件在drain3的github仓库里有
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
    print(cluster.cluster_id)
    if cluster.size >= min_size:
        template_dic[cluster.cluster_id] = cluster.size

temp_count_f = len(template_dic)





# data = data.apply(match_template, template_miner=template_miner, template_dic=template_dic, axis=1)
# data.to_pickle(drain_file + '_result_match_data.pkl')  # 将匹配好的数据存下来
data2 = data2.apply(match_template, template_miner=template_miner, template_dic=template_dic, axis=1)
print(data2)
data2.to_pickle(drain_file + '_result_match_data2.pkl')

df_data2 = pd.read_pickle(drain_file + '_result_match_data2.pkl')  # 读取匹配好模板的数据
df_data2[df_data2['template_id'] != 'None'].head()





df_data2.rename(columns={'time': 'collect_time'}, inplace=True)
feature_generation_for_short(df_data2, '1h', '', '', '3', 'sum',temp_count_f)

df_data = pd.read_pickle('cpu2_diag_comp_sel_log_all_feature_1h_3_sum.pkl')  # 读取之前构造好的特征数据
df_data.to_csv('qwe1.csv', index=0)
