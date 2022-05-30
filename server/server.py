from config import *
import imap
import psutil
import os
import time
import smtp
from datetime import datetime


dir_data = "data/"

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
    dir_file = None
    if("shutdown" in cmd):
        do = "shutdown /s"
        if("--" in cmd and cmd[11:].isnumeric()):
            do += " /t " + cmd[11:]

        os.system(do)
        return ["Shutdown completed!", ""] # [subject, text]

    elif ("restart" in cmd):
        do = "shutdown /r"
        if("--" in cmd and cmd[10:].isnumeric()):
            do += " /t " + cmd[10:]
        os.system(do)
        return ["Restart completed!", ""] # [subject, text]

    # Ngu dong
    elif ("hibernate" in cmd):
        do = "shutdown /h"
        if("--" in cmd and cmd[12:].isnumeric()):
            do += " /t " + cmd[12:]
        os.system(do)
        return ["Hibernate completed!", ""] # [subject, text]

    # list --all | list: list tat ca process
    # list --10: list 10 process su dung nhieu Memory Usage nhat
    elif ("list" in cmd):
        text = ""
        if (cmd == "list" or cmd == "list --all"):
            listOfRunningProcess = getListOfProcessSortedByMemory()
            text = "List all processes: complete!"
        else:
            if cmd[7:].isnumeric():
                listOfRunningProcess = getListOfProcessSortedByMemory()[:int(cmd[7:])]
                text = "List " + cmd[7:] + " processes: complete!"
            else:
                listOfRunningProcess = ["None"]
                text = "List cmd error!"

        dir_file = dir_data + cmd + ".txt"
        f = open(dir_file, "w+")
        
        # chuyen list dictionary sang chuoi
        listOfRunningProcess = [str(x) for x in listOfRunningProcess]
        listOfRunningProcess = '\n'.join(listOfRunningProcess)
        f.write(listOfRunningProcess)
        f.close()

        return [text, "", dir_file] # [subject, text, filepath]

    # kill --chrome messenger
    elif ("kill" in cmd):
        list_proc = cmd[7:].split()
        result = []
        for killed_proc in list_proc:
           for proc in psutil.process_iter():
               if killed_proc.lower() in proc.name().lower():
                   proc.kill()
                   if(len(result) == 0 or (len(result) > 0 and result[len(result) - 1] != proc.name())):
                       result.append(proc.name())
        dir_file = dir_data + "killed_list.txt"
        text = "There are " + str(len(result)) + "/" + str(len(list_proc)) + " proccess killed"
        f = open(dir_file, "w+")
        f.write(text)
        for item in result:
            f.write(item)
        f.close()
        return [text, "", dir_file] # [subject, text, filepath]
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
