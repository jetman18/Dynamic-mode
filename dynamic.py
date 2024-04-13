from math import *
from utils import *
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import multiprocessing as mp
import time

# max speed 100 km/h
# max thrust of electric motor 0.9 kg

# convert 
toDeg = 57.29577
toRad = 0.01745

# constan variables
pi           = 3.14159
earth_radius = 6371000  #m
gravity      = -9.81 

# dynamic parameters
air_density     = 1.293
mass            = 0.9         # weight of aircraft
wing_area       = 0.21        # m*m  ref area
wing_ctrl_area  = 0.015       # control surface area
Cd_o            = 0.14        # drag coeffient zero
Cl_0            = 0.04
aileron_Cl      = 0.011
aileron_Cd      = 0.0013
dis_aile2center = 0.12
dis_ele2center  = 0.2
max_aileron_angle = 20        # max control angle

cd_moment_x     = 0.05
cd_moment_y     = 0.1
cd_moment_z     = 0.042
Cm_o            = -0.0
Ixx             = 0.0106
Iyy             = 0.018 
Izz             = 0.0251
#init_latitude  = 37.628715674334124
#init_longitude = -122.39334575867426
init_latitude  = 37.472
init_longitude = -121.170
init_altitude  =  50

# attitude
isFly = 0
alpha = 0  # attack of angle
beta = 0   # sideslip angle

roll = 0          # rad
pitch = 10*toRad  # rad
yaw = 358*toRad   # rad

vx = 0; vy = 0; vz = 0
px = 0; py = 0; pz = 0 
P = 0; Q = 0; R = 0

T = 20          # thrust
ctrl_left = 0
ctrl_right = 0

