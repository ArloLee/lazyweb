# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.apps import AppConfig
from cmdb01.models import Host
from cmdb01.models import Crontab
from cmdb01.models import Crontab_host

admin.site.register(Host)
admin.site.register(Crontab)
admin.site.register(Crontab_host)
