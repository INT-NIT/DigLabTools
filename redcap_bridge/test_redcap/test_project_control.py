import pytest
from redcap_bridge.project_control import setup_project
from redcap_bridge.test_redcap.test_utils import (test_directory,
                                                  initialize_test_dir)

def test_setup_project(initialize_test_dir):
    working_dir = test_directory / 'working_dir'
    working_dir.mkdir(exist_ok=True)

    setup_project(test_directory / 'testfiles' / 'TestProject',
                  working_dir=working_dir)

