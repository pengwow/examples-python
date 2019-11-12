# coding=utf-8
# 导包
import sys
import os
import struct
from socket import *

# 全局变量

g_server_ip = ''

g_downloadFileName = ''


# 运行程序格式不正确

def run_test():
    "判断运行程序传入参数是否有错"

    global g_server_ip

    global g_downloadFileName

    if len(sys.argv) != 3:

        print("运行程序格式不正确")

        print('-' * 30)

        print("tips:")

        print("python3 tftp_download.py 192.168.1.1 test.jpg")

        print('-' * 30)

        exit()

    else:

        g_server_ip = sys.argv[1]

        g_downloadFileName = sys.argv[2]

    # print(g_server_ip, g_downloadFileName)


# 主程序

def main():
    run_test()

    # 打包

    sendDataFirst = struct.pack('!H%dsb5sb' % len(g_downloadFileName), 1, g_downloadFileName.encode('gb2312'), 0,
                                'octet'.encode('gb2312'), 0)

    # 创建UDP套接字

    s = socket(AF_INET, SOCK_DGRAM)

    # 发送下载文件请求数据到指定服务器

    s.sendto(sendDataFirst, (g_server_ip, 69))  # 第一次发送, 连接tftp服务器

    downloadFlag = True  # 表示能够下载数据，即不擅长，如果是false那么就删除

    fileNum = 0  # 表示接收文件的序号

    # 以二进制格式创建新文件

    f = open(g_downloadFileName, 'wb')

    while True:

        # 3. 接收服务发送回来的应答数据

        responseData = s.recvfrom(1024)

        # print(responseData)

        recvData, serverInfo = responseData

        # 解包

        packetOpt = struct.unpack("!H", recvData[:2])  # 操作码

        packetNum = struct.unpack("!H", recvData[2:4])  # 块编号

        # print(packetOpt, packetNum)

        # 接收到数据包

        if packetOpt[0] == 3:  # optNum是一个元组(3,)

            # 计算出这次文件的序号，是上一次接收到的+1。

            fileNum += 1

            # 文件超过了65535 那么就又从0开始计数。

            if fileNum == 65536:
                fileNum = 0

            # 包编号是否和上次相等

            if fileNum == packetNum[0]:
                f.write(recvData[4:])  # 写入文件

                fileNum = packetNum[0]

            # 整理ACK的数据包

            ackData = struct.pack("!HH", 4, packetNum[0])

            s.sendto(ackData, serverInfo)



        # 错误应答

        elif packetOpt[0] == 5:

            print("sorry，没有这个文件!")

            downloadFlag = False

            break



        else:

            print(packetOpt[0])

            break

        # 接收完成，退出程序。

        if len(recvData) < 516:
            downloadFlag = True

            print("%s文件下载完毕!" % g_downloadFileName)

            break

    if downloadFlag == True:

        f.close()

    else:

        os.unlink(g_downloadFileName)  # 没有下载的文件，就删除刚创建的文件。


# 调用main函数

if __name__ == '__main__':
    main()
