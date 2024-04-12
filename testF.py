from math import *    
toDeg = 57.29
toRad = 0.01745
vx = 1
vy = 1
vz = 0

pitch = 0
roll = -90
yaw = 0

a = 30
b = 10

yaw    /= toDeg
pitch  /= toDeg
roll   /= toDeg

tany = tan(pitch)

v_horizon = sqrt(vx*vx + vy*vy)
temp_a = atan2(vz,v_horizon)*toDeg

alpha = pitch*toDeg - temp_a
#print(alpha)


temp_beta  = abs(atan2(vy,vx)*toDeg)
beta_t = 0
if  vy >= 0:
    beta_t = temp_beta
elif  vy <= 0:
    beta_t = 360 - temp_beta

beta = beta_t
#eta = yaw*toDeg - beta_t

if beta > 180:
    beta = 360 - beta
elif beta < -180:
    beta = 360 + beta

alpha = temp_a*cos(roll) + beta*sin(roll)
beta  = -temp_a*sin(roll) + beta*cos(roll)
 
print(beta)
print(alpha)

'''
alpha = 0
beta = -10

sinA = sin(alpha*toRad)
cosA = cos(alpha*toRad)
cosB = cos(beta*toRad)
sinB = sin(beta*toRad)

L = 0
D = -0.5
T = 0

Fbx = L*sinA + D*cosA*cosB + T
Fby = -D*sinB
Fbz = L*cosA - D*cosB*sinA

print(Fbx,' ',Fby,' ',Fbz)'''