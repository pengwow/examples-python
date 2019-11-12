# coding=utf-8


# 导包

import sys

import struct

from socket import *

from threading import Thread

'''

利用多线程的机制，来实现tftp服务器同时进行上传和下载功能。

'''


# 客户端上传线程

def upload_thread(fileName, clientInfo):
    "负责处理客户端上传文件"

    fileNum = 0  # 表示接收文件的序号

    # 以二进制方式打开文件

    f = open(fileName, 'wb')

    # 创建UDP套接字

    s = socket(AF_INET, SOCK_DGRAM)

    # 打包

    sendDataFirst = struct.pack("!HH", 4, fileNum)

    # 回复客户端上传请求

    s.sendto(sendDataFirst, clientInfo)  # 第一次用随机端口发送

    while True:

        # 接收客户端发送的数据

        responseData = s.recvfrom(1024)  # 第二次客户连接我随机端口

        # print(responseData)

        recvData, clientInfo = responseData

        # print(recvData, clientInfo)

        # 解包

        packetOpt = struct.unpack("!H", recvData[:2])  # 操作码

        packetNum = struct.unpack("!H", recvData[2:4])  # 块编号

        # print(packetOpt, packetNum)

        # 客户端上传数据

        if packetOpt[0] == 3 and packetNum[0] == fileNum:

            # 　保存数据到文件中

            f.write(recvData[4:])

            # 　打包

            sendData = struct.pack("!HH", 4, fileNum)

            # 回复客户端ACK信号

            s.sendto(sendData, clientInfo)  # 第二次用随机端口发

            fileNum += 1

            if len(recvData) < 516:
                print("用户" + str(clientInfo), end='')

                print('：上传' + fileName + '文件完成！')

                break

    # 关闭文件

    f.close()

    # 关闭UDP套接字

    s.close()

    # 退出上传线程

    exit()


# 客户端下载线程

def download_thread(fileName, clientInfo):
    "负责处理客户端下载文件"

    # 创建UDP套接字

    s = socket(AF_INET, SOCK_DGRAM)

    fileNum = 0  # 表示接收文件的序号

    try:

        f = open(fileName, 'rb')

    except:

        # 打包

        errorData = struct.pack('!HHHb', 5, 5, 5, fileNum)

        # 发送错误信息

        s.sendto(errorData, clientInfo)  # 文件不存在时发送

        exit()  # 退出下载线程

    while True:

        # 从本地服务器中读取文件内容512字节

        readFileData = f.read(512)

        fileNum += 1

        # 打包

        sendData = struct.pack('!HH', 3, fileNum) + readFileData

        # 向客户端发送文件数据

        s.sendto(sendData, clientInfo)  # 数据第一次发送

        if len(sendData) < 516:
            print("用户" + str(clientInfo), end='')

            print('：下载' + fileName + '文件完成！')

            break

        # 第二次接收数据

        responseData = s.recvfrom(1024)

        # print(responseData)

        recvData, clientInfo = responseData

        # print(recvData, clientInfo)

        # 解包

        packetOpt = struct.unpack("!H", recvData[:2])  # 操作码

        packetNum = struct.unpack("!H", recvData[2:4])  # 块编号

        # print(packetOpt, packetNum)

        if packetOpt[0] != 4 or packetNum[0] != fileNum:
            print("文件传输错误！")

            break

    # 关闭文件

    f.close()

    # 关闭UDP套接字

    s.close()

    # 退出下载线程

    exit()


# main函数

def main():
    # 创建ＵＤＰ套接字

    s = socket(AF_INET, SOCK_DGRAM)

    # 解决重复绑定端口

    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 绑定任意IP，端口号69

    s.bind(('', 69))

    print("tftp服务器成功启动!")

    print("正在运行中...")

    while True:

        # 接收客户端发送的消息

        recvData, clientInfo = s.recvfrom(1024)  # 第一次客户连接69端口

        # print(clientInfo)

        # 　解包

        if struct.unpack('!b5sb', recvData[-7:]) == (0, b'octet', 0):

            opcode = struct.unpack('!H', recvData[:2])  # 操作码

            fileName = recvData[2:-7].decode('gb2312')  # 文件名

            # 请求下载

            if opcode[0] == 1:

                t = Thread(target=download_thread, args=(fileName, clientInfo))

                t.start()  # 启动下载线程



            # 请求上传

            elif opcode[0] == 2:

                t = Thread(target=upload_thread, args=(fileName, clientInfo))

                t.start()  # 启动上传线程

    # 关闭UDP套接字

    s.close()


# 调用main函数

if __name__ == '__main__':
    main()
