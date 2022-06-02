import imaplib
import time
import email
import config
import os
import datetime

# GMAIL = "email@gmail.com"
# PASSWORD = "pw"
IMAP_HOST = 'imap.gmail.com'
DIRECT_FOLDER_EMAIL = "INBOX"

global cmd_list
cmd_list = []

################ IMAP SSL ##############################


class MailFetcher:
    def __init__(self, gmail, password) -> None:
        self.app_config = config.Config()
        self.mailbox = imaplib.IMAP4_SSL(
            host=IMAP_HOST, port=imaplib.IMAP4_SSL_PORT, timeout=None)
        print("Connection Object : {}".format(self.mailbox))
        self.gmail = gmail
        self.password = password
        self.mailbox.login(self.gmail , self.password)
        self.mailbox.select(mailbox=DIRECT_FOLDER_EMAIL, readonly=False)

    def fetch_newest(self):
        self.mailbox.noop()
        date = (datetime.date.today() -
                datetime.timedelta(days=1)).strftime("%d-%b-%Y")
        resp_code, mails = self.mailbox.search(
            None, "(UNSEEN)", "SINCE {0}".format(date))
        mail_ids = [id for id in mails[0].decode().split()]

        for id in mail_ids[::-1]:
            print(id)
            resp_code, msg = self.mailbox.fetch(id, '(RFC822)')
            self.mailbox.store(id, '+FLAGS', '(\\SEEN)')

            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])

                    sender, encoding = email.header.decode_header(msg.get("From"))[
                        0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding)
                    if sender.find('<') >= 0:
                        sender = sender[sender.find('<') + 1: len(sender) - 1]

                    if sender not in self.app_config.whitelist:
                        continue

                    subject, encoding = email.header.decode_header(msg["Subject"])[
                        0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)

                    print(sender, subject, sep='<----->')
                    return sender, subject

        return "", ""

    @staticmethod
    def print():
        print('Hello')


if __name__ == '__main__':
    # start = time.time()
    # client, command = get_cmd()
    # print("client: " + client + ", command: " + command)
    # print(time.time() - start)
    pass
