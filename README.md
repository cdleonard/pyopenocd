# Python OpenOCD wrapper

This is a simple module for interfacing with openocd via TCL api.

## Installation

    pip install git+https://github.com/cdleonard/pyopenocd

## Usage

    >>> from openocd import OpenOcdTclRpc
    >>> with OpenOcdTclRpc() as openocd:
    ...     print(openocd.sendrecv('expr 1 + 1'))
    ...
    2

## Command line

The openocd module is executable and can serve as a very simple openocd remote:

    $ python3 -m openocd expr 1 + 2
    3

## Testing

pytest is used for testing. Most useful tests require openocd to be running but
they are skipped by default unless --openocd-running is passed on cmdline:

    pytest --test-openocd-tclrpc
