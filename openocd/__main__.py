import sys

def create_parser():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--host', help='Override hostname (default 127.0.0.1)')
    parser.add_argument('-p', '--port', type=int, help='Override port (default 6666)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('cmd', nargs='+', help='tcl command to execute');

    return parser

def main():
    opts = create_parser().parse_args()

    import logging
    logging.basicConfig(
            level=logging.DEBUG if opts.verbose else logging.INFO)

    from . import OpenOcdTclRpc
    rpc = OpenOcdTclRpc()
    if opts.host:
        rpc.tclRpcIp = opts.host
    if opts.port:
        rpc.tclRpcPort = opts.port

    with rpc:
        sys.stdout.write(rpc.sendrecv(' '.join(opts.cmd)) + '\n')

if __name__ == '__main__':
    main()
