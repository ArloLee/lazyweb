# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response, HttpResponse, Http404, HttpResponseRedirect
from cmdb01.models import Host, Crontab, Crontab_host
from cmdb01 import lee
import json, commands
from django.utils import timezone
import datetime, time
import salt.client

# Create your views here.

def index(request):
    return render_to_response('index.html')


def Hostlist(request):
    Host_list = Host.objects.order_by('id')
    return render_to_response('hostlist.html', {'Host_dict': Host_list})


def Hostdiscover(request):
    Host_name_list = lee.Get_salt_agent_hostname("unaccepted")[1:]
    ID = 1
    Host_dict = {}
    for Host_name in Host_name_list:
        Host_ip = lee.Get_salt_agent_ip(Host_name)
        Host_dict[ID] = [Host_name, Host_ip]
        ID += 1
    return render_to_response('hostdis.html', {"Host_list_dict": Host_dict})


def Accept_salt_key(request):
    if request.method == "POST":
        if request.POST["Todo"] == "accept":
            Accept_key_commands = "salt-key -a  %s -y" % request.POST["Minion_host_name"]
            Minion_host_name = request.POST["Minion_host_name"]
            Minion_ipaddress = request.POST["Minion_ipaddress"]
            result = commands.getoutput(Accept_key_commands)
            Host_in_db = Host(Ip=Minion_ipaddress, Hostname=Minion_host_name)
            Host_in_db.save()
            rollback = "success"
        else:
            result = "accept key faild"
            rollback = "error"
    else:
        print "Request method must be POST"
    return HttpResponse(json.dumps({"rollback": rollback, "result": result}))


def Initia_host_info(request):
    Hostname = request.POST['hostname']
    # Command_get_allstatus = "salt '%s' status.all_status --output=json" % Hostname
    Command_get_cpustatus = "salt '%s' status.cpuinfo --output=json" % Hostname
    Command_get_grains = "salt '%s' grains.items --output='json'" % Hostname
    # Command_ext_status = commands.getoutput(Command_get_allstatus)
    Command_ext_cpustatus = commands.getoutput(Command_get_cpustatus)
    Command_ext_grains = commands.getoutput(Command_get_grains)
    Status_dict = json.loads(Command_ext_cpustatus)
    Grains_dict = json.loads(Command_ext_grains)
    Macaddress = "Pass"
    CpuVersion = Grains_dict[Hostname]['cpu_model']
    # CpuCore = Status_dict[Hostname]['cpuinfo']['cpu cores']
    CpuCore = Status_dict[Hostname]['cpu cores']
    Operation = Grains_dict[Hostname]['osfullname'] + ' ' + Grains_dict[Hostname]['osrelease']
    # Disk = "500GB"
    IsVirtual = "True"
    Idc = ""
    Application = ""
    Uptime = "2天"
    Addtime = timezone.now()
    Changetime = timezone.now()
    Host.objects.filter(Hostname=Hostname).update(Cpu=CpuVersion, CpuCore=CpuCore, Operation=Operation,
                                                  Macaddress=Macaddress, Isvirtual=IsVirtual, Idc=Idc, Uptime=Uptime,
                                                  Applications=Application, Addtime=Addtime, Changetime=Changetime)
    return HttpResponse(json.dumps({"result": "success"}))


def Crontab_index(request):
    Host_id_list = Crontab.objects.values_list("id")
    Reback_dict = {}
    for Host_id in Host_id_list:
        Int_host_id = Host_id[0]
        Crontab_db = Crontab.objects.get(id=Int_host_id)
        Ipaddr = Crontab_db.hosts.Ip
        Hostname = Crontab_db.hosts.Hostname
        Cron_num = Crontab_db.Crontab_num
        Update_time = Crontab_db.Update_time
        Reback_dict[Hostname] = {'Ipaddres': Ipaddr, 'Hostname': Hostname, 'Updatetime': Update_time,
                                 'Cron_num': Cron_num}
    return render(request, 'crontabindex.html', {"data": Reback_dict})


def Host_crontab_list(request):
    if request.method == 'GET':
        Host_name = request.GET['id']
        Salt_resu = lee.Get_crontab_list_fromfile(Host_name)
        lee.prints("start get crontab file")
        Cron_dict = lee.Get_crontab_list(Host_name)
        Cron_user = Cron_dict.keys()
        resu = "success"
    return render(request, 'host-crontab-list.html', {'hostname':Host_name,'resu': resu,'Salt_resu':Salt_resu, 'Cron_dict':Cron_dict})


