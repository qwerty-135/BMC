import datetime

import torch
from django.http import JsonResponse
from Disk.module import disk_smart_parameter
from django.shortcuts import render
import xgboost as xgb

from Base.models import Disk
from Disk.models import Smart

# Create your views here.
model_path = "./Disk/module/"


def disk_list_view(request):
    objs = Disk.objects.all()
    result = [str(obj) for obj in objs]
    return JsonResponse(result, safe=False)


def xgboost_analysis_single(model, data):
    model = model_path + "XGB-" + model
    clf = xgb.XGBClassifier()
    bst = xgb.Booster({"nthread": 1})
    bst.load_model(model)
    clf._Booster = bst
    y_pred = clf.predict(
        [data])
    return y_pred[0]


def rnn_analysis_single(model, data):
    model = model_path + "RNN-" + model
    model = torch.load(model, map_location=torch.device('cpu'))
    data = torch.tensor(data, dtype=torch.float32)
    y_pred = round(model(data.to("cpu")).item() * 20)
    return y_pred


def rnn_analysis_list(model, data_list, choice: str = "RNN"):
    model = model_path + choice + "-" + model
    model = torch.load(model, map_location=torch.device('cpu'))
    y_pred_list = []
    # for i in range(len(data_list)):
    #     y_list = model(torch.tensor(data_list[i], dtype=torch.float32))
    #     y = []
    #     for t in y_list:
    #         y.append(round(t.item() * 20))
    #     y_pred_list.append(y[i+10])
    result = list(model(torch.tensor(data_list, dtype=torch.float32)))
    for y in result:
        y_pred_list.append(round(y.item() * 40, 1))
    return y_pred_list[-20:]


def min_max(smart_min_max, data):
    result = [None for _ in range(len(data))]
    for i in range(len(data)):
        result[i] = (data[i] - smart_min_max[i][0]) / smart_min_max[i][2]
    return result


def rnn_minmax_list(model, data_list):
    smart_min_max = model_path + "RNN-" + model + "-MINMAX"
    smart_min_max = eval(open(smart_min_max, "r").readline())
    for i in range(len(smart_min_max)):
        smart_min_max[i].append(smart_min_max[i][1] - smart_min_max[i][0])
    result_list = []
    for data in data_list:
        result_list.append(min_max(smart_min_max, data))
    return result_list


def get_backblaze_recommended_smart(model, data):
    target = getattr(disk_smart_parameter, model + "_REALIST")
    value = []
    for smart in disk_smart_parameter.BACKBLAZE_DISK_RECOMMENDED:
        index = target.index(smart)
        value.append(data[index])
    return value


def get_xgboost_recommended_smart(model, data):
    value = []
    for index in getattr(disk_smart_parameter, "XGBOOST_" + model + "_DISK_RECOMMENDED"):
        value.append(data[index])
    return value


def disk_view(request, date, sn):
    try:
        disk = Disk.objects.get(sn=sn)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)
    disk_status = "normal"
    query_date = datetime.date.fromisoformat(date)
    smart_list = list(Smart.objects.filter(disk=disk, date__lte=query_date).select_related(
        'disk').order_by("date"))[-20:]
    smart = eval(smart_list[-1].value)
    backblaze_recommended_smart = get_backblaze_recommended_smart(disk.model, smart)
    xgboost_recommended_smart = get_xgboost_recommended_smart(disk.model, smart)
    if not len(smart_list):
        # 查询的日期过早
        return JsonResponse({"disk_status": "N/A", "disk_model": disk.model})
    if smart_list[-1].date != query_date:
        # 已经没有日志了，默认是坏掉了
        return JsonResponse({"disk_status": "failure",
                             "disk_model": disk.model,
                             "life": -1,
                             "backblaze_recommended_smart": backblaze_recommended_smart,
                             "xgboost_recommended_smart": xgboost_recommended_smart, })

    # 20天时间的序列
    sv = []
    for obj in smart_list:
        temp = eval(obj.value)
        for i in range(len(temp)):
            temp[i] = int(temp[i])
        sv = sv + temp
    # 当天时间的序列
    life_predict = ["N/A" for _ in range(10)]
    future_days = "N/A"
    if len(smart_list) < 20:
        # 新硬盘
        pass
    else:
        smart = [int(_) for _ in smart]
        xgboost_result = xgboost_analysis_single(disk.model, smart)  # 原来为SV
        if xgboost_result:
            smart_list = list(
                Smart.objects.select_related('disk').filter(disk=disk, date__lte=query_date).order_by("date"))[-40:]
            disk_status = "warning"
            sv = []
            for smart in smart_list:
                temp = eval(smart.value)
                for i in range(len(temp)):
                    temp[i] = int(temp[i])
                sv.append(temp)
            sv = rnn_minmax_list(disk.model, sv)
            # data = []
            # for i in range(len(sv) - 40):
            #     temp = []
            #     for j in range(i, 20 + i):
            #         temp.append(sv[j])
            #     data.append(temp)
            life_predict = rnn_analysis_list(disk.model, sv)
            future_days = Smart.objects.select_related("disk").filter(disk=disk, date__gt=query_date).count()
            life_predict = life_predict[20 - future_days:min(30 - future_days, 20)]

    return JsonResponse({"disk_status": disk_status,
                         "disk_model": disk.model,
                         "life": life_predict[0] if life_predict else future_days,
                         "backblaze_recommended_smart": backblaze_recommended_smart,
                         "xgboost_recommended_smart": xgboost_recommended_smart,
                         "life_predict": life_predict})