#f = open("data.txt", "w")
def loop(dt,ch2,ch3):
    global yaw,vx,vy,vz,alpha,T,roll,pitch,yaw,alpha
    global px,py,pz,P,Q,R,isFly,ctrl_left,ctrl_right

    cosx = cos(roll)
    cosy = cos(pitch)
    cosz = cos(yaw)
    sinx = sin(roll)
    siny = sin(pitch)
    sinz = sin(yaw)
    tany = tan(pitch)
    
    # alpha
    v_horizon = sqrt(vx*vx + vy*vy)
    temp_a = atan2(vz,v_horizon)*toDeg
    temp_a =  pitch*toDeg - temp_a

    # beta
    temp_beta  = abs(atan2(vy,vx)*toDeg)
    beta_t = 0
    if  vy >= 0:
        beta_t = temp_beta
    elif  vy <= 0:
        beta_t = 360 - temp_beta
    beta_t = yaw*toDeg - beta_t  # beta 0 - 359

    if beta_t < -180:
        beta_t = beta_t + 360
    elif beta_t > 180:
        beta_t = beta_t - 360
    
    alpha =  temp_a*cosx + beta_t*sinx
    beta  = -temp_a*sinx + beta_t*cosx

    #print(int(pitch*toDeg),' ',int(alpha))

    Cd = (pow(abs(alpha),3.7)/125 + alpha)*3/3625 + Cd_o
    Cl = 0.01*alpha + Cl_0 
    #Cl = constrain(Cl,-1.3,1.3)
    
    # absolute velocity
    Vsqr = vx*vx + vy*vy + vz*vz
    dynamic_p = 0.5*air_density*Vsqr
    L =  dynamic_p*wing_area*Cl
    D = -dynamic_p*wing_area*Cd *0.5

    sinA = sin(alpha*toRad)
    cosA = cos(alpha*toRad)
    cosB = cos(beta*toRad)
    sinB = sin(beta*toRad)
    

    # rotate aero(or wind frame) to body frame
    Fbx =  L*sinA + D*cosA*cosB + T
    Fby = -D*sinB
    Fbz =  L*cosA - D*cosB*sinA
     
    # rotate body frame to inertial frame
    Fex = Fbx*cosy*cosz - Fbz*(sinx*sinz + cosx*cosz*siny) - Fby*(cosx*sinz - cosz*sinx*siny)
    Fey = Fby*(cosx*cosz + sinx*siny*sinz) + Fbz*(cosz*sinx - cosx*siny*sinz) + Fbx*cosy*sinz
    Fez = Fbx*siny + Fbz*cosx*cosy - Fby*cosy*sinx + mass*gravity

    accEx = Fex/mass
    accEy = Fey/mass
    accEz = Fez/mass
    
    # zero acce z on ground
    if accEz > 0 and isFly == 0:
        isFly = 1 
    elif accEz < 0 and isFly == 0:
        accEz = 0 
    
    px += vx*dt + 0.5*accEx*dt*dt
    py += vy*dt + 0.5*accEy*dt*dt
    pz += vz*dt + 0.5*accEz*dt*dt

    '''    
    if time.time() - last_t > 200:
        l =str(px) + ' ' + str(py) + ' ' + str(pz) + '\n'
        f.write(l)
        last_t = time.time()
    '''
    vx +=  accEx*dt 
    vy +=  accEy*dt
    vz +=  accEz*dt

    
    #moment
    '''    
      -  <---- CH2 -----> +
                +
                |
               ch3
                |
                -
    '''
    ch2 = 0.2*pow(ch2,3) + 0.2*ch2
    ch3 = 0.2*pow(ch3,3) + 0.2*ch3


    ctrl_left  = -ch2 + ch3
    ctrl_right =  ch2 + ch3
    ctrl_left = constrain(ctrl_left,-1,1)
    ctrl_right = constrain(ctrl_right,-1,1)
    #scale to deg
    ctrl_left  *= 20
    ctrl_right *= 20

    lift_left   = dynamic_p*wing_ctrl_area*aileron_Cl*ctrl_left
    lift_right  = dynamic_p*wing_ctrl_area*aileron_Cl*ctrl_right
    drag_left   = dynamic_p*wing_ctrl_area*aileron_Cd*ctrl_left
    drag_right  = dynamic_p*wing_ctrl_area*aileron_Cd*ctrl_right

    drag_left = 0
    drag_right = 0

    # pitching moment
    Cm_p = (0.002*pow(alpha,3) + 0.5*alpha)*0.0002 + Cm_o
    #Cm_p = alpha*0.0001
    
    #Cm_p = constrain(Cm_p,-1,1)

    Pitching_moment = dynamic_p*wing_area*Cm_p
    yaw_st = dynamic_p*0.0005*beta
    Mx_total = (lift_right - lift_left)*dis_aile2center -sign(P)*P*P*cd_moment_x
    My_total = (lift_right + lift_left)*dis_ele2center - Pitching_moment  -sign(Q)*Q*Q*cd_moment_y #
    Mz_total = (abs(drag_left) - abs(drag_right))*dis_aile2center - yaw_st*0.01  - sign(R)*R*R*cd_moment_z
    

    P_dot = Mx_total/Ixx
    Q_dot = My_total/Iyy
    R_dot = Mz_total/Izz

    P += P_dot*dt
    Q += Q_dot*dt
    R += R_dot*dt

    # cvt body rate to euler rate
    r_dot   = P + R*cosx*tany + Q*sinx*tany
    p_dot   = Q*cosx - R*sinx
    y_dot   = R*cosx/cosy + Q*sinx/cosy

    #print(int(y_dot*toDeg)),

    roll  += r_dot*dt
    pitch += p_dot*dt
    yaw   += y_dot*dt

    yaw   = swap360(yaw*toDeg)*toRad
    #roll  = swap180(roll*toDeg)*toRad
    #pitch = swap180(pitch*toDeg)*toRad

    

    
    '''    
    if roll*toDeg > 80 or roll*toDeg < -80:
        P = 0
    roll = constrain(roll,-80*toRad,80*toRad)
    
    if pitch*toDeg > 80 or pitch*toDeg < -80:
        Q = 0
    pitch = constrain(pitch,-80*toRad,80*toRad)'''

    return roll*toDeg ,pitch*toDeg,yaw*toDeg
    
 

def get_longitude():
    l = py/earth_radius*toDeg
    return l + init_longitude

def get_latitude():
    l = px/earth_radius*toDeg
    return l + init_latitude

def get_altitude():
    return pz + init_altitude



