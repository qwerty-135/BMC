import csv
import os
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
import xgboost as xgb
import matplotlib.pyplot as plt
from tqdm import tqdm
import random

XGB_PARAMETER = {'booster': 'gbtree',
                 'objective': 'binary:logistic',
                 'eval_metric': 'auc',
                 'max_depth': 5,
                 'lambda': 1,
                 'subsample': 1,
                 'colsample_bytree': 0.75,
                 'min_child_weight': 1,
                 'eta': 0.025,
                 'seed': 0,
                 'nthread': 8,
                 'gamma': 0.05,
                 'learning_rate': 0.01}
random.seed(20240201)


def xgb_pre_process(disk_smart_parameter, flow_size=20, positive_path="./failure_disk_data", negative_path="./data",
                    output_path="./clf_xgb"):
    # 随机抽取3倍于阳例的阴例
    positive_sample = os.listdir(positive_path)
    pn = len(os.listdir(positive_path))
    nn = 1 * pn
    temp_negative_sample = os.listdir(negative_path)
    random.shuffle(temp_negative_sample)
    negative_sample = []
    for x in temp_negative_sample:
        if x in positive_sample:
            continue
        negative_sample.append(x)
        if len(negative_sample) == nn:
            break

    # result = [["PID", "FAILURE"] + ["D" + str(i) + "S" + str(j) for i in range(flow_size) for j in
    #                                 range(disk_smart_parameter)], ]
    result = [["PID", "FAILURE"] + ["S" + str(j) for j in range(disk_smart_parameter)], ]
    for file in tqdm(positive_sample):
        csv_file = csv.reader(open(positive_path + "/" + file, "r", encoding="utf-8"))
        counter = 0
        temp_rows = []
        for row in csv_file:
            temp_rows.append(row)
        if len(temp_rows) < flow_size:  # 改为取20天前的数据
            continue
        temp_rows.reverse()  # 反向倒序判断天数
        # new_row = [temp_rows[0][1], "1"]
        # for i in range(flow_size, flow_size * 2):  # 改为取20天前的数据
        #     new_row.extend(temp_rows[i][3:])  # 去掉DATE、SN和FAILURE
        # result.append(new_row)

        # Positive部分
        for i in range(flow_size):
            new_row = [temp_rows[0][1], "1"]
            new_row.extend(temp_rows[i][3:])  # 去掉DATE、SN和FAILURE
            result.append(new_row)

        # 从Positive中抽样的Negative部分
        # if len(temp_rows) >= flow_size * 3:
        #     for i in range(flow_size + 1, 0, -1):
        #         new_row = [temp_rows[0][1], "0"]
        #         new_row.extend(temp_rows[-i][3:])  # 去掉DATE、SN和FAILURE
        #         result.append(new_row)
        #
        # if len(temp_rows) >= flow_size * 2:
        #     for i in range(flow_size):
        #         new_row = [temp_rows[0][1], "0"]
        #         new_row.extend(temp_rows[i + flow_size][3:])  # 去掉DATE、SN和FAILURE
        #         result.append(new_row)
        for i in range(flow_size, len(temp_rows)):
            new_row = [temp_rows[0][1], "0"]
            new_row.extend(temp_rows[i][3:])  # 去掉DATE、SN和FAILURE
            result.append(new_row)

    for file in tqdm(negative_sample):
        csv_file = csv.reader(open(negative_path + "/" + file, "r", encoding="utf-8"))
        counter = 0
        temp_rows = []
        for row in csv_file:
            temp_rows.append(row)
        if len(temp_rows) < flow_size:
            continue
        # t = random.randint(0, len(temp_rows) - flow_size)
        # temp_rows = temp_rows[t:t + flow_size]
        temp_rows.reverse()  # 反向倒序判断天数
        # new_row = [temp_rows[0][1], "0"]
        # for i in range(flow_size):
        #     new_row.extend(temp_rows[i][3:])
        # result.append(new_row)
        for i in range(len(temp_rows)):
            new_row = [temp_rows[0][1], "0"]
            new_row.extend(temp_rows[i][3:])
            result.append(new_row)

    output_csv = csv.writer(open(output_path + "/data-" + str(flow_size) + ".csv", "w", encoding="utf-8", newline=""))
    output_csv.writerows(result)


def xgboost_train(disk_model, data_source: str, image_save_path: str, num_boost_round: int = 50):
    # 导入数据集
    df = pd.read_csv(data_source)
    data = df.iloc[:, 2:]
    target = df.iloc[:, 1:2]

    # 切分训练集和测试集
    train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.2, random_state=7)

    # xgboost模型初始化设置
    dtrain = xgb.DMatrix(train_x, label=train_y)
    dtest = xgb.DMatrix(test_x)
    watchlist = [(dtrain, 'train')]

    # booster:
    params = XGB_PARAMETER

    # 建模与预测：num_boost_round棵树
    bst = xgb.train(params, dtrain, num_boost_round=num_boost_round, evals=watchlist)
    ypred = bst.predict(dtest)

    # 设置阈值、评价指标
    y_pred = (ypred >= 0.5) * 1
    print('Precesion: %.4f' % metrics.precision_score(test_y, y_pred))
    print('Recall: %.4f' % metrics.recall_score(test_y, y_pred))
    print('F1-score: %.4f' % metrics.f1_score(test_y, y_pred))
    print('Accuracy: %.4f' % metrics.accuracy_score(test_y, y_pred))
    print('AUC: %.4f' % metrics.roc_auc_score(test_y, ypred))

    # ypred = bst.predict(dtest)
    # print("测试集每个样本的得分\n", ypred)
    # ypred_leaf = bst.predict(dtest, pred_leaf=True)
    # print("测试集每棵树所属的节点数\n", ypred_leaf)
    # ypred_contribs = bst.predict(dtest, pred_contribs=True)
    # print("特征的重要性\n", ypred_contribs)
    plt.figure(figsize=(20, 10))
    plt.subplots_adjust(left=0.8)  # 左边距问题
    plt.tight_layout()
    xgb.plot_importance(bst, height=0.8, title=disk_model, ylabel='特征', max_num_features=22)
    plt.rc('font', family='Arial', size=8)
    plt.savefig(image_save_path)
    # plt.show()
    return [metrics.precision_score(test_y, y_pred), metrics.recall_score(test_y, y_pred),
            metrics.f1_score(test_y, y_pred), metrics.accuracy_score(test_y, y_pred),
            metrics.roc_auc_score(test_y, ypred)], bst
