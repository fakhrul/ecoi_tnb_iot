import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import sqlite3
import webbrowser


class IdleScreen(QDialog):
    def __init__(self):
        super(IdleScreen, self).__init__()
        loadUi("idleDlg.ui",self)
        
        self.pushButtonLogin.clicked.connect(self.gotologin)
        pixmap = QPixmap('images/logo.png')
        self.labelLogo.setPixmap(pixmap)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("loginDlg.ui",self)

        self.pushButtonLogin.clicked.connect(self.loginfunction)
        self.pushButtonCancel.clicked.connect(self.cancelfunction)

    def cancelfunction(self):
        idle = IdleScreen()
        widget.addWidget(idle)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def loginfunction(self):
        user = self.lineEditUserName.text()
        password = self.lineEditPassword.text()
        print(user)
        print(password)


        if len(user)==0 or len(password)==0:
            self.labelError.setText("Please input all fields.")
        else:
            conn = sqlite3.connect("ecoi.db")
            cur = conn.cursor()
            query = 'SELECT Password FROM User WHERE UserName =\''+user+"\'"
            cur.execute(query)
            result_pass = cur.fetchone()
            print(result_pass != None)
            
            if result_pass is None:
                self.labelError.setText("Invalid username or password")
            elif result_pass[0] == password:
                print("Successfully logged in.")
                self.labelError.setText("")
                mainScreen = MainScreen()
                widget.addWidget(mainScreen)
                widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                self.labelError.setText("Invalid username or password")

class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("mainDlg.ui",self)
        self.pushButtonLogout.clicked.connect(self.goToIdleScreen)
        self.pushButtonConfiguration.clicked.connect(self.goToConfigurationScreen)
        self.pushButtonCamera.clicked.connect(self.openCameraView)
    def openCameraView(self):
        webbrowser.open("https://google.com")

    def goToIdleScreen(self):
        screen = IdleScreen()
        widget.addWidget(screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToConfigurationScreen(self):
        screen = ConfigurationScreen()
        widget.addWidget(screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

class ConfigurationScreen(QDialog):
    def __init__(self):
        super(ConfigurationScreen, self).__init__()
        loadUi("configurationDlg.ui",self)
        self.pushButtonBack.clicked.connect(self.goToMainScreen)

    def goToMainScreen(self):
        screen = MainScreen()
        widget.addWidget(screen)
        widget.setCurrentIndex(widget.currentIndex()+1)


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

idle = IdleScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(idle)
widget.setFixedHeight(600)
widget.setFixedWidth(800)
# widget.setWindowFlags(Qt.FramelessWindowHint)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")