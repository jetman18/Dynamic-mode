import time
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
#from windowview import window
import multiprocessing as mp
import struct
import math
import utils 

# max speed 100 km/h
# max thrust of electric motor 0.9 kg

# parameters
S_ref = 0.33             # m*m  ref area
S_aile = 0.006           # m*m
P_ref = 0.024            # m*m
C_ref = 0.276            # m    ref chord
B_ref = 1.2              # m    ref span
X_aero = 0.201           # m   distance to aerodynamic center
mass   = 0.9             # kg
I_xx   = 0.0306          # kgm*m 
I_yy   = 0.018           # kgm*m 
I_zz   = 0.0251          # kgm*m 
d_aile_to_x = 0.2        # distance from aileron to x axis
d_ele_to_cg = 0.13        # distance from aileron to x axis
d_aile_to_z = 0.13        # distance from aileron to x axis

Air_density = 1.293
anlpha = 0               # attack angle
Cl_0 = 0.06              # lift coefficient
Cd_0 = 0.79              # drag coefficient 
aile_ele_max_angle = 40  #
earth_radius       = 6371000  
attack_angle = 7
max_pitch_angle = 60
max_roll_angle = 60
rad = 0.01745
_g = -9.81
_dt = 0.01
deg = 57.29

init_latitude  = 37.628715674334124
init_longitude = -122.39334575867426
init_altitude  =  2

aero_drag_moment_x_gain = 0.006
aero_drag_moment_y_gain = 0.002
aero_drag_moment_z_gain = 0.001
# end parameters
####################
_thrust = 0
_pitch = 0
_roll = 0
_yaw = 0
############
_pitch_dot = 0
_roll_dot = 0
_yaw_dot = 0

###########
_x_vel = 0
_y_vel = 0
_z_vel = 0
u_body = 0
############
_x_p = 0
_y_p = 0
_z_p = 0
############
_x_deg = init_latitude
_y_deg = init_longitude
#############
ctrl_deg_L = 0
ctrl_deg_R = 0


x=[]
y=[]
z=[]

mm = 0

def calcalate_air_density():
    density = Air_density*5000/(_z_p + 5000)
    return density

def calculate_lift_coefficient(anpha):
    anpha += attack_angle
    anpha_ = utils.cvrt(anpha)
    cl = 0.02*anpha_* utils.sign(anpha )
    return cl

def calculate_drag_coefficient(anpha):
    anpha += attack_angle
    anpha = utils.cvrt(anpha)
    cd = 0.01*anpha
    return cd

def calculate_force_x_body():
    F_drag_bx = 0.5*Cd_bx
    F_bx = _thrust

def calculate_force_z():
    T = _thrust*math.sin(_pitch)
    
    cl__ = calculate_lift_coefficient(_pitch*deg)
    lift_force = S_ref*_x_vel*_x_vel*calcalate_air_density()*cl__
    #print(cl__)
    #lift_force *= abs(math.cos(_roll))
    drag_force = 1.5*cl__*S_ref*_z_vel*_z_vel*calcalate_air_density()
    
    #print(_x_vel)
    P = mass*_g
    return T + lift_force - drag_force + P

def calculate_force_x():
    thrust = _thrust*math.cos(_pitch)
    cd = calculate_drag_coefficient(_pitch*deg)
    drag_force = 16*cd*P_ref*_x_vel*_x_vel*calcalate_air_density()
    #print(_x_vel)
    return thrust - drag_force

def calculate_force_y():
    cl = calculate_lift_coefficient(_pitch*deg)
    lift_force = 0.5*cl*S_ref*_x_vel*_x_vel*calcalate_air_density()

    lift_force *= math.sin(_roll)
    return  lift_force

def calculate_moment_x():
    global ctrl_deg_R,ctrl_deg_L
    ctrl_deg_L = utils.constrain(ctrl_deg_L,-aile_ele_max_angle,aile_ele_max_angle) 
    ctrl_deg_R = utils.constrain(ctrl_deg_R,-aile_ele_max_angle,aile_ele_max_angle) 
    cl_L = 0.01*ctrl_deg_L
    cl_R = 0.01*ctrl_deg_R

    ctrl_wing_force_L =  0.5*cl_L*S_aile*u_body*u_body*Air_density
    ctrl_wing_force_R =  0.5*cl_R*S_aile*u_body*u_body*Air_density
    moment_L = -ctrl_wing_force_L* d_aile_to_x
    moment_R = ctrl_wing_force_R* d_aile_to_x

    drag_moment = aero_drag_moment_x_gain*utils.sq(_roll_dot)
    return moment_L + moment_R - drag_moment

