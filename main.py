import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QCoreApplication
from sirenProcess import SirenProcess
import sqlite3
import webbrowser
import threading
import time
import datetime

class IdleScreen(QDialog):
    def __init__(self, sirenProcess):
        super(IdleScreen, self).__init__()
        self.sirenProcess = sirenProcess
        loadUi("idleDlg.ui",self)
        self.isRunning = True

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
        
        self.y = threading.Thread(target=self.thread_siren_status, args=(1,))
        self.y.start()

    def thread_siren_status(self, name):
        while self.isRunning:
            try:
                time.sleep(1)
                now = datetime.datetime.now()
                self.labelDateTime.setText(now.strftime("%d/%m/%Y %H:%M:%S"))

                equipementState = self.sirenProcess.getEquipementStatus()
                sirenMode = int(equipementState['sirenMode'])
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
            except Exception as e:
                print(e)

    def gotologin(self):
        self.isRunning = False
        login = LoginScreen(self.sirenProcess)
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def closeApp(self):
        self.isRunning = False
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
            print(result)

            if result == False:
                self.labelError.setText("Invalid username or password")
            else:
                print("Successfully logged in.")
                self.labelError.setText("")
                mainScreen = MainScreen(self.sirenProcess)
                widget.addWidget(mainScreen)
                widget.setCurrentIndex(widget.currentIndex()+1)


        # if len(user)==0 or len(password)==0:
        #     self.labelError.setText("Please input all fields.")
        # else:
        #     conn = sqlite3.connect("ecoi.db")
        #     cur = conn.cursor()
        #     query = 'SELECT Password FROM User WHERE UserName =\''+user+"\'"
        #     cur.execute(query)
        #     result_pass = cur.fetchone()
        #     print(result_pass != None)
            
        #     if result_pass is None:
        #         self.labelError.setText("Invalid username or password")
        #     elif result_pass[0] == password:
        #         print("Successfully logged in.")
        #         self.labelError.setText("")
        #         mainScreen = MainScreen()
        #         widget.addWidget(mainScreen)
        #         widget.setCurrentIndex(widget.currentIndex()+1)
        #     else:
        #         self.labelError.setText("Invalid username or password")

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


        self.y = threading.Thread(target=self.thread_siren_status, args=(1,))
        self.y.start()

    def thread_siren_status(self, name):
        while self.isRunning:
            try:
                time.sleep(1)
                # now = datetime.datetime.now()
                # self.labelDateTime.setText(now.strftime("%d/%m/%Y %H:%M:%S"))

                equipementState = self.sirenProcess.getEquipementStatus()
                print(equipementState)
                sirenMode = int(equipementState['sirenMode'])
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
                
                gpsLatitude = equipementState['gpsLatitude']
                gpsLongitude = equipementState['gpsLongitude']
                batteryVoltage = equipementState['batteryVoltage']
                solarVoltage = equipementState['solarVoltage']
                rtuTemperature = equipementState['rtuTemperature']
                gsmSignal = equipementState['gsmSignal']

                self.labelGpsLatitude.setText(str(gpsLatitude))
                self.labelGpsLongitude.setText(str(gpsLongitude))
                self.labelBattery.setText(str(batteryVoltage))
                self.labelSolar.setText(str(solarVoltage))
                self.labelTemperature.setText(str(rtuTemperature))
                self.labelGsm.setText(str(gsmSignal))


            except Exception as e:
                print(e)
            

    def sendWarning(self):
        self.sirenProcess.setSirenCommand(1)

    def sendDanger(self):
        self.sirenProcess.setSirenCommand(2)

    def sendStop(self):
        self.sirenProcess.setSirenCommand(0)

    def openCameraView(self):
        webbrowser.open("https://google.com")

    def goToIdleScreen(self):
        self.isRunning = False
        screen = IdleScreen(self.sirenProcess)
        widget.addWidget(screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    # def goToConfigurationScreen(self):
    #     screen = ConfigurationScreen()
    #     widget.addWidget(screen)
    #     widget.setCurrentIndex(widget.currentIndex()+1)

# class ConfigurationScreen(QDialog):
#     def __init__(self):
#         super(ConfigurationScreen, self).__init__()
#         loadUi("configurationDlg.ui",self)
#         self.pushButtonBack.clicked.connect(self.goToMainScreen)

#     def goToMainScreen(self):
#         screen = MainScreen()
#         widget.addWidget(screen)
#         widget.setCurrentIndex(widget.currentIndex()+1)


# class CreateAccScreen(QDialog):
#     def __init__(self):
#         super(CreateAccScreen, self).__init__()
#         loadUi("createacc.ui",self)
#         self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
#         self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
#         self.signup.clicked.connect(self.signupfunction)

#     def signupfunction(self):
#         user = self.emailfield.text()
#         password = self.passwordfield.text()
#         confirmpassword = self.confirmpasswordfield.text()

#         if len(user)==0 or len(password)==0 or len(confirmpassword)==0:
#             self.error.setText("Please fill in all inputs.")

#         elif password!=confirmpassword:
#             self.error.setText("Passwords do not match.")
#         else:
#             conn = sqlite3.connect("shop_data.db")
#             cur = conn.cursor()

#             user_info = [user, password]
#             cur.execute('INSERT INTO login_info (username, password) VALUES (?,?)', user_info)

#             conn.commit()
#             conn.close()

#             fillprofile = FillProfileScreen()
#             widget.addWidget(fillprofile)
#             widget.setCurrentIndex(widget.currentIndex()+1)

# class FillProfileScreen(QDialog):
#     def __init__(self):
#         super(FillProfileScreen, self).__init__()
#         loadUi("fillprofile.ui",self)
#         self.image.setPixmap(QPixmap('placeholder.png'))





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