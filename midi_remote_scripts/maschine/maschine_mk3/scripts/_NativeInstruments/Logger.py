# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/_NativeInstruments/Logger.py
# Compiled at: 2021-05-26 09:18:13
# Size of source mod 2**32: 1922 bytes
import sys, socket

class Logger:
    __doc__ = '\n    Simple logger.\n    Tries to use a socket which connects to localhost port 4444 by default.\n    If that fails then it logs to a file\n    '

    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except ConnectionError:
            print("Couldn't create socket")
            self.socket = None

        self.connected = 0
        if self.socket:
            try:
                self.socket.connect(('localhost', 4444))
                self.connected = 1
                self.stderr = sys.stderr
                sys.stderr = self
            except socket.error as e:
                try:
                    print("Couldn't connect socket: {}".format(e))
                finally:
                    e = None
                    del e

        self.buf = ''

    def log(self, msg):
        if self.connected:
            self.send(msg + '\n')
        else:
            print(msg)

    def send(self, msg):
        if self.connected:
            self.socket.send(msg.encode('ISO-8859-1'))

    def close(self):
        if self.connected:
            self.socket.send('Closing..')
            self.socket.close()

    def write(self, msg):
        self.stderr.write(msg)
        self.buf = self.buf + msg
        lines = self.buf.split('\n', 2)
        if len(lines) == 2:
            self.send('STDERR: ' + lines[0] + '\n')
            self.buf = lines[1]


logger = Logger()

def log(*args):
    text = ''
    for arg in args:
        if text != '':
            text = text + ' '
        text = text + str(arg)

    if logger is not None:
        logger.log(text)
# okay decompiling src/_NativeInstruments/Logger.pyc
