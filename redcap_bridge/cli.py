"""
Provide CLI for the main functionalities of the redcap bridge
"""

from redcap_bridge.server_interface import download_records


def main(command_line=None):
    # importing required modules
    import argparse

    # create a parser object
    parser = argparse.ArgumentParser(description="A simple Python interface for RedCap")

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print debug info'
    )

    subparsers = parser.add_subparsers(dest='command')
    download = subparsers.add_parser('download', help='Downloads the data records')
    download.add_argument("destination", nargs=1, metavar='destination', type=str,
                          help="The destination filename.")
    download.add_argument("config_json", nargs=1, metavar='config_json', type=str,
                          help="The json configuration file of the project")
    download.add_argument("--format", type=str, nargs=1, metavar='format',
                          help="Format to store the data (json/csv)")

    # parse arguments
    args = parser.parse_args(command_line)

    if args.debug:
        print("debug: " + str(args))
    if args.command == 'download':
        download_records(args.destination[0], args.config_json[0])


if __name__ == '__main__':
    main()
