import os
import pathlib
import json
import tempfile

from elab_bridge.project_building import build_project, customize_project
from elab_bridge.project_validation import validate_project_against_template_parts
from elab_bridge.server_interface import upload_template


def setup_project(proj_folder, working_dir=None, include_provenance=True):
    """
    Build a project json from its specifications and setup on the server

    Parameters
    ----------
        proj_folder: (path)
            folder containing the project specification files `project.json`,
            `structure.json` and `customizations.json`
        working_dir: (path)
            directory in which to store temporarily generated project files
        include_provenance: (bool)
            include hidden provenance information in project json.
            Default: True
    """

    if working_dir is None:
        working_dir = tempfile.TemporaryDirectory(prefix='elab_bridge_').name

    working_dir = pathlib.Path(working_dir)
    proj_folder = pathlib.Path(proj_folder)

    if not working_dir.exists():
        os.mkdir(working_dir)

    with open(proj_folder / 'project.json') as f:
        proj_conf = json.load(f)

    project_title = proj_conf.get('title', 'Unknown Project')

    build_project(proj_folder / 'structure.json', working_dir / 'build.json',
                  include_provenance=include_provenance)
    customize_project(working_dir / 'build.json',
                      proj_folder / 'customizations.json',
                      output_file=working_dir / 'customized.json')
    validate_project_against_template_parts(working_dir / 'customized.json',
                                            *proj_conf['validation'])

    upload_template(working_dir / 'customized.json', proj_folder / 'project.json', project_title)
