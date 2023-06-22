from diglab_utils.test_utils import (test_directory, initialize_test_dir)
from elab_bridge.server_interface import (download_experiment, upload_template, upload_experiment)

SERVER_CONFIG_YAML = (test_directory / 'testfiles_elab' / 'TestProject' / 'project.json').resolve()


def test_upload_template(initialize_test_dir):
    template_file = test_directory / 'testfiles_elab' / 'template.json'
    template = upload_template(server_config_json=SERVER_CONFIG_YAML,
                               template_file=template_file,
                               template_title='Testproject')

    assert 'elabftw' in template
    assert 'extra_fields' in template


def test_upload_experiment(initialize_test_dir):
    template_file = test_directory / 'testfiles_elab' / 'experiment.json'

    experiment = upload_experiment(server_config_json=SERVER_CONFIG_YAML,
                                   experiment_file=template_file,
                                   experiment_title='TestExperiment')

    assert 'extra_fields' in experiment


def test_download_experiment(initialize_test_dir):
    json_file = test_directory / 'testfiles_elab' / 'downloaded_experiment.json'
    upload_experiment_file = test_directory / 'testfiles_elab' / 'experiment.json'
    upload, experiment_id = upload_experiment(server_config_json=SERVER_CONFIG_YAML,
                                              experiment_file=upload_experiment_file,
                                              experiment_title='UploadExperiment')

    experiment = download_experiment(save_to=json_file,
                                     server_config_json=SERVER_CONFIG_YAML,
                                     experiment_id=experiment_id,
                                     format='json')

    assert upload == experiment

    assert json_file.exists()
    assert 'extra_fields' in experiment

    # cleanup
    json_file.unlink()
