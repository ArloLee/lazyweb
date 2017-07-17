"""devops01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from cmdb01 import views as cmdbviews


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', cmdbviews.index),
    url(r'^index/$', cmdbviews.index),
    url(r'^hostli/$', cmdbviews.Hostlist),
    url(r'^hostdis/$', cmdbviews.Hostdiscover),
    url(r'^accept_salt_key/$', cmdbviews.Accept_salt_key),
    url(r'^Initia/$', cmdbviews.Initia_host_info),
    url(r'Crontabindex/$', cmdbviews.Crontab_index),
    url(r'Host_crontab_list/$', cmdbviews.Host_crontab_list),
    url(r'Crontab_update/$', cmdbviews.Crontab_update),
    # url(r'Change_cron_time/$', cmdbviews.Change_Conrab_ex_time),
    # url(r'Change_cron_com/$', cmdbviews.Change_Crontab_com),
    url(r'Host_cron_update/$', cmdbviews.Host_cron_update),


]
