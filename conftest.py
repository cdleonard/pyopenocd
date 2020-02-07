import pytest

def pytest_addoption(parser):
    parser.addoption("--openocd-running", action='store_true',
        help="Assume openocd is running")

def pytest_collection_modifyitems(config, items):
    if not config.getoption('--openocd-running'):
        skip_marker = pytest.mark.skip(reason="needs --openocd-running")
        for item in items:
            if ("tclrpc" in item.fixturenames or
                    list(item.iter_markers(name='need_openocd_running'))):
                item.add_marker(skip_marker)