def calculate_moment_y():
    
    global ctrl_deg_R,ctrl_deg_L
    ctrl_deg_L = utils.constrain(ctrl_deg_L,-aile_ele_max_angle,aile_ele_max_angle) 
    ctrl_deg_R = utils.constrain(ctrl_deg_R,-aile_ele_max_angle,aile_ele_max_angle) 
    cl_L = 0.1*ctrl_deg_L
    cl_R = 0.1*ctrl_deg_R
 
    ctrl_wing_force_L =  0.5*cl_L*S_aile*u_body*u_body*Air_density

    ctrl_wing_force_R =  0.5*cl_R*S_aile*u_body*u_body*Air_density
 
    moment_L = ctrl_wing_force_L* d_ele_to_cg*0.01
    moment_R = ctrl_wing_force_R* d_ele_to_cg*0.01

    drag_moment = aero_drag_moment_y_gain*utils.sq(_pitch_dot)
    
    return 0#moment_L + moment_R - drag_moment

def calculate_moment_z():
    global ctrl_deg_R,ctrl_deg_L
    total_angle = abs(ctrl_deg_R) - abs(ctrl_deg_L)
    total_angle = utils.constrain(total_angle,-aile_ele_max_angle,aile_ele_max_angle) 
    cl_d = 0.007*total_angle
    ctrl_wing_force =  0.5*cl_d*S_aile*u_body*u_body*Air_density
    moment =  ctrl_wing_force* d_aile_to_z
    drag_moment = aero_drag_moment_z_gain*utils.sq(_yaw_dot)
    return moment - drag_moment

state = 1
_yaw = 180*rad
def dynamicMode():
    global _x_p,_x_vel,_pitch,_pitch_dot,_x_deg,_y_deg
    global _y_p,_y_vel,_roll,_roll_dot,state
    global _z_p,_z_vel,_yaw,_yaw_dot,u_body

    # U body m/s
    a_x_body = (_thrust + mass*_g*math.sin(_pitch) - utils.sq(u_body)*0.014)/mass
    u_body += a_x_body*_dt
    #u_body= utils.constrain(u_body,-25,25)
    #print(u_body)

    # x axis longitude
    F_x = calculate_force_x()
    _x_acc = F_x/mass
    _x_p   += _x_vel*_dt + 0.5*_x_acc*_dt*_dt
    x_temp = _x_p
    x_temp   *=math.cos(_yaw)
    print(x_temp/earth_radius)
    _x_deg += x_temp/earth_radius
    _x_vel += _x_acc*_dt
    _x_vel= utils.constrain(_x_vel,-25,25)

    # y axis
    F_y = calculate_force_y()
    _y_acc = F_y/mass
    _y_p   += _y_vel*_dt + 0.5*_y_acc*_dt*_dt
    y_temp = _y_p
    y_temp   *=math.sin(_yaw)
    _y_deg += y_temp/earth_radius
    _y_vel += _y_acc*_dt
    _y_vel= utils.constrain(_y_vel,-25,25)

    # z axis
    F_z = calculate_force_z()
    _z_acc = F_z/mass
    if state and F_z<0:
        _z_acc = 0
    elif F_z>0:
        state = 0
    _z_p   += _z_vel*_dt + 0.5*_z_acc*_dt*_dt
    _z_vel += _z_acc*_dt
    _z_vel= utils.constrain(_z_vel,-25,25)
    _z_p= utils.constrain(_z_p,0,7000)

   # moment
    M_y = calculate_moment_y()
    if(_z_p > 0):
        pitch_acc = M_y/I_yy
        _pitch += _pitch_dot*_dt + 0.5*pitch_acc*_dt*_dt
        _pitch_dot += pitch_acc*_dt
        _pitch = utils.swap180(_pitch*deg)/deg
        _pitch = utils.constrain(_pitch,-60,60)

    M_x = calculate_moment_x()
    roll_acc = M_x/I_xx
    _roll += _roll_dot*_dt + 0.5*roll_acc*_dt*_dt
    _roll_dot += roll_acc*_dt
    _roll = utils.swap180(_roll*deg)/deg
    _roll = utils.constrain(_roll,-60,60)


    M_z = calculate_moment_z()
    yaw_acc = M_z/I_zz
    _yaw += _yaw_dot*_dt + 0.5*yaw_acc*_dt*_dt
    _yaw_dot += yaw_acc*_dt
    _yaw = utils.swap360(_yaw*deg)/deg

_thrust = 9  # max
attack_angle = 3

# for i in range(3000):
#     if i>1000:
#         pass
#         #_pitch = 160*rad
#         #ctrl_deg_L = 2
#         #ctrl_deg_R = 2
#         #_pitch = 1*rad
#         #print(_pitch*deg)
#     dynamicMode()
#     #print(_x_deg,' ',_y_deg)
#     #x.append(_x_deg)
#     #y.append(_y_deg)
#     #z.append(_z_p)
#     #time.sleep(0.01)


# fig = plt.figure(figsize = (8,7))
# ax = plt.axes(projection ="3d")
# #ax.set_xlim([0,3000])
# #ax.set_ylim([0,3000])
# #ax.set_zlim([0,2000])
# ax.scatter3D(x, y, z)
# ax.set_aspect('equal')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# plt.title("simple 3D scatter plot")

# #plt.plot(x,z, color='black');
# #plt.grid()
# plt.show()


