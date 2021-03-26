import redcap
import json
import pandas as pd

def upload_datadict(csv_file, server_config_json):
    """
    Upload data dictionary to the redcap server.

    Args:
        csv_file: (str)
            Path to the csv file to be used as data dictionary
        server_config_json: (str)
            Path to the json file containing the redcap url and api token

    Returns:
        (int): The number of uploaded fields
    """

    df = pd.read_csv(csv_file, dtype=str)

    # Upload csv using pycap
    config = json.load(open(server_config_json, 'r'))
    redproj = redcap.Project(config['api_url'], config['api_token'])
    n = redproj.import_metadata(df, format='csv', return_format='json')
    return n


def download_datadict(save_to, server_config_json, format='csv'):
    """
    Download data dictionary from the redcap server.

    Args:
        save_to: (str)
            Path where to save the retrieved data dictionary
        server_config_json: (str)
            Path to the json file containing the redcap url and api token
        format: 'csv', 'json'
            Format of the retrieved data dictionary

    """
    raise NotImplementedError()


def download_records(save_to, server_config_json, format='csv'):
    """
    Download records from the redcap server.

    Args:
        save_to: (str)
            Path where to save the retrieved records csv
        server_config_json: (str)
            Path to the json file containing the redcap url and api token
        format: 'csv', 'json'
            Format of the retrieved records
    """

    raise NotImplementedError()


def get_json_csv_header_mapping(server_config_json):
    """
    Extract the mapping of json headers (underscore-based) to csv headers (
    human readable)

    Returns:
        dict: Mapping of json to csv headers
    """

    # TODO: This function should replace utils.py/map_header_json_to_csv
    raise NotImplementedError()



if __name__ == '__main__':
    # TODO: Add CLI here
    pass