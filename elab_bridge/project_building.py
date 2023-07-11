import pathlib
import json
import warnings

import elab_bridge
from elab_bridge.project_validation import \
    validate_project_against_template_parts
from diglab_utils.provenance import get_repo_state

elab_bridge_dir = pathlib.Path(elab_bridge.__file__).parent
template_dir = elab_bridge_dir / 'template_parts'


def _extend_extra_fields_groups(group_list, group_list_to_add):
    """
    Extend a group list by another group list while ensuring non-overlapping
    group ids.

    Parameters
    ----------
    group_list: list
        The group list to extend
    group_list_to_add: list
        The list of groups to be added

    Returns
    -------
        (dict) Mapping of previous to new group ids for the added groups
    """

    def current_group_ids():
        return [int(g['id']) for g in group_list]

    id_map = {}
    for group_to_add in group_list_to_add:
        if group_to_add['id'] not in current_group_ids():
            pass
        else:  # conflicting group id detected, assigning new id
            new_id = max(current_group_ids())+1
            id_map[group_to_add['id']] = new_id
            # update group id to be sequential
            group_to_add['id'] = new_id
            group_list.append(group_to_add)

    return id_map


def _extend_extra_fields(extra_fields, extra_fields_to_add, group_id_map):
    """
    Extend a dict of extra_fields by another dict of extra_fields while ensuring non-overlapping
    group ids by mapping the group_ids of the added fields with a group_id_map

    Parameters
    ----------
    extra_fields: dict
        The dict of extra_fields to extend
    extra_fields_to_add: dict
        The dict of extra_fields to be added
    group_id_map: dict
        The dictionary mapping the to be added group ids to non-overlapping ids wrt the
        extra_fields to be extended
    """

    overlapping_keys = set(extra_fields).intersection(extra_fields_to_add)
    if overlapping_keys:
        raise ValueError(f'Overlapping keys detected: {overlapping_keys}')

    # update group_ids of groups to be added
    for extra_field in extra_fields_to_add:
        if 'group_id' in extra_field:
            extra_field['group_id'] = group_id_map[extra_field['group_id']]

    extra_fields.update(extra_fields_to_add)


def _extend_extra_field(extra_field, extra_field_to_add):
    """
    Extend an extra field dictionary with additional data
    """
    protected_attributes = {'group_id', 'type'}

    if protected_attributes.issubset(extra_field_to_add.keys()):
        raise ValueError(f'Can not overwrite protected attributes: {protected_attributes}')

    for key, value in extra_field_to_add.items():
        if key not in extra_field:
            extra_field[key] = value
        elif key == 'options':  # options are lists and need to be handled separately
            if not isinstance(value, list):
                value = list(value)
            if extra_field[key] != []:
                warnings.warn(f'Not overwriting non-empty options {extra_field[key]} by {value}')
            else:
                extra_field[key] = value
        else:
            extra_field[key] = value


def build_project(project_file, output_file=None, include_provenance=True):
    """
    Build a complete ElabFTW form from a set of template_parts and a
    project json file.

    Parameters
    ----------
    project_file: str
        Filepath of the project structure json file
    
    output_file: str, None
        Filepath of the resulting, complete project json (with inserted
        template_parts. If None, the content is only returned and not saved.
        Default: None

    include_provenance: bool
        If True, include hidden fields in the project json that contain
        git commits of source files
        Default: True

    Returns
    -------
        (dict) json dictionary of the project
    """

    if isinstance(project_file, str):
        project_file = pathlib.Path(project_file)

    with open(project_file, 'r') as f:
        form = json.load(f)

        assert 'elabftw' in form

        if 'extra_fields' not in form:
            form['extra_fields'] = {}
        if 'extra_fields_groups' not in form['elabftw']:
            form['elabftw']['extra_fields_groups'] = []

        include_templates = {}
        # include templates if specified
        if 'include_templates' in form:
            include_templates = form.pop('include_templates')
            for template_name in include_templates:
                template_filename = (template_dir / template_name).with_suffix('.json')
                if not template_filename.exists():
                    raise ValueError(f'Template {template_filename} not found')
                with open(template_filename, 'r') as t:
                    template = json.load(t)

                group_id_map = _extend_extra_fields_groups(
                    form['elabftw']['extra_fields_groups'],
                    template['elabftw']['extra_fields_groups']
                )

                _extend_extra_fields(form['extra_fields'], template['extra_fields'], group_id_map)
    # Print of templates used
    if include_templates:
        print(f"Used templates: {include_templates}")

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(form, f)
    else:
        return form


def customize_project(project_built_json, customization_json, output_file=None):
    """
    Fill in a built project json with project specific customizations.

    This can be used to e.g. change the default values of fields or customize
    the list of experimenters to be selected

    Parameters
    ----------
    project_built_json: str
        The filepath to the json containing the built project (see also `build_project`)
    customization_json: str
        The filepath to the json containing the project customizations
    output_file: str
        The path to save the combined json. Default: None

    Returns
    -------
    dict
        dict json representation of the customized project definition
    """

    # Loading project and customization data
    with open(project_built_json, 'r') as f:
        form = json.load(f)

        assert 'elabftw' in form
        assert 'extra_fields' in form

    with open(customization_json, 'r') as c:
        customization = json.load(c)

    if 'extra_fields' in customization:
        customization = customization['extra_fields']

    for field_name, field_content in customization.items():
        if field_name not in form['extra_fields']:
            warnings.warn('Customization is adding a new field to the form: '
                          f' {field_name}: {field_content}')
            form['extra_fields'][field_name] = field_content
        else:
            _extend_extra_field(form['extra_fields'][field_name], field_content)

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(form, f)
    else:
        return form


def extract_customization(project_json, export_custom_json, *template_parts):
    """
    Extract custom parts of a project data dict by subtracting template parts

    Parameters
    ----------
        project_json: path
            path to the complete project json file
        export_custom_json: path
            path to store the resulting customization json file
        *template_parts: (list)
            list of template parts included in the project

    Returns
    -------

    """

    raise NotImplementedError()

    # # ensure the project json is compatible with the templates
    # validate_project_against_template_parts(project_json, *template_parts)
    #
    # custom_df = pd.read_json(project_json, dtype=str)
    # custom_df = custom_df.rename(columns=map_header_json_to_json)
    # custom_df.index = custom_df['Variable / Field Name']
    # custom_df.drop('Variable / Field Name', axis=1, inplace=True)
    #
    # for template_part in template_parts:
    #     template_path = (template_dir / template_part).with_suffix('.json')
    #     template_df = pd.read_json(template_path, dtype=str)
    #     template_df.index = template_df['Variable / Field Name']
    #     template_df.drop('Variable / Field Name', axis=1, inplace=True)
    #
    #     mask = ~ template_df.isna()
    #     custom_df[mask] = np.nan
    #     # keep variable / field name column entries
    #
    # # remove custom structural fields (from structure.json)
    # mask = ((custom_df['Form Name'].isna()) & (custom_df['Field Type'].isna()) &
    #         (custom_df['Field Label'].isna()))
    # custom_df = custom_df.loc[mask]
    #
    # # remove rows and columns that don't contain custom infos
    # custom_df.dropna(axis=0, how='all', inplace=True)
    # custom_df.dropna(axis=1, how='all', inplace=True)
    #
    # # save the resulting customization json
    # if export_custom_json is not None:
    #     custom_df.to_json(export_custom_json, index=True)


if __name__ == '__main__':
    pass
