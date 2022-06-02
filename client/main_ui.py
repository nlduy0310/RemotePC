from cProfile import label
from email import message
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, 
                             QLabel, QPushButton, QWidget,
                             QLineEdit, QMessageBox,
                             QStackedLayout, QListWidget,
                             QVBoxLayout, QHBoxLayout,
                             QStackedWidget,
                             QGridLayout)
from PyQt5.QtCore import QRect, Qt
import client
import imap
import smtp

class Ui(QWidget):

    def setupUi(self, Main):

        Main.setObjectName("Main")
        Main.setFixedSize(900, 500)

        self.width = 900
        self.height = 500

        self.setFixedSize(self.width, self.height)

        '''MENU ON THE MAIN WINDOW'''
        self.menu = QStackedLayout()

        self.signin_wid = QWidget()
        self.main_wid = QWidget()

        self.signin_Ui()
        self.main_Ui()

        self.menu.addWidget(self.signin_wid)
        self.menu.addWidget(self.main_wid)

    def signin_Ui(self):
        self.signin_wid.setFixedSize(600, 400)
        self.setWindowTitle("Login window...")
        # stylesheet = """
        #         background-image: url("login_bg.png")
        #         """
        # self.signin_wid.setStyleSheet(stylesheet)
        self.welcome = QLabel(self.signin_wid)
        self.welcome.setGeometry(QRect(30, 120, 480, 200))
        self.welcome.setStyleSheet("font: 20pt Century Gothic")
        self.welcome.setAlignment(Qt.AlignCenter|Qt.AlignTop)
        self.welcome.setText("Welcome to the Control PC!")

        self.signin_user = QLineEdit(self)
        self.signin_user.setFixedSize(300, 30)
        #self.signin_user.setAlignment(Qt.AlignCenter)
        self.signin_pass = QLineEdit(self)
        self.signin_pass.setFixedSize(300, 30)
        #self.signin_pass.setAlignment(Qt.AlignCenter)
        self.signin_user_label = QLabel("E-Mail: ")
        self.signin_user_label.setFixedSize(100, 30)
        self.signin_user_label.setAlignment(Qt.AlignLeft)
        self.signin_pass_label = QLabel("Password: ")
        self.signin_pass_label.setFixedSize(100,30)       
        self.signin_pass_label.setAlignment(Qt.AlignLeft) 

        self.buttonLogin = QPushButton('Login', self)
        #self.buttonLogin.clicked.connect(self.handleLogin)  
        self.label_gmail = QLabel("@gmail.com")
        self.label_gmail.setFixedSize(150,30)
        self.label_gmail.setAlignment(Qt.AlignLeft)

        self.layout_user = QHBoxLayout()
        self.layout_user.addWidget(self.signin_user_label)
        self.layout_user.addWidget(self.signin_user)
        self.layout_user.addWidget(self.label_gmail)

        self.layout_sigin_2 = QHBoxLayout()
        self.layout_sigin_2.addWidget(self.signin_pass_label)
        self.layout_sigin_2.addWidget(self.signin_pass)
        self.layout_sigin_2.addWidget(self.buttonLogin)

        self.main_signin_layout = QVBoxLayout()
        self.main_signin_layout.addWidget(self.welcome)
        self.main_signin_layout.addLayout(self.layout_user)
        self.main_signin_layout.addLayout(self.layout_sigin_2)

        self.signin_wid.setLayout(self.main_signin_layout)

    def main_Ui(self):
        self.setWindowTitle("This is main window...")
        self.main_wid.setFixedSize(self.width, self.height)
        self.label_main = QLabel(self.main_wid)
        self.label_main.setGeometry(QRect(30, 120, 480, 200))
        self.label_main.setStyleSheet("font: 14pt Century Gothic")
        self.label_main.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_main.setText("This is main")
        self.button_back = QPushButton("Go Back")

        self.test_layout = QHBoxLayout()
        self.test_layout.addWidget(self.label_main)
        self.test_layout.addWidget(self.button_back)

        self.main_wid.setLayout(self.test_layout)

class Main(QMainWindow, Ui):

    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.buttonLogin.clicked.connect(self.signin_event)
        self.button_back.clicked.connect(self.setSigninWindow)

    def signin_event(self):
        # self.mail_sender = smtp.MailSender(self.signin_user.text() + "@gmail.com", self.signin_pass.text())
        # self.setMainWindow()
        try:
            print(self.signin_user.text() + "@gmail.com", self.signin_pass.text())
            self.mail_sender = smtp.MailSender(self.signin_user.text() + "@gmail.com", self.signin_pass.text())
            self.setMainWindow()
        except Exception:
            self.messageErrorSignIn()

    def messageErrorSignIn(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("The g-mail account does not exist or you entered the wrong password")
        #msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Cannot sign-in")
        #msg.setDetailedText("The details are as follows:")
        msg.exec_()
    def setSigninWindow(self):
        self.menu.setCurrentIndex(0)
    def setMainWindow(self):
        self.menu.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    M = Main()
    sys.exit(app.exec())

