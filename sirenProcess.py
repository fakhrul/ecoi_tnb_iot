import logging
import threading
import time
from dbApi import DbApi
from rut955 import Rut955
from ioBoard import IoBoard
import os

class SirenProcess:
    def __init__(self):
        self.isRunning = True
        self.dbApi = DbApi()
        self.rut955 = Rut955()
        self.ioBoard = IoBoard()

        self.gsmSignal = 0
        self.gpsLatitude = 0
        self.gpsLongitude = 0
        self.ipAddress = ""
        self.currentSirenCommand = 0

        self.batteryVoltage = 0
        self.solarVoltage = 0
        self.rtuTemperature = 0
        self.checkIoStatusInSecond = int(os.getenv('IO_STATUS_SECOND'))
        self.checkRut955StatusInSecond = int(os.getenv('MODEM_STATUS_SECOND'))
        self.checkSmsStatusInSecond = int(os.getenv('SMS_STATUS_SECOND'))

        self.ioLock = threading.Lock()

    def smsSend(self, smsTo, message):
        result = self.rut955.smsSend(smsTo, message)
        return result

    def smsSendSirenState(self, appName, sirenCommand):
        print('appName',appName)
        print('sirenCommand',sirenCommand)
        try:
            result = self.dbApi.getSession("admin@email.com", "Qwerty@123")
            result = self.dbApi.getConfiguration()
            sirenMessage = str(sirenCommand)
            if sirenCommand == "0":
                sirenMessage = "OFF"
            elif sirenCommand == "1":
                sirenMessage = "WARNING"
            elif sirenCommand == "2":
                sirenMessage = "DANGER"

            isSms1Enable = result['smsAlertEnable1']
            if isSms1Enable:
                self.smsSend(result['smsAlertPhone1'], appName + "-" + sirenMessage)

            isSms2Enable = result['smsAlertEnable2']
            if isSms2Enable:
                self.smsSend(result['smsAlertPhone2'], appName + "-" + sirenMessage)

            isSms3Enable = result['smsAlertEnable3']
            if isSms3Enable:
                self.smsSend(result['smsAlertPhone3'], appName + "-" + sirenMessage)

            isSms4Enable = result['smsAlertEnable4']
            if isSms4Enable:
                self.smsSend(result['smsAlertPhone4'], appName + "-" + sirenMessage)

            isSms5Enable = result['smsAlertEnable5']
            if isSms5Enable:
                self.smsSend(result['smsAlertPhone5'], appName + "-" + sirenMessage)

            isSms6Enable = result['smsAlertEnable6']
            if isSms6Enable:
                self.smsSend(result['smsAlertPhone6'], appName + "-" + sirenMessage)

            isSms7Enable = result['smsAlertEnable7']
            if isSms7Enable:
                self.smsSend(result['smsAlertPhone7'], appName + "-" + sirenMessage)

            isSms8Enable = result['smsAlertEnable8']
            if isSms8Enable:
                self.smsSend(result['smsAlertPhone8'], appName + "-" + sirenMessage)

            isSms9Enable = result['smsAlertEnable9']
            if isSms9Enable:
                self.smsSend(result['smsAlertPhone9'], appName + "-" + sirenMessage)

            isSms10Enable = result['smsAlertEnable10']
            if isSms10Enable:
                self.smsSend(result['smsAlertPhone10'], appName + "-" + sirenMessage)

        except Exception as e:
            print('Exception', e)
        pass

    def smsGetList(self):
        result = self.rut955.smsGetList()
        return result

    def smsRead(self, number):
        result = self.rut955.smsRead(number)
        return result
    def smsTotal(self):
        result = self.rut955.smsTotal()
        return result

    def smsDelete(self, number):
        result = self.rut955.smsDelete(number)
        return result
    def smsDeleteAll(self):
        result = self.rut955.smsDeleteAll()
        return result


    def thread_rut955_status(self, name):
        while self.isRunning:
            try: 
                sessionId = self.rut955.getSession("root", "Ampang2020")
                if sessionId != "":
                    gsm = self.rut955.getGsmRSSI(sessionId)
                    if gsm != "":
                        self.gsmSignal = int(gsm)
                    gps = self.rut955.getGps(sessionId)
                    self.gpsLatitude = float(gps.splitlines()[0])
                    self.gpsLongitude = float(gps.splitlines()[1])
                    
                    ipAddress = self.rut955.getIP(sessionId)
                    self.ipAddress = ipAddress

            except Exception as e:
                print('Exception', e)
            
            time.sleep(self.checkRut955StatusInSecond)


    def thread_sms_status(self, name):
        while self.isRunning:
            try: 
                time.sleep(self.checkSmsStatusInSecond)
                messages = self.rut955.smsGetList()
                for message in messages:
                    if message['text'].startswith('*SIR,0#'):
                        print('SMS setSirenCommand', 0)
                        self.setSirenCommand('sms',0)
                    elif message['text'].startswith('*SIR,1#'):
                        print('SMS setSirenCommand', 1)
                        self.setSirenCommand('sms',1)
                    elif message['text'].startswith('*SIR,2#'):
                        print('SMS setSirenCommand', 2)
                        self.setSirenCommand('sms',2)
                    else:
                        print('SMS UNKNOWN')

                
                self.rut955.smsDeleteAll()
            except Exception as e:
                print('Exception', e)


    def thread_ioboard_button(self, name):
        while self.isRunning:
            time.sleep(0.01)
            self.ioLock.acquire()
            try: 
                buttonStatus = self.ioBoard.getData()
                if buttonStatus == 0:
                    print("button off")
                    self.setSirenCommand('button',0)
                elif buttonStatus == 1:
                    print("button warning")
                    self.setSirenCommand('button',1)
                elif buttonStatus == 2:
                    print("button danger")
                    self.setSirenCommand('button',2)

            except Exception as e:
                print('Exception', e)
            self.ioLock.release()

    def thread_ioboard_status(self, name):
        while self.isRunning:
            time.sleep(self.checkIoStatusInSecond)
            self.ioLock.acquire()
            try: 

                boardStatus = self.ioBoard.getMebt()
                boardStatusString = boardStatus.decode("utf-8")

                boardStatuses = boardStatusString.split(",")
                self.batteryVoltage = float(boardStatuses[1])
                self.solarVoltage = float(boardStatuses[2])
                self.rtuTemperature = float(boardStatuses[3])

                equipmentStatus = {
                    "gpsLatitude" : str(self.gpsLatitude),
                    "gpsLongitude" : str(self.gpsLongitude),
                    "batteryVoltage" : str(self.batteryVoltage),
                    "solarVoltage" : str(self.solarVoltage),
                    "rtuTemperature" : str(self.rtuTemperature),
                    "gsmSignal" : str(self.gsmSignal),
                    "sirenMode" : str(self.currentSirenCommand),
                }
                result = self.dbApi.getSession("admin@email.com", "Qwerty@123")
                self.dbApi.addEquipmentStatus(equipmentStatus)

            except Exception as e:
                print('Exception', e)
            self.ioLock.release()


    def thread_pending_command(self, name):
        while self.isRunning:
            try:
                time.sleep(1)
                logging.info("Command Thread    : Login to DB")
                result = self.dbApi.getSession("admin@email.com", "Qwerty@123")
                sirenInfo = self.dbApi.getPendingCommand()
                
                if sirenInfo is None:
                    logging.info("Command Thread    : No Pending Command")
                else:
                    appName = sirenInfo['appName']
                    sirenCommand = str(sirenInfo['sirenMode'])
                    
                    logging.info("Command Thread    : App " + appName + " Command " + sirenCommand)

                    if appName == "sms" or "web" or "rtu":
                        if sirenCommand != "":
                            # do siren process
                            self.ioLock.acquire()
                            sirenProcessState = self.ioBoard.setSiren(sirenCommand)
                            self.ioLock.release()
                            sirenProcessState = True
                            if  sirenProcessState == True:
                                logging.info("Command Thread    : Success set Siren")

                                self.smsSendSirenState(appName, sirenCommand)

                                res = self.dbApi.updatePendingCommand()
                                equipmentStatus = {
                                    "gpsLatitude" : str(self.gpsLatitude),
                                    "gpsLongitude" : str(self.gpsLongitude),
                                    "batteryVoltage" : str(self.batteryVoltage),
                                    "solarVoltage" : str(self.solarVoltage),
                                    "rtuTemperature" : str(self.rtuTemperature),
                                    "gsmSignal" : str(self.gsmSignal),
                                    "sirenMode" : str(sirenCommand),
                                }
                                self.currentSirenCommand = sirenCommand
                                self.dbApi.addEquipmentStatus(equipmentStatus)

                                # verify
                                res = self.dbApi.getPendingCommand()
                            else:
                                logging.info("Command Thread    : Failed to set siren")
                        else:
                            logging.info("Command Thread    : No valid sirenCommand")
                    elif appName == "button":
                        self.smsSendSirenState(appName, sirenCommand)
                        res = self.dbApi.updatePendingCommand()
                        equipmentStatus = {
                            "gpsLatitude" : str(self.gpsLatitude),
                            "gpsLongitude" : str(self.gpsLongitude),
                            "batteryVoltage" : str(self.batteryVoltage),
                            "solarVoltage" : str(self.solarVoltage),
                            "rtuTemperature" : str(self.rtuTemperature),
                            "gsmSignal" : str(self.gsmSignal),
                            "sirenMode" : str(sirenCommand),
                        }
                        self.currentSirenCommand = sirenCommand
                        self.dbApi.addEquipmentStatus(equipmentStatus)                        
                    else:
                        logging.info("Command Thread    : No valid command")

            except Exception as e:
                logging.info("Command Thread    : Exception ")
                logging.info(e)

    def setSirenCommand(self, appName, sirenState):
        result = self.dbApi.getSession("admin@email.com", "Qwerty@123")
        self.dbApi.setSirenCommand(appName, sirenState)

    def tryLogin(self, user, password):
        result = self.dbApi.getSession(user, password)
        print(result)
        if result == "":
            return False
        else:
            return True

    def getEquipementStatus(self):
        result = self.dbApi.getSession("admin@email.com", "Qwerty@123")
        result = self.dbApi.getEquipementStatus()
        return result

    def getConfiguration(self):
        result = self.dbApi.getSession("admin@email.com", "Qwerty@123")
        result = self.dbApi.getConfiguration()
        stationCode = result['stationCode']
        stationName = result['stationName']
        serialNumber = result['serialNumber']

        sessionId = self.rut955.getSession("root", "Ampang2020")
        if sessionId != "":
            ip = self.rut955.getIP(sessionId)
            self.ipAddress = ip


        ipAddress = self.ipAddress

        return (stationCode, stationName, serialNumber, ipAddress)

    def stop(self):
        self.isRunning = False

    def start(self):
        try:
            format = "%(asctime)s: %(message)s"
            logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

            x = threading.Thread(target=self.thread_pending_command, args=(1,))
            x.start()

            y = threading.Thread(target=self.thread_ioboard_status, args=(1,))
            y.start()

            monitor_button_thread = threading.Thread(target=self.thread_ioboard_button, args=(1,))
            monitor_button_thread.start()

            modem_thread = threading.Thread(target=self.thread_rut955_status, args=(1,))
            modem_thread.start()

            sms_thread = threading.Thread(target=self.thread_sms_status, args=(1,))
            sms_thread.start()

            # logging.info("Main    : wait for the thread to finish")
            #sms_thread.join()
            # y.join()
            # logging.info("Main    : all done")
        except  Exception as e:
            print("FAILED: ", e)

        return ""


if __name__ == "__main__":
    process = SirenProcess()
    process.start()
    # list = process.smsGetList()
    # print('list', list)

    # read = process.smsRead(2)
    # print('read', read)

    # total = process.smsTotal()
    # print('total', total)

    # delete = process.smsDeleteAll()
    # print('delete', delete)

    # list = process.smsGetList()
    # print('list', list)

    # read = process.smsRead(2)
    # print('read', read)

    # total = process.smsTotal()
    # print('total', total)
