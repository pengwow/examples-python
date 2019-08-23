import subprocess


class OSHardwareInfo(object):
    """
    系统层获取硬件信息
    """

    def __init__(self):
        # 注释掉里面的键值意味着忽略某些类型
        self._DMI_TYPE = {
            0: "BIOS Information",  # BIOS信息 提供商、版本等
            1: "System Information",  # 系统信息包括服务器厂商、服务器的星号、服务器序列号
            2: "Base Board Information",
            3: "Chassis Information",  # 可以获取服务器的高度，比如1U等。
            4: "Processor Information",  # 每个逻辑CPU的信息，物理CPU数量*核心数量=逻辑CPU数量
            6: "Memory Module Information",
            7: "Cache Information",
            8: "Port Connector Information",
            9: "System Slot Information",
            10: "On Board Device Information",
            11: "OEM Strings",
            15: "System Event Log",
            16: "Physical Memory Array",
            17: "Memory Device",  # 每个内存槽位上查的内存条信息，类型、容量、主频、序列号等
            18: "32-bit Memory Error Information",
            19: "Memory Array Mapped Address",
            20: "Memory Device Mapped Address",
            23: "System Reset",
            24: "Hardware Security",
            30: "Out-of-band Remote Access",
            32: "System Boot Information",
            33: "64-bit Memory Error Information",
            38: "IPMI Device Information",
            41: "Onboard Device",
            # 126: "Inactive",
            # 127: "End Of Table"
        }

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
            print("Error occured in Function parse_dmi")
            print(err)

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
            print("Error occured in Function parse_handle_section")
            print("Data section is %s " % title)
            print(err)
        return data

    def get_dmi(self):
        cmd = "sshpass -p password ssh {user}@{ip} dmidecode".format(user='root', ip='172.16.1.102')
        try:
            completed_process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if completed_process.returncode == 0:
                data = completed_process.stdout
                print(self.parse_dmi(data))
            else:
                print("Returncode is not 0")
        except Exception as err:
            print(err)


sss = OSHardwareInfo()

sss.get_dmi()