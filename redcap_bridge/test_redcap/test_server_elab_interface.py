from redcap_bridge.server_elab_interface import (upload_template_from_csv, download_experiment,
                                                 upload_template)
from redcap_bridge.test_redcap.test_utils import (test_directory, initialize_test_dir)

SERVER_CONFIG_YAML = (test_directory / 'testfiles' / 'TestProject' / 'project.json').resolve()


def test_upload_template(initialize_test_dir):
    template_file = test_directory / 'testfiles' / 'elab_template.json'

    res, http_stat_code = upload_template(server_config_json=SERVER_CONFIG_YAML, template_file=template_file)

    # 200 is for creation of a template with metadata / 201 is for creation of a template without metadata
    assert http_stat_code == 200 or http_stat_code == 201


def test_upload_template_from_csv(initialize_test_dir):
    csv_file = test_directory / 'testfiles' / 'metadata.csv'

    res, http_stat_code = upload_template_from_csv(server_config_json=SERVER_CONFIG_YAML, csv_file=csv_file,
                                                   title='General Template')

    assert http_stat_code == 201


def test_download_experiment(initialize_test_dir):
    csv_file = test_directory / 'testfiles' / 'elabConversion' / 'download_to_csv.csv'
    http_stat_code, df = download_experiment(save_to=csv_file, server_config_json=SERVER_CONFIG_YAML, experiment_id=232,
                                             experiment_axis='columns')

    df.to_csv(csv_file, index=False)

    assert http_stat_code == 200
