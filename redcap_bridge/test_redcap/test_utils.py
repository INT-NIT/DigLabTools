import json
import os
import pathlib
import shutil
import tempfile

import pytest

from redcap_bridge.utils import compress_record
from redcap_bridge.utils import conversion_csv_to_json
test_directory = pathlib.Path(tempfile.gettempdir()) / 'diglabtools_testfiles'
project_dir = test_directory / 'testfiles' / 'TestProject'


@pytest.fixture
def initialize_test_dir(clean=True):
    """
    Create main test folder if required and add test files

    Parameters
    ----------
    clean: (bool)
        Remove test folder first in case it exists.

    Returns
    -------
    path
        path of the test directory
    """
    if clean and os.path.exists(test_directory):
        shutil.rmtree(test_directory)
    if not os.path.exists(test_directory):
        os.mkdir(test_directory)

    # initialize test files
    packaged_testfolder = pathlib.Path(__file__).parent / 'testfiles'
    shutil.copytree(packaged_testfolder, test_directory / 'testfiles')
    return test_directory


def test_compressedCSV(initialize_test_dir):

    test_dir = test_directory / 'testfiles' / 'compression_test'

    compress_record(test_dir / 'original_record.csv', test_dir / 'compressed_record.csv')
    with open(test_dir / 'compressed_record.csv') as comp_file:
        with open(test_dir / 'expected_record.csv') as exp_file:
            res = comp_file.read()
            exp = exp_file.read()
            assert res == exp

def test_conversion_csv_to_json(initialize_test_dir):

    test_dir = test_directory / 'testfiles' / 'elabConversion'

    f = open(test_dir / 'elabFinal.json')
    elab_final = json.load(f)
    elab_conversion = conversion_csv_to_json(test_dir / 'csvRecord.csv')
    assert elab_conversion == elab_final

