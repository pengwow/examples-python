# -*- coding:utf-8 -*-
__author__ = 'admin'
from subprocess import Popen, PIPE
import json
import time


def exec_command(command, flag=True):
    new_command = "sshpass -p password ssh root@172.16.1.102 "+command
    process = Popen(command, shell=flag, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout


def getOSInfo():
    # ip = ''
    sn = exec_command("dmidecode -s system-serial-number | awk '{printf(\"%s\",$0)}'")
    ip = exec_command("/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{printf $2}'|tr -d 'addr:'")
    # print ipex
    # if re.search("((^10\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[0-9]))|(^172\.(1[6789]|2[0-9]|3[01]))|(^192\.168)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[0-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[0-9])$)", ipex):
    #     ip = ipex
    # print ip
    # 服务器制造商
    manufacturer = exec_command("dmidecode -s system-manufacturer | awk '{printf(\"%s\",$0)}'")
    # 服务器型号
    model = exec_command("dmidecode -s system-product-name | awk '{printf(\"%s\",$0)}'")

    # CPU型号
    cpuModel = exec_command(
        "dmidecode -t processor | grep Version | uniq -c| awk -F ':'  '{printf $2}'| sed 's/^ *\| *$//g'")
    # 物理CPU核心数
    cpuPhyNum = exec_command("cat /proc/cpuinfo | grep 'physical id' | sort | uniq | wc -l | awk '{printf(\"%s\",$0)}'")
    # 逻辑CPU核心数
    cpuLogicNun = exec_command("cat /proc/cpuinfo| grep processor| wc -l| awk '{printf(\"%s\",$0)}'")
    # CPU数量
    cpuNum = exec_command("cat /proc/cpuinfo | grep 'cpu cores' | uniq | cut -d: -f2| awk '{printf(\"%s\",$0)}'")
    # CPU总核数=物理CPU个数X每颗物理CPU的核数
    cpuCore = int(cpuPhyNum) * int(cpuNum)

    # 内存频率
    memSpeed = exec_command(
        "dmidecode|grep -A12 'Memory Device' | grep Speed | grep -v Unknown | uniq -c | sed 's/ \t*Speed: /\*/g'|sed 's/^ *//g'| awk '{printf(\"%s\",$0)}'")
    # 内存槽位数
    memCaowei = exec_command("dmidecode|grep -A5 'Memory Device' | grep Size | wc -l| awk '{printf(\"%s\",$0)}'")
    # memInfo = exec_command("dmidecode|grep -A5 'Memory Device' | grep 'Size' | grep -v 'No Module Installed' | awk -F: '{{printf\"%s \",$2}}'")
    # 每个内存条大小
    memInfo = exec_command(
        "dmidecode | grep '^[[:space:]]*Size.*MB$' | uniq -c | sed 's/ \t*Size: /\*/g' | sed 's/^ *//g'| awk '{printf(\"%s\",$0)}'")
    # 内存条数量
    memNum = exec_command(
        "dmidecode|grep -P -A5 'Memory\s+Device'| grep Size | grep -v Range |grep -v No | wc -l | awk '{printf(\"%s\",$0)}'")
    # 总内存大小
    memSize = exec_command(
        "dmidecode|grep -P -A5 'Memory\s+Device'| grep Size | grep -v Range |grep -v No|grep -o '[0-9]\+' | awk '{sum += $1} END {printf sum/1024\"G\"}'")
    # 内存品牌
    memModel = exec_command(
        "dmidecode|grep -P -A16 'Memory\s+Device' | grep 'Manufacturer' | grep -v ':  '|awk -F ':' '{print $2}' | uniq -c | awk -F' ' '{printf $2}'")
    # 内存接口类型
    memType = exec_command(
        "dmidecode -t memory | grep 'Type' | grep -v 'Error '| grep -v 'Type Detail' | grep -v 'Type: Unknown'|uniq | awk -F ':' '{printf $2}'| sed 's/^ *\| *$//g")

    # 网卡型号
    netModel = exec_command("lspci | grep -i eth | awk -F : '{printf $3}'| uniq -c | sed 's/^      [0-9]  //'")

    # 硬盘型号和序列号
    diskModel = exec_command(
        "/opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -aALL -NoLog|grep 'Inquiry Data'| awk -F ':' '{print $2}'| sed 's/^ *\| *$//g'")
    # 硬盘数量
    diskNum = exec_command(
        "/opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -aALL -NoLog|grep 'Inquiry Data' |wc -l | awk '{printf(\"%s\",$0)}'")
    # 每块硬盘大小
    diskSizeOne = exec_command(
        "/opt/MegaRAID/MegaCli/MegaCli64 -PDlist -aALL -NoLog| grep 'Raw Size' | awk '{print $3}' | awk 'BEGIN{i=1} {while(i<NF) print NF,$i,i++}{sum = int($i*1024*1024*1024/1000/1000/1000)}{printf sum\"T\"}'")
    # 总硬盘大小
    diskSize = exec_command(
        "/opt/MegaRAID/MegaCli/MegaCli64 -PDlist -aALL -NoLog| grep 'Raw Size' | awk '{print $3}' | awk 'BEGIN{i=1} {while(i<NF) print NF,$i,i++}{sum = int($i*1024*1024*1024/1000/1000/1000)}{u += sum}END{printf u\"T\"}'")

    # RAID卡型号
    raidcardModel = exec_command(
        "/opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aALL -NoLog| grep 'Product Name'| awk -F ':' '{print $2}'| sed 's/^ *\| *$//g' | awk '{printf(\"%s\",$0)}'")
    # RAID卡缓存
    raidcardMemory = exec_command(
        "/opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aALL -NoLog| grep 'Memory Size' | awk '{printf $4}'")

    # 显卡型号
    gpuModel = exec_command(
        "nvidia-smi -a|grep 'Product Name'| awk -F ':' '{print $2}'| sed 's/^ *\| *$//g' | awk '{printf(\"%s\",$0)}'")
    # 显卡数量
    gpuNum = exec_command("nvidia-smi -a|grep 'Product Name'|wc -l | awk '{printf(\"%s\",$0)}'")

    output = {
        "endpoint": ip,
        "timestamp": int(time.time()),
        "sn": sn,
        "manufacturer": manufacturer,
        "model": model,
        "cpuModel": cpuModel,
        "cpuNum": cpuNum,
        "cpuCore": cpuCore,
        "memModel": memModel,
        "memSpeed": memSpeed,
        "memSize": memSize,
        "memType": memType,
        "memCaowei": memCaowei,
        "memInfo": memInfo,
        "netModel": netModel,
        "diskModel": diskModel,
        "diskNum": diskNum,
        "diskSize": diskSize,
        "raidcardModel": raidcardModel,
        "raidcardMemory": raidcardMemory,
        "gpuModel": gpuModel,
        "gpuNum": gpuNum
    }
    print(output)


getOSInfo()
