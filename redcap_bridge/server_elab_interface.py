import os
import warnings
import json

import pandas as pd
import elabapi_python
from elabapi_python.rest import ApiException


def create_template_with_metadata(server_config_json, template_file):
    """
    Create a template with metadata.

    Parameters
    ----------
    server_config_json: str
        Path to the json file containing the redcap url, api token and required external modules
    template_file: str
        Path to the template you want to create

    Returns
    -------
        location_response: location of the new template

    """

    api_client = get_elab_config(server_config_json)
    template_api = elabapi_python.ExperimentsTemplatesApi(api_client)

    if json.load(open(template_file, 'r')):
        template = json.load(open(template_file, 'r'))
        response = template_api.post_experiment_template_with_http_info(body={"title": template['title']})
        location_response = response[2].get('Location')

        itemId = int(location_response.split('/').pop())

        if template['metadata']:
            template_api.patch_experiment_template(itemId, body={'metadata': template['metadata']})
        else:
            raise ValueError(f'No metadata No metadata in the template')
    else:
        raise ValueError(f'Unknown format or template. Valid format is "json".')

    return location_response


def create_template_without_metadata(server_config_json, template_file):
    """
    Create a simple template with a title without metadata.

    Parameters
    ----------
    server_config_json: str
        Path to the json file containing the redcap url, api token and required external modules
    template_file: str
        Path to the template you want to create

    Returns
    -------
        location_response: location of the new template

    """

    api_client = get_elab_config(server_config_json)
    template_api = elabapi_python.ExperimentsTemplatesApi(api_client)

    if json.load(open(template_file, 'r')):
        template = json.load(open(template_file, 'r'))
        response = template_api.post_experiment_template_with_http_info(body={"title": template['title']})
        location_response = response[2].get('Location')
    else:
        raise ValueError(f'Unknown format or template. Valid format is "json".')

    return location_response


def get_elab_config(server_config_json):
    """
    Initialize a pycap project based on the provided server configuration
    :param server_config_json: json file containing the api_key and api_url
    :return: pycap project
    """

    config = json.load(open(server_config_json, 'r'))
    configuration = elabapi_python.Configuration()

    if config['api_key'] in os.environ:
        configuration.api_key['api_key'] = os.environ[config['api_key']]
        configuration.api_key_prefix['api_key'] = 'Authorization'

    configuration.api_key['api_key'] = config['api_key']
    configuration.api_key_prefix['api_key'] = 'Authorization'

    if config['api_url'] in os.environ:
        configuration.host = os.environ[config['api_url']]

    configuration.host = config['api_url']

    configuration.debug = True
    configuration.verify_ssl = False

    api_client = elabapi_python.ApiClient(configuration)
    api_client.set_default_header(header_name='Authorization', header_value=config['api_key'])
    return api_client


if __name__ == '__main__':
    pass