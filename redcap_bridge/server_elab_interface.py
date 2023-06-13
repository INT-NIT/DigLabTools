import json
import os
import elabapi_python
import pandas as pd

from redcap_bridge.utils import conversion_csv_to_json

import json


def download_experiment(save_to, server_config_json, experiment_id, experiment_axis='columns', format='csv'):
    """
    Download an individual experiment.

    Parameters
    ----------
    save_to: str
        Path where to save the retrieved experiment data
    server_config_json: str
        Path to the json file containing the redcap url, api token and required external modules
    format: 'csv', 'json'
        Format of the retrieved records
    experiment_id: int
        ID of the experiment you want to download
    experiment_axis: str
        Option to control whether experiments are arranged in columns or rows

    Returns
    -------
        status_code: Return code of the API request
        df: Dataframe of the experiment
    """

    api_client = get_elab_config(server_config_json)
    experiment_api = elabapi_python.ExperimentsApi(api_client)

    exp = experiment_api.get_experiment_with_http_info(experiment_id)
    status_code = exp[1]

    metadata = json.loads(exp[0].metadata)

    extra_fields_data = metadata.get("extra_fields", {})
    unwanted_columns = ["position", "options", "allow_multi_values", "blank_value_on_duplicate"]

    if experiment_axis == "columns":
        df = pd.DataFrame.from_dict(extra_fields_data, orient='columns')
        df = df.drop(unwanted_columns, axis=0)  # Delete unwanted columns
        if format == "csv":
            df.to_csv(save_to, index=False)
        elif format == "json":
            df.to_json(save_to, orient='records')
        else:
            raise ValueError("Invalid format value. Must be 'csv' or 'json'.")
    elif experiment_axis == "rows":
        df = pd.DataFrame.from_dict(extra_fields_data, orient='index')
        df = df.drop(unwanted_columns, axis=1)
        if format == "csv":
            df.to_csv(save_to, index=True)
        elif format == "json":
            df.to_json(save_to, orient='index')
        else:
            raise ValueError("Invalid format value. Must be 'csv' or 'json'.")
    else:
        raise ValueError("Invalid experiment_axis value. Must be 'columns' or 'rows'.")

    return status_code, df


def upload_template(server_config_json, template_file):
    """
    Upload a template with metadata.

    Parameters
    ----------
    server_config_json: str
        Path to the json file containing the redcap url, api token and required external modules
    template_file: str
        Path to the template you want to upload

    Returns
    -------
        location_response: location of the new template

    """

    try:
        with open(template_file, 'r') as f:
            template = json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f'Invalid JSON file: {template_file}')

    api_client = get_elab_config(server_config_json)
    template_api = elabapi_python.ExperimentsTemplatesApi(api_client)

    if template['metadata']:
        response = template_api.post_experiment_template_with_http_info(body={"title": template['title']})
        location_response = response[2].get('Location')
        item_id = int(location_response.split('/').pop())
        response = template_api.patch_experiment_template_with_http_info(
            item_id, body={'metadata': template['metadata']})
        status_code = response[1]

    else:
        response = template_api.post_experiment_template_with_http_info(body={"title": template['title']})
        status_code = response[1]
        location_response = response[2].get('Location')

    return location_response, status_code


def upload_template_from_csv(server_config_json, csv_file, title):
    """
    Upload a template with an old csv file.

    Parameters
    ----------
    server_config_json: str
        Path to the json file containing the redcap url, api token and required external modules
    csv_file: str
        Path to the csv file you want to convert into an Elab version
    title: str
        Title of the template to upload

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
