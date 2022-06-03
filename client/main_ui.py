from cProfile import label
from email import message
from email.charset import QP
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, 
                             QLabel, QPushButton, QWidget,
                             QLineEdit, QMessageBox, QComboBox,
                             QStackedLayout, QListWidget,
                             QVBoxLayout, QHBoxLayout,
                             QStackedWidget, QTextEdit,
                             QGridLayout, QGroupBox, QTableWidget)
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRect, Qt
import client
import imap
import smtp

dir_to_icon = "ui/icon/"
dir_to_bg = "ui/background/"
class Ui(QWidget):

    def setupUi(self, Main):

        Main.setObjectName("Main")
        Main.setFixedSize(1000, 600)

        self.width = 1000
        self.height = 600

        self.setFixedSize(self.width, self.height)

        '''MENU ON THE MAIN WINDOW'''
        self.menu = QStackedLayout()

        self.signin_wid = QWidget()
        self.main_wid = QWidget()
        self.server_list_wid = QWidget()

        self.signin_Ui()
        self.main_Ui()
        self.server_list_Ui()

        self.menu.addWidget(self.signin_wid)
        self.menu.addWidget(self.main_wid)
        self.menu.addWidget(self.server_list_wid)

    def signin_Ui(self):
        self.signin_wid.setFixedSize(600, 400)
        self.setAutoFillBackground(True)
        self.signin_wid.setWindowTitle("Login window")
        self.signin_wid.setWindowIcon(QtGui.QIcon(dir_to_icon + "icon_gmail.png"))
        self.signin_wid.setStyleSheet("color: black;"
                        "background-color: white;"
                        "selection-color: black;"
                        "selection-background-color: blue;")
        self.welcome = QLabel(self.signin_wid)
        #self.welcome.setGeometry(QRect(30, 120, 480, 200))
        self.welcome.setStyleSheet("font: 20pt Century Gothic")
        self.welcome.setAlignment(Qt.AlignCenter|Qt.AlignTop)
        self.welcome.setText("Welcome to the Control PC!")

        self.welcome_icon = QLabel()
        pixmap = QtGui.QPixmap(dir_to_icon + 'control.jpg')
        self.welcome_icon.setPixmap(pixmap)
        self.welcome_icon.setMask(pixmap.mask())
        self.welcome_icon.setAlignment(Qt.AlignCenter|Qt.AlignTop)


        self.signin_user = QLineEdit(self)
        self.signin_user.setFixedSize(300, 30)
        #self.signin_user.setAlignment(Qt.AlignCenter)
        self.signin_pass = QLineEdit(self)
        self.signin_pass.setFixedSize(300, 30)
        self.signin_pass.setEchoMode(QLineEdit.Password)
        self.signin_pass.setStyleSheet('lineedit-password-character: 9679')
        #self.signin_pass.setAlignment(Qt.AlignCenter)
        self.signin_user_label = QLabel("E-Mail: ")
        self.signin_user_label.setStyleSheet("font-weight: bold")
        self.signin_user_label.setFixedSize(100, 30)
        self.signin_user_label.setAlignment(Qt.AlignLeft)
        self.signin_pass_label = QLabel("Password: ")
        self.signin_pass_label.setStyleSheet("font-weight: bold")
        self.signin_pass_label.setFixedSize(100,30)       
        self.signin_pass_label.setAlignment(Qt.AlignLeft) 

        self.buttonLogin = QPushButton('Login')
        self.buttonLogin.setStyleSheet('''
QPushButton {
    background-color: #2B5DD1;
    color: #FFFFFF;
    border-style: outset;
    padding: 2px;
    font: bold 20px;
    border-width: 6px;
    border-radius: 10px;
    border-color: #2752B8;
}
QPushButton:hover {
    background-color: lightgreen;
}
        ''')

        #self.buttonLogin.clicked.connect(self.handleLogin)  
        self.label_gmail = QLabel("@gmail.com")
        self.label_gmail.setStyleSheet("font-weight: bold")
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
        self.main_signin_layout.addWidget(self.welcome_icon)
        self.main_signin_layout.addWidget(self.welcome)
        self.main_signin_layout.addLayout(self.layout_user)
        self.main_signin_layout.addLayout(self.layout_sigin_2)

        self.signin_wid.setLayout(self.main_signin_layout)

    def main_Ui(self):
        self.main_wid.setWindowTitle("Main window")
        self.main_wid.setWindowIcon(QtGui.QIcon(dir_to_icon + "client"))
        self.main_wid.setFixedSize(self.width, self.height)

        self.btn_1 = QPushButton("List processes")
        self.btn_2 = QPushButton("Kill processes") 
        self.btn_3 = QPushButton("Shutdown/Restart/Hibernate")
        self.btn_4 = QPushButton("Keylog")
        self.btn_5 = QPushButton("Edit resgistry")
        self.btn_6 = QPushButton("Screenshot")
        self.btn_7 = QPushButton("Webcam")
        self.btn_8 = QPushButton("Retrieve a file")
        
        self.btn_1.setStyleSheet("text-align:left;")
        self.btn_2.setStyleSheet("text-align:left;")
        self.btn_3.setStyleSheet("text-align:left;")
        self.btn_4.setStyleSheet("text-align:left;")
        self.btn_5.setStyleSheet("text-align:left;")
        self.btn_6.setStyleSheet("text-align:left;")
        self.btn_7.setStyleSheet("text-align:left;")
        self.btn_8.setStyleSheet("text-align:left;")

        self.btn_1.setFixedSize(190, 30)
        self.btn_2.setFixedSize(190, 30)
        self.btn_3.setFixedSize(190, 30)
        self.btn_3.setFont(QtGui.QFont('Times', 5))
        self.btn_4.setFixedSize(190, 30)
        self.btn_5.setFixedSize(190, 30)
        self.btn_6.setFixedSize(190, 30)
        self.btn_7.setFixedSize(190, 30)
        self.btn_8.setFixedSize(190, 30)

        self.btn_1.setIcon(QtGui.QIcon(dir_to_icon + "list.png"))
        self.btn_2.setIcon(QtGui.QIcon(dir_to_icon + "kill.png"))
        self.btn_3.setIcon(QtGui.QIcon(dir_to_icon + "power.png"))
        self.btn_4.setIcon(QtGui.QIcon(dir_to_icon + "keylog.png"))
        self.btn_5.setIcon(QtGui.QIcon(dir_to_icon + "registry.png"))
        self.btn_6.setIcon(QtGui.QIcon(dir_to_icon + "screenshot.png"))
        self.btn_7.setIcon(QtGui.QIcon(dir_to_icon + "webcam.png"))
        self.btn_8.setIcon(QtGui.QIcon(dir_to_icon + "file.png"))
        
        # Items on left layout
        self.btn_server_ls = QPushButton("List servers")
        self.btn_server_ls.setFixedSize(150, 40)
        self.btn_server_ls.setIcon(QtGui.QIcon(dir_to_icon + "servers.png"))
        self.main_left_label_cbb = QLabel("Choose a server:")
        self.cbb = QComboBox()
        self.cbb.setFixedSize(150, 30)
        self.btn_back = QPushButton("Back to Sign-in")
        self.btn_back.setFixedSize(150, 40)
        self.btn_back.setIcon(QtGui.QIcon(dir_to_icon + "return.png"))

        # Items on center Layout
        self.main_result = QTextEdit()
        self.main_result.setReadOnly(True)
        document = self.main_result.document()
        cursor = QtGui.QTextCursor(document)
        #p = cursor.position()

        # text
        text = ''.join(open('data/text.txt').readlines())
        cursor.insertText(text)
        # image
        cursor.insertImage('data/desktop.jpg')

        self.main_left_layout = QVBoxLayout()
        self.main_left_layout.addWidget(self.main_left_label_cbb)
        self.main_left_layout.addWidget(self.cbb)
        self.main_left_layout.addStretch()
        self.main_left_layout.addWidget(self.btn_server_ls)
        self.main_left_layout.addWidget(self.btn_back)

        # Center laout
        self.main_center_layout = QVBoxLayout()
        self.main_center_gb = QGroupBox("Result: ")
        self.main_center_gb.setStyleSheet("font-weight: bold")
        self.main_center_layout.addWidget(self.main_result)
        self.main_center_gb.setLayout(self.main_center_layout)

        # Right layout
        self.layout_cmd = QVBoxLayout()
        self.layout_cmd.addWidget(self.btn_1)
        self.layout_cmd.addWidget(self.btn_2)
        self.layout_cmd.addWidget(self.btn_3)
        self.layout_cmd.addWidget(self.btn_4)
        self.layout_cmd.addWidget(self.btn_5)
        self.layout_cmd.addWidget(self.btn_6)
        self.layout_cmd.addWidget(self.btn_7)
        self.layout_cmd.addWidget(self.btn_8)

        self.main_right_gb = QGroupBox("Some functions: ")
        self.main_right_gb.setStyleSheet("font-weight: bold")
        self.main_right_gb.setLayout(self.layout_cmd)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.main_left_layout)
        self.main_layout.addWidget(self.main_center_gb)
        self.main_layout.addWidget(self.main_right_gb)

        self.main_wid.setLayout(self.main_layout)

    def server_list_Ui(self):
        self.serverList = dict()
        self.server_list_wid.setWindowTitle("Server list")
        self.server_list_wid.setWindowIcon(QtGui.QIcon(dir_to_icon + "serverlist.png"))
        self.server_list_wid.setFixedSize(self.width, self.height)
        
        self.server_list_layout = QVBoxLayout()
        self.server_list_label = QLabel("<b>List of accessed remote PC<b>")
        self.server_list_label.setAlignment(Qt.AlignCenter)
        self.server_list_layout.addWidget(self.server_list_label)        
        self.server_list_hlayout = QHBoxLayout()
        self.server_list_layout.addLayout(self.server_list_hlayout)

        self.server_list_table = QTableWidget()
        self.server_list_table.setColumnCount(2)
        self.server_list_table.setRowCount(15)
        self.server_list_table.setHorizontalHeaderLabels(["Server Name", "Email"])
        self.server_list_table.setColumnWidth(0, 300)
        self.server_list_table.setColumnWidth(1, 500)        
        for r in range(15):
            for c in range(2):
                self.server_list_table.setItem(r , c, None)
        self.server_list_hlayout.addWidget(self.server_list_table)

        self.server_list_vlayout = QVBoxLayout()
        self.server_list_btn_save = QPushButton()
        self.server_list_btn_save.setText("Save")
        self.server_list_btn_close = QPushButton()
        self.server_list_btn_close.setText("Close")
        self.server_list_vlayout.addWidget(self.server_list_btn_save)
        self.server_list_vlayout.addWidget(self.server_list_btn_close)
        self.server_list_vlayout.addStretch(0)
        self.server_list_hlayout.addLayout(self.server_list_vlayout)

        self.server_list_wid.setLayout(self.server_list_layout)
    
    


