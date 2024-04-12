import serial
#Serial takes these two parameters: serial device and baudrate
ser = serial.Serial('COM13', 19200,parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\

    timeout=1000)

while True:
    data = ser.read(1)
    print(data)