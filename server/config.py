whitelist_path = 'data/whitelist.txt'

def get_lines(file_path):
    res = []

    with open(file_path, 'r') as f:
        res = f.read().splitlines()

    return res


class Config:
    def __init__(self):
        self.whitelist = get_lines(whitelist_path)
        # ...

    def is_authorized(self, email: str):
        return email in self.whitelist
