import socket
import time
from windowview import window
import multiprocessing as mp
import struct
import config as cfg
import controller as ctrl
import dynamic as plane
from joystick import *
toDeg = 57.29577
toRad = 0.01745
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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', 12000))
    addr = ("127.0.0.1",5500)
    #p1,p2 = mp.Pipe()
    #wd = window(p1)

    #plane._thrust = 9  # max
    #plane.attack_angle = 3
    while 1:#wd.isRun():    
        if first_run:
            last_time = time.time()
            first_run = 0
        '''    
        if p2.poll():
            data = p2.recv()
            data = struct.unpack('dddd',data)
            cfg.roll_cmd = data[0]
            cfg.pitch_cmd = data[1]
            cfg.yaw_cmd = data[2]
            cfg.altitude_cmd = data[3]
            print(int(cfg.roll_cmd),'  ',int(cfg.pitch_cmd),'  ',int(cfg.yaw_cmd),' ',int(cfg.altitude_cmd))
        '''
        ch2,ch3 = getjoystick()
        #print(ch2*10,'-',ch3*10)
        
        roll,pitch,yaw = plane.loop(0.02,ch2,ch3)
        lat = plane.get_latitude()
        lon = plane.get_longitude()
        alt = plane.get_altitude()
        roll = plane.roll*toDeg
        pitch = plane.pitch*toDeg
        try:
            buffer = ctrl.control2(lat,lon,alt,roll,pitch,yaw)
            server_socket.sendto(buffer,addr)
        except:
            print('error')
            pass
        #buffer = ctrl.control2(37.628715674334124,-122.39334575867426,100,0,0,0)
        
        while(time.time() - last_time < 0.02):
            loop_check = 0 # 50hz
        if loop_check:
            loop_timeout_count +=1
            print('timeout ',loop_timeout_count)
        loop_check = 1
        last_time = time.time()


