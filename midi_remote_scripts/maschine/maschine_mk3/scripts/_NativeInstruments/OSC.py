# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.2 (default, Apr 30 2021, 11:26:30) 
# [GCC Apple LLVM 12.0.0 (clang-1200.0.31.1)]
# Embedded file name: /Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/_NativeInstruments/OSC.py
# Compiled at: 2021-05-26 12:23:47
# Size of source mod 2**32: 7873 bytes
import struct, math, time
from .Logger import log

class OSCMessage:
    __doc__ = 'Builds typetagged OSC messages.'

    def __init__(self, address='', msg=()):
        self.address = address
        self.typetags = ','
        self.message = ''
        if type(msg) in (str, int, float):
            self.append(msg)
        else:
            if type(msg) in (list, tuple):
                for m in msg:
                    if type(m) not in (str, int, float):
                        log("don't know how to encode message element: {} | {}".format(m, type(m)))
                    self.append(m)

    def append(self, argument, typehint=None):
        """Appends data to the message,
        updating the typetags based on
        the argument's type.
        If the argument is a blob (counted string)
        pass in 'b' as typehint."""
        if typehint == 'b':
            binary = osc_blob(argument)
        else:
            binary = osc_argument(argument)
        self.typetags = self.typetags + binary[0]
        self.message = self.message + bytes(binary[1])

    def get_binary(self):
        """Returns the binary message (so far) with typetags."""
        address = osc_argument(self.address)[1]
        typetags = osc_argument(self.typetags)[1]
        return address + typetags + self.message

    def __repr__(self):
        return self.get_binary()


JAN_1970 = 2208988800
SECS_TO_PICOS = 4294967296

def abs_to_timestamp(abs):
    """ since 1970 => since 1900 64b OSC """
    sec_1970 = int(abs)
    sec_1900 = sec_1970 + JAN_1970
    sec_frac = float(abs - sec_1970)
    picos = int(sec_frac * SECS_TO_PICOS)
    return struct.pack('!LL', sec_1900, picos)


class OSCBundle:
    __doc__ = 'Builds OSC bundles'

    def __init__(self, when=None):
        self.items = []
        if when is None:
            when = time.time()
        self.when = when

    def append(self, address: OSCMessage, msg=None):
        if address is not None:
            if isinstance(address, str):
                self.items.append(OSCMessage(address, msg))
            else:
                if isinstance(address, OSCMessage):
                    self.items.append(address)
                else:
                    raise Exception('invalid type of first argument to OSCBundle.append(), need address string or OSCMessage, not ', str(type(address)))

    def get_binary(self):
        retval = osc_argument('#bundle')[1] + abs_to_timestamp(self.when)
        for item in self.items:
            binary = item.get_binary()
            retval = retval + osc_argument(len(binary))[1] + binary

        return retval


def read_string(data):
    length = str.find(data.decode('ISO-8859-1'), '\x00')
    next_data = int(math.ceil((length + 1) / 4.0) * 4)
    return (data[0:length].decode('ISO-8859-1'), data[next_data:])


def read_blob(data):
    length = struct.unpack('>i', data[0:4])[0]
    next_data = int(math.ceil(length / 4.0) * 4) + 4
    return (data[4:length + 4], data[next_data:])


def read_int(data):
    if len(data) < 4:
        log('Error: too few bytes for int', data, len(data))
        rest = data
        integer = 0
    else:
        integer = struct.unpack('>i', data[0:4])[0]
        rest = data[4:]
    return (integer, rest)


def read_long(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit signed integer."""
    high, low = struct.unpack('>ll', data[0:8])
    big = (int(high) << 32) + low
    rest = data[8:]
    return (big, rest)


def read_float(data):
    if len(data) < 4:
        log('Error: too few bytes for float', data, len(data))
        rest = data
        float = 0
    else:
        float = struct.unpack('>f', data[0:4])[0]
        rest = data[4:]
    return (float, rest)


def osc_blob(next):
    """Convert a string into an OSC Blob,
    returning a (typetag, data) tuple."""
    if isinstance(next, str):
        length = len(next)
        padded = math.ceil(len(next) / 4.0) * 4
        binary = struct.pack('>i%ds' % int(padded), length, next.encode('ISO-8859-1'))
        tag = 'b'
    else:
        tag = ''
        binary = ''
    return (tag, binary)


def osc_argument(data):
    """Convert some Python types to their
    OSC binary representations, returning a
    (typetag, data) tuple."""
    if isinstance(data, str):
        OSCstringLength = math.ceil((len(data) + 1) / 4.0) * 4
        binary = struct.pack('>%ds' % OSCstringLength, data.encode('ISO-8859-1'))
        tag = 's'
    else:
        if isinstance(data, float):
            binary = struct.pack('>f', data)
            tag = 'f'
        else:
            if isinstance(data, int):
                binary = struct.pack('>i', data)
                tag = 'i'
            else:
                raise Exception("don't know how to encode " + str(data) + ' as OSC argument, type=' + str(type(data)))
    return (
     tag, binary)


def parse_args(args):
    """Given a list of strings, produces a list
    where those strings have been parsed (where
    possible) as floats or integers."""
    parsed = []
    for arg in args:
        print(arg)
        arg = arg.strip()
        try:
            interpretation = float(arg)
            if str.find(str(arg), '.') == -1:
                interpretation = int(interpretation)
        except IOError:
            interpretation = arg

        parsed.append(interpretation)

    return parsed


def decode_osc(data):
    """Converts a typetagged OSC message to a Python list."""
    table = {'i':read_int, 
     'f':read_float,  's':read_string,  'b':read_blob}
    decoded = []
    address, rest = read_string(data)
    if address == '#bundle':
        time, rest = read_long(rest)
        decoded.append(address)
        decoded.append(time)
        while len(rest) > 0:
            length, rest = read_int(rest)
            decoded.append(decode_osc(rest[:length]))
            rest = rest[length:]

    else:
        if len(rest) > 0:
            typetags, rest = read_string(rest)
            decoded.append(address)
            decoded.append(typetags)
            if typetags[0] == ',':
                for tag in typetags[1:]:
                    value, rest = table[tag](rest)
                    decoded.append(value)

            else:
                print('Oops, typetag lacks the magic ,')
        else:
            decoded.append(address)
            decoded.append(',')
    return decoded


class CallbackManager:
    __doc__ = 'This utility class maps OSC addresses to callables.\n\n    The CallbackManager calls its callbacks with a list\n    of decoded OSC arguments, including the address and\n    the typetags as the first two arguments.'

    def __init__(self):
        self.callbacks = {}
        self.add('#bundle', self.unbundler)

    def handle(self, data, source):
        """Given OSC data, tries to call the callback with the right address."""
        decoded = decode_osc(data)
        self.dispatch(decoded, source)

    def dispatch(self, message, source):
        """Sends decoded OSC data to an appropriate calback"""
        address = message[0]
        self.callbacks[address](message, source)

    def add(self, address, callback):
        """Adds a callback to our set of callbacks,
        or removes the callback with name if callback
        is None."""
        if callback is None:
            del self.callbacks[address]
        else:
            self.callbacks[address] = callback

    def unbundler(self, messages, source):
        """Dispatch the messages in a decoded bundle."""
        for message in messages[2:]:
            self.dispatch(message, source)
# okay decompiling src/_NativeInstruments/OSC.pyc
