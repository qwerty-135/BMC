from django.db import models

# from Base.models import Server

# Create your models here.

SERVER_LOG_LEVEL_CHOICE = (
    ("INFO", "INFO"),
    ("WARNING", "WARNING"),
    ("CRITICAL", "CRITICAL"),
    ("ALERT", "ALERT"),
    ("UNDEFINED", "UNDEFINED"),
)

SERVER_LOG_TYPE_CHOICE = (
    ("CPU", "CPU"),
    ("PSU", "PSU"),
    ("Memory", "Memory"),
    ("Disk", "Disk"),
    ("PCIE", "PCIE"),
    ("FAN", "FAN"),
    ("Other", "Other"),
)


class ServerLog(models.Model):
    class Meta:
        verbose_name = '服务器日志'
        verbose_name_plural = '服务器日志'

    # server = models.ForeignKey(to=Server, on_delete=models.CASCADE, verbose_name="所属服务器", )
    level = models.CharField(max_length=16, verbose_name="故障等级", choices=SERVER_LOG_LEVEL_CHOICE)
    type = models.CharField(max_length=16, verbose_name="故障类型", choices=SERVER_LOG_TYPE_CHOICE)
    code = models.CharField(max_length=64, verbose_name="事件码", default="AUGG0000")  # 注意事件码理论上不会有0000
    datetime = models.DateTimeField(verbose_name="产生时间", )
    message = models.TextField(verbose_name="日志信息", )

    def __str__(self):
        return str(self.datetime) + "日志"

    def get_dict(self):
        return {
            "id": str(self.id),
            "level": self.level,
            "type": self.type,
            "code": self.code,
            "datetime": str(self.datetime),
            "message": self.message,
            # "server_sn": str(self.server),
        }


class MemoryLog(models.Model):
    class Meta:
        verbose_name = '内存日志'
        verbose_name_plural = '内存日志'

    memory = models.IntegerField(verbose_name="Memory")
    rankid = models.IntegerField(verbose_name="Rank ID")
    bankid = models.IntegerField(verbose_name="Bank ID")
    row = models.IntegerField(verbose_name="行")
    col = models.IntegerField(verbose_name="列")
    datetime = models.DateTimeField(verbose_name="产生时间", )

    def __str__(self):
        return str(self.memory) + " " + str(self.datetime) + "日志"

    def get_dict(self):
        return {
            "id": self.id,
            "memory":self.memory,
            "rankid": self.rankid,
            "bankid": self.bankid,
            "row": self.row,
            "col": self.col,
            "datetime": str(self.datetime)
        }


class PCIELog(models.Model):
    class Meta:
        verbose_name = 'PCIE日志'
        verbose_name_plural = 'PCIE日志'

    error_severity = models.CharField(verbose_name="Error Severity", max_length=64)
    pcie_bus_error_type = models.CharField(verbose_name="PCIE Bus Error Type", max_length=64)
    receiver_id = models.CharField(verbose_name="Receiver ID", max_length=64)
    vendor_id = models.CharField(verbose_name="Vendor ID", max_length=64)
    device_id = models.CharField(verbose_name="Device ID", max_length=64)
    bus = models.CharField(verbose_name="Bus", max_length=64)
    device = models.CharField(verbose_name="Device", max_length=64)
    function = models.CharField(verbose_name="Device", max_length=64)
    datetime = models.DateTimeField(verbose_name="产生时间", )

    def __str__(self):
        return str(self.datetime) + "日志"

    def get_dict(self):
        return {
            "id": self.id,
            "error_severity": self.error_severity,
            "pcie_bus_error_type": self.pcie_bus_error_type,
            "receiver_id": self.receiver_id,
            "device_id": self.device_id,
            "bus": self.bus,
            "device": self.device,
            "datetime": str(self.datetime)
        }
