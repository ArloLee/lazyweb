# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models


# Create your models here.

class Host(models.Model):
    Ip = models.CharField(max_length=32)
    Hostname = models.CharField(max_length=64)
    Cpu = models.CharField(max_length=128)
    CpuCore = models.CharField(max_length=16)
    Operation = models.CharField(max_length=128)
    Macaddress = models.CharField(max_length=64)
    Isvirtual = models.BooleanField(default="True")
    Idc = models.CharField(max_length=128)
    Uptime = models.CharField(max_length=32)
    Applications = models.CharField(max_length=128)
    Addtime = models.CharField(max_length=32)
    Changetime = models.CharField(max_length=32)

    def __unicode__(self):
        return self.Ip


class Crontab(models.Model):
    hosts = models.ForeignKey(Host)
    Crontab_num = models.CharField(max_length=8)
    Chars = models.CharField(max_length=16)
    Update_time = models.CharField(max_length=32)

    def __unicode__(self):
        return self.Crontab_num


class Crontab_host(models.Model):
    crontab = models.ForeignKey(Crontab)
    host = models.ForeignKey(Host)
    Minute = models.CharField(max_length=8)
    Hour = models.CharField(max_length=8)
    Day = models.CharField(max_length=8)
    Month = models.CharField(max_length=8)
    Week = models.CharField( max_length=8)
    Command = models.CharField(max_length=256)
    Add_time = models.CharField(max_length=32)
    Change_time = models.CharField(max_length=32)
    Content = models.CharField(max_length=256)
    User = models.CharField(max_length=32)

    def __unicode__(self):
        return self.id

