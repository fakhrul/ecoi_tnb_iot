import logging
import threading
import time
from dbApi import DbApi
from rut955 import Rut955
from ioBoard import IoBoard

class SirenProcess:
    def __init__(self):
        self.isRunning = True
        self.dbApi = DbApi()
        self.equipment = Rut955()
        self.ioBoard = IoBoard()

        self.gsmSignal = 0
        self.gpsLatitude = 0
        self.gpsLongitude = 0

        self.batteryVoltage = 0
        self.solarVoltage = 0
        self.rtuTemperature = 0

    def thread_equipment_status(self, name):
        while self.isRunning:
            try: 
                time.sleep(1)
                sessionId = self.equipment.getSession("root", "Ampang2020")
                if sessionId != "":
                    self.gsmSignal = int(self.equipment.getGsmRSSI(sessionId))
                    gps = self.equipment.getGps(sessionId)
                    self.gpsLatitude = float(gps.splitlines()[0])
                    self.gpsLongitude = float(gps.splitlines()[1])

                    boardStatus = self.ioBoard.getMebt()
                    boardStatuses = boardStatus.split(",")
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
                    }
                    result = self.dbApi.getSession("admin@email.com", "Qwerty@123")
                    self.dbApi.addEquipmentStatus(equipmentStatus)

                print(str(self.gsmSignal))
                print(self.gpsLatitude)
                print(self.gpsLongitude)

            except:
                print('ERROR')


    def thread_command(self, name):
        while self.isRunning:
            try:
                time.sleep(1)
                logging.info("Command Thread    : Login to DB")
                result = self.dbApi.getSession("admin@email.com", "Qwerty@123")
                sirenCommand = self.dbApi.getPendingCommand()
                print(sirenCommand)

                if sirenCommand != "":
                    # do siren process
                    print('do siren process')
                    sirenProcessState = self.ioBoard.setSiren(sirenCommand)

                    sirenProcessState = True

                    if  sirenProcessState == True:
                        logging.info("Command Thread    : Success set Siren")
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
                        self.dbApi.addEquipmentStatus(equipmentStatus)

                        # verify
                        res = self.dbApi.getPendingCommand()
                        print("pending", res)
                    else:
                        logging.info("Command Thread    : Failed to set siren")

                else:
                    print('no pending')
            except Exception as e:
                logging.info("Command Thread    : Exception ")
                logging.info(e)

    def setSirenCommand(self, sirenState):
        result = self.dbApi.getSession("admin@email.com", "Qwerty@123")
        self.dbApi.setSirenCommand(sirenState)

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

        ipAddress = 'Unknown'

        return (stationCode, stationName, serialNumber, ipAddress)

    def stop(self):
        self.isRunning = False

    def start(self):
        try:
            format = "%(asctime)s: %(message)s"
            logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

            x = threading.Thread(target=self.thread_command, args=(1,))
            x.start()

            y = threading.Thread(target=self.thread_equipment_status, args=(1,))
            y.start()

            # logging.info("Main    : wait for the thread to finish")
            # x.join()
            # y.join()
            # logging.info("Main    : all done")
        except  Exception as e:
            print("FAILED: ", e)

        return ""


if __name__ == "__main__":
    process = SirenProcess()
