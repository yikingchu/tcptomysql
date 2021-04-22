import socketserver
import struct
import subprocess
import MySQLdb
import time
class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:

            print('客户端<%s,%s>已连接' % self.client_address)
            try:
                cmd = self.request.recv(1024).decode('utf-8')
                res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout = res.stdout.read()
                stderr = res.stderr.read()
                head = struct.pack('i', len(stdout + stderr))
                self.request.send(head)
                self.request.send(stdout)
                self.request.send(stderr)
                msg = '我已收到您的请求[%s]，感谢您的关注！' % cmd
                # 打开数据库连接
                db = MySQLdb.connect("127.0.0.1", "root", "root", "mess", charset='utf8' )
                cursor = db.cursor()
                ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                sql = "INSERT INTO u(content,ctime) VALUES ('%s','%s')" % \
                       (cmd,ctime)
                try: 
                # 执行sql语句 
                     cursor.execute(sql) 
                     # 提交到数据库执行 
                     db.commit() 
                except: 
                     # 发生错误时回滚 
                     db.rollback()
                print('%s' % msg)
            except ConnectionResetError:
                print('客户端<%s,%s>已中断连接' % self.client_address)
                self.request.close()
                # 关闭数据库连接
                db.close()
                break


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8080), MyTcpHandler)
    server.serve_forever()
 