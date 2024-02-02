"""
Provide CLI for the main functionalities of the elab bridge
"""

from elab_bridge.server_interface import download_experiment, extended_download


def main(command_line=None):
    # importing required modules
    import argparse

    # create a parser object
    parser = argparse.ArgumentParser(description="A simple Python interface for ElabFTW")

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print debug info'
    )

    subparsers = parser.add_subparsers(dest='command')
    download = subparsers.add_parser('download', help='Download an experiment')
    download.add_argument("destination", nargs=1, metavar='destination', type=str,
                          help="The destination filename.")
    download.add_argument("config_json", nargs=1, metavar='config_json', type=str,
                          help="The json configuration file of the project")
    download.add_argument("-f", "--format", type=str, nargs=1, metavar='format',
                          help="Format to store the data (json/csv)")
    download.add_argument("-c", "--compressed", action='store_true',
                          help="Compress the output file (use labels and merge checkbox columns)")

    extended_download_parser = subparsers.add_parser('extended_download',
                                                     help='Download experiments'
                                                          ' with extended options')
    extended_download_parser.add_argument("destination", nargs=1, metavar='destination', type=str,
                                          help="The destination directory"
                                               " to save the downloaded experiments.")
    extended_download_parser.add_argument("config_json", nargs=1, metavar='config_json', type=str,
                                          help="The json configuration file of the project")
    extended_download_parser.add_argument("tags", nargs='+', metavar='tags', type=str,
                                          help="List of tags of the experiments to download")
    extended_download_parser.add_argument("-f", "--format", type=str, nargs=1, metavar='format',
                                          help="Format to store the data (json/csv)")

    # parse arguments
    args = parser.parse_args(command_line)

    if args.debug:
        print("debug: " + str(args))
    if args.command == 'download':
        if args.format:
            raise NotImplementedError()
        if args.compressed:
            raise NotImplementedError()
        if not args.format:
            args.format = ['csv']

        download_experiment(args.destination[0], args.config_json[0], format=args.format[0],
                            compressed=bool(args.compressed))

    elif args.command == 'extended_download':
        extended_download(args.destination[0], args.config_json[0], args.tags)


if __name__ == '__main__':
    main()
