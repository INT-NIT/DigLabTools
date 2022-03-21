import os
import warnings
import json

import pandas as pd

import redcap
from redcap_bridge.utils import map_header_csv_to_json, compress_record


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
    n = redproj.import_metadata(df, import_format='df', return_format_type='json')
    return n


def download_datadict(save_to, server_config_json, format='csv'):
    """
    Parameters
    ----------
    save_to: str
        Path where to save the retrieved data dictionary
    server_config_json: str
        Path to the json file containing the redcap url and api token
    format:  'csv', 'json', 'df'
        Format of the retrieved data dictionary
    """

    redproj = get_redcap_project(server_config_json)
    data_dict = redproj.export_metadata(format_type=format)

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


def download_records(save_to, server_config_json, format='csv', compressed=False, **kwargs):
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
    kwargs: dict
        Additional arguments passed to PyCap `export_records`

    """

    if compressed:
        fixed_params = {'raw_or_label': 'label',
                        'raw_or_label_headers': 'label',
                        'export_checkbox_labels': True}
        for fix_key, fix_value in fixed_params.items():
            if fix_key in kwargs and kwargs[fix_key] != fix_value:
                warnings.warn(f'`compressed` is overwriting current {fix_key} setting.')

        kwargs.update(fixed_params)

    redproj = get_redcap_project(server_config_json)
    records = redproj.export_records(format_type=format, **kwargs)

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

    if compressed:
        if format != 'csv':
            warnings.warn('Can only compress csv output. Ignoring `compressed` parameter.')
        else:
            # run compression in place
            compress_record(save_to, save_to)


def upload_records(csv_file, server_config_json):
    """
   Parameters
   ----------
   csv_file: str
       Path to the csv file to be used as records
   server_config_json: str
       Path to the json file containing the redcap url and api token

    Returns:
    ----------

    Returns:
        (int): Number of uploaded records
    """

    df = pd.read_csv(csv_file, dtype=str)
    df.rename(columns=map_header_csv_to_json, inplace=True)

    # Upload csv using pycap
    redproj = get_redcap_project(server_config_json)

    # activate repeating instrument feature if present in records
    if 'redcap_repeat_instrument' in df.columns:
        form_name = df['redcap_repeat_instrument'].values[0]
        redproj.import_repeating_instruments_events([{"form_name": form_name,
                                                      "custom_form_label": ""}])

    n = redproj.import_records(df, import_format='df', return_format_type='json')
    return n['count']


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
    proj_json = redproj.export_project_info(format_type='json')

    missing_modules = []

    for ext_mod in config['external_modules']:
        if ext_mod not in proj_json['external_modules']:
            missing_modules.append(ext_mod)

    if missing_modules:
        warnings.warn(f'Project on server is missing external modules: {missing_modules}')
        return False
    else:
        return True


def download_project_settings(server_config_json, format='json'):
    """
    Get project specific settings from server

    Parameters
    ----------
    server_config_json: str
        Path to the json file containing the redcap url, api token and required external modules
    format: str
        Return format to use (json, csv, xml, df)

    Returns
    -------
        (dict|list|xml|df): The project settings in the corresponding format
    """

    redproj = get_redcap_project(server_config_json)
    proj_settings = redproj.export_project_info(format_type=format)

    return proj_settings


def configure_project_settings(server_config_json):
    """
    Setting project specific settings on server

    Parameters
    ----------
    server_config_json: str
        Path to the json file containing the redcap url, api token and required external modules

    Returns
    -------
        bool: True if required external modules are present
    """

    redproj = get_redcap_project(server_config_json)
    proj_json = redproj.export_project_info(format_type='json')

    config = json.load(open(server_config_json, 'r'))

    # configure default settings (surveys) and configured settings
    # setting project info requires a SUPER API token - not for standard usage
    if not proj_json['surveys_enabled']:
        warnings.warn(f'Surveys are not enabled for project {proj_json["project_title"]} '
                      f'(project_id {proj_json["project_id"]}). Visit the RedCap webinterface and '
                      f'enable surveys to be able to collect data via the survey URL')


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

    proj_json = json.load(open(server_config_json, 'r'))

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
    redproj = redcap.Project(config['api_url'], config['api_token'])
    return redproj


if __name__ == '__main__':
    pass
