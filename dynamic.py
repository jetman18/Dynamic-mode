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
mass            = 0.9         # weight of aircraft  0.9
wing_area       = 0.21        # m*m  ref area
wing_ctrl_area  = 0.015       # control surface area
rudder_area     = 0.0168
Cd_o            = 0.14        # drag coeffient zero
Cl_0            = 0.03
aileron_Cl      = 0.011
aileron_Cd      = 0.0013
dis_aile2center = 0.12
dis_ruderr2CG   = 0.12
dis_ele2center  = 0.2
max_aileron_angle = 20        # max control angle

cd_moment_x     = 0.05
cd_moment_y     = 0.1
cd_moment_z     = 0.2
Cm_o            = -0.0
Ixx             = 0.0106
Iyy             = 0.018 
Izz             = 0.0251
init_latitude  = 37.472
init_longitude = -121.170
init_altitude  =  500

# attitude
r_dot   = 0
p_dot   = 0
y_dot   = 0
isFlying = 0
alpha = 0  # attack of angle
beta = 0   # sideslip angle
velocity = 0

roll = 0          # rad
pitch = 0  # rad
yaw = 180*toRad   # rad

vex = 0; vey = 0; vez = 0
px = 0; py = 0; pz = 0 
P = 0; Q = 0; R = 0
U = 0; V = 0; W = 0

T_max = 15 # thrust (N)
T = 0
ctrl_left = 0
ctrl_right = 0

accx = 0
accy = 0
accz = 0

total_fly_dis = 0

def control_cmd(thrust,servoL,servoR):
    global ctrl_left,ctrl_right,T
    ctrl_left = (servoL - 1500)/500
    ctrl_right = (servoR - 1500)/500
    T = T_max*(thrust - 1000)/1000

