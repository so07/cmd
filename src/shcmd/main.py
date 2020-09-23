import argparse
from . import shcmd

__version__ = "0.7.4"


def main():

    parser = argparse.ArgumentParser(
        prog="shcmd",
        description="""Command shell execution with shcmd module.""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help="print version information",
    )

    parser.add_argument(
        "-c",
        "--command",
        dest="command",
        required=True,
        help="command to run. (default %(default)s)",
    )

    parser.add_argument(
        "-o",
        "--stdout",
        dest="stdout",
        help="redirect command stdout. (default %(default)s)",
    )

    parser.add_argument(
        "-e",
        "--stderr",
        dest="stderr",
        help="redirect command stderr. (default %(default)s)",
    )

    parser.add_argument(
        "-i",
        "--stdinp",
        dest="stdinp",
        help="command stdinp. NOT YET SUPPORTED (default %(default)s)",
    )

    parser.add_argument(
        "-m",
        "--message",
        dest="message",
        help="print a message before execution of command. (default %(default)s)",
    )

    parser.add_argument(
        "-a",
        "--append",
        dest="append",
        action="store_true",
        help="append stdout. (default %(default)s)",
    )

    parser.add_argument(
        "-s",
        "--silent",
        dest="silent",
        action="store_true",
        help="execute command in silent mode. (default %(default)s)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="enable verbose mode. (default %(default)s)",
    )

    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="enable debug mode. (default %(default)s)",
    )

    args = parser.parse_args()

    c = shcmd.shcmd(
        args.command,
        stdout=args.stdout,
        stderr=args.stderr,
        stdin=args.stdinp,
        msg=args.message,
        append=args.append,
        verbose=args.verbose,
        silent=args.silent,
        debug=args.debug,
    )

    c()


if __name__ == "__main__":
    main()
