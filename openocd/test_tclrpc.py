import pytest
from . import OpenOcdTclRpc
from . import TclException

def test_tclrpc_expr1(tclrpc):
    assert(tclrpc.sendrecv('expr 1 + 1') == '2')

def test_tclrpc_expr2(tclrpc):
    assert(tclrpc.sendrecv('expr 1234') == '1234')

def test_run_string_length(tclrpc):
    assert(tclrpc.run(['string', 'length', '123']) == '3')

def test_run_string_length_whitespace(tclrpc):
    assert(tclrpc.run(['string', 'length', '1 2 3']) == '5')

def test_run_string_length_whitespace(tclrpc):
    with pytest.raises(TclException):
        tclrpc.run(['command which does not exist'])

def test_run_command(tclrpc):
    assert(tclrpc.run('string length {1 2 3}') == '5')

@pytest.fixture(scope='function')
def tclrpc():
    with OpenOcdTclRpc() as item:
        yield item
