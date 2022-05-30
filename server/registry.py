from email.mime import base
from msilib.schema import Registry
import winreg

STR_TO_BYTES_ENCODING = 'utf-8'

def get_base_key(string: str):
    if string == 'HKEY_CLASSES_ROOT':
        return winreg.HKEY_CLASSES_ROOT
    elif string == 'HKEY_CURRENT_USER':
        return winreg.HKEY_CURRENT_USER
    elif string == 'HKEY_LOCAL_MACHINE':
        return winreg.HKEY_LOCAL_MACHINE
    elif string == 'HKEY_USERS':
        return winreg.HKEY_USERS
    elif string == 'HKEY_CURRENT_CONFIG':
        return winreg.HKEY_CURRENT_CONFIG
    
    return None

def convert_value_type(value_str:str, value_type):
    if value_type == winreg.REG_BINARY:
        if value_str.isnumeric():
            return bytes(int(value_str).to_bytes(length=(int(value_str).bit_length() + 7) //8, byteorder='little')), True
        else:
            return bytes(value_str, STR_TO_BYTES_ENCODING)
    elif value_type == winreg.REG_DWORD:
        if value_str.isnumeric():
            return int(value_str), True
    elif value_type == winreg.REG_QWORD:
        if value_str.isnumeric():
            return int(value_str), True
    elif value_type in [winreg.REG_SZ, winreg.REG_EXPAND_SZ, winreg.REG_MULTI_SZ]:
        return value_str, True

    return None, False

def edit_registry(base_key_str, sub_key_str, name_str, value_str):
    try:
        base_key = get_base_key(base_key_str)
        if base_key is None:
            return 'Invalid base key'
        key = winreg.OpenKeyEx(base_key, sub_key_str)
        if not key:
            return 'Invalid sub key'

        old_value, value_type = winreg.QueryValueEx(key, name_str)
        value, convert_status = convert_value_type(value_str, value_type)
        if not convert_status:
            return 'Invalid value'
        
        winreg.SetValueEx(key, name_str, 0, value_type, value)
        winreg.CloseKey(key) 
        return 'Success'

    except Exception as e:
        print(e)
        return str(e)
    

    return 'Failed'
