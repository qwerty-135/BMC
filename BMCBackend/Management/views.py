from django.http import JsonResponse
from django.shortcuts import render

from Log.models import ServerLog


# TODO 这一应用的所有View均是预览状态，等待高天润的更新
# Create your views here.
def log_data_by_year(request, year: int):
    obj_list = ServerLog.objects.filter(datetime__year=year).order_by("-datetime")[:2]
    data = [_.get_dict() for _ in obj_list]
    return JsonResponse(data, safe=False)


def service_1_by_year(request, year: int):
    # TODO 预览Service1
    data = [{
        "type": 'Rack Mount Chassis',
        "name": 'NF5280M6',
        "manufacturer": 'Inspur',
        "id": '24A506266',
        "id2": '24A506266',
        "SUID": 'NULL',
        "DUID": 'NULL',
        "int": '192.168.10.3',

    },
    ]
    return JsonResponse(data, safe=False)


def service_2_by_year(request, year: int):
    # TODO 预览Service2
    data = [
        {
            "onoff": '正常',
            "UID": 'NULL',
            "total": '正常',
            "pro": '正常',
            "mem": '正常',
            "disk": '正常',
            "fan": '正常',
            "net": '正常',
            "power": "正常",

        }
    ]
    return JsonResponse(data, safe=False)


def cpu_card_by_year(request, year: int):
    # TODO 预览CPUCard
    data = [
        {
            "id": 'cpu0',
            "type": 'Intel(R) Genuine processor',
            "ison": '是',
            "speed": 2600,
            "core": 28,
            "thread": 56,
            "c1": 80,
            "c2": 1280,
            "c3": 43000,

        },
        {
            "id": 'cpu1',
            "type": 'Intel(R) Genuine processor',
            "ison": '是',
            "speed": 2600,
            "core": 28,
            "thread": 56,
            "c1": 80,
            "c2": 1280,
            "c3": 43000,

        },
    ]
    return JsonResponse(data, safe=False)


def memory_card_1_by_year(request, year: int):
    # TODO 预览MemCard1
    data = [
        {
            "n1": 32,
            "n2": 2,
            "n3": 32,

        }
    ]
    return JsonResponse(data, safe=False)


def memory_card_2_by_year(request, year: int):
    # TODO 预览MemCard2
    data = [
        {

            "ps": 'CPU0_C0D1',
            "ison": '否',
            "ct": 'N/A',
            "type": 'N/A',
            "bit": 'N/A',
            "mhz": 'N/A',
            "nmhz": 'N/A',
            "mn": 'N/A',
            "se": 'N/A',
            "Rank": 'N/A',

        },
        {
            "ps": 'CPU0_C0D1',
            "ison": '是',
            "ct": 32,
            "type": 'DDR4',
            "bit": 4,
            "mhz": 2000,
            "nmhz": 2000,
            "mn": 'Samsung',
            "se": 'C09Z00052840CAD5F8',
            "Rank": 2,

        },
    ]
    return JsonResponse(data, safe=False)
