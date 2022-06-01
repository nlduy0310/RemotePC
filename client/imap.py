import threading
from concurrent.futures import thread
from ctypes.wintypes import tagRECT
import imaplib
import time
import email
import os
import datetime

GMAIL = "email@gmail.com"
PASSWORD = "pw"
IMAP_HOST = 'imap.gmail.com'
DIRECT_FOLDER_EMAIL = "INBOX"

global cmd_list
cmd_list = []

################ IMAP SSL ##############################

# https://www.thepythoncode.com/article/reading-emails-in-python


class MailReceiver:
    def __init__(self) -> None:
        self.mailbox = imaplib.IMAP4_SSL(
            host=IMAP_HOST, port=imaplib.IMAP4_SSL_PORT, timeout=None)
        print("Connection Object : {}".format(self.mailbox))
        self.mailbox.login(GMAIL, PASSWORD)
        self.mailbox.select(mailbox=DIRECT_FOLDER_EMAIL, readonly=False)

    def search_for(self, expected_sender, expected_subject):
        self.mailbox.noop()
        date = (datetime.date.today() -
                datetime.timedelta(days=1)).strftime("%d-%b-%Y")
        search_criteria = '(FROM \"' + expected_sender + \
            '\" SUBJECT \"' + expected_subject + '\")'
        resp_code, mails = self.mailbox.search(
            None, "(UNSEEN)", "SINCE {0}".format(date), search_criteria)
        mail_ids = [id for id in mails[0].decode().split()]

        for id in mail_ids[::-1]:
            # print(id)
            resp_code, msg = self.mailbox.fetch(id, '(RFC822)')

            for response in msg:
                if isinstance(response, tuple):
                    # print('selected')
                    msg = email.message_from_bytes(response[1])
                    # get sender
                    sender, encoding = email.header.decode_header(msg.get("From"))[
                        0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding)
                    if sender.find('<') >= 0:
                        sender = sender[sender.find('<') + 1:-1]
                    # if sender != expected_sender:
                    #     print(sender, 'not expected')
                    #     continue

                    # get subject
                    subject, encoding = email.header.decode_header(msg["Subject"])[
                        0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)
                    # if subject != expected_subject:
                    #     continue

                    # print('found requirements:', sender, subject)
                    self.mailbox.store(id, '+FLAGS', '(\\SEEN)')

                    # get attachment
                    if isinstance(msg, str) == False:
                        path = self.save_attachment(msg)
                    else:
                        path = None

                    # get body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(
                                part.get("Content-Disposition"))
                            if content_type == 'text/plain':
                                try:
                                    body += part.get_payload(
                                        decode=True).decode()
                                except:
                                    pass
                    else:
                        content_type = msg.get_content_type()
                        body += msg.get_payload(decode=True).decode()

                    # print(sender, subject, sep='<----->')
                    return sender, subject, body, path

        return "", "", None, None

    def save_attachment(self, msg, download_folder="./data"):
        """
        Given a message, save its attachments to the specified
        download folder (default is /tmp)
        return: file path to attachment
        """
        att_path = "No attachment found."
        for part in msg.walk():
            filename = part.get_filename()
            if filename:
                att_path = os.path.join(download_folder, filename)
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
        return att_path

    @staticmethod
    def print():
        print('Hello')


def await_response(expected_sender, expected_subject, time_s=30):
    print('waiting for response from', expected_sender,
          'on', expected_subject, 'for', time_s, 'seconds')
    receiver = MailReceiver()
    try:
        timeout = time.time() + time_s
        while time.time() <= timeout:
            sender, subject, body, path = receiver.search_for(
                expected_sender, expected_subject)
            if sender and subject:
                print('found', sender, subject)
                print('content:', body)
                if os.path.isfile(path):
                    print('attachment(s) found')
                print('displaying to GUI')
                return
        print(time_s, 'seconds passed')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # start = time.time()
    # client, command = get_cmd()
    # print("client: " + client + ", command: " + command)
    # print(time.time() - start)
    pass
