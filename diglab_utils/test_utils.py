import shutil
import os
import pathlib
import tempfile
import pytest

test_directory = pathlib.Path(tempfile.gettempdir()) / 'diglabtools_testfiles'
project_dir = test_directory / 'testfiles_redcap' / 'TestProject'

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
    packaged_testfolders = [
        pathlib.Path(__file__).parents[1] / 'redcap_bridge' / 'tests' /'testfiles_redcap',
        pathlib.Path(__file__).parents[1] / 'elab_bridge' / 'tests' / 'testfiles_elab',
        pathlib.Path(__file__).parents[1] / 'diglab_utils' / 'tests' / 'testfiles_diglab_utils']
    for server, packaged_testfolder in zip(['redcap', 'elab', 'diglab_utils'], packaged_testfolders):
        shutil.copytree(packaged_testfolder, test_directory / packaged_testfolder.name)
    return test_directory