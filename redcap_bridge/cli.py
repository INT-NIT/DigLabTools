"""
Provide CLI for the main functionalities of the redcap bridge
"""

from redcap_bridge.server_interface import download_records
from redcap_bridge.server_elab_interface import download_experiment


def main(command_line=None):
    # importing required modules
    import argparse

    # create a parser object
    parser = argparse.ArgumentParser(description="A simple Python interface for RedCap and ElabFTW")

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print debug info'
    )

    parser.add_argument('--redcap', action='store_true', help='Use RedCap')
    parser.add_argument('--elabftw', action='store_true', help='Use ElabFTW')

    subparsers = parser.add_subparsers(dest='command')

    download = subparsers.add_parser('download', help='Downloads the data records')
    download.add_argument("destination", nargs=1, metavar='destination', type=str,
                          help="The destination filename.")
    download.add_argument("config_json", nargs=1, metavar='config_json', type=str,
                          help="The json configuration file of the project")
    download.add_argument("-f", "--format", type=str, nargs=1, metavar='format',
                          help="Format to store the data (json/csv)")
    download.add_argument("-c", "--compressed", action='store_true',
                          help="Compress the output file (use labels and merge checkbox columns)")

    # Options for downloading Elab. To be modified afterwards
    elabftw = subparsers.add_parser('elabftw', help='Downloads the data records from ElabFTW')
    elabftw.add_argument("config_json", nargs=1, metavar='config_json', type=str,
                         help="The json configuration file of the project")
    elabftw.add_argument("experiment_id", nargs=1, metavar='config_json', type=str,
                         help="The experiment id")

    args = parser.parse_args(command_line)

    if args.debug:
        print("debug: " + str(args))

    # We need to have 1 option
    if not args.redcap and not args.elabftw:
        parser.error("Please specify either --redcap or --elabftw")

    # Only elab or redcap as options choosing both is not possible
    if args.redcap and args.elabftw:
        parser.error("Please specify only one of --redcap or --elabftw")

    if args.command == 'download':
        if not args.format:
            args.format = ['csv']

        if args.redcap:
            download_records(args.destination[0], args.config_json[0], format=args.format[0],
                             compressed=bool(args.compressed))
        elif args.elabftw:
            download_experiment(args.config_json[0], args.experiment_id[0])


if __name__ == '__main__':
    main()