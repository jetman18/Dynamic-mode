
from utils import *
Pi = 3.14156
class pidcontroller():
    def __init__(self,kp,ki,kd,I_range,f_cut,dt) -> None:
        self.init = 1
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.i_term = 0
        self.last_input = 0
        self.dt = dt
        self.maxI = I_range
        self.minI = -I_range
        self.d_term = 0
        self.f_cut = f_cut

    def pid_cal(self,input,setpoint):
        if self.init or self.dt == 0:
            self.last_input = input
            self.init = 0
            return 0
        erorr = input - setpoint
        p_term = erorr*self.kp
        self.i_term += erorr*self.dt*self.ki
        self.i_term = constrain(self.i_term,self.minI,self.maxI)
        if self.kd != 0:
            d_term = self.kd*(input - self.last_input)/self.dt
            self.last_input = input
            rc = 1/(2*Pi*self.f_cut)
            lfp_g = self.dt/(self.dt + rc)
            self.d_term += lfp_g*(d_term - self.d_term)
        pid = p_term + self.i_term + self.d_term
        return pid
    
    def pid_reset(self):
        self.init = 1
        self.i_term = 0
        self.last_input = 0

    def pid_set_gain(self,kp,ki,kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd


