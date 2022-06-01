import os


def remove_files(folder, ends_with=None, excepts=['whitelist.txt']):
    for filename in os.listdir(folder):
        if filename in excepts:
            continue
        if ends_with is None:
            os.remove(os.path.join(folder, filename))
        else:
            if filename.endswith(ends_with):
                os.remove(os.path.join(folder, filename))
