import json

import pytest

from elab_bridge.project_building import build_project, customize_project
from elab_bridge.project_validation import \
    validate_project_against_template_parts, validate_experiment_against_template
from diglab_utils.test_utils import (test_directory, initialize_test_dir)

project_dir = test_directory / 'testfiles_elab' / 'TestProject'

@pytest.fixture
def setup_project_jsons():
    # pre-build project csvs based on project definition
    build_project(project_dir / 'structure.json',
                  project_dir / 'build.json')
    customize_project(project_dir / 'build.json',
                      project_dir / 'customizations.json',
                      output_file=project_dir / 'customized.json')


def test_validate_project_against_template_parts(initialize_test_dir,
                                                 setup_project_jsons):
    with open(project_dir / 'project.json') as f:
        project_dict = json.load(f)
    template_parts = project_dict['validation']

    validate_project_against_template_parts(project_dir / 'customized.json',
                                            *template_parts)


def test_validate_experiment_against_template(initialize_test_dir, setup_project_jsons):
    experiment_json = test_directory / 'testfiles_elab' / 'experiment.json'

    # validate against provided project template and constructed template
    validate_experiment_against_template(experiment_json,
                                         test_directory / 'testfiles_elab' / 'template.json')
    validate_experiment_against_template(experiment_json, project_dir / 'customized.json')


def test_validate_project_without_template(initialize_test_dir, setup_project_jsons):
    # test with an empty list of template parts
    validate_project_against_template_parts(project_dir / 'customized.json')
