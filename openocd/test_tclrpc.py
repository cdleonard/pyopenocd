import pytest
from . import OpenOcdTclRpc

def test_tclrpc_expr(tclrpc):
    assert(tclrpc.sendrecv('expr 1 + 1') == '2')

@pytest.fixture(scope='function')
def tclrpc():
    with OpenOcdTclRpc() as item:
        yield item
