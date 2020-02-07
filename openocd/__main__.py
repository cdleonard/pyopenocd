import sys

def create_parser():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--host', help='Override hostname (default 127.0.0.1)')
    parser.add_argument('-p', '--port', type=int, help='Override port (default 6666)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    subparsers = parser.add_subparsers(dest='subcmd')

    subparser = subparsers.add_parser('run', help='Run a command remotely')
    subparser.add_argument('cmd', nargs='+', help='tcl command to execute')

    subparser = subparsers.add_parser('raw', help='Send a raw command (no quoting) and show reply')
    subparser.add_argument('msg', help='tclrpc message to send')

    return parser

def main(argv=None):
    opts = create_parser().parse_args(argv)

    import logging
    logging.basicConfig(
            level=logging.DEBUG if opts.verbose else logging.INFO)

    from . import OpenOcdTclRpc
    openocd = OpenOcdTclRpc()
    if opts.host:
        openocd.host = opts.host
    if opts.port:
        openocd.port = opts.port

    if opts.subcmd == 'run':
        from .tclrpc import TclException
        with openocd:
            try:
                sys.stdout.write(str(openocd.run(opts.cmd) + '\n'))
            except TclException as ex:
                sys.stdout.write(ex.msg + '\n')
                sys.exit(ex.code)
    elif opts.subcmd == 'raw':
        with openocd:
            sys.stdout.write(openocd.sendrecv(opts.msg) + '\n')
    else:
        raise Exception("Unknown subcmd {}".format(opts.subcmd))

if __name__ == '__main__':
    main()
