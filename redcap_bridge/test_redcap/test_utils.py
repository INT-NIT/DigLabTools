import os
import pathlib
import shutil
import tempfile

import pandas as pd
import pytest

from redcap_bridge.utils import compressed_record
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
    custom_csv = pd.read_csv(test_directory / 'testfiles' / 'compression_test' / 'expected_record.csv', sep=';')
    print(custom_csv)
    result = compressed_record(test_directory / 'testfiles' / 'compression_test' / 'original_record.csv')
