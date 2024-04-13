from math import *    
toDeg = 57.29577
vx = 1
vy = -0.0001
yaw = 4
temp_beta  = abs(atan2(vy,vx)*toDeg)
beta_t = 0
if  vy >= 0:
    beta_t = temp_beta
elif  vy <= 0:
    beta_t = 360 - temp_beta

print(beta_t,'  ',yaw)

beta_t = yaw - beta_t
if beta_t < -180:
    beta_t = beta_t + 360
elif beta_t > 180:
    beta_t =  - 360 + beta_t
    
print(beta_t)