from pymavlink import mavutil
import time
import socket
from controller import *
master = mavutil.mavlink_connection("COM13",baud=115200)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('127.0.0.1', 12000))
addr = ("127.0.0.1",5500)

while True:
    try:
        data = master.recv_match().to_dict()
        roll = data['param1'] 
        pitch = data['param2'] 
        yaw = data['param3'] 
        lat = data['param4']
        lon = data['param5']
        alt = data['param6']
        buffer = control(roll,pitch,yaw,lat,lon,alt)
        server_socket.sendto(buffer,addr)
    except:
        pass
