import config as cfg
import dynamic
from utils import *
def control1(throttle,e_start,latitude,longitude,altitude,roll,pitch,yaw):
    str_ =''
    str_ += str(throttle)
    str_ +='\t'
    str_ += str(e_start)
    str_ +='\t'
    str_ += str(latitude)
    str_ +='\t'
    str_ += str(longitude)
    str_ +='\t'
    str_ += str(altitude*3.280839895)
    str_ +='\t'
    str_ += str(roll)
    str_ +='\t'
    str_ += str(pitch)
    str_ +='\t'
    str_ += str(yaw)
    str_ +='\n'
    bytess = bytes(str_, 'utf-8')
    return bytess

def control2(latitude,longitude,altitude,roll,pitch,yaw):
    latitude = constrain(latitude,-90,90)
    longitude = constrain(longitude,-180,180)
    altitude = constrain(altitude,3,10000)
    roll =constrain(roll,-180,180)
    pitch = constrain(pitch,-180,180)
    yaw = constrain(yaw,0,360)
    str_ =''
    str_ += str(latitude)
    str_ +='\t'
    str_ += str(longitude)
    str_ +='\t'
    str_ += str(altitude*3.280839895)
    str_ +='\t'
    str_ += str(roll)
    str_ +='\t'
    str_ += str(pitch)
    str_ +='\t'
    str_ += str(yaw)
    str_ +='\n'
    bytess = bytes(str_, 'utf-8')
    return bytess

