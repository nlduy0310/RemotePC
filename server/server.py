from config import *
import imap
import psutil
import os
import time
import smtp
from datetime import datetime

# https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/

def getListOfProcessSortedByMemory():
    
    # Lấy danh sách proccess theo Memory Usage
    listOfProcObjects = []
    
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           # Append dict to list
           listOfProcObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
    return listOfProcObjects



def execute_one_command(cmd):
    if(cmd == "shutdown"):
        os.system("shutdown: /s /t 1")
        return ["Shutdown completed!", ""] # [subject, text]
    elif (cmd == "restart"):
        os.system("shutdown /r /t 1")
        return ["Restart completed!", ""] # [subject, text]

    # list --all | list: list tat ca process
    # list --10: list 10 process su dung nhieu Memory Usage nhat
    elif ("list" in cmd):
        if (cmd == "list" or cmd == "list --all"):
            listOfRunningProcess = getListOfProcessSortedByMemory()
        else:
            if cmd[7:].isnumeric():
                listOfRunningProcess = getListOfProcessSortedByMemory()[:int(cmd[7:])]
            else:
                listOfRunningProcess = ["None"]
        return listOfRunningProcess # gửi đính kèm ,  #sửa theo dạng [subject, text]
    # kill --chrome messenger
    elif ("kill" in cmd):
        list_proc = cmd[7:].split()
        result = []
        for killed_proc in list_proc:
           for proc in psutil.process_iter():
               if killed_proc.lower() in proc.name().lower():
                   proc.kill()
                   result.append(proc.name()) # gửi mess
        return result   #sửa theo dạng [subject, text]
    elif (cmd == "screenshot"):
        filepath = smtp.screenshot()
        now = datetime.now().strftime("%H:%M:%S, %Y/%m/%d")
        return [f"Screenshot at {now}", "", filepath]
    elif (cmd == "webcamshot"):
        filepath = smtp.webcamshot()
        now = datetime.now().strftime("%H:%M:%S, %Y/%m/%d")
        return [f"Webcamshot at {now}", "", filepath]




if __name__ == '__main__':
    handler = imap.MailFetcher()
    sender = smtp.MailSender()

    cmd_list = []
    try:
        while True:
            print('Idling...\t Press Ctrl + C to escape')
            user_mail, cmd = handler.fetch_newest()
            if user_mail and cmd:
                cmd_list.append([user_mail, cmd, False])
                print('Executing', cmd, 'from', user_mail)
                result = execute_one_command(cmd)
                time.sleep(3)
                print('Sending result to', user_mail)
                sender.send_attached_email(user_mail, result[0], result[1], result[2] if len(result)==3 else None)
                # MailSender.send(user_mail, result_text, result_file)

    except KeyboardInterrupt:
        print('Ctrl C pressed')
        print('Whole cmd list:', cmd_list, sep='\n')
    
