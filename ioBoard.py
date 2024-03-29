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
        time.sleep(0.5)
        data_left = self.ser.inWaiting()
        received_data += self.ser.read(data_left)
        #receive_data_string = received_data.decode("utf-8")
        
        print("rawdata")
        print(received_data)

        self.ser.flush() #clean data

        stopCommand = b"*SIR,,OK,*,0,0,0,\r"
        stopCommand1 = b"*SIR,,OK,*,1,0,0,\r*SIR,,OK,*,0,0,0,\r"
        stopCommand2 = b"*SIR,,OK,*,0,1,0,\r*SIR,,OK,*,0,0,0,\r"
        warningCommand = b"*SIR,,OK,*,1,0,0,\r"
        dangerCommand = b"*SIR,,OK,*,0,1,0,\r"
        
        if stopCommand == received_data:
            print('stopCommand')
            return 0
        elif stopCommand1 == received_data:
            print('stopCommand1')
            return 0
        elif stopCommand2 == received_data:
            print('stopCommand2')
            return 0
        elif warningCommand == received_data:
            print('warningCommand')
            return 1
        elif dangerCommand == received_data:
            print('dangerCommand')
            return 2
        else:
            print('unknown command')
            return -1
        
        #old logic, not used
        if receive_data_string.startswith("*SIR,,OK,*,0,0,0,R,,OK,*,1,0,0,"):
            print('received_data',receive_data_string)
            return 0
        elif receive_data_string.startswith("*SIR,,OK,*,0,0,0,R,,OK,*,0,1,0,"):
            print('received_data',receive_data_string)
            return 0
        elif receive_data_string.startswith("*SIR,,OK,*,1,0,0,"):
            print('received_data',receive_data_string)
            return 1
        elif receive_data_string.startswith("*SIR,,OK,*,0,1,0,"):
            print('received_data',receive_data_string)
            return 2
        else:
            print('received_data',receive_data_string)
            return -1
        #*SIR,,OK,*,0,0,0,R,,OK,*,1,0,0,
        #*SIR,,OK,*,0,0,0,R,,OK,*,1,0,0,
        #*SIR,,OK,*,0,0,0,R,,OK,*,0,1,0, 

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
        print('setSiren', state)
        if state == '0':
            self.ser.write(b"*SIR,0#\r\n")
            received_data = self.ser.read()
            time.sleep(0.5)
            data_left = self.ser.inWaiting()
            received_data += self.ser.read(data_left)
            receive_data_string = received_data.decode("utf-8")
            print('received_data', receive_data_string)
                                                              
            if receive_data_string.startswith("*SIR,0,OK,#,0,1,0,"):
                return True
            else:
                return False
        if state == '1':
            self.ser.write(b"*SIR,1#\r\n")
            received_data = self.ser.read()
            time.sleep(0.5)
            data_left = self.ser.inWaiting()
            received_data += self.ser.read(data_left)
            receive_data_string = received_data.decode("utf-8")
            print('received_data', received_data.decode("utf-8"))
            if receive_data_string.startswith("*SIR,1,OK,#,0,1,0,"):
                return True
            else:
                return False
        if state == '2':
            self.ser.write(b"*SIR,2#\r\n")
            received_data = self.ser.read()
            time.sleep(0.5)
            data_left = self.ser.inWaiting()
            received_data += self.ser.read(data_left)
            receive_data_string = received_data.decode("utf-8")
            print('received_data', received_data.decode("utf-8"))
            if receive_data_string.startswith("*SIR,2,OK,#,0,1,0,"):
                return True
            else:
                return False

        return False


if __name__ == "__main__":
    io = IoBoard()
#    result = io.setSiren(2)
#    print('result',result)
#    result = io.setSiren(1)
#    print('result',result)
#    result = io.setSiren(0)
#    print('result',result)


    
    while True:
        time.sleep(.01)
        data = io.getData()
        print(data); 
#    pass

