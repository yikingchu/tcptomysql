from socket import *
import struct
import time
import random
while True:
    try:
        client = socket(AF_INET,SOCK_STREAM)
        client.connect(('127.0.0.1', 8080))
        while True:
            try:
                cmd = "002:dddddddddddddddd" 
                cmdstr = cmd.encode('utf-8')
                client.send(cmdstr)
                time.sleep(5)
                head = client.recv(4)
                size = struct.unpack('i', head)[0]
                cur_size = 0
                result = b''
                while cur_size < size:
                    data = client.recv(1024)
                    cur_size += len(data)
                    result += data
               # print(result.decode('gbk'))   # windows系统默认编码是gbk，解码肯定也要用gbk
            except ConnectionResetError:
                print('服务端已中断')
                client.close()
                break

    except ConnectionRefusedError:
        print('无法连接服务端')
 