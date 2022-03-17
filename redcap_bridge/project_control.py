import os
import pathlib
import json
import tempfile

from redcap_bridge.project_building import build_project, customize_project
from redcap_bridge.project_validation import validate_project_against_template_parts
from redcap_bridge.server_interface import (upload_datadict, download_records,
                                            check_external_modules)

def setup_project(proj_folder, working_dir=None, include_provenance=True):
    """
    Build a project csv from its specifications and setup on the server

    Parameters
    ----------
        proj_folder: (path)
            folder containing the project specification files `project.json`,
            `structure.csv` and `customizations.csv`
        working_dir: (path)
            directory in which to store temporarily generated project files
        include_provenance: (bool)
            include hidden provenance information in project csv.
            Default: True
    """

    if working_dir is None:
        working_dir = tempfile.TemporaryDirectory(prefix='redcap_bridge_').name

    working_dir = pathlib.Path(working_dir)
    proj_folder = pathlib.Path(proj_folder)

    if not working_dir.exists():
        os.mkdir(working_dir)

    with open(proj_folder / 'project.json') as f:
        proj_conf = json.load(f)

    build_project(proj_folder / 'structure.csv', working_dir / 'build.csv',
                  include_provenance=include_provenance)
    customize_project(working_dir / 'build.csv',
                      proj_folder / 'customizations.csv',
                      output_file=working_dir / 'customized.csv')
    validate_project_against_template_parts(working_dir / 'customized.csv',
                                            *proj_conf['validation'])
    check_external_modules(proj_folder / 'project.json')

    upload_datadict(working_dir / 'customized.csv', proj_folder / 'project.json')
