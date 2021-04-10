import os
import pathlib
import shutil
import tempfile

import pytest

test_directory = pathlib.Path(tempfile.gettempdir()) / 'diglabtools_testfiles'


@pytest.fixture
def initialize_test_directory(clean=True):
    """
    Create main test folder if required

    Parameters
    ----------
    clean: (bool)
        Remove test folder first in case it exists.

    Returns
    -------
    test_directory: (str)
        path of the test directory
    """
    if clean and os.path.exists(test_directory):
        shutil.rmtree(test_directory)
    if not os.path.exists(test_directory):
        os.mkdir(test_directory)
    return test_directory


@pytest.fixture
def initialize_testfiles():
    packaged_testfolder = pathlib.Path(__file__).parent / 'testfiles'
    shutil.copytree(packaged_testfolder, test_directory / 'testfiles')
