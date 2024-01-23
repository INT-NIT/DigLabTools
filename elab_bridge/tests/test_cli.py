import subprocess
import pytest

from elab_bridge.server_interface import upload_template, download_experiment
from diglab_utils.test_utils import (test_directory, initialize_test_dir)
from elab_bridge.tests.test_server_interface import SERVER_CONFIG_YAML

project_dir = test_directory / 'testfiles_elab' / 'TestProject'

@pytest.mark.skip('Requires `upload_experiment` to be implemented')
def test_installed(initialize_test_dir):
    """
    Check that ElabBridge was installed successfully
    """
    result = subprocess.run(['ElabBridge', '--help'], stdout=subprocess.PIPE)
    assert 'usage:' in str(result.stdout)

@pytest.mark.skip('Requires `upload_experiment` to be implemented')
def test_download(initialize_test_dir):
    """
    Check that download option works for Test Project
    """

    # Set up project on server
    template = test_directory / 'testfiles_elab' / 'template.json'
    upload_template(template, SERVER_CONFIG_YAML, 'Testproject')
    # records_csv = test_directory / 'testfiles_elab' / 'record.csv'
    # upload_records(records_csv, SERVER_CONFIG_YAML)

    output_file = test_directory / 'cli_download_test.csv'

    # download with default arguments
    result = subprocess.run(['ElabBridge', 'download', output_file, SERVER_CONFIG_YAML],
                            stdout=subprocess.PIPE)
    assert 'error' not in str(result.stdout)
    assert output_file.exists()
    output_file.unlink()

    # # download in compressed mode
    # result = subprocess.run(['ElabBridge', 'download', '--compressed', output_file,
    #                          SERVER_CONFIG_YAML],
    #                         stdout=subprocess.PIPE)
    # assert 'error' not in str(result.stdout)
    # assert pathlib.Path(output_file).exists()
    # output_file.unlink()

    # # download with format argument
    # result = subprocess.run(['ElabBridge', 'download', '--format', 'csv', output_file,
    #                          SERVER_CONFIG_YAML],
    #                         stdout=subprocess.PIPE)
    # assert 'error' not in str(result.stdout)
    # assert pathlib.Path(output_file).exists()

def test_download(initialize_test_dir):
    """
    Check extended_download
    """

    tags = ['BIDS']
    output_file = test_directory / 'cli_download_test.csv'

    result = subprocess.run(['ElabBridge', 'extended_download', output_file, SERVER_CONFIG_YAML] + tags,
                             stdout=subprocess.PIPE)

    assert 'error' not in str(result.stdout)
    assert output_file.exists()
    output_file.unlink()

