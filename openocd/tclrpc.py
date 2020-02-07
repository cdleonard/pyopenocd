# SPDX-License-Identifier: MIT

import re
import socket
from logging import getLogger
logger = getLogger(__name__)

class TclException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __repr__(self):
        return 'TclException(%d, %r)' % (self.code, self.msg)

_RE_SIMPLE_TCL_WORD = re.compile(r"^[a-zA-Z_0-9:+./@=,'-]+$")
def tcl_quote_word(word):
    """Quotes one word for TCL"""
    global _RE_SIMPLE_TCL_WORD
    if _RE_SIMPLE_TCL_WORD.match(word):
        return word
    else:
        return '{' + word + '}'

def tcl_quote_cmd(arg):
    """Quote a TCL command

    Argument must be a string (assumed to be already quoted) or list
    """
    if type(arg) is str:
        return arg
    elif type(arg) is list or type(arg) is tuple:
        return ' '.join([tcl_quote_word(word) for word in arg])
    else:
        raise TypeError("Expected str or list or tuple, got %s: %r" % (type(arg), arg))

class OpenOcdTclRpc:
    DEFAULT_PORT = 6666
    SEPARATOR_VALUE = 0x1a
    SEPARATOR_BYTES = b'\x1a'
    BUFFER_SIZE = 256

    __slots__ = (
        'host',
        'port',
        'sock',
    )

    def __init__(self, host='127.0.0.1', port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.sock = None

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        return self

    def __exit__(self, *args):
        self.sock.close()
        self.sock = None

    def sendrecv(self, cmd):
        """Send a command string and return reply"""
        logger.debug('send: %s', cmd)
        data = cmd.encode('utf-8') + self.SEPARATOR_BYTES
        self.sock.sendall(data)
        reply = self._recv().decode('utf-8')
        logger.debug('recv: %s', reply)
        return reply

    def _recv(self):
        """Read bytes until self.SEPARATOR"""
        data = bytes()
        while True:
            chunk = self.sock.recv(self.BUFFER_SIZE)
            data += chunk
            index = data.find(self.SEPARATOR_BYTES)
            if index >= 0:
                if index != len(data) - 1:
                    raise Exception('Unhandled extra bytes after %r'.format(self.SEPARATOR_BYTES))
                return data[:-1]

    def run(self, cmd):
        """Run a command and raise an error if it returns an error"""
        wrap = 'set _code [catch {%s} _msg];expr {"$_code $_msg"}' % tcl_quote_cmd(cmd)
        reply = self.sendrecv(wrap)
        code, msg = reply.split(' ', 1)
        code = int(code)

        if code:
            raise TclException(code, msg)
        else:
            return msg