def loop(dt):
    global yaw,vex,vey,vez,alpha,T,roll,pitch,yaw,alpha,accx,ch3,P,Q,R
    global px,py,pz,P,Q,R,isFlying,ctrl_left,ctrl_right,U,V,W,velocity
    global p_dot,r_dot,accy,accz,total_fly_dis

    cosx = cos(roll)
    cosy = cos(pitch)
    cosz = cos(yaw)
    sinx = sin(roll)
    siny = sin(pitch)
    sinz = sin(yaw)
    tany = tan(pitch)
    
    # alpha
    v_horizon = sqrt(vex*vex + vey*vey)
    temp_a = atan2(vez,v_horizon)*toDeg
    temp_a =  pitch*toDeg - temp_a

    # beta
    temp_beta  = abs(atan2(vey,vex)*toDeg)
    beta_t = 0
    if  vey >= 0:
        beta_t = temp_beta
    elif  vey <= 0:
        beta_t = 360 - temp_beta
    beta_t = yaw*toDeg - beta_t  # beta 0 - 359

    if beta_t < -180:
        beta_t = beta_t + 360
    elif beta_t > 180:
        beta_t = beta_t - 360
    
    alpha =  temp_a*cosx + beta_t*sinx
    beta  = -temp_a*sinx + beta_t*cosx

    Cd = (pow(abs(alpha),3.7)/125 + alpha)*3/3625 + Cd_o
    Cl = 0.01*alpha + Cl_0 
    Cl_rudder = 0.01*beta
    #Cl = constrain(Cl,-1.3,1.3)
    
    # absolute velocity
    Vsqr = vex*vex + vey*vey + vez*vez
    velocity = sqrt(Vsqr)
    dynamic_p = 0.5*air_density*Vsqr
    Side_force = dynamic_p*rudder_area*Cl_rudder
    L =  dynamic_p*wing_area*Cl
    D = -dynamic_p*wing_area*Cd *0.5

    sinA = sin(alpha*toRad)
    cosA = cos(alpha*toRad)
    cosB = cos(beta*toRad)
    sinB = sin(beta*toRad)

    # rotate aero(or wind frame) to body frame
    Fbx = L*sinA + D*cosA*cosB + Side_force*cosA*sinB
    Fby = Side_force*cosB - D*sinB
    Fbz = L*cosA - D*cosB*sinA - Side_force*sinA*sinB

    # rotate gravity to body frame
    g_bx =  gravity*siny
    g_by = -gravity*cosy*sinx
    g_bz =  gravity*cosx*cosy

    accx = g_bx;
    accy = g_by;
    accz = g_bz;
    
    Fbx += mass*g_bx + T
    Fby += mass*g_by
    Fbz += mass*g_bz

    #print(round(Fbx,2) ,' ',round(Fby,2) ,' ',round(Fbz,2))
    acc_bx = Fbx/mass
    acc_by = Fby/mass
    acc_bz = Fbz/mass



    
    #print(round(acc_bx,2) ,' ',round(acc_by,2) ,' ',round(acc_bz,2))
    U += acc_bx*dt
    V += acc_by*dt
    W += acc_bz*dt
    
    #print(round(U,2) ,' ',round(V,2) ,' ',round(W,2))

    # rotate acc body  to inertial frame
    accEx = acc_bx*cosy*cosz - acc_bz*(sinx*sinz + cosx*cosz*siny) - acc_by*(cosx*sinz - cosz*sinx*siny)
    accEy = acc_by*(cosx*cosz + sinx*siny*sinz) + acc_bz*(cosz*sinx - cosx*siny*sinz) + acc_bx*cosy*sinz
    accEz = acc_bx*siny + acc_bz*cosx*cosy - acc_by*cosy*sinx

    #print(round(accEx,2) ,' ',round(accEy,2) ,' ',round(accEz,2))
    # zero acce z on ground
    '''
    if accEz > 0 and isFlying == 0:
        isFlying = 1 
    elif accEz < 0 and isFlying == 0:
        accEz = 0 
    '''
    px += vex*dt + 0.5*accEx*dt*dt
    py += vey*dt + 0.5*accEy*dt*dt
    pz += vez*dt + 0.5*accEz*dt*dt

    if pz <=0:
        pz = 0
        vez = 0

    vex +=  accEx*dt 
    vey +=  accEy*dt
    vez +=  accEz*dt

    total_fly_dis = sqrt(px*px + py*py)
    #print(round(vex,2) ,' ',round(vey,2) ,' ',round(vez,2))

    
    '''************ rotation  moment  ************************ 
         joystick direction

      -1  <---- CH2 -----> +1

               +1
                |
               ch3
                |
               -1
    '''

    #scale to deg
    ctrl_left  *= 40
    ctrl_right *= 40

    lift_left   = dynamic_p*wing_ctrl_area*aileron_Cl*ctrl_left
    lift_right  = dynamic_p*wing_ctrl_area*aileron_Cl*ctrl_right
    drag_left   = dynamic_p*wing_ctrl_area*aileron_Cd*ctrl_left
    drag_right  = dynamic_p*wing_ctrl_area*aileron_Cd*ctrl_right

    #drag_left = 0
    #drag_right = 0

    # pitching moment
    Cm_p = (0.002*pow(alpha,3) + 0.5*alpha)*0.0002 + Cm_o
    #Cm_p = alpha*0.0001
    
    Pitching_moment = dynamic_p*wing_area*Cm_p
    yaw_moment = Side_force*dis_ruderr2CG

    Mx_total = (lift_right - lift_left)*dis_aile2center -sign(P)*P*P*cd_moment_x
    My_total = (lift_right + lift_left)*dis_ele2center - Pitching_moment  -sign(Q)*Q*Q*cd_moment_y #
    Mz_total = (abs(drag_left) - abs(drag_right))*dis_aile2center - yaw_moment  - sign(R)*R*R*cd_moment_z
    

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

    roll  += r_dot*dt
    pitch += p_dot*dt
    yaw   += y_dot*dt

    yaw   = swap360(yaw*toDeg)*toRad
    roll  = swap180(roll*toDeg)*toRad
    pitch = swap180(pitch*toDeg)*toRad

def total_fly():
    return total_fly_dis

def imu_get():
    return P*toDeg,Q*toDeg,R*toDeg,accx,accy,accz

def get_velocity():
    return velocity

def get_roll_rate():
    return r_dot*toDeg

def get_pitch_rate():
    return p_dot*toDeg

def get_yaw_rate():
    return y_dot*toDeg
    
def get_roll_rate():
    return r_dot*toDeg

def get_R():
    return R*toDeg

def get_Q():
    global Q
    return Q*toDeg

def get_P():
    return P*toDeg

def get_yaw():
    return yaw*toDeg

def get_roll():
    return roll*toDeg

def get_pitch():
    return pitch*toDeg

def get_longitude():
    l = py/earth_radius*toDeg
    return init_longitude + l

def get_latitude():
    l = px/earth_radius*toDeg
    return init_latitude + l

def get_altitude():
    return init_altitude + pz 



