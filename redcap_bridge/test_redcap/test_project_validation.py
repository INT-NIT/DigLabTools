import pytest
import pathlib
import json
from redcap_bridge.test_redcap.test_utils import (test_directory,
                                                  initialize_test_directory,
                                                  initialize_testfiles)
from redcap_bridge.project_building import build_project, customize_project
from redcap_bridge.project_validation import validate_project_against_template_parts, load_template, load_records, validate_record_against_template

project_dir = test_directory / 'testfiles' / 'TestProject'


def test_validate_project_against_template_parts(initialize_test_directory, initialize_testfiles):
    # create the customized project
    build_project(project_dir / 'structure.csv',
                  project_dir / 'build.csv')
    customize_project(project_dir / 'build.csv',
                      project_dir / 'customizations.csv',
                      output_file=project_dir / 'customized.csv')

    with open(project_dir / 'project.json') as f:
        project_dict = json.load(f)
    template_parts = project_dict['validation']

    validate_project_against_template_parts(project_dir / 'customized.csv',
                                            *template_parts)


def test_load_template():
    testfile = test_directory / 'testfiles' / 'Diglabform_2021-02-15_1731.zip'
    template = load_template(testfile)

    assert not testfile.with_suffix('').exists()

    mandatory_columns = ['Variable / Field Name', 'Form Name', 'Section Header',
                         'Field Type', 'Field Label',
                         'Choices, Calculations, OR Slider Labels',
                         'Field Note',
                         'Text Validation Type OR Show Slider Number',
                         'Text Validation Min', 'Text Validation Max',
                         'Identifier?',
                         'Branching Logic (Show field only if...)',
                         'Required Field?', 'Custom Alignment',
                         'Question Number (surveys only)', 'Matrix Group Name',
                         'Matrix Ranking?', 'Field Annotation']

    for mandatory_column in mandatory_columns:
        assert mandatory_column in template

    mandatory_vars = ['record_id', 'diglab', 'diglab_version',
                      'redcap_form_version']

    for mandatory_var in mandatory_vars:
        assert mandatory_var in template['Variable / Field Name'].values


# TODO: Add pytest fixture that ensure that project is defined on server side and contains records
def test_load_records():
    # NOTE: This test might fail due to connection issues to the server.
    # Ensure to use either lan or wireless connection, but not both at the
    # same time.
    data = load_records(project_dir / 'project.json')

    assert data is not None

# TODO: Add pytest.fixture for this test
def test_validate():
    records = load_records(project_dir / 'project.json')
    # This template might be outdated for these records. Add proper pytest.fixture configuration
    template = load_template(test_directory / 'testfiles' / 'DiglabformV4a_2021-03-17_1038.zip')

    validate_record_against_template(template, records)

