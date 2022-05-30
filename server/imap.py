import imaplib
import time
import email
import config
import os
import datetime
GMAIL = "email@gmail.com"
PASSWORD = "pw"
IMAP_HOST = 'imap.gmail.com'
DIRECT_FOLDER_EMAIL = "INBOX"

global cmd_list
cmd_list = []

################ IMAP SSL ##############################


def get_cmd(time_out=None):

    app_config = config.Config()

    while (True):
        with imaplib.IMAP4_SSL(host=IMAP_HOST, port=imaplib.IMAP4_SSL_PORT, timeout=time_out) as imap_ssl:
            print("Connection Object : {}".format(imap_ssl))

            ############### Login to Mailbox ######################
            #print("Logging into mailbox...")
            resp_code, response = imap_ssl.login(
                GMAIL, PASSWORD)

            ############### Set Mailbox #############
            resp_code, mail_count = imap_ssl.select(
                mailbox=DIRECT_FOLDER_EMAIL, readonly=True)

            resp_code, mails = imap_ssl.search(None, "ALL")
            cnt_mails = len(mails[0].decode().split())
            if (cnt_mails > 0):
                # Lấy từ thư mới nhất
                for i in range(cnt_mails - 1, -1, -1):
                    mail_id = mails[0].decode().split()[i]
                    resp_code, mail_data = imap_ssl.fetch(mail_id, '(RFC822)')

                    content = email.message_from_bytes(mail_data[0][1])
                    client_mail = content.get("From")
                    client_mail = client_mail[client_mail.find(
                        '<') + 1: len(client_mail) - 1]
                    # Kiểm tra có trong danh sách không
                    if (client_mail not in app_config.whitelist):
                        continue
                    subject = content.get("Subject")
                    return client_mail, subject

            imap_ssl.close()


class MailFetcher:
    def __init__(self) -> None:
        self.app_config = config.Config()
        self.mailbox = imaplib.IMAP4_SSL(
            host=IMAP_HOST, port=imaplib.IMAP4_SSL_PORT, timeout=None)
        print("Connection Object : {}".format(self.mailbox))
        self.mailbox.login(GMAIL, PASSWORD)
        self.mailbox.select(mailbox=DIRECT_FOLDER_EMAIL, readonly=False)

    def fetch_newest(self):
        self.mailbox.noop()
        date = (datetime.date.today() -
                datetime.timedelta(days=1)).strftime("%d-%b-%Y")
        resp_code, mails = self.mailbox.search(
            None, "(UNSEEN)", "SINCE {0}".format(date))
        mail_ids = [id for id in mails[0].decode().split()]

        for id in mail_ids[::-1]:
            # print(id)
            resp_code, msg = self.mailbox.fetch(id, '(RFC822)')
            self.mailbox.store(id, '+FLAGS', '(\\SEEN)')

            for response in msg:
                if isinstance(response, tuple):
                    # print('selected')
                    msg = email.message_from_bytes(response[1])

                    sender, encoding = email.header.decode_header(msg.get("From"))[
                        0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding)
                    sender = sender[sender.find('<') + 1: len(sender) - 1]

                    if sender not in self.app_config.whitelist:
                        # print(sender, 'not in whitelist')
                        continue

                    subject, encoding = email.header.decode_header(msg["Subject"])[
                        0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)

                    # print(sender, subject, sep='<----->')
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

    handler = MailFetcher()
    MailFetcher.print()
    try:
        while True:
            print('Idling...\t Press Ctrl + C to escape')
            user_mail, cmd = handler.fetch_newest()
            if user_mail and cmd:
                cmd_list.append([user_mail, cmd, False])
                print('Executing', cmd, 'from', user_mail)
                # result_text, result_file = execute_command(cmd)
                print('Sending result to', user_mail)
                # MailSender.send(user_mail, result_text, result_file)

    except KeyboardInterrupt:
        print('Ctrl C pressed')
        print('Whole cmd list:', cmd_list, sep='\n')
