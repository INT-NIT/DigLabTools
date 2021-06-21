import pathlib
import json
import tempfile

from redcap_bridge.project_building import build_project, customize_project
from redcap_bridge.project_validation import validate_project_against_template_parts
from redcap_bridge.server_interface import upload_datadict, download_records

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
        working_dir = tempfile.tempdir().name
    working_dir = pathlib.Path(working_dir)
    proj_folder = pathlib.Path(proj_folder)

    with open(proj_folder / 'project.json') as f:
        proj_conf = json.load(f)

    build_project(proj_folder / 'structure.csv', working_dir / 'build.csv',
                  include_provenance=include_provenance)
    customize_project(working_dir / 'build.csv',
                      proj_folder / 'customizations.csv',
                      output_file=working_dir / 'customized.csv')
    validate_project_against_template_parts(working_dir / 'customized.csv',
                                            *proj_conf['validation'])

    upload_datadict(working_dir / 'customized.csv',
                    proj_folder / 'project.json')