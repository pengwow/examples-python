# import sys
import logging
import json
import os
import time
import subprocess
import random
from collections import Counter


def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre + [key, '{}']
                else:
                    for d in dict_generator(value, pre + [key]):
                        yield d
            elif isinstance(value, list):
                if len(value) == 0:
                    yield pre + [key, '[]']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield pre + [key, '()']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            else:
                yield pre + [key, value]
    else:
        yield indict


def json2path(json_str):
    result = list()
    if isinstance(json_str, str):
        data = json.loads(json_str)
    else:
        data = json_str
    for i in dict_generator(data):
        result.append(".".join(i[0:-1]) + ':' + str(i[-1]))
    return result


class OSHardwareInfo(object):
    """
    系统层获取硬件信息
    """

    def __init__(self, ip, user):
        self.ip = ip
        self.user = user
        self.lshw_data = None
        self.dmi_data = None
        self.lscpu_data = None
        self.dmi_memory = None
        self.lshw_network = None
        # 注释掉里面的键值意味着忽略某些类型
        self._DMI_TYPE = {
            0: "BIOS Information",  # BIOS信息 提供商、版本等
            1: "System Information",  # 系统信息包括服务器厂商、服务器的星号、服务器序列号
            2: "Base Board Information",  # 基板信息
            3: "Chassis Information",  # 机箱信息 可以获取服务器的高度，比如1U等。
            4: "Processor Information",  # 处理器信息 每个逻辑CPU的信息，物理CPU数量*核心数量=逻辑CPU数量
            6: "Memory Module Information",  # 内存模块信息
            7: "Cache Information",  # 缓存信息
            8: "Port Connector Information",  # 端口连接器信息
            9: "System Slot Information",  # 系统插槽信息
            10: "On Board Device Information",  # 板载设备信息
            11: "OEM Strings",  # 原始设备制造商字符串
            15: "System Event Log",  # 系统事件日志
            16: "Physical Memory Array",  # 物理内存阵列
            17: "Memory Device",  # 内存 每个内存槽位上查的内存条信息，类型、容量、主频、序列号等
            18: "32-bit Memory Error Information",  # 32位内存错误信息
            19: "Memory Array Mapped Address",  # 内存阵列映射地址
            20: "Memory Device Mapped Address",  # 内存设备映射地址
            23: "System Reset",  # 系统重置
            24: "Hardware Security",  # 硬件安全
            30: "Out-of-band Remote Access",  # 带外远程访问
            32: "System Boot Information",  # 系统引导信息
            33: "64-bit Memory Error Information",  # 64位内存错误信息
            38: "IPMI Device Information",  # IPMI设备信息
            41: "Onboard Device",  # 板载设备
            # 126: "Inactive",
            # 127: "End Of Table"
        }

    def init(self):
        self.lshw_data = self.get_lshw()
        self.dmi_data = self.get_dmi()
        self.lscpu_data = self.get_lscpu()
        self.dmi_memory = self.get_dmi_memory()
        self.lshw_network = self.get_lshw_network()

    def parse_dmi(self, content):
        """
        解析dmidecode命令输出
        :param content: 传递进来dmidecode命令执行的原始输出结果
        :return: 重新组装后的数据字典
        """
        info = {}
        try:
            """
            这里是一个关键点，dmidecode命令输出其实是层级结构的，它使用制表符\t来表示层级，lines可以列表，但后续处理会比较麻烦
            所以这里使用迭代器一个是占用空间少，另外是你每一次传递lines到其他地方当调用next()或者for循环时它都是从上一次的位置
            继续向下，这样对于处理这种dmidecode输出的有层级关系的非结构化数据比较方便。
            """
            lines = iter(content.strip().splitlines())
            while True:
                try:
                    line = next(lines)
                    if line.startswith(b'Handle 0x'):
                        typ = int(str(line).split(',', 2)[1].strip()[len('DMI type'):])
                        if typ in self._DMI_TYPE:
                            if typ not in info:
                                info[self._DMI_TYPE[typ]] = []
                                info[self._DMI_TYPE[typ]].append(self._parse_handle_section(lines))
                            else:
                                info[self._DMI_TYPE[typ]].append(self._parse_handle_section(lines))
                except StopIteration:
                    break
            return info
        except Exception as err:
            logging.error("Error occured in Function parse_dmi err: %s" % str(err))

    @staticmethod
    def _parse_handle_section(lines):
        """
        解析每个type下面的信息，也就是每一个 Handle 0x 下面的信息
        :param lines: 传递所有的内容进来，也就是之前生成的迭代器，而且这个迭代器是接着上面的位置继续向后迭代
        :return: 字典，每个type下面的子信息组成的字典
        """
        data = {}
        title = str(next(lines).strip().decode(encoding='utf-8'))
        try:
            for line in lines:
                line = line.rstrip()
                strline = str(line.strip().decode(encoding='utf-8'))

                if line.startswith(b'\t\t'):
                    data[k].append(strline)
                elif line.startswith(b'\t'):
                    k, v = strline.split(":", 1)
                    if v:
                        data[k] = v.strip()
                    else:
                        data[k] = []
                else:
                    break
        except Exception as err:
            logging.error("Error occured in Function parse_handle_section")
            logging.error("Data section is %s " % title)
            logging.error(str(err))
        return data

    @staticmethod
    def write_lshw_json(content):
        """
        获取lshw命令json数据
        :param content: 传递进来lshw命令执行的原始输出结果,需要缓存到文件在读取
        :return:
        """
        new_data = {}
        temp_json_file = "lshw.json"
        try:
            with open(temp_json_file, 'wb') as json_file:
                json_file.write(content)
            with open(temp_json_file, 'r') as _file:
                new_data = json.load(_file)
        except Exception as err:
            logging.error(str(err))
        finally:
            # 清理临时文件
            if os.path.exists(temp_json_file):
                os.remove(temp_json_file)
        return new_data

    def parse_lshw(self, content):
        """
        解析lshw命令输出
        :param content: 传递进来lshw命令执行的原始输出结果
        :return: 重新组装后的数据字典
        """
        lshw_json = self.write_lshw_json(content)
        return lshw_json

    @staticmethod
    def parse_dmi_memory(content):
        total = list()
        result = ''
        memory_item = str(content).split('\\n')
        for item in memory_item:
            memory_size_list = item.split(':')
            if len(memory_size_list) >= 2:
                _size = memory_size_list[1].strip()
                total.append(_size)
        count = Counter(total)
        for item in count.keys():
            result += "{size} * {unit},".format(size=item,unit=count[item])
        if result:
            result = result[:-1]
        return result

    def get_dmi(self):
        """
        调用系统dmidecode命令获取硬件信息
        :return:
        """
        result = None
        cmd = "sshpass -p password ssh {user}@{ip} dmidecode".format(user=self.user, ip=self.ip)
        try:
            completed_process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if completed_process.returncode == 0:
                data = completed_process.stdout
                result = self.parse_dmi(data)
            else:
                logging.error("Returncode is not 0")
        except Exception as err:
            logging.error(err)
        return result

    def get_dmi_memory(self):
        """
        调用系统dmidecode命令获取硬件信息
        :return:
        """
        result = None
        cmd = 'sshpass -p password ssh {user}@{ip} dmidecode -t memory | grep Size: | grep -v "No Module Installed"'.format(
            user=self.user, ip=self.ip)
        try:
            completed_process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if completed_process.returncode == 0:
                data = completed_process.stdout
                result = self.parse_dmi_memory(data)
            else:
                logging.error("Returncode is not 0")
        except Exception as err:
            logging.error(err)
        return result

    def get_lshw(self):
        """
        调用系统lshw命令获取硬件信息
        :return:
        """

        cmd = "sshpass -p password ssh {user}@{ip} lshw -json".format(user=self.user, ip=self.ip)
        try:
            completed_process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if completed_process.returncode == 0:
                data = completed_process.stdout
                self.lshw_data = self.parse_lshw(data)
            else:
                logging.error("Returncode is not 0")
        except Exception as err:
            logging.error(err)
        return self.lshw_data

    def get_lshw_network(self):
        """

        :return:
        """
        re_list = list()
        file_name = str(random.random())
        cmd = "sshpass -p password ssh {user}@{ip} lshw -json |grep -A6 network".format(user=self.user, ip=self.ip)
        try:
            completed_process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if completed_process.returncode == 0:
                data = completed_process.stdout

                with open(file_name, 'wb') as _file:
                    _file.write(data)
                with open(file_name, 'r') as _file:
                    result = _file.readlines()
                for item in result:
                    line = item.split(':')
                    if len(line) >= 2 and 'product' in line[0]:
                        re_list.append(line[1].strip()[1:-2])
            else:
                logging.error("Returncode is not 0")
        except Exception as err:
            logging.error(err)
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)
        return Counter(re_list)

    def get_lscpu(self):
        cmd = "sshpass -p password ssh {user}@{ip} lscpu".format(user=self.user, ip=self.ip)
        # cmd = "sshpass -p password ssh {user}@{ip} lscpu ".format(user='root', ip='172.16.1.102')
        result = dict()
        try:
            completed_process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if completed_process.returncode == 0:
                data = completed_process.stdout
                filename = './cpu.txt'
                with open(filename, 'wb') as _file:
                    _file.write(data)
                with open(filename, 'r') as _file:
                    new_data = _file.readlines()
                for item in new_data:
                    cpu_line = item.split(':')
                    if len(cpu_line) >= 2:
                        result[cpu_line[0].strip()] = cpu_line[1].strip()
                if os.path.exists(filename):
                    os.remove(filename)
                return result
            else:
                logging.error("Returncode is not 0")
        except Exception as err:
            logging.error(err)

    @property
    def cpu_s(self):
        """
        获取cpu个数
        :return:
        """
        return self.lscpu_data.get('CPU(s)')

    @property
    def cpu_model_name(self):
        """
        获取cpu型号名称
        :return:
        """
        processor = self.dmi_data.get('Processor Information')
        if processor:
            return processor[0].get('Version')
        return ''

    def get_disk(self):
        diskspace = "df"
        diskspace_arg = "-h"
        print("Gathering diskspace information %s command :\n" % diskspace)
        subprocess.call([diskspace, diskspace_arg])

    @property
    def serial_number(self):
        """

        :return:
        """
        result = ''
        if self.lshw_data:
            result = self.lshw_data.get('serial')
        else:
            data = self.get_lshw()
            if data:
                result = data.get('serial')
        return result

    @property
    def mfg(self):
        """

        :return:
        """
        return self.lshw_data.get('vendor')

    @property
    def product(self):
        """

        :return:
        """
        return self.lshw_data.get('product')

    @property
    def memory(self):
        """

        :return:
        """
        return self.dmi_memory

    @property
    def network_card(self):
        result = ""
        for item in self.lshw_network.keys():
            result += "{key} * {count},".format(key=item, count=self.lshw_network[item])
        if result:
            result = result[:-1]
        return result


test = OSHardwareInfo('172.16.1.102', 'root')
test.init()
result = test.serial_number
print(result)
result = test.cpu_model_name
print(result)
result = test.mfg
print(result)
result = test.product
print(result)
result = test.cpu_s
print(result)
result = test.memory
print(result)
result = test.network_card
print(result)
