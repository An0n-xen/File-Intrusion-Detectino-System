# Import PyQt5 dep
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QApplication
from PyQt5 import uic
from PyQt5.QtCore import Qt

import sys
import hashlib
import brain

class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        self.log = uic.loadUi('UI_files/Login3.ui',self)
        self.log.setWindowFlags(Qt.FramelessWindowHint)
        self.log.setAttribute(Qt.WA_TranslucentBackground)

        # Setting up Username and Pasword
        self.usrname = self.log.findChild(QLineEdit, 'Username')
        self.passwrd = self.log.findChild(QLineEdit, 'Password')

        # Setting up login button
        self.login = self.log.findChild(QPushButton, 'Login')
        self.login.clicked.connect(self.credcheck)

        self.log.show()

    def credcheck(self):
        username = self.usrname.text().encode()
        password = self.passwrd.text().encode()

        username = hashlib.sha256(username).hexdigest()
        password = hashlib.sha256(password).hexdigest()

        if username == 'c1c224b03cd9bc7b6a86d77f5dace40191766c485cd55dc48caf9ac873335d6f' and password == '82f0586bfa6ab4eeb9a65130379e40156187e48c096fa4b979d171dd626d78bc':
                print('Welcome Negar')
                self.log.close()
        

if __name__ == '__main__':
        app = QApplication(sys.argv)
        UIWindow = Login()
        app.exec()

brain.initialize()