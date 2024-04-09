import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as Data
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from model import RandomForestClassifier,classifier
from drain3 import TemplateMiner
from drain3.file_persistence import FilePersistence
from drain3.template_miner_config import TemplateMinerConfig
from util import match_template,feature_generation

from sklearn.metrics import confusion_matrix, classification_report
import warnings
warnings.filterwarnings("ignore")
from sklearn import svm
from datetime import datetime
from datetime import timedelta
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
drain_file = 'comp_a_sellog'
print(DEVICE)
data_train = pd.read_csv('preliminary_sel_log_dataset.csv')
data_test = pd.read_csv('preliminary_sel_log_dataset_a.csv')
data = pd.concat([data_train, data_test])
config = TemplateMinerConfig()
config.load('drain3.ini')
config.profiling_enabled = False


persistence = FilePersistence(drain_file + '.bin')
template_miner = TemplateMiner(persistence, config=config)
for msg in data.msg.tolist():
    template_miner.add_log_message(msg)
temp_count = len(template_miner.drain.clusters)
template_dic = {}
size_list = []
for cluster in template_miner.drain.clusters:
    size_list.append(cluster.size)
size_list = sorted(size_list, reverse=True)[:200]
min_size = size_list[-1]

for cluster in template_miner.drain.clusters:
    if cluster.size >= min_size:
        template_dic[cluster.cluster_id] = cluster.size

temp_count_f = len(template_dic)
# temp_count_f = 207
data = data.apply(match_template, template_miner=template_miner, template_dic=template_dic, axis=1)
data.to_pickle(drain_file + '_result_match_data.pkl')

df_data = pd.read_pickle(drain_file + '_result_match_data.pkl')
df_data[df_data['template_id'] != 'None'].head()
df_data.rename(columns={'time': 'collect_time'}, inplace=True)
feature_generation(df_data, '1h', '', '', '3', 'sum',len_template_dic=temp_count_f)

df_data = pd.read_pickle('cpu_diag_comp_sel_log_all_feature_1h_3_sum.pkl')
# df_data.to_csv("rt.csv")
df_train_label = pd.read_csv('preliminary_train_label_dataset.csv')
df_train_label_s = pd.read_csv('preliminary_train_label_dataset_s.csv')
df_train_label = pd.concat([df_train_label, df_train_label_s])
df_train_label = df_train_label.drop_duplicates(['sn', 'fault_time', 'label'])

df_data_train = pd.merge(df_data[df_data.sn.isin(df_train_label.sn)], df_train_label, on='sn', how='left')
df_data_train["collect_time_gap"]=df_data_train["collect_time_gap"].apply(lambda x:x.timestamp()).astype(int)
df_data_train["fault_time"]=df_data_train["fault_time"].apply(lambda x:datetime.strptime(x, "%Y-%m-%d %H:%M:%S").timestamp()).astype(int)


df_data_train['label'].apply(lambda x:x)

df_data_train=df_data_train[abs(df_data_train.fault_time-df_data_train.collect_time_gap)<3600*24]



y = df_data_train['label']
x = df_data_train.drop(['sn', 'collect_time_gap', 'fault_time', 'label'], axis=1)
# X_train, X_val, y_train, y_val = train_test_split(x, y, test_size=0.1, random_state=6)
X_train, X_val, y_train, y_val = train_test_split(x, y, test_size=0.1, random_state=6)

X_train = np.array(X_train)
y_train = np.array(y_train)
df_tensor = torch.Tensor(X_train)
tensor_y = torch.Tensor(y_train)
n=X_train.shape[1]

X_val = np.array(X_val)
y_val = np.array(y_val)
X_val = torch.Tensor(X_val)

y_val = torch.Tensor(y_val)


best_f1 = 0
precision = 0
recall = 0
fpr = 0
model,hyperparameters = classifier("MLP")
model = model(random_state=42)
model.fit(X_train, y_train)
torch.save(model,'mlp.pth')

y_pred=model.predict(X_val)
print(y_pred)
y_truth = y_val
report=classification_report(y_truth, y_pred=model.predict(X_val),output_dict=True)
df = pd.DataFrame(report).transpose()
print (df)
# y_pred2=model.predict(x)
# print(y_pred2)
# res = df_data_train[['sn', 'collect_time_gap']]
# res['label']=y_pred2
# res.to_csv('comp_a_result_3.csv', index=0)
