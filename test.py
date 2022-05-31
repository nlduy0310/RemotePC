from importlib.resources import path
from pandas import value_counts


cmd = 'regedit 12345 HKEY_CURRENT_USER|Soft ware\\Sample Key<>bin value<>1 2'

# Needs to return id, basekey, subkey, name, value

def foo(k):
    if k == 1:
        return "case", "1", "valid path"
    elif k == 2:
        return "case", "1", None
    
    return "", "", None


def parse_regedit_cmd(cmd: str):
    paths = cmd[cmd.find('|') + 1:]
    if len(paths.split('<>')) != 3:
        print('1')
        return None, None, None, None, None
    subkey, name, value = paths.split('<>')

    cmd_id_base = cmd[:cmd.find('|')]
    if len(cmd_id_base.split(' ')) != 3:
        print('2')
        return None, None, None, None, None
    cmd, id, basekey = cmd_id_base.split(' ')

    return id, basekey, subkey, name, value


if __name__ == '__main__':
    a, b, c = foo(1)
    if a and b:
        print('mail found')
    else:
        print('mail not found')
    if c:
        print('File found')
    else:
        print('File not found')
        
    a, b, c = foo(2)
    if a and b:
        print('mail found')
    else:
        print('mail not found')
    if c:
        print('File found')
    else:
        print('File not found')

    a, b, c = foo(3)
    if a and b:
        print('mail found')
    else:
        print('mail not found')
    if c:
        print('File found')
    else:
        print('File not found')
