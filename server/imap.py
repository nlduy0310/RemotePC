import imaplib
import time
import email
import config
import os
GMAIL = "emailcuamayong@gmail.com"
PASSWORD = "password"
DRIRECT_FOLDER_EMAIL = "INBOX"


################ IMAP SSL ##############################
def get_cmd(time_out = None):

    app_config = config.Config()

    while (True):
        with imaplib.IMAP4_SSL(host="imap.gmail.com", port=imaplib.IMAP4_SSL_PORT, timeout = time_out) as imap_ssl:
            print("Connection Object : {}".format(imap_ssl))

            ############### Login to Mailbox ######################
            #print("Logging into mailbox...")
            resp_code, response = imap_ssl.login(GMAIL, PASSWORD)

            ############### Set Mailbox #############
            resp_code, mail_count = imap_ssl.select(mailbox=DRIRECT_FOLDER_EMAIL, readonly=True)

            resp_code, mails = imap_ssl.search(None, "ALL")
            cnt_mails = len(mails[0].decode().split())
            if (cnt_mails> 0):
                # Lấy từ thư mới nhất
                for i in range(cnt_mails - 1, -1, -1):
                    mail_id = mails[0].decode().split()[i]
                    resp_code, mail_data = imap_ssl.fetch(mail_id, '(RFC822)') 

                    content = email.message_from_bytes(mail_data[0][1])
                    client_mail = content.get("From")
                    client_mail = client_mail[client_mail.find('<') + 1 : len(client_mail) - 1]
                    # Kiểm tra có trong danh sách không
                    if (client_mail not in app_config.whitelist):
                        continue
                    subject = content.get("Subject")                  
                    return client_mail, subject

            imap_ssl.close()

if __name__ == '__main__':
    start = time.time()
    client, command = get_cmd()
    print("client: " + client + ", command: " + command)
    print(time.time() - start)
