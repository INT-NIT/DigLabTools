import pytest
import json
import pathlib
import redcap
import pandas as pd
from redcap_bridge.server_interface import upload_datadict
from redcap_bridge.test_redcap.test_utils import (test_directory,
                                                  initialize_test_directory,
                                                  initialize_testfiles)
from redcap_bridge.utils import map_header_csv_to_json

SERVER_CONFIG_YAML = (test_directory / 'testfiles' / 'TestProject' / 'project.json').resolve()


@pytest.fixture
def clean_server():
    # replace existing datadict and record at server by default ones
    config = json.load(open(SERVER_CONFIG_YAML, 'r'))
    redproj = redcap.Project(config['api_url'], config['api_token'], lazy=False)

    default_datadict = pd.DataFrame(data=[['record_id', 'my_first_instrument',
                                           'text', 'Record ID'] + ['']*14],
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