class Main(QMainWindow, Ui):

    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)

        self.buttonLogin.clicked.connect(self.signin_event)
        self.btn_back.clicked.connect(self.setSigninWindow)
        self.btn_server_ls.clicked.connect(self.setListServer)
        self.server_list_btn_save.clicked.connect(self.saveServerList)
        self.server_list_btn_close.clicked.connect(self.setMainWindow)

    def signin_event(self):
        # self.mail_sender = smtp.MailSender(self.signin_user.text() + "@gmail.com", self.signin_pass.text())
        # self.setMainWindow()
        try:
            #print(self.signin_user.text() + "@gmail.com", self.signin_pass.text())
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
        self.signin_pass.setText("")
        self.menu.setCurrentIndex(0)

    def setMainWindow(self):
        self.menu.setCurrentIndex(1)

    def setListServer(self):
        self.menu.setCurrentIndex(2)

    def saveServerList(self):
        for r in range(15):
            if (not isinstance(self.server_list_table.item(r,0),type(None)) and not isinstance(self.server_list_table.item(r,1),type(None))):
                self.serverList[self.server_list_table.item(r,0).text()] = self.server_list_table.item(r,1).text()
        for x in range(len(self.serverList)):
            self.cbb.insertItem(x, str(list(self.serverList)[x]))
        print(self.serverList)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    M = Main()
    sys.exit(app.exec())

