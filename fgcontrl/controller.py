def control(roll,pitch,yaw,latitude,longitude,altitude):
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

def constrain(val,min,max):
    if val > max:
        return max
    elif val < min:
        return min
    return val