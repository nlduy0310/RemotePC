import smtplib
import imaplib
import smtp
import imap
import time

if __name__ == '__main__':
    handler = imap.MailFetcher()
    sender = smtp.MailSender()
    sender.send_attached_email("thukhoacntt@gmail.com", "screenshot", "")
    try:
        while True:
            print('Idling...\t Press Ctrl + C to escape')
            user_mail, cmd = handler.fetch_newest()

    except KeyboardInterrupt:
        print('Ctrl C pressed')