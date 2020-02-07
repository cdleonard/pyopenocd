import pytest
from . import OpenOcdTclRpc

def test_tclrpc_expr1(tclrpc):
    assert(tclrpc.sendrecv('expr 1 + 1') == '2')

def test_tclrpc_expr2(tclrpc):
    assert(tclrpc.sendrecv('expr 1234') == '1234')

@pytest.fixture(scope='function')
def tclrpc():
    with OpenOcdTclRpc() as item:
        yield item
