from config import *
import imap
import psutil


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
    elif (cmd == "restart"):
        os.system("shutdown /r /t 1")
    elif (cmd == "list"):
        listOfRunningProcess = getListOfProcessSortedByMemory()
        for elem in listOfRunningProcess[:10] :
            print(elem)

    
if __name__ == '__main__':
    client, cmd = imap.get_cmd()
    execute_one_command(cmd)
    
