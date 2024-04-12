from pymavlink import mavutil
import time
import socket
from controller import *
master = mavutil.mavlink_connection("COM13",baud=19200)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('127.0.0.1', 12000))
addr = ("127.0.0.1",5500)

while True:
    try:
        data = master.recv_match().to_dict()
        aile = data['param1']  # 1000 - 2000
        ele = data['param2']  # 1000 - 2000
        throttle = data['param3'] # 1000 - 2000  -> 0 - 9 (N)
        # scale factor
        #throttle = (throttle - 1000)*0.001 
        #aile = (aile - 1500)/500
        #ele = (ele - 1500)/500
        
        #mixer_aile = (ele - aile)/2
        #mixer_ele  = (aile + ele)/2
        mixer_aile = constrain(aile,-1,1)
        mixer_ele = constrain(ele,-1,1)
        buffer = control(mixer_aile*1.3,-mixer_ele,1)
        server_socket.sendto(buffer,addr)

    except:
        pass
