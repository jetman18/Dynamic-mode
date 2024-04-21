from tkinter import *
import os,signal
from multiprocessing import Process
import multiprocessing as mp
import time
import struct
class window():
    root = Tk()
    root.title('view')
    root.geometry("340x250")
  
    x_offset = 0
    y_offset = 0
    #roll
    label1=Label(root, text='roll:', font=('Helvetica 10'))
    label1.place(x=10 + x_offset,y=10 + y_offset)
    label11=Label(root, text='0.0', font=('Helvetica 10'))
    label11.place(x=50 + x_offset,y=10 + y_offset)
    #pitch
    label2=Label(root, text='pitch:', font=('Helvetica 10'))
    label2.place(x=10 + x_offset,y=35 + y_offset)
    label22=Label(root, text='0.0', font=('Helvetica 10'))
    label22.place(x=50 + x_offset,y=35 + y_offset)
    #yaw
    label3=Label(root, text='yaw:', font=('Helvetica 10'))
    label3.place(x=10 + x_offset,y=60 + y_offset)
    label33=Label(root, text='0.0', font=('Helvetica 10'))
    label33.place(x=50 + x_offset,y=60 + y_offset)
    #altitude
    label4=Label(root, text='alt:', font=('Helvetica 10'))
    label4.place(x=10 + x_offset,y=85 + y_offset)
    label44=Label(root, text='0.0', font=('Helvetica 10'))
    label44.place(x=50 + x_offset,y=85 + y_offset)
    #lat
    label5=Label(root, text='v:', font=('Helvetica 10'))
    label5.place(x=10 + x_offset,y=110 + y_offset)
    label55=Label(root, text='0.0', font=('Helvetica 10'))
    label55.place(x=50 + x_offset,y=110 + y_offset)
    #lon
    label6=Label(root, text='dis:', font=('Helvetica 10'))
    label6.place(x=10 + x_offset,y=135 + y_offset)
    label66=Label(root, text='0.0', font=('Helvetica 10'))
    label66.place(x=50 + x_offset,y=135 + y_offset)
    #yaw dot
    label7=Label(root, text='y_dot:', font=('Helvetica 10'))
    label7.place(x=10 + x_offset,y=160 + y_offset)
    label77=Label(root, text='0.0', font=('Helvetica 10'))
    label77.place(x=70 + x_offset,y=160 + y_offset)

    thrust_text=Label(root, text='thrust', font=('Helvetica 10'))
    thrust_text.place(x=10 + x_offset,y=185 + y_offset)
    thrust_value =Label(root, text='0.0', font=('Helvetica 10'))
    thrust_value.place(x=50 + x_offset,y=185 + y_offset)

    ww = Scale(root, from_=-9, to=9,resolution=0.1,length=100)
    ww.place(x=400,y=100)

    roll_in = StringVar(root)  
    pitch_in = StringVar(root)
    yaw_in = StringVar(root)
    altitude_in = StringVar(root)
    tt = 0
    def update_log(self):
        window.tt +=10
        if(window.tt>200):
            window.tt=0
        window.canva.create_text(20,window.tt, text=str(window.tt), fill="white", font=('Helvetica 7'))
    #pipe
    def __init__(self,pipe) -> None:
        self.roll =0 
        self.att = []
        self.last_t = time.time()
        self.p1,self.p2 = mp.Pipe()
        self.pp1,self.pp2 = mp.Pipe()
        self.run = 1
        p = Process(target=self.show,args=(pipe,))
        p.start()
    def bt_cback(self):
        window.label11.configure(text=str())
        #pipe.send('hello')
        #print(self.roll)
    def setAttitude(self,roll,pitch,yaw,alt,lat,lon,yaw_dot):
        if time.time() - self.last_t > 0.4:
            self.last_t = time.time()
            da = struct.pack('ddiiddi',roll,pitch,yaw,alt,lat,lon,int(yaw_dot))
            self.p2.send(da)
       
    def update_sc(self):
        if self.p1.poll():
            data = self.p1.recv()
            data = struct.unpack('ddiiddi',data)
            window.label11.configure(text=str(data[0]))
            window.label22.configure(text=str(data[1]))
            window.label33.configure(text=str(data[2]))
            window.label44.configure(text=str(data[3]))
            window.label55.configure(text=str(data[4]))
            window.label66.configure(text=str(data[5]))
            window.label77.configure(text=str(data[6]))
        #print(window.ww.get())
        window.root.after(100,self.update_sc)

    def setAtitud(self,pipe):
        roll = 0
        pitch = 0
        yaw = 0
        altitude = 0
        try:
            roll = float(window.roll_in.get())
            pitch =float(window.pitch_in.get())
            yaw = float(window.yaw_in.get())
            altitude = float(window.altitude_in.get())
        except:
            roll = 0
            pitch =0
            yaw = 0
            altitude = 0
        data = struct.pack('dddd',roll,pitch,yaw,altitude)
        pipe.send(data)
    def resetAtitud(self,pipe):
        data = struct.pack('dddd',0.0,0.0,0.0,0.0)
        pipe.send(data)


    def show(self,pipe):
        roll = Entry(window.root, textvariable=window.roll_in)
        roll.place(width=50,height=17)
        roll.place(x=100 + window.x_offset,y=13 + window.y_offset)

        pitch = Entry(window.root, textvariable=window.pitch_in)
        pitch.place(width=50,height=17)
        pitch.place(x=100 + window.x_offset,y=38 + window.y_offset)

        yaw = Entry(window.root, textvariable=window.yaw_in)
        yaw.place(width=50,height=17)
        yaw.place(x=100 + window.x_offset,y=63 + window.y_offset)

        altitude = Entry(window.root, textvariable=window.altitude_in)
        altitude.place(width=50,height=17)
        altitude.place(x=100 + window.x_offset,y=88 + window.y_offset)

        # button
        B = Button(padx=20,pady=2, text ="set", command = lambda: self.setAtitud(pipe))
        B.place(x=170,y=13)
        RB = Button(padx=20,pady=2, text ="reset", command = lambda: self.resetAtitud(pipe))
        RB.place(x=240,y=13)
    
        window.root.after(100,self.update_sc)
        window.root.mainloop()
        self.pp1.send('close')
    def isClose(self):
        if self.run:
            if self.pp2.poll():
                rec = self.pp2.recv()
                if rec == 'close':
                    self.run = 0
            else:
                return 1
        return self.run



