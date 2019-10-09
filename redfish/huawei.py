# coding=utf-8
import requests


class HWRedfish(object):
    def __init__(self, device_ip):
        # 忽略https协议接口的警告信息
        requests.packages.urllib3.disable_warnings()
        self.device_ip = device_ip
        self.headers = {'Content-Type': 'application/json'}

    # 4.2.1 创建会话
    def create_session(self, user, pasd):
        """
        创建会话，返回X-Auth-Token
        :param user: 用户
        :param pasd: 密码
        :return:
        """
        url = 'https://{device_ip}/redfish/v1/SessionService/Sessions'.format(device_ip=self.device_ip)
        data = dict(UserName=user, Password=pasd)
        result = requests.post(url, json=data, headers=self.headers, verify=False)
        if result.status_code in [200, 201, 202]:
            self.headers['X-Auth-Token'] = result.headers.get('X-Auth-Token')
        else:
            raise Exception(result.content)

    # 3.7.3 查询指定可升级固件资源信息
    def query_firmware_info(self, softid):
        """
        查询指定可升级固件资源信息
        :param softid:可升级固件资源的ID 可通过可升级固件集合资 源获得
        :return:
        """
        url = 'https://{device_ip}/redfish/v1/UpdateService/FirmwareInventory/{softid}'.format(device_ip=self.device_ip,
                                                                                               softid=softid)
        result = requests.get(url, headers=self.headers, verify=False)
        if result.status_code in [200, 201, 202]:
            return result.json()
        else:
            raise Exception(result.content)

    # 3.7.4 升级固件
    def update_firmware(self, filepath, protocol):
        """
        升级固件
        :param filepath:升级包所在路径
                        升级包的URL，支持的 大长度为256个字符（支持 本地tmp目录升级）
                        例如：“sftp://username:password@10.10.10.191/tmp/package/cpldimage.hpm”
                        本地升级：“/tmp/cpldimage.hpm”
        :param protocol:下载升级包时使用的协议HTTPS/SCP/SFTP/CIFS/TFTP/NFS
                        如果是本地升级则不需要该 字段。
        :return:
        """
        url = 'https://{device_ip}/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate'.format(
            device_ip=self.device_ip)
        data = dict(ImageURI=filepath, TransferProtocol=protocol)
        result = requests.post(url, json=data, headers=self.headers, verify=False)


client = HWRedfish('172.16.11.14')
client.create_session('hy', '123')
dd = client.query_firmware_info('Bios')
print(dd)
