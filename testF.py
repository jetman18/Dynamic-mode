
import socket
import time
from windowview import window
import multiprocessing as mp
import struct
import config as cfg
import controller as ctrl
import dynamic as plane
from joystick import *
from pid import pidcontroller
from utils import *


toDeg = 57.29577
toRad = 0.01745
loop_dt = 0.02

first_run = 1
loop_check = 1
loop_timeout_count = 0

roll_cmd = 0
pitch_cmd = 0
yaw_cmd = 0
altitude_cmd = 10
i = 0

roll_cmd = 0

attitude_axis = []
cmd_axis=[]
time_axis=[]
last_time = 0
if __name__ == '__main__':  # NOTE: 

    p1,p2 = mp.Pipe()
    wd_view = window(p1)

  
    while wd_view.isClose():    
    
        
     

        
 
        while(time.time() - last_time < loop_dt):
            loop_check = 0 # 50hz
        if loop_check:
            loop_timeout_count +=1
            print('timeout ',loop_timeout_count)
        loop_check = 1
        last_time = time.time()
        
