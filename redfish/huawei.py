# coding=utf-8
import requests
import copy
import os
import time


def get_filename_by_path(filepath):
    """
    获取文件名+后缀
    :param filepath:文件路径
    :return: xxx.x
    """
    return os.path.split(filepath)[1]


def dict_get(src, objkey, default):
    tmp = src
    for k, v in tmp.items():
        if k == objkey:
            return v
        else:
            if isinstance(v, dict):
                result = dict_get(v, objkey, default)
                if result is not default:
                    return result
    return default


class HWRedfish(object):
    def __init__(self, device_ip):
        # 忽略https协议接口的警告信息
        requests.packages.urllib3.disable_warnings()
        self.device_ip = device_ip
        self.headers = {'Content-Type': 'application/json'}
        self.sessionId = None

    # 3.5.2 修改会话服务信息
    def modify_session(self,):
        """

        :return:
        """

    # 3.5.3 创建会话
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
        if 200 <= result.status_code <= 299:
            self.headers['X-Auth-Token'] = result.headers.get('X-Auth-Token')
            self.sessionId = result.json().get('Id')
            print(self.headers)
            print(self.sessionId)
        else:
            raise Exception(result.content)

    # 3.7.3 查询指定可升级固件资源信息
    def query_firmware_info(self, softid):
        """
        查询指定可升级固件资源信息
        :param softid:可升级固件资源的ID 可通过可升级固件集合资 源获得
        默认有：ActiveBMC，Bios
        :return:
        """
        url = 'https://{device_ip}/redfish/v1/UpdateService/FirmwareInventory/{softid}'.format(device_ip=self.device_ip,
                                                                                               softid=softid)
        result = requests.get(url, headers=self.headers, verify=False)
        if 200 <= result.status_code <= 299:
            return result.json()
        else:
            raise Exception(result.content)

    # 3.7.4 升级固件
    def update_firmware(self, filepath, protocol=None):
        """
        升级固件
        :param filepath:升级包所在路径
                        升级包的URL，支持的 大长度为256个字符（支持 本地tmp目录升级）
                        例如：“sftp://username:password@10.10.10.191/tmp/package/cpldimage.hpm”
                        本地升级：“/tmp/cpldimage.hpm”
        :param protocol:下载升级包时使用的协议HTTPS/SCP/SFTP/CIFS/TFTP/NFS
                        如果是本地升级则不需要该 字段。
        :return: 任务的ID
        """
        url = 'https://{device_ip}/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate'.format(
            device_ip=self.device_ip)
        data = dict(ImageURI=filepath)
        if protocol:
            data['TransferProtocol'] = protocol

        result = requests.post(url, json=data, headers=self.headers, verify=False)
        if 200 <= result.status_code <= 299:
            result = result.json()
            return result.get('Id')
        else:
            raise Exception(result.content)

    # 3.8.3 查询指定任务资源信息
    def task_info(self, taskid):
        """
        查询服务器指定任务资源的信息
        :param taskid: 待查询任务的ID
        :return:
        """
        url = 'https://{device_ip}/redfish/v1/TaskService/Tasks/{taskid}'.format(device_ip=self.device_ip,
                                                                                 taskid=taskid)
        result = requests.get(url, headers=self.headers, verify=False)
        if 200 <= result.status_code <= 299:
            result = result.json()
            # 发生异常
            if 'Exception' == result.get('TaskState'):
                raise Exception(result.get('Message'))
            # 完成
            elif 'Completed' == result.get('TaskState'):
                return 'Completed'
            # 运行中则返回进度
            elif 'Running' == result.get('TaskState'):
                return dict_get(result, 'TaskPercentage', False)
            else:
                raise Exception(str(result))
        else:
            raise Exception(result.content)

    # 3.7.5 文件上传
    def upload_files(self, filepath):
        """
        通过redfish接口进行文件上传，上传成功后文件被放在/tmp/web目录下。
        :param filepath:本地文件路径
        :return:
        """
        from requests_toolbelt.multipart.encoder import MultipartEncoder
        url = 'https://{device_ip}/redfish/v1/UpdateService/FirmwareInventory'.format(device_ip=self.device_ip)
        headers = copy.deepcopy(self.headers)

        filename = get_filename_by_path(filepath)
        multipart_encoder = MultipartEncoder(
            fields={
                'imgfile': (filename, open(filepath, 'rb')),
                "submit": (None, 'uploadfile')
            },
        )
        headers['Content-Type'] = multipart_encoder.content_type
        # files = {
        #     "imgfile": (filename, open(filepath, 'rb').read(),'application/octet-stream'),
        #     "submit": (None, 'uploadfile')
        # }
        # 设置代理 给fidder抓包工具抓取使用
        # proxies = {'http': 'http://172.16.11.122:8888', 'https': 'http://172.16.11.122:8888'}
        # result = requests.post(url, data=multipart_encoder, proxies=proxies, headers=headers, verify=False)
        result = requests.post(url, data=multipart_encoder, headers=headers, verify=False)
        # result = requests.request('POST',url,files=files,headers=headers,verify=False)
        # result = requests.post(url, files=files, headers=headers, verify=False)
        if result.status_code != 202:
            # 发生异常
            print('XXXXXXXXXXXXXXXXXXXXX')
            print(result.content)
            self.delete_session()
            # raise Exception(str(result.content))
        else:
            print('OK!!!!!!!!!!!')
            return os.path.join('/tmp/web/', filename)

    # 3.5.6 删除指定会话
    def delete_session(self, session_id=None):
        """
        删除指定会话
        :param session_id:待删除的会话ID
        :return:
        """
        if not session_id:
            session_id = self.sessionId
        url = 'https://{device_ip}/redfish/v1/SessionService/Sessions/{session_id}'.format(device_ip=self.device_ip,
                                                                                           session_id=session_id)
        result = requests.delete(url, headers=self.headers, verify=False)
        if 200 <= result.status_code <= 299:
            return True
        else:
            raise Exception("删除会话失败 %s" % str(result.content))

    # 3.3.4 重启服务器
    def computer_system_reset(self, system_id=1):
        """
        重启服务器
        :param system_id:系统资源的ID
        针对机架服务器，取值 为1 l 针对高密服务器，
        取值 为BladeN（N表示节点 槽位号），
        例如 “Blade1” l 针对刀片服务器，
        取值 可以为BladeN（N表示 计算节点槽位号）或 SwiN（N表示交换模块 槽位号），
        例如 “Swi1”
        :return:
        """
        url = 'https://{device_ip}/redfish/v1/Systems/{system_id}/Actions/ComputerSystem.Reset'.format(
            device_ip=self.device_ip,
            system_id=str(system_id))
        # 强制下电
        value = 'ForceOff'
        data = dict(ResetType=value)
        result = requests.post(url, json=data, headers=self.headers, verify=False)
        if 200 <= result.status_code <= 299:
            print(result.json())
            # 等待
            time.sleep(30)
            # 上电
            value = 'On'
            data = dict(ResetType=value)
            result = requests.post(url, json=data, headers=self.headers, verify=False)
            if 200 <= result.status_code <= 299:
                print(result.json())
            else:
                raise Exception(result.content)
        else:
            raise Exception(result.content)


if __name__ == '__main__':
    # 接收包，缓存本地的nfs目录
    nfs_filepath = ''
    # 创建redfish对象
    client = HWRedfish('172.16.11.14')
    session = client.create_session('hy', '123')
    client.computer_system_reset()
    # filepath = "E:\\Temp\\biosimage.hpm"
    # # filepath = '/mnt/e/Temp/biosimage.hpm'
    # webpath = client.upload_files(filepath)
    # print(webpath)
    # taskid = client.update_firmware(webpath)
    # print(taskid)
    # count = 0
    # while True:
    #     count += 1
    #     if count >= 20:
    #         break
    #     status = client.task_info(taskid)
    #     print(status)
    #     time.sleep(2)
    client.delete_session(session)
    # while True:
    #     result = client.task_info(taskid)
    #     if 'Completed' == result:
    #         break
    #     else:
    #         print(result)
