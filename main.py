import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QCoreApplication, QObject, QThread, pyqtSignal
from sirenProcess import SirenProcess
import sqlite3
import webbrowser
# import threading
import time
import datetime

class SirenStateThread(QObject):
    finished = pyqtSignal()
    sirenStateSignal = pyqtSignal(object)

    def __init__(self, sirenProcess):
        super(SirenStateThread, self).__init__()
        self.sirenProcess = sirenProcess
        self.isRunning = True

    def run(self):
        while self.isRunning:
            try:
                time.sleep(1)
                equipmentState = self.sirenProcess.getEquipementStatus()
                # sirenMode = int(equipementState['sirenMode'])
                self.sirenStateSignal.emit(equipmentState)
            except Exception as e:
                print(e)
        self.finished.emit()

class IdleScreen(QDialog):
    def __init__(self, sirenProcess):
        super(IdleScreen, self).__init__()
        self.sirenProcess = sirenProcess
        loadUi("idleDlg.ui",self)

        (stationCode, stationName, serialNumber, ipAddress) = self.sirenProcess.getConfiguration()

        self.labelStationCode.setText(stationCode)
        self.labelStationName.setText(stationName)
        self.labelSerialNumber.setText(serialNumber)
        self.labelIpAddress.setText(ipAddress)

        self.pushButtonLogin.clicked.connect(self.gotologin)
        self.pushButtonClose.clicked.connect(self.closeApp)
        pixmap = QPixmap('images/ecoi_logo.png')
        self.labelLogo.setPixmap(pixmap)
        self.labelSirenState.setText('UNKNOWN')
        self.frameSirenState.setStyleSheet('background-color: #E4E7EA')
        now = datetime.datetime.now()
        self.labelDateTime.setText(now.strftime("%d/%m/%Y %H:%M:%S"))
        
        # self.y = threading.Thread(target=self.thread_siren_status, args=(1,))
        # self.y.start()
        self.thread = QThread()
        self.sirenStateThread = SirenStateThread(sirenProcess)
        self.sirenStateThread.moveToThread(self.thread)
        self.thread.started.connect(self.sirenStateThread.run)
        self.sirenStateThread.finished.connect(self.thread.quit)
        self.sirenStateThread.finished.connect(self.sirenStateThread.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.sirenStateThread.sirenStateSignal.connect(self.updateSirenstate)
        self.thread.start()

    def updateSirenstate(self, equipmentState):
        now = datetime.datetime.now()
        self.labelDateTime.setText(now.strftime("%d/%m/%Y %H:%M:%S"))
        # print("equipmentState",equipmentState)
        sirenMode = int(equipmentState['sirenMode'])
        if sirenMode == 0:
            self.labelSirenState.setText('STOP')
            self.frameSirenState.setStyleSheet('background-color: #636F83')
        elif sirenMode == 1:
            self.labelSirenState.setText('WARNING')
            self.frameSirenState.setStyleSheet('background-color: #F9B115')
        elif sirenMode == 2:
            self.labelSirenState.setText('DANGER')
            self.frameSirenState.setStyleSheet('background-color: #E55353')
        else:
            self.labelSirenState.setText('UNKNOWN')
            self.frameSirenState.setStyleSheet('background-color: #E4E7EA')


    def gotologin(self):
        self.sirenStateThread.isRunning = False
        login = LoginScreen(self.sirenProcess)
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def closeApp(self):
        self.sirenStateThread.isRunning = False
        QCoreApplication.instance().quit()


class LoginScreen(QDialog):
    def __init__(self, sirenProcess):
        super(LoginScreen, self).__init__()
        self.sirenProcess = sirenProcess
        loadUi("loginDlg.ui",self)

        pixmap = QPixmap('images/ecoi_logo.png')
        self.labelLogo.setPixmap(pixmap)
        
        self.pushButtonLogin.clicked.connect(self.loginfunction)
        self.pushButtonCancel.clicked.connect(self.cancelfunction)

    def cancelfunction(self):
        idle = IdleScreen(self.sirenProcess)
        widget.addWidget(idle)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def loginfunction(self):
        user = self.lineEditUserName.text()
        password = self.lineEditPassword.text()

        if len(user)==0 or len(password)==0:
            self.labelError.setText("Please input all fields.")
        else:
            result = self.sirenProcess.tryLogin(user, password)
            # print(result)

            if result == False:
                self.labelError.setText("Invalid username or password")
            else:
                print("Successfully logged in.")
                self.labelError.setText("")
                mainScreen = MainScreen(self.sirenProcess)
                widget.addWidget(mainScreen)
                widget.setCurrentIndex(widget.currentIndex()+1)



class MainScreen(QDialog):
    def __init__(self, sirenProcess):
        super(MainScreen, self).__init__()
        self.sirenProcess = sirenProcess
        loadUi("mainDlg.ui",self)
        self.isRunning = True

        (stationCode, stationName, serialNumber, ipAddress) = self.sirenProcess.getConfiguration()
        
        self.labelStationInfo.setText(stationName + '(' + stationCode + ') - ' + serialNumber)

        self.labelSirenState.setText('UNKNOWN')
        self.frameSirenState.setStyleSheet('background-color: #E4E7EA')

        self.pushButtonWarning.setStyleSheet('image: url(images/siren.png); background-color: #F9B115;')
        self.pushButtonDanger.setStyleSheet('image: url(images/siren.png); background-color: #E55353;')
        self.pushButtonStop.setStyleSheet('image: url(images/no_siren.png); background-color: #636F83;')
        self.pushButtonCamera.setStyleSheet('image: url(images/cctv.png);')

        self.pushButtonLogout.clicked.connect(self.goToIdleScreen)
        #self.pushButtonConfiguration.clicked.connect(self.goToConfigurationScreen)
        self.pushButtonCamera.clicked.connect(self.openCameraView)

        self.pushButtonWarning.clicked.connect(self.sendWarning)
        self.pushButtonDanger.clicked.connect(self.sendDanger)
        self.pushButtonStop.clicked.connect(self.sendStop)


        # self.y = threading.Thread(target=self.thread_siren_status, args=(1,))
        # self.y.start()
        self.thread = QThread()
        self.sirenStateThread = SirenStateThread(sirenProcess)
        self.sirenStateThread.moveToThread(self.thread)
        self.thread.started.connect(self.sirenStateThread.run)
        self.sirenStateThread.finished.connect(self.thread.quit)
        self.sirenStateThread.finished.connect(self.sirenStateThread.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.sirenStateThread.sirenStateSignal.connect(self.updateSirenstate)
        self.thread.start()

    def updateSirenstate(self, equipmentState):
        # now = datetime.datetime.now()
        # self.labelDateTime.setText(now.strftime("%d/%m/%Y %H:%M:%S"))

        sirenMode = int(equipmentState['sirenMode'])

        if sirenMode == 0:
            self.labelSirenState.setText('STOP')
            self.frameSirenState.setStyleSheet('background-color: #636F83')
        elif sirenMode == 1:
            self.labelSirenState.setText('WARNING')
            self.frameSirenState.setStyleSheet('background-color: #F9B115')
        elif sirenMode == 2:
            self.labelSirenState.setText('DANGER')
            self.frameSirenState.setStyleSheet('background-color: #E55353')
        else:
            self.labelSirenState.setText('UNKNOWN')
            self.frameSirenState.setStyleSheet('background-color: #E4E7EA')

        gpsLatitude = equipmentState['gpsLatitude']
        gpsLongitude = equipmentState['gpsLongitude']
        batteryVoltage = equipmentState['batteryVoltage']
        solarVoltage = equipmentState['solarVoltage']
        rtuTemperature = equipmentState['rtuTemperature']
        gsmSignal = equipmentState['gsmSignal']

        self.labelGpsLatitude.setText(str(gpsLatitude))
        self.labelGpsLongitude.setText(str(gpsLongitude))
        self.labelBattery.setText(str(batteryVoltage))
        self.labelSolar.setText(str(solarVoltage))
        self.labelTemperature.setText(str(rtuTemperature))
        self.labelGsm.setText(str(gsmSignal))


    def sendWarning(self):
        self.sirenProcess.setSirenCommand(1)

    def sendDanger(self):
        self.sirenProcess.setSirenCommand(2)

    def sendStop(self):
        self.sirenProcess.setSirenCommand(0)

    def openCameraView(self):
        webbrowser.open("https://google.com")

    def goToIdleScreen(self):
        self.sirenStateThread.isRunning = False
        screen = IdleScreen(self.sirenProcess)
        widget.addWidget(screen)
        widget.setCurrentIndex(widget.currentIndex()+1)


# main
app = QApplication(sys.argv)
siren = SirenProcess()

idle = IdleScreen(siren)
widget = QtWidgets.QStackedWidget()
widget.addWidget(idle)
widget.setFixedHeight(480)
widget.setFixedWidth(800)
widget.setWindowFlags(Qt.FramelessWindowHint)
widget.show()

siren.start()


try:
    sys.exit(app.exec_())
    
except:
    siren.stop()
    print("Exiting")