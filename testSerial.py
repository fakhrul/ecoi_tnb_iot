import time
from time import sleep
import serial

#  ttyAMA0
# /dev/ttyS0
# serial0
# ser = serial.Serial("/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
# counter=0

# ser.write(b"?MEAS")
# print("sent")    
# rx_data = ser.read()
# sleep(1)
# data_left = ser.inWaiting()
# rx_data += ser.read(data_left)
# print(rx_data)


# ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
# ser = serial.Serial(            
#     port='/dev/ttyS0',
#     baudrate = 9600,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS,
#     timeout=1
# )

# ser.reset_input_buffer()

# while True:
#     ser.write("?MEAS".encode('utf-8'))
#     print("sent")
#     line = ser.readline()
#     print(line)
#     sleep(1)


# import time
# import serial
# ser = serial.Serial(
#         port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
#         baudrate = 9600,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         bytesize=serial.EIGHTBITS,
#         timeout=1
# )
# counter=0
# while True: 
#     ser.write(b'?MEAS') #encode to bytes
#     print("SENT")
#     time.sleep(1) 
#     counter += 1

import serial
from time import sleep

ser = serial.Serial ("/dev/ttyS0", 9600, timeout=1)    #Open port with baud rate
while True:

#     ser.write(b"?MEAS\r\n")       
#     print('SENT')
#     received_data = ser.read()              #read serial port
#     print('READ')
#     sleep(0.03)
#     data_left = ser.inWaiting()             #check for remaining byte
#     received_data += ser.read(data_left)
#     print (received_data)                   #print received data

    ser.write(b"*sir,1#")       
    print('SENT')
    received_data = ser.read()              #read serial port
    print('READ')
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    print (received_data)                   #print received data


#     ser.write(received_data)       
