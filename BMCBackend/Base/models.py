from django.db import models


# Create your models here.
# class Server(models.Model):
#     class Meta:
#         verbose_name = "服务器"
#         verbose_name_plural = "服务器"
#
#     sn = models.CharField(max_length=255, verbose_name="序列号", unique=True)
#     server_model = models.CharField(max_length=255, verbose_name="服务器类型", blank=True, null=True)
#
#     def __str__(self):
#         return self.sn

class Disk(models.Model):
    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = '硬盘'

    sn = models.CharField(max_length=255, verbose_name="序列号", unique=True)
    model = models.CharField(max_length=255, verbose_name="服务器类型")

    def __str__(self):
        return self.sn
