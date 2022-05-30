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



class MailFetcher:
    def __init__(self) -> None:
        #self.app_config = config.Config()
        self.mailbox = imaplib.IMAP4_SSL(
            host=IMAP_HOST, port=imaplib.IMAP4_SSL_PORT, timeout=None)
        print("Connection Object : {}".format(self.mailbox))
        self.mailbox.login(GMAIL, PASSWORD)
        self.mailbox.select(mailbox=DIRECT_FOLDER_EMAIL, readonly=False)

    count = 0

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
            mail = email.message_from_bytes(msg[1 if (self.count > 0) else 0][1])
            if isinstance(mail, str) == False:
                self.save_attachment(mail)
            self.mailbox.store(id, '+FLAGS', '(\\SEEN)')
            self.count += 1
            

            for response in msg:
                if isinstance(response, tuple):
                    # print('selected')
                    msg = email.message_from_bytes(response[1])

                    sender, encoding = email.header.decode_header(msg.get("From"))[
                        0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding)
                    #sender = sender[sender.find('<') + 1: len(sender) - 1]

                    #if sender not in self.app_config.whitelist:
                        # print(sender, 'not in whitelist')
                        #continue

                    subject, encoding = email.header.decode_header(msg["Subject"])[
                        0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding)

                    # print(sender, subject, sep='<----->')
                    return sender, subject

        return "", ""

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
