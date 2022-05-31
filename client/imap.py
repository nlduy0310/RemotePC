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
        resp_code, mails = self.mailbox.search(
            None, "(UNSEEN)", "SINCE {0}".format(date))
        mail_ids = [id for id in mails[0].decode().split()]

        for id in mail_ids[::-1]:
            # print(id)
            resp_code, msg = self.mailbox.fetch(id, '(RFC822)')

            for response in msg:
                if isinstance(response, tuple):
                    # print('selected')
                    msg = email.message_from_bytes(response[1])

                    sender, encoding = email.header.decode_header(msg.get("From"))[
                        0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding)
                    if sender.find('<') >= 0:
                        sender = sender[sender.find('<') + 1:-1]
                    print('sender:', sender)

                    if sender != expected_sender:
                        print(sender, 'not expected')
                        continue

                    subject, encoding = email.header.decode_header(msg["Subject"])[
                        0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)
                    print('subject: ', subject)
                    if subject != expected_subject:
                        print(subject, 'not expected')
                        continue

                    print('found requirements:', sender, subject)
                    self.mailbox.store(id, '+FLAGS', '(\\SEEN)')
                    # print('marked as seen')
                    print('found')

                    if isinstance(msg, str) == False:
                        path = self.save_attachment(msg)
                    else:
                        path = None
                    # print(sender, subject, sep='<----->')
                    return sender, subject, path

        return "", "", None

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


def await_response(receiver: MailReceiver, expected_sender, expected_subject, time_s=30):
    print('waiting for response from', expected_sender,
          'on', expected_subject, 'for', time_s, 'seconds')
    try:
        timeout = time.time() + time_s
        while time.time() <= timeout:
            sender, subject, path = receiver.search_for(
                expected_sender, expected_subject)
            if sender and subject:
                print('found', sender, subject)
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
