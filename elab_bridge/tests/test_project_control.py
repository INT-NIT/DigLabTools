from elab_bridge.project_control import setup_project
from diglab_utils.test_utils import (test_directory, initialize_test_dir)

def test_setup_project(initialize_test_dir):
    """
    Test building a complete project from its specifications and uploading it
    to the server
    """
    working_dir = test_directory / 'working_dir'
    working_dir.mkdir(exist_ok=True)

    setup_project(test_directory / 'testfiles_elab' / 'TestProject',
                  working_dir=working_dir)

