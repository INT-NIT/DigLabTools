import json
import os
import warnings
import elabapi_python
import pandas as pd


def download_experiment(save_to, server_config_json, experiment_id, experiment_axis='columns', format='csv'):
    """
    Download an individual experiment.

    Parameters
    ----------
    save_to: str
        Path where to save the retrieved experiment data
    server_config_json: str
        Path to the json file containing the api_url and the api_token
    format: 'csv', 'json'
        Format of the retrieved records
    experiment_id: int
        ID of the experiment you want to download
    experiment_axis: str
        Option to control whether experiments are arranged in columns or rows. Default: 'columns'

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


def upload_experiment(experiment_file, server_config_json, experiment_title):
    """
    Upload an experiment.

    Parameters
    ----------
    experiment_file: str
        Path to the experiment you want to upload. This has to be a json file
        containing the keys `elabftw' and `extra_fields`.
    server_config_json: str
        Path to the json file containing the api_url and the api_token
    experiment_title: str
        The title of the experiment you want to upload

    Returns
    -------
        location_response: location of the new template
    """

    try:
        with open(experiment_file, 'r') as f:
            experiment_json = json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f'Invalid JSON file: {experiment_file}')

    if 'extra_fields' not in experiment_json:
        raise ValueError('Mandatory field "extra_fields" not present in experiment')

    with open(experiment_file, 'r') as f:
        experiment_form_string = f.read()

    api_client = get_elab_config(server_config_json)
    experiment_api = elabapi_python.ExperimentsApi(api_client)

    response = experiment_api.post_experiment_with_http_info(body={"category_id": -1})
    location_response = response[2].get('Location')
    item_id = int(location_response.split('/').pop())
    response = experiment_api.patch_experiment_with_http_info(
        item_id,
        body={"title": experiment_title, "metadata": experiment_form_string}
    )
    status_code = response[1]

    return location_response, status_code


def upload_template(template_file, server_config_json, template_title):
    """
    Upload a template with metadata.

    Parameters
    ----------
    template_file: str
        Path to the template you want to upload. This has to be a json file
        containing the keys `elabftw' and `extra_fields`.
    server_config_json: str
        Path to the json file containing the api_url and the api_token
    template_title: str
        The title of the template you want to upload

    Returns
    -------
        location_response: location of the new template

    """

    try:
        with open(template_file, 'r') as f:
            template_json = json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f'Invalid JSON file: {template_file}')

    if 'extra_fields' not in template_json:
        raise ValueError('Mandatory field "extra_fields" not present in template')

    with open(template_file, 'r') as f:
        template_form_string = f.read()

    api_client = get_elab_config(server_config_json)
    template_api = elabapi_python.ExperimentsTemplatesApi(api_client)

    response = template_api.post_experiment_template_with_http_info(body={"title": template_title})
    location_response = response[2].get('Location')
    item_id = int(location_response.split('/').pop())
    response = template_api.patch_experiment_template_with_http_info(
        item_id,
        body={'metadata': template_form_string}
    )
    status_code = response[1]

    return location_response, status_code


def get_elab_config(server_config_json):
    """
    Initialize an elab project based on the provided server configuration
    :param server_config_json: json file containing the api_token and api_url
    :return: elab api client
    """

    config = json.load(open(server_config_json, 'r'))
    configuration = elabapi_python.Configuration()

    if config['api_token'] in os.environ:
        api_token = os.environ[config['api_token']]
    else:
        api_token = config['api_token']

    configuration.api_key['api_token'] = api_token
    configuration.api_key_prefix['api_token'] = 'Authorization'

    configuration.host = config['api_url']
    configuration.debug = True
    configuration.verify_ssl = False

    api_client = elabapi_python.ApiClient(configuration)
    api_client.set_default_header(header_name='Authorization', header_value=api_token)

    return api_client


if __name__ == '__main__':
    pass
