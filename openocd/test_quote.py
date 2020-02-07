from .tclrpc import tcl_quote_word
from .tclrpc import tcl_quote_cmd

def test_tcl_quote_simple_word():
    assert(tcl_quote_word('a') == 'a')

def test_tcl_quote_word():
    assert(tcl_quote_word('a"b') == '{a"b}')

def test_tcl_quote_word():
    assert(tcl_quote_word('a"b') == '{a"b}')

def test_tcl_quote_list():
    assert(tcl_quote_cmd(['a', 'b c']) == 'a {b c}')