def Crontab_update(request):
    if request.method == "POST":
        if len(request.POST["Hostname"]) > 0:
            Host_name = request.POST["Hostname"]  # get hostname from web
            print Host_name
            # get all crontab user
            User_list = lee.Get_crontab_user_list()
            # get all user crontab num
            i = 0

            for user in User_list:
                Json_dict = {}
                Salt_cron_command = "salt '%s' cron.ls '%s' --output=json" % (Host_name, user)
                Salt_cron_command_resu = commands.getoutput(Salt_cron_command)
                Json_dict = json.loads(Salt_cron_command_resu)
                # 获取所有crontab值
                for cron in Json_dict[Host_name]['pre']:
                    if cron:
                        i += 1
                    else:
                        pass
            Db_ops = Crontab(Crontab_num=i, Update_time=time.strftime('%Y-%m-%d %H:%S:%M'),
                             hosts_id=Host.objects.get(Hostname=Host_name).id)
            Db_ops.save()  # 判断是否存在主机记录 未作
            return HttpResponse(json.dumps({"back": "success", "length": i}))
        else:
            return HttpResponse(json.dumps({"back": "HostName error"}))
    else:
        return HttpResponse(json.dumps({"back": "Method must be post"}))


def Host_cron_update(request):
    if request.method == "POST":
        Ex_time = request.POST['Ex_time']
        File = request.POST['User']
        Hostname = request.POST['Hostname']
        Format_time = str(Ex_time).replace('[','').replace(']','').replace('\'','').replace(',',' ')
        Command = request.POST['Command']
        if len(Command) == 0 and len(Ex_time) == 0:
            Change_cron = ''
        else:
            Change_cron = Format_time + ' ' + Command + '\n'
        if request.POST['Line']
        Line = int(request.POST['Line'])
        Dir = "/var/spool/cron/"
        Open_file = str('/var/cache/salt/master/minions/'+ str(Hostname) +'/files' + Dir + str(File))

        f = open(Open_file,'r+')
        lines = f.readlines()
        f.close()
        lines[Line-1] = Change_cron
        Salt_root = "/srv/salt/"
        f = open(Salt_root+File,'w+')
        f.writelines(lines)
        f.close()
        local = salt.client.LocalClient()
        Master_file = "salt://"+str(File)
        Minion_file = str(Dir) + str(File)
        resu = local.cmd(Hostname,'cp.get_file',[Master_file,Minion_file])
    else:
        resu = "method must be POST"

    return HttpResponse(json.dumps({"resu": resu}))


def Change_Conrab_ex_time(request):
    lee.prints("Change_Conrab_ex_time function pass")
    return HttpResponse(json.dumps({"resu":'success'}))


def Change_Crontab_com(request):
    lee.prints("Change_Crontab_com function pass")
    return HttpResponse(json.dumps({"resu":"success"}))




# 获取主机所有crontab任务
#             resu = lee.Get_crontab_list(Host_name)
            # 根据主机名获取id
            # Host_id = Host.objects.get(Hostname=Host_name).id
            # 检查是否存在host对应的crontab
            # try:
                # Db_cron_ops = Crontab_host.objects.get(host_id=Host_id)
            # 如果不存在，插入新纪录
            # except Crontab_host.DoesNotExist:
            #     print "Dont't have this recard"
            #     for user in resu.keys():
            #         for num in resu[user].keys():
            #             print "the %s is ::::::::" % num
            #             print resu[user][num]
                    # Db_cron_host_ops = Crontab_host(Minute=resu[user]['Minute'], Hour=resu[user]['Hour'],
                    #                                 Day=resu[user]['Day'], Month=resu[user]['Month'],
                    #                                 Week=resu[user]['Week'], Command=resu[user]['Command'],
                    #                                 Add_time=resu[user]['Add_time'],
                    #                                 Change_time=resu[user]['Change_time'], User=user,
                    #                                 Content=resu[user]['Content'])
                    # Db_cron_host_ops.save()
            # 如果存在，更新记录
            # else:
                # pass
                # Db_cron_ops.update(Minute=resu[user]['Minute'], Hour=resu[user]['Hour'], Day=resu[user]['Day'],
                #                    Month=resu[user]['Month'], Week=resu[user]['Week'], Command=resu[user]['Command'],
                #                    Add_time=resu[user]['Add_time'], Change_time=resu[user]['Change_time'], User=user,
                #                    Content=resu[user]['Content'])
