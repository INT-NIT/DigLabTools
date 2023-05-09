from redcap_bridge.server_elab_interface import (create_template_with_converted_csv, download_experiment,
                                                 create_template)
from redcap_bridge.test_redcap.test_utils import (test_directory, initialize_test_dir)

SERVER_CONFIG_YAML = (test_directory / 'testfiles' / 'TestProject' / 'project.json').resolve()

test_file = (test_directory / 'testfiles' / 'elabConversion' / 'csvRecord.csv')


def test_create_template(initialize_test_dir):
    template_file = test_directory / 'testfiles' / 'elab_template.json'

    res, http_stat_code = create_template(server_config_json=SERVER_CONFIG_YAML, template_file=template_file,
                                          metadata=True)

    # 200 is for creation of a template with metadata / 201 is for creation of a template without metadata
    assert http_stat_code == 200 or http_stat_code == 201


def test_create_template_with_converted_csv(initialize_test_dir):
    csv_file = test_directory / 'testfiles' / 'metadata.csv'

    res, http_stat_code = create_template_with_converted_csv(server_config_json=SERVER_CONFIG_YAML, csv_file=csv_file,
                                             title='General Template')

    assert http_stat_code == 201


def test_download_experiment(initialize_test_dir):
    res, http_stat_code = download_experiment(server_config_json=SERVER_CONFIG_YAML, experiment_id=232)

    assert http_stat_code == 200
