import pandas as pd
import pytest

from redcap_bridge.server_interface import (upload_datadict, download_records,
                                            download_datadict, check_external_modules,
                                            get_redcap_project)

from redcap_bridge.test_redcap.test_utils import (test_directory,
                                                  initialize_test_dir)
from redcap_bridge.utils import map_header_csv_to_json

SERVER_CONFIG_YAML = (
        test_directory / 'testfiles' / 'TestProject' / 'project.json').resolve()


@pytest.fixture
def clean_server(initialize_test_dir):
    """
    Put testing server in a defined state: only minimal metadata (instruments)
    and records present
    """
    # replace existing datadict and record at server by default ones

    # TODO: Add step 0: Initialize project (activate surveys and repeating
    #  instruments )
    #  -> requires extension of PyCap by `import_project_info` method

    # first initialize in lazy mode to configure metadata even if server status
    # is corrupted
    redproj = get_redcap_project(SERVER_CONFIG_YAML)

    default_datadict = pd.DataFrame(data=[['record_id', 'my_first_instrument',
                                           'text', 'Record ID'] + [''] * 14],
                                    columns=map_header_csv_to_json)
    redproj.import_metadata(default_datadict, format='csv')

    # second initialize in non-lazy mode to configure records
    redproj = get_redcap_project(SERVER_CONFIG_YAML)
    default_records = pd.DataFrame(columns=['record_id',
                                            'my_first_instrument_complete'])
    redproj.import_records(default_records,
                           format='csv', return_format='json',
                           overwrite="overwrite")


def test_upload_datadict(clean_server, initialize_test_dir):
    """
    Test uploading a survey definition (datadict) csv to the server
    """
    # uploading metadata csv files from testfile dataset and compare to
    # return value of upload
    metadata_csv = test_directory / 'testfiles' / 'metadata.csv'
    res = upload_datadict(metadata_csv, SERVER_CONFIG_YAML)

    # count number of non-empty lines in original csv
    with open(metadata_csv) as f:
        lines = f.readlines()
        exp = len(lines) - 1  # header row does not generate a record

    assert exp == res

def test_upload_records(clean_server, initialize_test_dir):
    """
    Test upload of records to the server

    TODO: Finally this test should test the corresponding redcap_bridge
    `upload_records` method instead of pycap itself
    """
    # upload data records
    redproj = get_redcap_project(SERVER_CONFIG_YAML)

    upload_datadict(test_directory / 'testfiles' / 'metadata.csv',
                    SERVER_CONFIG_YAML)

    uploaded_records = pd.read_csv(test_directory / 'testfiles' / 'record.csv',
                                   index_col=0, dtype='str')
    redproj.import_records(uploaded_records, format='csv', overwrite='overwrite')


def test_download_records(clean_server, initialize_test_dir):
    """
    Download datadict from server and compare to previously uploaded datadict
    """
    # uploading metadata csv files from testfile dataset and compare to
    # return value of upload
    original_metadata_csv = test_directory / 'testfiles' / 'metadata.csv'
    upload_datadict(original_metadata_csv, SERVER_CONFIG_YAML)


    downloaded_metadata_csv = test_directory / 'testfiles' / 'metadata_downloaded.csv'
    download_datadict(downloaded_metadata_csv, SERVER_CONFIG_YAML)


    import csv
    original_reader = csv.reader(open(original_metadata_csv))
    download_reader = csv.reader(open(downloaded_metadata_csv))

    # comparing headers
    original_header = original_reader.__next__()
    downloaded_header = download_reader.__next__()
    for oh, dh in zip(original_header, downloaded_header):
        # translate header of uploaded csv to follow csv standard
        assert map_header_csv_to_json[oh] == dh

    # compare content
    for oline, dline in zip(original_reader, download_reader):
        assert oline == dline


def test_check_external_modules(clean_server, initialize_test_dir):
    """
    Download project info from server and compare to required external modules
    """

    assert check_external_modules(SERVER_CONFIG_YAML)
