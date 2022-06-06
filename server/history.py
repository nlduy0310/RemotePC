# pip install browser-history
from datetime import datetime, timedelta
from browser_history.browsers import Chrome
from browser_history.browsers import Vivaldi
from browser_history.browsers import Edge
from browser_history.browsers import Firefox
from browser_history.browsers import Opera

DIR_OUTPUT = "data/"

class History:
    def __init__(self, name):
        self.browser_name = name
        if name == "Chrome":
            self.Browser = Chrome()
        elif name == "Vivaldi":
            self.Browser = Vivaldi()
        elif name == "Edge":
            self.Browser = Edge()
        elif name == "Firefox":
            self.Browser = Firefox()
        elif name == "Opera":
            self.Browser = Opera()
        self.his = self.Browser.fetch_history().histories
        self.his = sorted(self.his, key = lambda x: x[0], reverse = True)

    def __str__(self):
        return '\n'.join(map(lambda x: str(x[0]) + ' ' + str(x[1]), self.his))

    def get_history_by_date(self, date):
        date =  datetime.strptime(date, '%Y/%m/%d').date()
        res = self 
        res.his = [x for x in self.his if x[0].date() == date]
        return res

if __name__ == "__main__":
    t = History("Vivaldi").get_history_by_date("2022/05/28")
    print(str(t), type(t))
    
