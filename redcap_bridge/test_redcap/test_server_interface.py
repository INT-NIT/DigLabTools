import pytest
import json
import pathlib
import redcap
import pandas as pd
from redcap_bridge.project_building import build_project, customize_project
from redcap_bridge.server_interface import upload_datadict
from redcap_bridge.test_redcap.test_utils import (initialize_test_directory,
                                                  initialize_testfiles,
                                                  test_directory)
from redcap_bridge.utils import map_header_csv_to_json

SERVER_CONFIG_YAML = (pathlib.Path(__file__) / '..' / '../' / 'config.yaml').resolve()


@pytest.fixture
def setup_server():
    # this adds a dummy server configuration
    test_server_config = {'api_token': 'A85D960267EF6240BC16A64B298948E1',
                          'api_url': 'https://redcap.int.univ-amu.fr/api/'}
    # overwriting existing configuration
    with open(SERVER_CONFIG_YAML, 'w') as c:
        json.dump(test_server_config, c)

@pytest.fixture
def clean_server():
    # remove datadict and record from server
    config = json.load(open(SERVER_CONFIG_YAML, 'r'))
    redproj = redcap.Project(config['api_url'], config['api_token'], lazy=False)
    # # This is a dirty fix to deal with completely empty projects
    # for var in ['events', 'arm_nums', 'arm_names']:
    #     if getattr(redproj, var) is None:
    #         setattr(redproj, var, [])

    default_datadict = pd.DataFrame(data=[['record_id', 'my_first_instrument',
                                           'text', 'Record ID'] + ['']*14],
                                    columns=map_header_csv_to_json)
    redproj.import_metadata(default_datadict, format='csv')

    default_records = pd.DataFrame(columns=['record_id',
                                            'my_first_instrument_complete'])
    redproj.import_records(default_records,
                           format='csv', return_format='json',
                           overwrite="overwrite")



def test_upload_datadict(setup_server, clean_server, initialize_test_directory,
                         initialize_testfiles):
    metadata_csv = test_directory / 'testfiles' / 'metadata.csv'
    res = upload_datadict(metadata_csv, SERVER_CONFIG_YAML)

    # count number of non-empty lines in original csv
    with open(metadata_csv) as f:
        lines = f.readlines()
        exp = len(lines) - 1  # header row does not generate a record

    assert exp == res
