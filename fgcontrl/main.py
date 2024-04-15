from pymavlink import mavutil
import time
import socket
from controller import *
try:
    master = mavutil.mavlink_connection("COM13",baud=115200)
except:
    pass
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('127.0.0.1', 12000))
addr = ("127.0.0.1",5500)

init_latitude  = 37.472
init_longitude = -121.170

t = 0

while True:
    try:

         
        data = master.recv_match().to_dict()
        roll = data['param1'] 
        pitch = data['param2'] 
        yaw = data['param3'] 
        lat = data['param4']
        lon = data['param5']
        alt = data['param6']
        
        #print(int(roll),' ',int(pitch),' ',int(alt))

        #buffer = control(init_longitude,init_latitude,0,0,0,0)
        buffer = control(roll,pitch,yaw,lat,lon,alt)
        server_socket.sendto(buffer,addr)
    except:
        pass
    while(time.time() - t < 0.001):
        pass
    t = time.time()
