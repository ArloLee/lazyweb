# _*_ coding: utf-8 _*_
# custom function by lee
import os, commands, re, json
import time
import salt.client


def prints(parm):
    print ("\033[1;35m %s \033[0m") % parm


def Cron_line(line):
    Format = ' '.join(line.split())
    List = Format.split()
    return List


def Get_salt_agent_hostname(status):
    Hostname_command = "salt-key --list=%s --no-color" % status
    Hostname_command_result = commands.getoutput(Hostname_command).split('\n')
    print Hostname_command_result
    return Hostname_command_result


def Get_salt_agent_ip(hostname):
    Ssh_command = "ping -c 1 %s | head -1" % hostname
    Command_result = commands.getoutput(Ssh_command)
    Agent_ip = re.findall("\d{3}\.\d{3}\.\d{3}\.\d{3}", Command_result)[0]
    return Agent_ip


def Get_crontab_user_list(user=None):
    Dir = "/var/spool/cron/"
    if user == None:
        List = []
        for file in os.listdir(Dir):  # 获取所有用户的cron文件
            List.append(file)
        return List
    else:
        return user


# get crontab list from salt.cron.ls not use
def Get_crontab_list_01(Hostname=None, user=None):
    if Hostname is not None:
        Users = Get_crontab_user_list()
        dict = {}
        dict_tmp = {}
        for User in Users:
            Cmd_cron = "salt %s cron.ls %s --output=json" % (Hostname, User)
            Cmd_cron_output = commands.getoutput(Cmd_cron)
            dict_tmp[User] = json.loads(Cmd_cron_output)
            dictnum = {}
            if len(dict_tmp[User][Hostname]['pre']):
                i = 0
                for cron in dict_tmp[User][Hostname]['pre']:
                    if len(cron):
                        i += 1
                        Minute = cron.split(' ')[0]
                        Hour = cron.split(' ')[1]
                        Day = cron.split(' ')[2]
                        Month = cron.split(' ')[3]
                        Week = cron.split(' ')[4]
                        Command = cron.split(' ')[5:]
                        Add_time = time.strftime('%Y-%m-%d %H:%M:%S')
                        Change_time = time.strftime('%Y-%m-%d %H:%M:%S')
                        User = User
                        Content = "content"
                        dictnum[i] = {"Hostname": Hostname, "Minute": Minute, "Hour": Hour, "Day": Day, "Month": Month,
                                          "Week": Week, "Command": Command, "Add_time": Add_time,
                                          "Change_time": Change_time,"Content": Content}
                    else:
                        pass
                    dict[User] = dictnum

    return dict


def Get_crontab_list(Hostname=None, User=None):
    Cron_dir = "/var/spool/cron/"
    Cache_dir = '/var/cache/salt/master/minions/'+Hostname+'/files' + Cron_dir
    if User is None:
        # user_list = []
        Cron_dict = {}
        for file in os.listdir(Cache_dir):
            # user_list.append(file)
            Cron_flie = Cache_dir + file
            f = open(Cron_flie,'r+')
            linenum = 1
            temp_dict = {}
            Content_dict = {}
            for line in f.readlines():
                if len(line.strip()) > 0:
                    if line.startswith("#"):
                        # Content_dict[linenum] = line
                        pass
                    else:
                        line_sp = Cron_line(line)
                        print ">>>>>>lins sp is:",line_sp
                        Ex_time = line_sp[0:5]
                        print(Ex_time)
                        Command = ' '.join(line_sp[5:])
                        print(Command)
                        temp_dict[linenum] = {"Ex_time": Ex_time,"Command":Command}
                        print(temp_dict)
                    linenum += 1
                Cron_dict[file] = temp_dict
        return Cron_dict

    else:
        return "error"


def Get_crontab_list_fromfile(Hostname=None, User=None):
    if Hostname is None:
        resu = "error : Hostname none"
    else:
        local = salt.client.LocalClient()
        resu = local.cmd(Hostname,"cp.push_dir",["/var/spool/cron"])
    return resu


