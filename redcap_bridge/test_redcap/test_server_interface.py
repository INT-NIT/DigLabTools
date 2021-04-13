import json

import pandas as pd
import pytest

import redcap
from redcap_bridge.server_interface import upload_datadict, download_records
from redcap_bridge.test_redcap.test_utils import (test_directory,
                                                  initialize_test_directory,
                                                  initialize_testfiles)
from redcap_bridge.utils import map_header_csv_to_json

SERVER_CONFIG_YAML = (
        test_directory / 'testfiles' / 'TestProject' / 'project.json').resolve()


@pytest.fixture
def clean_server(initialize_test_directory, initialize_testfiles):
    """
    Put testing server in a defined state: only minimal metadata (instruments)
    and records present
    """
    # replace existing datadict and record at server by default ones
    config = json.load(open(SERVER_CONFIG_YAML, 'r'))

    # TODO: Add step 0: Initialize project (activate surveys and repeating
    #  instruments )
    #  -> requires extension of PyCap by `import_project_info` method

    # first initialize in lazy mode to configure metadata even if server status
    # is corrupted
    redproj = redcap.Project(config['api_url'], config['api_token'], lazy=True)

    default_datadict = pd.DataFrame(data=[['record_id', 'my_first_instrument',
                                           'text', 'Record ID'] + [''] * 14],
                                    columns=map_header_csv_to_json)
    redproj.import_metadata(default_datadict, format='csv')

    default_records = pd.DataFrame(columns=['record_id',
                                            'my_first_instrument_complete'])
    redproj.import_records(default_records,
                           format='csv', return_format='json',
                           overwrite="overwrite")


def test_upload_datadict(clean_server, initialize_test_directory,
                         initialize_testfiles):
    metadata_csv = test_directory / 'testfiles' / 'metadata.csv'
    res = upload_datadict(metadata_csv, SERVER_CONFIG_YAML)

    # count number of non-empty lines in original csv
    with open(metadata_csv) as f:
        lines = f.readlines()
        exp = len(lines) - 1  # header row does not generate a record

    assert exp == res

def test_upload_records(clean_server, initialize_test_directory, initialize_testfiles):
    """
    TODO: Finally this test should test the corresponding redcap_bridge
    `upload_records` method instead of pycap itself
    """
    # upload data records
    config = json.load(open(SERVER_CONFIG_YAML, 'r'))
    redproj = redcap.Project(config['api_url'], config['api_token'], lazy=False)

    upload_datadict(test_directory / 'testfiles' / 'metadata.csv',
                    SERVER_CONFIG_YAML)

    uploaded_records = pd.read_csv(test_directory / 'testfiles' / 'record.csv',
                                   index_col=0, dtype='str')
    redproj.import_records(uploaded_records, format='csv', overwrite='overwrite')


def test_download_records(clean_server, initialize_test_directory, initialize_testfiles):
    # Step 1: uploading records
    # TODO: This part needs to be updated together with `test_upload_records`
    # upload data records
    config = json.load(open(SERVER_CONFIG_YAML, 'r'))
    redproj = redcap.Project(config['api_url'], config['api_token'], lazy=False)

    upload_datadict(test_directory / 'testfiles' / 'metadata.csv',
                    SERVER_CONFIG_YAML)

    uploaded_records = pd.read_csv(test_directory / 'testfiles' / 'record.csv',
                                   index_col=0, dtype='str')
    redproj.import_records(uploaded_records, format='csv', overwrite='overwrite')

    # Step 2: download data records
    downloaded_csv = test_directory / 'record_downloaded.csv'
    download_records(downloaded_csv, SERVER_CONFIG_YAML)

    # Step 3: Compare entries
    assert downloaded_csv.exists()

    # Step 4: Comparison of values
    downloaded_records = pd.read_csv(downloaded_csv, dtype='str')
    uploaded_records.equals(downloaded_records)
