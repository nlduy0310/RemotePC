from config import *
import smtplib
import imaplib

if __name__ == '__main__':
    global app_config
    app_config = Config()
    print(app_config.is_authorized('abc123@gmail.com'))
    print(app_config.is_authorized('abc1234@gmail.com'))
