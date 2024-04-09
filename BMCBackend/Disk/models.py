from django.db import models

from Base.models import Disk


# Create your models here.
class Smart(models.Model):
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE, verbose_name="所属硬盘")
    date = models.DateField(verbose_name="日期")
    value = models.TextField(verbose_name="SMART值")  # 我们不可能创建那么多Smart属性值，所以用Text存储，需要的时候拆解。
    failure = models.BooleanField(verbose_name="是否损坏")
