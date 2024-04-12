def constrain(val,min,max):
    if val > max:
        val = max
    elif val < min:
        val = min
    return val
def sq(x):
    return x*x

def swap180(val):
    if val > 179:
        val = -179
    elif val < -179:
        val = 179
    return val

def swap90(val):
    if val > 89:
        val = -89
    elif val < -89:
        val = 89
    return val

def swap360(val):
    if val > 359:
        val = 0
    elif val < 0:
        val = 359
    return val

#-179 0 179
def cvrt(val):
    if val > 89:
        val = val - 180
    elif val < -89:
        val = val + 180
    return abs(val)

def sign(val):
    if val< 0:
        return -1
    else:
        return 1

