from config import *
import imap
import psutil
import os
import time

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

    if("shutdown" in cmd):
        do = "shutdown /s"
        if("--" in cmd and cmd[11:].isnumeric()):
            do += " /t " + cmd[11:]

        os.system(do)
        return "shutdown completed!" # gửi mess

    elif ("restart" in cmd):
        do = "shutdown /r"
        if("--" in cmd and cmd[10:].isnumeric()):
            do += " /t " + cmd[10:]
        os.system(do)
        return "restart completed!" # gửi mess

    # Ngu dong
    elif ("hibernate" in cmd):
        do = "shutdown /h"
        if("--" in cmd and cmd[12:].isnumeric()):
            do += " /t " + cmd[12:]
        os.system(do)
        return "hibernate completed!" # gửi mess

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
        for item in listOfRunningProcess:
            print(item)
        return listOfRunningProcess # 

    # kill --chrome messenger
    elif ("kill" in cmd):
        list_proc = cmd[7:].split()
        result = []
        for killed_proc in list_proc:
           for proc in psutil.process_iter():
               if killed_proc.lower() in proc.name().lower():
                   proc.kill()
                   result.append(proc.name()) # gửi mess
        for item in result:
            print(item)
        return result

    
if __name__ == '__main__':

    handler = imap.MailFetcher()

    cmd_list = []
    try:
        while True:
            print('Idling...\t Press Ctrl + C to escape')
            user_mail, cmd = handler.fetch_newest()
            if user_mail and cmd:
                cmd_list.append([user_mail, cmd, False])
                print('Executing', cmd, 'from', user_mail)
                result_text = execute_one_command(cmd)
                time.sleep(3)
                print('Sending result to', user_mail)
                # MailSender.send(user_mail, result_text, result_file)

    except KeyboardInterrupt:
        print('Ctrl C pressed')
        print('Whole cmd list:', cmd_list, sep='\n')
