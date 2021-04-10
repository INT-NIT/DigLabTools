import json

import pytest

from redcap_bridge.project_building import build_project, customize_project
from redcap_bridge.project_validation import \
    validate_project_against_template_parts, validate_record_against_template
from redcap_bridge.test_redcap.test_utils import (test_directory,
                                                  initialize_test_directory,
                                                  initialize_testfiles)

project_dir = test_directory / 'testfiles' / 'TestProject'


@pytest.fixture
def setup_project_csvs():
    build_project(project_dir / 'structure.csv',
                  project_dir / 'build.csv')
    customize_project(project_dir / 'build.csv',
                      project_dir / 'customizations.csv',
                      output_file=project_dir / 'customized.csv')


def test_validate_project_against_template_parts(initialize_test_directory,
                                                 initialize_testfiles,
                                                 setup_project_csvs):
    with open(project_dir / 'project.json') as f:
        project_dict = json.load(f)
    template_parts = project_dict['validation']

    validate_project_against_template_parts(project_dir / 'customized.csv',
                                            *template_parts)


def test_validate_record_against_template(initialize_test_directory,
                                          initialize_testfiles,
                                          setup_project_csvs):
    record_csv = test_directory / 'testfiles' / 'record.csv'

    # validate against provided project metadata and constructed metadata
    validate_record_against_template(record_csv,
                                     test_directory / 'testfiles' / 'metadata.csv')
    validate_record_against_template(record_csv, project_dir / 'customized.csv')
