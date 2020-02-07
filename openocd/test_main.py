import pytest
from .__main__ import main

@pytest.mark.need_openocd_running
def test_main_run_llength(capsys):
    main(['run', 'string', 'length', '12 34'])
    assert(capsys.readouterr().out == '5\n')
