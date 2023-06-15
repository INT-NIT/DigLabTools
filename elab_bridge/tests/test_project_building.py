import json

import pandas as pd
import pytest
from elab_bridge.project_building import (build_project, customize_project,
                                            extract_customization)
from diglab_utils.test_utils import (test_directory, initialize_test_dir)

project_dir = test_directory / 'testfiles_elab' / 'TestProject'


def test_build_and_customize_project(initialize_test_dir):
    """
    Test building and customizing a project based on its project specifications
    """
    # Running test project build
    build_project(project_dir / 'structure.json',
                  project_dir / 'build.json')
    assert (project_dir / 'build.json').exists()

    # Running test project customization
    customize_project(project_dir / 'build.json',
                      project_dir / 'customizations.json',
                      output_file=project_dir / 'customized.json')
    assert (project_dir / 'customized.json').exists()


@pytest.mark.skip("provenance is not supported yet")
def test_project_build_with_provenance():
    # Running test project build
    build_project(project_dir / 'structure.json',
                  project_dir / 'build.json')

    exp_prov_lines = ["provenance_diglabtools_commit,diglabform,,descriptive",
                      "provenance_diglabtools_version,diglabform,,descriptive",
                      "provenance_elab_forms_commit,diglabform,,descriptive"]

    with open(project_dir / 'build.json', 'r') as f:
        lines = f.readlines()
        for lid, line in enumerate(lines[-3:]):
            assert line.startswith(exp_prov_lines[lid])
            assert line.endswith(',@HIDDEN\n')


@pytest.mark.skip('extract_customization is not supported yet.')
def test_extract_customization(initialize_test_dir):
    """
    Test extracting the customizations.json from a complete project build and
    known included template parts
    """
    # build and customize project
    build_project(project_dir / 'structure.json',
                  project_dir / 'build.json')
    customize_project(project_dir / 'build.json',
                      project_dir / 'customizations.json',
                      output_file=project_dir / 'customized.json')

    # get template parts to compare to
    with open(project_dir / 'project.json') as f:
        project_dict = json.load(f)
    template_parts = project_dict['validation']

    # extract customization
    extract_customization(project_dir / 'customized.json',
                          project_dir / 'extracted_customizations.json',
                          *template_parts)

    original = pd.read_csv(project_dir / 'customizations.json')
    extracted = pd.read_csv(project_dir / 'extracted_customizations.json')

    assert original.equals(extracted)
