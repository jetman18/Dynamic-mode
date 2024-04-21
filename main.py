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
if __name__ == '__main__':  # NOTE: 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', 12000))
    addr = ("127.0.0.1",5500)
    logfile =  open('logfile.txt',"w")
    p1,p2 = mp.Pipe()
    wd_view = window(p1)

    # pid
    roll_rate_pid  = pidcontroller(2,0.0,0,100,100,loop_dt)
    roll_angle_pid = pidcontroller(10,0,0,0,0,loop_dt)

    pitch_rate_pid  = pidcontroller(5,0,0.0,100,100,loop_dt)
    pitch_angle_pid = pidcontroller(10,0,0,0,0,loop_dt)
    
    timer_at_start = time.time()
    timer=time.time()
    count = 0
    pitch_cmd = 0
    while wd_view.isClose():    
        if first_run:
            last_time = time.time()
            first_run = 0
            continue
          
        '''        if p2.poll():
            data = p2.recv()
            data = struct.unpack('dddd',data)
            cfg.roll_cmd = data[0]
            cfg.pitch_cmd = data[1]
            cfg.yaw_cmd = data[2]
            cfg.altitude_cmd = data[3]'''
        
        ch2,ch3,throtlle = getjoystick()
        
        # attitude process
        plane.loop(loop_dt)
        lat = plane.get_latitude()
        lon = plane.get_longitude()
        alt = plane.get_altitude()
        
        yaw = plane.get_yaw()
        
    
        # roll pid
        roll_cmd = ch2*70
        pitch_cmd = ch3*70
        thrust = throtlle*1000 + 1000


        # roll pid
        roll = plane.get_roll()
        P = plane.get_roll_rate()
        r_angle_pid = roll_angle_pid.pid_cal(roll,roll_cmd)
        r_rate_pid = -roll_rate_pid.pid_cal(-P,r_angle_pid)

        # pitch pid
        pitch = plane.get_pitch()
        Q = plane.get_pitch_rate()
        print(Q)
        p_angle_pid = pitch_angle_pid.pid_cal(pitch,pitch_cmd)
        p_rate_pid  = -pitch_rate_pid.pid_cal(-Q,p_angle_pid)

        vel = plane.get_velocity()
        pid_scale = 900/max(900,vel*vel)
        r_rate_pid = r_rate_pid*pid_scale
        p_rate_pid = p_rate_pid*pid_scale

        servo_left  = 1500 + r_rate_pid - p_rate_pid
        servo_right = 1500 - r_rate_pid - p_rate_pid

        # imu 
        #p,q,r,ax,ay,az = plane.imu_get()
        #print(round(ax,2),' ',round(ay,2),' ',round(az,2))
        #print(int(servo_left),'  ',int(servo_right))

        # munual controll
             
        #ch2 = 0.5*pow(ch2,3) + 0.15*ch2
        #ch3 = 0.5*pow(ch3,3) + 0.15*ch3 
        #servo_left  = 1500  + ch3*500  - ch2*500
        #servo_right = 1500  + ch3*500  + ch2*500
        #servo_left  += ch3*500#  - ch2*500
        #servo_right += ch3*500#  + ch2*500
  
        servo_left = constrain(servo_left,1000,2000)
        servo_right = constrain(servo_right,1000,2000)
        '''
        if time.time() - timer > 0.1:
            count += 1
            if count > 50 and count < 90:
                roll_cmd = 30
            if count > 90:
                roll_cmd = 0
            if count > 120:
                break
            #logfile.write(str(round(pitch,3)) +' '+ str(round(pitch_cmd+10,3))+' '+ str(round(time.time()-timer_at_start,3))+'\n')
            timer = time.time()
        '''
        
        #attitude_axis.append(roll)
        #cmd_axis.append(roll_cmd)
        #time_axis.append(time.time()-timer_at_start)
        plane.control_cmd(2000,servo_left,servo_right)
        try:
            buffer = ctrl.control2(lat,lon,alt,roll,pitch,yaw)
            server_socket.sendto(buffer,addr)
        except:
            print('error')
            pass
        
        wd_view.setAttitude(round(roll,2),round(pitch,2),int(yaw),int(alt),round(vel*3.6,2),round(plane.total_fly(),2),plane.get_R())
        
        while(time.time() - last_time < loop_dt):
            loop_check = 0 # 50hz
        if loop_check:
            loop_timeout_count +=1
            print('timeout ',loop_timeout_count)
        loop_check = 1
        last_time = time.time()
        


'''
import matplotlib.pyplot as plt
import numpy as np


plt.plot(time_axis,attitude_axis)
plt.plot(time_axis,cmd_axis)
plt.grid()
plt.suptitle("pitch control", size=14)
plt.xlabel('time (s)', fontsize=10)
plt.ylabel('pitch (deg)', fontsize=10)
plt.show()
'''