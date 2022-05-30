import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

from imap import PASSWORD

send_from = 'from@gmail.com'
PASSW = ''
server= "smtp.gmail.com"
port = 587

def send_mail(send_to, subject, text, files=None):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    smtp.ehlo()
    smtp.starttls()

    smtp.login(send_from, PASSW)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

if __name__ == "__main__":

    send_to = ""
    subject = ""
    text = ""
    files = ['data/1.txt', 'data/2.txt']

    send_mail(send_to, subject, "text", files)
