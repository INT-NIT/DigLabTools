from elab_bridge.server_interface import (download_experiment, upload_template)
from diglab_utils.test_utils import (test_directory, initialize_test_dir)

SERVER_CONFIG_YAML = (test_directory / 'testfiles_elab' / 'TestProject' / 'project.json').resolve()


def test_upload_template(initialize_test_dir):
    template_file = test_directory / 'testfiles_elab' / 'elab_template.json'

    res, http_stat_code = upload_template(server_config_json=SERVER_CONFIG_YAML, template_file=template_file)

    # 200 is for creation of a template with metadata / 201 is for creation of a template without metadata
    assert http_stat_code == 200 or http_stat_code == 201


def test_download_experiment(initialize_test_dir):
    csv_file = test_directory / 'testfiles_elab' / 'downloaded_experiment.csv'
    http_stat_code, df = download_experiment(save_to=csv_file, server_config_json=SERVER_CONFIG_YAML, experiment_id=232,
                                             experiment_axis='columns', format='csv')

    df.to_csv(csv_file, index=False)

    assert http_stat_code == 200
