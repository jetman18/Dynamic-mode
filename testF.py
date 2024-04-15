import socket
import time
from windowview import window
import multiprocessing as mp
import struct
import config as cfg
import controller as ctrl
import dynamic2 as plane
from joystick import *
from pid import pidcontroller
from utils import *

'''toDeg = 57.29577
toRad = 0.01745
loop_dt = 0.02
#cfg.home_lat = 37.628715674334124
#cfg.home_lon = -122.39334575867426
first_run = 1
loop_check = 1
loop_timeout_count = 0

roll_cmd = 0
pitch_cmd = 0
yaw_cmd = 0
altitude_cmd = 10
i = 0
if __name__ == '__main__':  # NOTE: 

    p1,p2 = mp.Pipe()
    wd_view = window(p1)

    

    while wd_view.isClose():    

        while(time.time() - last_time < loop_dt):
            pass
        last_time = time.time()
'''

def control2(ele_trim,ele):
    str_ =''
    str_ += str(ele_trim)
    str_ +='\t'
    str_ += str(ele)
    str_ +='\n'
    bytess = bytes(str_, 'utf-8')
    return bytess

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('127.0.0.1', 12000))
addr = ("127.0.0.1",5500)

while 1:
    buffer = control2(0,-1)
    server_socket.sendto(buffer,addr)
    time.sleep(1)



