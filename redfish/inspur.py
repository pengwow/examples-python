# coding=utf-8
import requests
import copy
import os
from uphmp.common.commons import check_response
from uphmp.utils.util import get_filename_by_path

MAINTENANCE_LIST = dict(
    id=1, sdr=1, fru=1,
    sel=1, ipmi=1, network=1,
    ntp=1, snmp=1, ssh=1,
    kvm=1, authentication=1, syslog=1,
    pef=1, sol=1, smtp=1,
    user=1, dcmi=1, hostname=1
)


class RedfishInspur(object):

    def __init__(self, device_ip):
        # 忽略https协议接口的警告信息
        requests.packages.urllib3.disable_warnings()
        self.device_ip = device_ip
        self.headers = {'Content-Type': 'application/json'}
        self.sessionId = None

    # 1.1 创建会话
    def create_session(self, user, pasd, encrypt_flag=0):
        """
        创建一个新的会话
        在使用 API之前，首先使用该 API来获取 X-CSRFTOKEN，
        接下来的API调用要用到这里获取的 X-CSRFTOKEN,
        并且该 API 响应中的 Cookie（QSESSIONID）也会用到。
        :param user: 用户
        :param pasd: 密码
        :param encrypt_flag: 加密标志 ０:不加密　1:加密
        :return:
        """
        url = 'https://{device_ip}/api/session'.format(device_ip=self.device_ip)
        data = dict(username=user, password=pasd, encrypt_flag=encrypt_flag)
        headers = {'X-Requested-With': "XMLHttpRequest"}
        result = requests.post(url, json=data, headers=headers, verify=False)
        if check_response(result):
            self.headers['Cookie'] = result.headers.get('SetCookie')
            self.headers['X-CSRFTOKEN'] = result.json().get('CSRFToken')
            self.sessionId = self.headers['Cookie']
            return self.sessionId
        else:
            raise Exception(result.content)

    # 1.2 删除会话
    def delete_session(self, token=None, cookie=None):
        """
        删除会话
        :param token:创建会话所返回的token，从CSRFToken获取
        :param cookie:创建会话所返回的cookie，SetCookie获取
        :return:
        """

        url = 'https://{device_ip}/api/session'.format(device_ip=self.device_ip)
        headers = copy.deepcopy(self.headers)
        if token:
            headers['X-CSRFTOKEN'] = token
        if cookie:
            headers['Cookie'] = cookie
        result = requests.delete(url, headers=headers, verify=False)
        if check_response(result):
            return result.json()
        else:
            raise Exception(result.content)

    # BMC ######################################################
    # 9.4 设置升级时的保留列表
    def set_bmc_preserve(self, maintenance_list=None):
        """
        设置升级时的保留列表，默认全部保留
        :param maintenance_list:
        :return:
        """
        url = 'https://{device_ip}/api/maintenance/preserve'.format(device_ip=self.device_ip)
        if not maintenance_list:
            maintenance_list = MAINTENANCE_LIST
        result = requests.put(url=url, data=maintenance_list, headers=self.headers, verify=False)
        if check_response(result):
            return True
        else:
            return False

    # 9.6 触发BMC进入升级模式
    def into_bmc_flash(self):
        """
        BMC将会切换运行级别（runlevel），
        关闭绝大多数服务，
        将 Flash从 rootfsunmount，
        为BMC固件升级做好准备
        :return:
        """
        url = 'https://{device_ip}/api/maintenance/flash'.format(device_ip=self.device_ip)
        result = requests.put(url=url, headers=self.headers, verify=False)
        if check_response(result):
            return True
        else:
            return False

    # 9.7 上传镜像
    def upload_firmware(self, filepath):
        """
        上传镜像到BMC
        :param filepath:本地文件路径
        :return:
        """
        from requests_toolbelt.multipart.encoder import MultipartEncoder
        url = 'https://{device_ip}/api/maintenance/firmware'.format(device_ip=self.device_ip)
        headers = copy.deepcopy(self.headers)

        filename = get_filename_by_path(filepath)
        multipart_encoder = MultipartEncoder(
            fields={
                'fwimage': (filename, open(filepath, 'rb'))
            },
        )
        headers['Content-Type'] = multipart_encoder.content_type
        result = requests.post(url, data=multipart_encoder, headers=headers, verify=False)
        if check_response(result):
            return result.json()
        else:
            return False

    # 9.8 获取上传镜像的状态
    # TODO: To be continued
    # 9.9 将镜像刷写进Flash
    def firmware_upgrade(self, preserve_config=1, flash_status=1):
        """
        将镜像写进Flash
        :param preserve_config:升级过程中配置保留状态： 0 ： 不保留 1 ： 保留
        :param flash_status:刷写Flash状态：
                1 ： 刷写整个固件
                2 ： 基于段的固件刷写
                4 ： 基于版本比较的固件 刷写
                8 ： 双Image刷写
        :return:
        """
        data = dict(preserve_config=preserve_config, flash_status=flash_status)
        url = 'https://{device_ip}/api/maintenance/firmware/upgrade'.format(device_ip=self.device_ip)
        result = requests.put(url=url, headers=self.headers, data=data, verify=False)
        if check_response(result):
            return True
        else:
            return False

    # 9.10 获取Flash刷写进度
    def get_flash_progress(self):
        """
        获取Flash刷写进度
        :return:
        响应包括两种情况，当正在刷新的时候，每次获取到的内容如下：
        { "id": 1, "action": "Flashing...", "progress": "0% done ", "state": 0 } 　　　　　
        当刷新完成后获取到的刷新进度内容如下：
        { "id": 1, "action": "Firmware Update", "progress": "Completed.", "state": 2 }
        """
        url = 'https://{device_ip}/api/maintenance/firmware/flash-progress'.format(device_ip=self.device_ip)
        result = requests.get(url=url, headers=self.headers, verify=False)
        if check_response(result):
            return result.json()
        else:
            return False

    # 9.11 触发BMC在升级结束后重启
    def set_completed_reset(self):
        """
        触发BMC在升级结束后重启
        :return:
        """
        url = 'https://{device_ip}/api/maintenance/reset'.format(device_ip=self.device_ip)
        result = requests.post(url=url, headers=self.headers, verify=False)
        if check_response(result):
            return True
        else:
            return False

    # 升级BMC
    def update_bmc(self, filepath):
        """
        升级BMC
        :param filepath:BMC文件路径
        :return:
        """
        # 设置升级时的保留列表
        self.set_bmc_preserve()
        # 触发BMC进入升级模式
        self.into_bmc_flash()
        # 上传镜像到BMC
        self.upload_firmware(filepath)

        pass

    # BIOS #####################################################
