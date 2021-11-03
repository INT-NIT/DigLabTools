import json

import pandas as pd

from redcap_bridge.project_building import (build_project, customize_project,
                                            extract_customization)
from redcap_bridge.test_redcap.test_utils import (test_directory,
                                                  initialize_test_dir)

project_dir = test_directory / 'testfiles' / 'TestProject'


def test_build_and_customize_project(initialize_test_dir):
    """
    Test building and customizing a project based on its project specifications
    """
    # Running test project build
    build_project(project_dir / 'structure.csv',
                  project_dir / 'build.csv')
    assert (project_dir / 'build.csv').exists()

    # Running test project customization
    customize_project(project_dir / 'build.csv',
                      project_dir / 'customizations.csv',
                      output_file=project_dir / 'customized.csv')
    assert (project_dir / 'customized.csv').exists()


def test_project_build_with_provenance():
    # Running test project build
    build_project(project_dir / 'structure.csv',
                  project_dir / 'build.csv')

    exp_prov_lines = ["provenance_diglabtools_commit,diglabform,,descriptive",
                      "provenance_diglabtools_version,diglabform,,descriptive",
                      "provenance_redcap_forms_commit,diglabform,,descriptive"]

    with open(project_dir / 'build.csv', 'r') as f:
        lines = f.readlines()
        for lid, line in enumerate(lines[-3:]):
            assert line.startswith(exp_prov_lines[lid])
            assert line.endswith(',@HIDDEN\n')


def test_extract_customization(initialize_test_dir):
    """
    Test extracting the customizations.csv from a complete project build and
    known included template parts
    """
    # build and customize project
    build_project(project_dir / 'structure.csv',
                  project_dir / 'build.csv')
    customize_project(project_dir / 'build.csv',
                      project_dir / 'customizations.csv',
                      output_file=project_dir / 'customized.csv')

    # get template parts to compare to
    with open(project_dir / 'project.json') as f:
        project_dict = json.load(f)
    template_parts = project_dict['validation']

    # extract customization
    extract_customization(project_dir / 'customized.csv',
                          project_dir / 'extracted_customizations.csv',
                          *template_parts)

    original = pd.read_csv(project_dir / 'customizations.csv')
    extracted = pd.read_csv(project_dir / 'extracted_customizations.csv')

    assert original.equals(extracted)
