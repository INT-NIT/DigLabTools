"""
Provide CLI for the main functionalities of the redcap bridge
"""

from redcap_bridge.server_interface import download_records
from redcap_bridge.server_elab_interface import download_experiment


def main(command_line=None):
    # importing required modules
    import argparse

    # create a parser object
    parser = argparse.ArgumentParser(description="A simple Python interface for RedCap and elabftw")

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Print debug info'
    )

    parser.add_argument(
        'command',
        choices=['redcap', 'elabftw'],
        help='Choose the server to download from (redcap or elabftw)'
    )

    parser.add_argument("destination", metavar='destination', type=str,
                        help="The destination filename.")
    parser.add_argument("config_json", metavar='config_json', type=str,
                        help="The json configuration file of the project")
    parser.add_argument("-f", "--format", type=str, metavar='format',
                        help="Format to store the data (json/csv)")
    parser.add_argument("-c", "--compressed", action='store_true',
                        help="Compress the output file (use labels and merge checkbox columns)")
    parser.add_argument("experiment_id", metavar='experiment', type=str,
                        help="Experiment id")

    # parse arguments
    args = parser.parse_args(command_line)

    if args.debug:
        print("debug: " + str(args))

    if args.command == 'redcap':
        if not args.format:
            args.format = 'csv'

        download_records(args.destination, args.config_json, format=args.format,
                         compressed=bool(args.compressed))
    elif args.command == 'elabftw':
        if not args.format:
            args.format = 'csv'

        download_experiment(args.config_json, args.experiment_id)


if __name__ == '__main__':
    main()