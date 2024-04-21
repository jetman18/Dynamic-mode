import config as cfg
from utils import *


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

