import os
import warnings
import json

import pandas as pd

import redcap
from redcap_bridge.utils import map_header_csv_to_json


def upload_datadict(csv_file, server_config_json):
    """
   Parameters
   ----------
   csv_file: str
       Path to the csv file to be used as data dictionary
   server_config_json: str
       Path to the json file containing the redcap url and api token

    Returns:
    ----------

    Returns:
        (int): The number of uploaded fields
    """

    df = pd.read_csv(csv_file, dtype=str)
    df.rename(columns=map_header_csv_to_json, inplace=True)

    # Upload csv using pycap
    redproj = get_redcap_project(server_config_json)
    n = redproj.import_metadata(df, format='csv', return_format='json')
    return n


def download_datadict(save_to, server_config_json, format='csv'):
    """
    Parameters
    ----------
    save_to: str
        Path where to save the retrieved data dictionary
    server_config_json: str
        Path to the json file containing the redcap url and api token
    format:  'csv', 'json'
        Format of the retrieved data dictionary

            Format of the retrieved data dictionary

    """

    redproj = get_redcap_project(server_config_json)
    data_dict = redproj.export_metadata(format=format)

    if format == 'csv':
        with open(save_to, 'w') as save_file:
            save_file.writelines(data_dict)
    elif format == 'df':
        data_dict.to_csv(save_to)
    elif format == 'json':
        with open(save_to, 'w') as save_file:
            json.dump(data_dict, save_file)
    else:
        raise ValueError(f'Unknown format {format}. Valid formats are "csv" '
                         f'and "json".')


def download_records(save_to, server_config_json, format='csv'):
    """
    Download records from the redcap server.

    Parameters
    ----------
    save_to: str
        Path where to save the retrieved records csv
    server_config_json: str
        Path to the json file containing the redcap url and api token
    format: 'csv', 'json'
        Format of the retrieved records
    """

    redproj = get_redcap_project(server_config_json)
    records = redproj.export_records(format=format)

    if format == 'csv':
        with open(save_to, 'w') as save_file:
            save_file.writelines(records)
    elif format == 'df':
        records.to_csv(save_to)
    elif format == 'json':
        with open(save_to, 'w') as save_file:
            json.dump(records, save_file)
    else:
        raise ValueError(f'Unknown format {format}. Valid formats are "csv" '
                         f'and "json".')


def get_json_csv_header_mapping(server_config_json):
    """
    Retruns
    ----------
    dict: 
        Mapping of json to csv headers

    Returns:
        dict: Mapping of json to csv headers
    """

    # TODO: This function should replace utils.py/map_header_json_to_csv
    raise NotImplementedError()


def check_external_modules(server_config_json):
    """
    Download records from the redcap server.

    Parameters
    ----------
    server_config_json: str
        Path to the json file containing the redcap url, api token and required external modules

    Returns
    -------
        bool: True if required external modules are present

    """
    config = json.load(open(server_config_json, 'r'))

    if 'external_modules' not in config:
        warnings.warn('No external_modules defined in project configuration')
        return True

    redproj = get_redcap_project(server_config_json)
    proj_json = redproj.export_project_info(format='json')

    missing_modules = []

    for ext_mod in config['external_modules']:
        if ext_mod not in proj_json['external_modules']:
            missing_modules.append(ext_mod)

    if missing_modules:
        warnings.warn(f'Project on server is missing external modules: {missing_modules}')
        return False
    else:
        return True


def get_redcap_project(server_config_json):
    """
    Initialize a pycap project based on the provided server configuration
    :param server_config_json: json file containing the api_url and api_token
    :return: pycap project
    """
    config = json.load(open(server_config_json, 'r'))
    if config['api_token'] in os.environ:
        config['api_token'] = os.environ[config['api_token']]
    redproj = redcap.Project(config['api_url'], config['api_token'], lazy=False)
    return redproj


def check_external_modules(server_config_json):
    """
    Download records from the redcap server.

    Parameters
    ----------
    server_config_json: str
        Path to the json file containing the redcap url, api token and required external modules

    Returns
    -------
        bool: True if required external modules are present

    """
    config = json.load(open(server_config_json, 'r'))

    if 'external_modules' not in config:
        warnings.warn('No external_modules defined in project configuration')
        return True

    proj_json = get_redcap_project(server_config_json)

    missing_modules = []

    for ext_mod in config['external_modules']:
        if ext_mod not in proj_json['external_modules']:
            missing_modules.append(ext_mod)

    if missing_modules:
        warnings.warn(f'Project on server is missing external modules: {missing_modules}')
        return False
    else:
        return True


def get_redcap_project(server_config_json):
    """
    Initialize a pycap project based on the provided server configuration
    :param server_config_json: json file containing the api_url and api_token
    :return: pycap project
    """
    config = json.load(open(server_config_json, 'r'))
    if config['api_token'] in os.environ:
        config['api_token'] = os.environ[config['api_token']]
    redproj = redcap.Project(config['api_url'], config['api_token'], lazy=False)
    return redproj
>>>>>>> pep8 cleaning


if __name__ == '__main__':
    pass
