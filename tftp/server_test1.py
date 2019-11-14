# coding=utf-8
from socket import *
import time
import struct


class TFTPServer(object):
    # 操作码
    DOWNLOAD = 1
    UPLOAD = 2
    DATA = 3
    ACK = 4
    ERROR = 5

    def __init__(self):
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)
        self.serverSocket.bind(("", 69))
        self.recvData = list()
        self.recvAddr = None
        self.cmdType = 0

    def run(self):
        while True:
            print("#" * 30)
            print("等待客户端连接！")
            self.listen()

            if self.cmdType == self.DOWNLOAD:
                self.download()
            elif self.cmdType == self.UPLOAD:
                self.upload()

    def listen(self):
        # 等待client链接
        self.recvData, self.recvAddr = self.serverSocket.recvfrom(1024)
        self.cmdType = struct.unpack("!H", self.recvData[:2])[0]

    # 客户端请求下载
    def download(self):
        # 新建随机端口
        udpSocket = socket(AF_INET, SOCK_DGRAM)

        fileReq = None
        try:
            # 读取客户端要下载的文件名
            print(self.recvData[-7:])
            fileReqName = self.recvData[2:-7].decode()
            print(fileReqName)
            print("客户端请求下载文件：%s" % fileReqName)
            # 打开文件
            try:
                fileReq = open(fileReqName, "rb")
            except:
                print("文件 《%s》 不存在" % fileReqName)
                # 向 client 发送异常信息
                errInfo = struct.pack("!HHHb", 5, 5, 5, 0)
                udpSocket.sendto(errInfo, self.recvAddr)
                return False

            # 初始化块编号
            frameNum = 1

            while True:
                fileData = fileReq.read(512)
                # 打包
                # frameData = struct.pack(str("!HH%ds" % len(fileData)), 3, frameNum, fileData)
                frameData = struct.pack(str("!HH"), 3, frameNum) + fileData
                # 发送
                for i in range(0, 3):
                    udpSocket.sendto(frameData, self.recvAddr)

                    # 若文件已发送完成
                    if len(fileData) < 512:
                        print("文件发送完成！")
                        fileReq.close()
                        fileReq = None
                        return True

                    # 等待client响应
                    # 接收数据
                    self.recvData, self.recvAddr = udpSocket.recvfrom(1024)
                    cmdType, recvFrameNum = struct.unpack("!HH", self.recvData[:4])
                    if cmdType == self.ACK and recvFrameNum == frameNum:
                        break
                    elif i == 3:
                        print("链接异常，取消发送")
                        # 向 client 发送异常信息
                        errInfo = struct.pack("!HHHb", 5, 5, 5, 0)
                        udpSocket.sendto(errInfo, self.recvAddr)
                        exit()

                # 编号+1
                frameNum += 1
        finally:
            if fileReq != None:
                fileReq.close()

    # 客户端请求上传
    def upload(self):
        # 新建随机端口
        udpSocket = socket(AF_INET, SOCK_DGRAM)

        # 发送相应，确认开始接收
        ack = struct.pack("!HH", self.ACK, 0)
        udpSocket.sendto(ack, self.recvAddr)

        # 帧计数，用于数据校验
        recvFrameNum = 1
        # 等待 client 数据
        while True:
            # 接收数据
            recvData, recvAddr = udpSocket.recvfrom(1024)
            # 数据帧： 操作码2 快编号2 数据n
            cmdType, frameNum = struct.unpack("!HH", recvData[:4])
            # 判断接收的是否是“数据”
            if cmdType == self.DATA and frameNum == recvFrameNum:
                print("接收到第%d帧数据！" % frameNum)  # for test
                # 打开文件
                if frameNum == 1:
                    fileRecv = open("upload.txt", "ab")
                    fileRecv.write(b"#" * 30 + time.strftime("%Y-%m-%d %H:%M:%S").encode() + b"#" * 30 + b"\n")

                fileRecv.write(recvData[4:])

                # 响应 : 操作码2 快编号2
                ack = struct.pack("!HH", self.ACK, frameNum)
                udpSocket.sendto(ack, recvAddr)

                # 判断是否发送完
                if len(recvData) < 516:
                    fileRecv.close()
                    fileRecv = None
                    print("接收完毕， 关闭文件。")
                    break

                # 计数+1
                recvFrameNum += 1

            elif cmdType == self.ERROR:
                print("客户端连接异常，退出！")
                break


server = TFTPServer()
server.run()
