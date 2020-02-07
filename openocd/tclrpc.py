# SPDX-License-Identifier: MIT

import socket
from logging import getLogger
logger = getLogger(__name__)

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
            index = chunk.find(self.SEPARATOR_BYTES)
            if index >= 0:
                return data[:index + 1]
