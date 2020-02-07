# Python OpenOCD wrapper

This is a simple module for interfacing with openocd via TCL api.

## Installation

pip install git+http://github.com/cdleonard/pyopenocd

## Usage

>>> from openocd import OpenOcdTclRpc
>>> with OpenOcdTclRpc() as openocd:
...     print(openocd).sendmsg('expr 1 + 2')
... 4

## Command line

The openocd module is executable:

    $ python3 -m openocd expr 1 + 2
    3

## Testing

pytest is used for testing. Most useful tests require openocd to be running but
they are skipped by default unless --openocd-running is passed on cmdline:

    pytest --test-openocd-tclrpc
