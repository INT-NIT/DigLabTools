import json
import os

import elabapi_python

from redcap_bridge.utils import conversion_csv_to_json


def download_experiment(server_config_json, id):
    api_client = get_elab_config(server_config_json)
    experiment_api = elabapi_python.ExperimentsApi(api_client)

    exp = experiment_api.get_experiment(id)

    return exp


def create_template(server_config_json, template_file, metadata):
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

    try:
        with open(template_file, 'r') as f:
            json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f'Invalid JSON file: {template_file}')

    api_client = get_elab_config(server_config_json)
    template_api = elabapi_python.ExperimentsTemplatesApi(api_client)

    template = json.load(open(template_file, 'r'))
    if metadata:
        response = template_api.post_experiment_template_with_http_info(body={"title": template['title']})
        location_response = response[2].get('Location')
        item_id = int(location_response.split('/').pop())

        if template['metadata']:
            response = template_api.patch_experiment_template_with_http_info(
                item_id, body={'metadata': template['metadata']})
            status_code = response[1]

        else:
            raise ValueError(f'No metadata No metadata in the template')
    else:
        response = template_api.post_experiment_template_with_http_info(body={"title": template['title']})
        status_code = response[1]
        location_response = response[2].get('Location')

    return location_response, status_code


def create_template_with_converted_csv(server_config_json, csv_file, title):
    """
    Creating a template with an old csv file.

    Parameters
    ----------
    server_config_json: str
        Path to the json file containing the redcap url, api token and required external modules
    template_file: str
        Path to the csv file you want to convert into an Elab version
    title: str
        Title of the template created

    Returns
    -------
        location_response: location of the new template

    """

    conversion_json = conversion_csv_to_json(csv_file)
    final_json = json.dumps(conversion_json)

    api_client = get_elab_config(server_config_json)
    template_api = elabapi_python.ExperimentsTemplatesApi(api_client)

    response = template_api.post_experiment_template_with_http_info(body={"title": title})
    location_response = response[2].get('Location')
    item_id = int(location_response.split('/').pop())

    template_api.patch_experiment_template_with_http_info(item_id, body={'metadata': final_json})
    status_code = response[1]

    return location_response, status_code


def get_elab_config(server_config_json):
    """
    Initialize a pycap project based on the provided server configuration
    :param server_config_json: json file containing the api_key and api_url
    :return: pycap project
    """

    config = json.load(open(server_config_json, 'r'))
    configuration = elabapi_python.Configuration()

    if config['api_elab_key'] in os.environ:
        configuration.api_key['api_key'] = os.environ[config['api_elab_key']]
        configuration.api_key_prefix['api_key'] = 'Authorization'

    configuration.host = config['api_elab_url']
    configuration.debug = True
    configuration.verify_ssl = False

    api_client = elabapi_python.ApiClient(configuration)
    api_client.set_default_header(header_name='Authorization', header_value=os.environ[config['api_elab_key']])

    return api_client


if __name__ == '__main__':
    pass
