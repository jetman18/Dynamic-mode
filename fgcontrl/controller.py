def control(aileron,elevator,throttle):
    str_ =''
    str_ += str(aileron)
    str_ +='\t'
    str_ += str(-elevator)
    str_ +='\t'
    str_ += str(throttle)
    #str_ +='\t'
    #str_ += str(stater)
    str_ +='\n'
    bytess = bytes(str_, 'utf-8')
    return bytess

def constrain(val,min,max):
    if val > max:
        return max
    elif val < min:
        return min
    return val