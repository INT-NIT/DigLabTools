import json
import os
import elabapi_python
import pandas as pd


def extended_download(save_to, server_config_json, experiment_tags=None, format='csv', experiment_axis='columns'):
    """
    Download experiments based on tags or a specific experiment by ID.

    Parameters
    ----------
    save_to: str
        Path where to save the retrieved experiment data
    server_config_json: str
        Path to the json file containing the api_url and the api_token
    experiment_tags: list, optional
        List of tags of your experiments. Default is None.
    experiment_id: int, optional
        ID of the experiment you want to download. Default is None.
    format: str
        Format of the retrieved records. Options are 'csv' or 'json'. Default: 'csv'
    experiment_axis: str
        Option to control whether in the csv format experiments are arranged in columns or rows.
        Default: 'columns'

    Returns
    -------
    list
        List of the experiment(s) downloaded
    """

    api_client = get_elab_config(server_config_json)
    experiment_api = elabapi_python.ExperimentsApi(api_client)

    if experiment_tags:
        response = experiment_api.read_experiments_with_http_info(tags=experiment_tags)
        experiments = response[0]
        experiment_ids = [experiment.id for experiment in experiments]
    else:
        raise ValueError("Either experiment_tags or experiment_id must be provided.")

    downloaded_experiments = []
    combined_df = pd.DataFrame()

    for exp_id in experiment_ids:
        experiment_body, status_get, http_dict = experiment_api.get_experiment_with_http_info(exp_id)

        if status_get != 200:
            raise ValueError('Could not download experiment. '
                             'Check your internet connection and permissions.')

        experiment_json = experiment_body.metadata
        metadata = json.loads(experiment_json)
        extra_fields = metadata.get("extra_fields", {})

        if format == 'json':
            with open(save_to, 'w') as f:
                json.dump(extra_fields, f)
        elif format == 'csv':
            if experiment_axis == 'columns':
                df = pd.DataFrame.from_dict(extra_fields, orient='columns')
                combined_df = pd.concat([combined_df, df.iloc[[1]]], ignore_index=True, sort=False)
            elif experiment_axis == 'rows':
                df = pd.DataFrame.from_dict(extra_fields, orient='index')
                df = df[['value']].transpose()
                combined_df = pd.concat([combined_df, df], ignore_index=True, sort=False)
            else:
                raise ValueError(f'Unknown experiment axis: {experiment_axis}. Valid arguments are '
                                 f'"columns" and "rows".')
        else:
            raise ValueError(f'Unknown format: {format}. Valid arguments are "json" and "csv".')

        downloaded_experiments.append(metadata)

    if format == 'csv':
        combined_df.to_csv(save_to, index=False)

    return downloaded_experiments


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
        (dict) Content of the experiment as registered on the server
        (int) ID of the experiment
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

    res = experiment_api.post_experiment_with_http_info(body={"category_id": -1})
    _, status_creation, http_dict = res
    if status_creation != 201:
        raise ValueError('Creation of experiment on server failed.'
                         ' Check your internet connection and permissions.')
    item_id = http_dict.get('Location').split('/')[-1]
    item_id = int(item_id)
    res = experiment_api.patch_experiment_with_http_info(
        item_id,
        body={"title": experiment_title, "metadata": experiment_form_string}
    )
    experiment_obj, status_population, http_dict = res

    if status_population != 200:
        raise ValueError('Population of experiment on server failed. '
                         'Check your internet connection and permissions.')

    metadata = json.loads(experiment_obj.metadata)

    return metadata, item_id


def delete_experiment(experiment_id, server_config_json):
    """
    Delete an existing experiment.

    Parameters
    ----------
    experiment_id: int
        ID of the experiment you want to delete
    server_config_json: str
        Path to the json file containing the api_url and the api_token
    """
    api_client = get_elab_config(server_config_json)
    experiment_api = elabapi_python.ExperimentsApi(api_client)

    res = experiment_api.delete_experiment_with_http_info(id=experiment_id)
    status_delete = res[1]

    if status_delete != 204:
        raise ValueError('Deletion of an experiment on server failed.'
                         ' Check your internet connection and permissions.')


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
        (dict) Content of the template as registered on the server
        (int) ID of the template
    """

    try:
        with open(template_file, 'r') as f:
            template_json = json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f'Invalid JSON file: {template_file}')

    if 'extra_fields' not in template_json:
        raise ValueError('Mandatory field "extra_fields" not present in template')

    with open(template_file, 'r') as f:
        template_form_str = f.read()

    api_client = get_elab_config(server_config_json)
    template_api = elabapi_python.ExperimentsTemplatesApi(api_client)

    res = template_api.post_experiment_template_with_http_info(
        body={"title": template_title}
    )
    _, status_creation, http_dict = res
    if status_creation != 201:
        raise ValueError('Creation of template on server failed.'
                         ' Check your internet connection and permissions.')
    template_id = http_dict.get('Location').split('/')[-1]
    template_id = int(template_id)

    res = template_api.patch_experiment_template_with_http_info(template_id,
                                                                body={'metadata': template_form_str})
    template_obj, status_population, http_dict = res

    if status_population != 200:
        raise ValueError('Population of template on server failed. '
                         'Check your internet connection and permissions.')

    assert template_id == template_obj.id

    metadata = json.loads(template_obj.metadata)

    return metadata, template_id


def delete_template(template_id, server_config_json):
    """
    Delete an existing template.

    Parameters
    ----------
    template_id: int
        ID of the experiment you want to delete
    server_config_json: str
        Path to the json file containing the api_url and the api_token
    """
    api_client = get_elab_config(server_config_json)
    template_api = elabapi_python.ExperimentsTemplatesApi(api_client)

    res = template_api.delete_experiment_template_with_http_info(id=template_id)
    status_delete = res[1]

    if status_delete != 204:
        raise ValueError('Deletion of an template on server failed.'
                         ' Check your internet connection and permissions.')


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
