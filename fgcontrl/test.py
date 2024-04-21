import time
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('127.0.0.1', 12000))
addr = ("127.0.0.1",5500)

init_latitude  = 37.472
init_longitude = -121.170
def control(a,b):
    str_ =''
    str_ += str(a)
    str_ +='\t'
    str_ += str(b)
    str_ +='\n'
    bytess = bytes(str_, 'utf-8')
    return bytess
while True:

    buffer = control(0,1)
    server_socket.sendto(buffer,addr)
    while(time.time() - t < 0.1):
        pass
    t = time.time()
