import csv
import datetime
import os
import time

import paramiko
from django.http import JsonResponse, Http404
from django.conf import settings

from Base.models import Disk
from Disk.models import Smart
from Log.module.server_log_processor import server_log_process, memory_log_process, pcie_log_process

from Log.models import ServerLog, MemoryLog, PCIELog
from glob import glob

from Log.module.util import server_query


# Create your views here.

def response_test(request):
    return JsonResponse({'code': 200, 'msg': 'OK'})


def server_log_data_receiver(request):
    # TODO 在未来，这个地方应该换成接收数据，写入本地文件，目前是直接模拟本地文件
    start_time = time.time()
    raw_data_file = "data/server_log/raw/log-2.csv"
    type, message, level, code, time_stamp = server_log_process(raw_data_file, 'msg')
    # try:
    #     server = Server.objects.get(sn=sn)
    # except Exception as e:
    #     print("No such server of" + sn)
    #     print(e)
    #     return JsonResponse({"code": "500", "message": "No such server"})
    server_log_list = []
    n = len(time_stamp)
    for i in range(n):
        sl = ServerLog(
            level=level[i],
            type=type[i],
            code=code[i],
            datetime=time_stamp[i],
            message=message[i],
        )
        server_log_list.append(sl)
    ServerLog.objects.bulk_create(server_log_list, batch_size=2000)
    print("Data Receiver Cost Time: " + str(time.time() - start_time))
    return JsonResponse({"code": "200", "message": "OK"})


def memory_log_data_receiver(request):
    # TODO 在未来，这个地方应该换成接收数据，写入本地文件，目前是直接模拟本地文件
    raw_data_file = "data/server_log/raw/memory.csv"
    obj_list = memory_log_process(raw_data_file)
    MemoryLog.objects.bulk_create(obj_list, batch_size=2000)
    return JsonResponse({"code": "200", "message": "OK"})


def pcie_log_data_receiver(request):
    # TODO 在未来，这个地方应该换成接收数据，写入本地文件，目前是直接模拟本地文件
    raw_data_file = "data/server_log/raw/pcie2.csv"
    obj_list = pcie_log_process(raw_data_file)
    PCIELog.objects.bulk_create(obj_list, batch_size=2000)
    return JsonResponse({"code": "200", "message": "OK"})


def disk_log_data_receiver(request):
    # TODO 在未来，这个地方应该换成接收数据，写入本地文件，目前是直接模拟本地文件
    raw_data_file_path = "data/disk_log/"
    disk_log_list = []
    for model in os.listdir(raw_data_file_path):
        for disk in glob(raw_data_file_path + model + "/*.csv"):
            try:
                d = Disk.objects.get(
                    sn=disk.replace(".csv", "").replace(raw_data_file_path + model + "\\", ""))  # TODO linux下是 "/"
            except Exception as e:
                d = Disk(
                    sn=disk.replace(".csv", "").replace(raw_data_file_path + model + "\\", ""),
                    model=model,
                )
                d.save()
            file = csv.reader(open(disk, "r", encoding="utf-8"))
            for row in file:
                obj = Smart(
                    disk=d,
                    date=datetime.date.fromisoformat(row[0]) - datetime.timedelta(days=730),
                    value=str(row[3:]),
                    failure=False
                )
                disk_log_list.append(obj)
    Smart.objects.bulk_create(disk_log_list, batch_size=1000)
    return JsonResponse({"code": "200", "message": "OK"})


def server_index(request, year: int, month: int):
    data = list(ServerLog.objects.filter(datetime__year=year, datetime__month=month).values())  # 把Values直接拿出来是最快的。
    return JsonResponse(data, safe=False)  # 正确传输方式


def memory_index(request, year: int, month: int):
    data = list(MemoryLog.objects.filter(datetime__year=year, datetime__month=month).values())  # 把Values直接拿出来是最快的。
    return JsonResponse(data, safe=False)


def pcie_index(request, year: int, month: int):
    data = list(PCIELog.objects.filter(datetime__year=year, datetime__month=month).values())  # 把Values直接拿出来是最快的。
    return JsonResponse(data, safe=False)


def log_detail(request, id: int):
    try:
        sl = ServerLog.objects.get(id=id)
    except Exception as e:
        print("No such server log")
        print(e)
        return Http404("No such server log")
    detail_dict = {"PCIE": "PCIE", "MEM": "Memory"}
    if sl.type not in detail_dict:  # TODO Disk的适配
        return Http404("Can't find the target log")
    model_name = detail_dict[sl.type] + "Log"
    data_later = eval(model_name).objects.filter(datetime__gte=sl.datetime).order_by('datetime')
    data_earlier = eval(model_name).objects.filter(datetime__lte=sl.datetime).order_by('-datetime')

    if not len(data_later) and not len(data_earlier):
        return Http404("Can't find the target log")
    if not len(data_later):
        data = data_earlier[0].get_dict()
    elif not len(data_earlier):
        data = data_later[0].get_dict()
    else:
        data_later = data_later[0]
        data_earlier = data_earlier[0]
        delta_later = abs(sl.datetime - data_later.datetime)
        delta_earlier = abs(sl.datetime - data_earlier.datetime)
        if delta_later > delta_earlier:
            data = data_earlier.get_dict()
        else:
            data = data_later.get_dict()

    return JsonResponse(data, safe=False)


def server_status_update(request):
    try:
        server_query()
        return JsonResponse({'code': 200, 'message': 'ok'})
    except Exception as e:
        return JsonResponse({'code': 500, 'message': str(e)})
