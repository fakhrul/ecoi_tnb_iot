import serial
import time
import os
from dotenv import load_dotenv

class IoBoard:
    def __init__(self):
        load_dotenv()
        comPort = os.getenv('IOBOARD_PORT')
        
        # Open port with baud rate
        # self.ser = serial.Serial("/dev/ttyS0", 9600, timeout=1)
        self.ser = serial.Serial(comPort, 9600, timeout=1)

    def getData(self):
        received_data = self.ser.read()
        data_left = self.ser.inWaiting()
        received_data += self.ser.read(data_left)
        return received_data

    def getMeas(self):
        self.ser.write(b"?MEAS\r\n")
        received_data = self.ser.read()
        time.sleep(0.5)
        data_left = self.ser.inWaiting()
        received_data += self.ser.read(data_left)
        return received_data

    def getMebt(self):
        self.ser.write(b"?MEBT\r\n")
        received_data = self.ser.read()
        time.sleep(0.5)
        data_left = self.ser.inWaiting()
        received_data += self.ser.read(data_left)
        return received_data

    def setSiren(self, state):
        if state == 0:
            self.ser.write(b"*SIR,0#\r\n")
            received_data = self.ser.read()
            time.sleep(0.5)
            data_left = self.ser.inWaiting()
            received_data += self.ser.read(data_left)
            if received_data == "*SIR,0,OK,#":
                return True
            else:
                return False
        if state == 1:
            self.ser.write(b"*SIR,1#\r\n")
            received_data = self.ser.read()
            time.sleep(0.5)
            data_left = self.ser.inWaiting()
            received_data += self.ser.read(data_left)
            if received_data == "*SIR,1,OK,#":
                return True
            else:
                return False
        if state == 2:
            self.ser.write(b"*SIR,2#\r\n")
            received_data = self.ser.read()
            time.sleep(0.5)
            data_left = self.ser.inWaiting()
            received_data += self.ser.read(data_left)
            if received_data == "*SIR,2,OK,#":
                return True
            else:
                return False

        return False


if __name__ == "__main__":
    io = IoBoard()

    while True:
        time.sleep(1)
        data = io.getData()
        print(data); 
    pass
