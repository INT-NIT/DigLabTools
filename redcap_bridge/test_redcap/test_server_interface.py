
import pandas as pd
import pytest

from redcap_bridge.server_interface import (upload_datadict, download_records, download_datadict,
                                            check_external_modules, get_redcap_project,
                                            upload_records, download_project_settings,
                                            configure_project_settings)

from redcap_bridge.test_redcap.test_utils import (test_directory, initialize_test_dir)
from redcap_bridge.utils import map_header_csv_to_json

SERVER_CONFIG_YAML = (test_directory / 'testfiles_redcap' / 'TestProject' / 'project.json').resolve()


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
    #  -> requires RedCap SUPER API TOKEN (64 characters), beyond standard user rights

    # first initialize in lazy mode to configure metadata even if server status
    # is corrupted
    redproj = get_redcap_project(SERVER_CONFIG_YAML)

    default_datadict = pd.DataFrame(data=[['record_id', 'my_first_instrument',
                                           'text', 'Record ID'] + [''] * 14],
                                    columns=map_header_csv_to_json)
    redproj.import_metadata(default_datadict, import_format='df')

    # second initialize in non-lazy mode to configure records
    redproj = get_redcap_project(SERVER_CONFIG_YAML)
    default_records = pd.DataFrame(columns=['record_id',
                                            'my_first_instrument_complete'])
    redproj.import_records(default_records,
                           import_format='df', return_format_type='json',
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
    """
    upload_datadict(test_directory / 'testfiles' / 'metadata.csv', SERVER_CONFIG_YAML)
    res = upload_records(test_directory / 'testfiles' / 'record.csv', SERVER_CONFIG_YAML)

    # test record.csv contains 2 records
    assert res == 2


def test_download_records(clean_server, initialize_test_dir):
    """
    Download datadict from server and compare to previously uploaded datadict
    """
    # uploading metadata csv files from testfile dataset and compare to
    # return value of upload
    original_record_csv = test_directory / 'testfiles' / 'record.csv'
    upload_datadict(test_directory / 'testfiles' / 'metadata.csv', SERVER_CONFIG_YAML)
    upload_records(test_directory / 'testfiles' / 'record.csv', SERVER_CONFIG_YAML)

    downloaded_record_csv = test_directory / 'testfiles' / 'record_downloaded.csv'
    download_records(downloaded_record_csv, SERVER_CONFIG_YAML)

    import csv
    original_reader = csv.reader(open(original_record_csv))
    download_reader = csv.reader(open(downloaded_record_csv))

    # comparing headers
    original_header = original_reader.__next__()
    downloaded_header = download_reader.__next__()
    for i, oh in enumerate(original_header):
        # uploading of records can fail if the record cache on the server is not clean
        # in this case reset the record cache on the webinterface of redcap
        assert oh in downloaded_header, f'{oh} not in downloaded header'

    # compare content
    for oline, dline in zip(original_reader, download_reader):
        assert oline == dline


def test_download_datadict(clean_server, initialize_test_dir):
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


def test_download_project_settings(clean_server):
    """
    Download project settings
    """
    res = download_project_settings(SERVER_CONFIG_YAML)
    assert type(res) == dict
    required_project_info = ['project_id', 'project_title', 'external_modules']
    for key in required_project_info:
        assert key in res


def test_configure_project_settings(clean_server, initialize_test_dir):
    """
    Test configure server project based on default values and project.json
    """
    configure_project_settings(SERVER_CONFIG_YAML)

    # confirm project settings on server are consistent with project configuration
    proj_settings = download_project_settings(SERVER_CONFIG_YAML)
    assert proj_settings['surveys_enabled']
    assert len(proj_settings['external_modules'])

    # no repeating instruments set at this time as no records were imported
    # redproj = get_redcap_project(SERVER_CONFIG_YAML)
    # rep_inst_settings = redproj.export_repeating_instruments_events()
    # assert len(rep_inst_settings) == 1
    # assert "form_name" in rep_inst_settings[0]
    # assert "custom_form_label" in rep_inst_settings[0]

    redproj = get_redcap_project(SERVER_CONFIG_YAML)
    metadata = redproj.export_metadata()
    records = redproj.export_records()
    assert 'field_name' in metadata[0]
    assert 'record_id' in records[0]

