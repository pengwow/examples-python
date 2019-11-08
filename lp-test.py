import paramiko
import warnings
import os
import time
warnings.filterwarnings("ignore")


def file_get_by_ssh_password(ip, port, username, password, remote_file, location_file):
    """
    基于密码ssh 下载
    :param ip: 目标服务器IP
    :param port: 端口
    :param username: 用户名
    :param password: 密码
    :param remote_file: 远端文件路径
    :param location_file: 本地文件路径
    :return:
    """
    if not port:
        port = 22
    transport = transportPasswordFactory(ip, password, port, username)
    if not transport:
        return
    sftp = sftpFactory(transport)
    getFile(remote_file, location_file, sftp)
    transport.close()


# 下载文件
def getFile(remoteServerFile, destFile, sftp):
    # 将/tmp/test.txt 下载到本地 f_linux.txt
    # sftp.get('/tmp/test.txt', 'f_linux.txt')
    sftp.get(remoteServerFile, destFile)


# 构建sftp对象
def sftpFactory(transport):
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp


# 上传文件
def putFile(destFile, locationFile, sftp):
    destFilePath = destFile[0:int(destFile.rindex('/'))]
    destFilePathList = destFilePath.split('/')
    destFilePathExist = '/'
    for destFilePathPice in destFilePathList:
        if destFilePathPice is '':
            continue
        try:
            destFilePathExist += destFilePathPice + "/"
            sftp.stat(destFilePathExist)
            # print(destFilePathExist + " exist")
        except IOError:
            print(destFilePathExist + " not exist")
            sftp.mkdir(destFilePathExist)
    sftp.put(locationFile, destFile)


# 通过密码构建连接
def transportPasswordFactory(ip, password, port, username):
    try:
        transport = paramiko.Transport((ip, port))
        transport.connect(username=username, password=password)
        return transport
    except Exception:
        print('transportPasswordFactory %s@%s: %s' % (username, ip, Exception))


def filePushBySshPassword(ip, port, username, password, locationFile, destFile):
    transport = transportPasswordFactory(ip, password, port, username)
    if not transport:
        return
    sftp = sftpFactory(transport)
    # # 这里的os.path.join 只是个人需要 可以直接sftp.put(local_file_path, remote_file_path)
    putFile(destFile, locationFile, sftp)
    # sftp.put(os.path.join('/home/update','a.txt'))
    transport.close()


# 构建连接工厂
def sshClientFactory():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return ssh


# 执行命令
def exex_command(cmd, ssh, get_pty, timeout):
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=get_pty, timeout=timeout)
    return stdout


# 通过密码构建连接
def sshConnectPassword(ip, password, port, ssh, username):
    ssh.connect(hostname=ip, port=port, username=username, password=password)


# 根据执行命令返回执行结果
def returnOutResult(ssh, stdout):
    outPutArray = []
    while True:
        nextline = stdout.readline().strip()  # 读取脚本输出内容
        print(nextline.strip())
        # 判断消息为空时,退出循环
        outPutArray.append(nextline.strip())
        if not nextline:
            break
    ssh.close()  # 关闭ssh连接
    return outPutArray


# 通过用户名密码构建ssh 执行命令
def execCommandByPassword(ip, port, username, password, cmd, get_pty, timeout):
    ssh = sshClientFactory()
    sshConnectPassword(ip, password, port, ssh, username)
    # 务必要加上get_pty=True,否则执行命令会没有权限
    stdout = exex_command(cmd, ssh, get_pty, timeout)
    return returnOutResult(ssh, stdout)


if __name__ == "__main__":
    command1 = 'chmod 777 /tmp/storcli64'
    command2 = '/tmp/storcli64 /c0 show > /tmp/storcli64.log'
    command3 = 'df -lh -T'
    ip_list = [
        {"ip": "172.16.11.121", "passwd": "1", 'user': "root"},
    ]
    for item in ip_list:
        print('-----------------{ip}------------------'.format(ip=item['ip']))
        filePushBySshPassword(item['ip'], 22, item['user'], item['passwd'], 'E:/Temp/storcli64', '/tmp/storcli64')

        ret = execCommandByPassword(item['ip'], 22, item['user'], item['passwd'], command1, True, 60)
        ret = execCommandByPassword(item['ip'], 22, item['user'], item['passwd'], command2, True, 60)
        time.sleep(2)
        file_get_by_ssh_password(item['ip'], 22, item['user'], item['passwd'], '/tmp/storcli64.log',
                                 '/tmp/storcli64.log')
        with open('/tmp/storcli64.log', 'r') as fd:
            print(fd.read())
        print('----------------------------------------------')
        if os.path.exists('/tmp/storcli64.log'):
            os.remove('/tmp/storcli64.log')
        ret = execCommandByPassword(item['ip'], 22, item['user'], item['passwd'], command3, True, 60)
        # print(ret)
        print('END-------------------------------------------')
