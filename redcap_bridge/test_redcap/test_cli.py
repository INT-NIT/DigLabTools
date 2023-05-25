import subprocess
import pathlib

from redcap_bridge.server_interface import upload_datadict, upload_records
from redcap_bridge.test_redcap.test_utils import (test_directory, initialize_test_dir)
from redcap_bridge.test_redcap.test_server_interface import SERVER_CONFIG_YAML

project_dir = test_directory / 'testfiles' / 'TestProject'


def test_installed(initialize_test_dir):
    """
    Check that RedCapBridge was installed successfully
    """
    result = subprocess.run(['RedCapBridge', '--help'], stdout=subprocess.PIPE)
    assert 'usage:' in str(result.stdout)


def test_download(initialize_test_dir):
    """
    Check that download option works for Test Project
    """

    # Set up project on server
    metadata_csv = test_directory / 'testfiles' / 'metadata.csv'
    upload_datadict(metadata_csv, SERVER_CONFIG_YAML)
    records_csv = test_directory / 'testfiles' / 'record.csv'
    upload_records(records_csv, SERVER_CONFIG_YAML)

    output_file = test_directory / 'cli_download_test.csv'

    # download with default arguments
    result = subprocess.run(['RedCapBridge', 'download', output_file, SERVER_CONFIG_YAML],
                            stdout=subprocess.PIPE)
    assert 'error' not in str(result.stdout)
    assert output_file.exists()
    output_file.unlink()

    # download in compressed mode
    result = subprocess.run(['RedCapBridge', 'download', '--compressed', output_file,
                             SERVER_CONFIG_YAML],
                            stdout=subprocess.PIPE)
    assert 'error' not in str(result.stdout)
    assert pathlib.Path(output_file).exists()
    output_file.unlink()

    # download with format argument
    result = subprocess.run(['RedCapBridge', 'download', '--format', 'csv', output_file,
                             SERVER_CONFIG_YAML],
                            stdout=subprocess.PIPE)
    assert 'error' not in str(result.stdout)
    assert pathlib.Path(output_file).exists()

    # download with Elabftw server
    result = subprocess.run(['RedCapBridge', 'download', SERVER_CONFIG_YAML, '--server', 'elabftw', '232'],
                            stdout=subprocess.PIPE)
    assert 'error' not in str(result.stdout)
    assert pathlib.Path(output_file).exists()

