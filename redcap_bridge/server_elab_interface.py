import json
import os

import elabapi_python

from redcap_bridge.utils import conversion_csv_to_json



def download_experiment(server_config_json, id):

    api_client = get_elab_config(server_config_json)
    experiment_api = elabapi_python.ExperimentsApi(api_client)

    exp = experiment_api.get_experiment(id)

    return exp


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

        item_id = int(location_response.split('/').pop())

        if template['metadata']:
            template_api.patch_experiment_template(item_id, body={'metadata': template['metadata']})
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

    json_conversion_file = conversion_csv_to_json(csv_file)
    json_conversion_file = json.dumps(json_conversion_file)

    api_client = get_elab_config(server_config_json)
    template_api = elabapi_python.ExperimentsTemplatesApi(api_client)

    response = template_api.post_experiment_template_with_http_info(body={"title": title})
    location_response = response[2].get('Location')
    item_id = int(location_response.split('/').pop())

    template_api.patch_experiment_template(item_id, body={'metadata': json_conversion_file})

    return location_response


def get_elab_config(server_config_json):
    """
    Initialize a pycap project based on the provided server configuration
    :param server_config_json: json file containing the api_key and api_url
    :return: pycap project
    """

    config = json.load(open(server_config_json, 'r'))
    configuration = elabapi_python.Configuration()

    print(os.environ.keys())

    if config['api_elab_key'] in os.environ:
        print("Key is on environ")
        configuration.api_key['api_key'] = os.environ[config['api_elab_key']]
        if configuration.api_key['api_key']:
            print("Key is here")
        if os.environ[config['api_elab_key']]:
            print("Environ is here")
        configuration.api_key_prefix['api_key'] = 'Authorization'

    configuration.host = config['api_elab_url']
    configuration.debug = True
    configuration.verify_ssl = False

    api_client = elabapi_python.ApiClient(configuration)
    api_client.set_default_header(header_name='Authorization', header_value=os.environ[config['api_elab_key']])

    return api_client


if __name__ == '__main__':
    pass
