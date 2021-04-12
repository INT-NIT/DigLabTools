import pathlib

import pandas as pd

import redcap_bridge
from redcap_bridge.utils import map_header_json_to_csv

index_column_header = 'Variable / Field Name'

template_dir = pathlib.Path(redcap_bridge.__file__).parent / 'template_parts'


def validate_project_against_template_parts(project, *templates):
    """
    Validate a built project csv
    Args:
        project: (str, buffer)
            Filepath of the csv file or csv buffer of the built project
        templates: (str, list)
            List of names of template parts to validate against.

    Returns:
        (bool): True if the validation was successful
    """

    df_project = pd.read_csv(project)
    # unify column names to conform to csv style
    df_project = df_project.rename(columns=map_header_json_to_csv)
    df_project.index = df_project[index_column_header]
    dfs_templates = []

    if not templates:
        raise ValueError(
            'No template_parts to validate against were specified.')

    for template in templates:
        df_template = pd.read_csv((template_dir / template).with_suffix('.csv'))
        df_template.index = df_template[index_column_header]
        dfs_templates.append(df_template)

    # compare content of template_parts and project
    for template_df in dfs_templates:
        if not all(template_df.columns == df_project.columns):
            raise ValueError(f'Incompatible columns in project '
                             f'({project.columns}) and template '
                             f'({template_df.columns})')

        for i in template_df.index:
            if i not in df_project.index:
                raise ValueError(f'Row {i} is missing in project csv')

            # compare entries of the row and exclude `na` entries
            na_values = template_df.loc[i].isna()
            equal_entries = df_project.loc[i] == template_df.loc[i]
            if not (equal_entries | na_values).all():
                raise ValueError(f'Row {i} is differs between project csv and '
                                 f'template')

    print('Validation successful')
    return True


def validate_record_against_template(record_csv, template_csv):
   Parameters
   ----------
   template: dataframe
       template structure of an instrument
   record: dataframe
       data of a single record

    Returns
    ----------
     True

    Raises
    ----------
    ValueError in case of failing validation

    Returns
    -------
        True

    Raises:
        ValueError in case of failing validation
    """

    template = pd.read_csv(template_csv)
    record = pd.read_csv(record_csv)

    assert 'Variable / Field Name' in template

    # remove 'record_id' as it is unique to template
    template = template.loc[template['Variable / Field Name'] != 'record_id']

    # Step 1: Assert all fields are preserved
    type_groups = template.groupby(template['Field Type'])
    for group_type in type_groups.groups:

        # check if all options are present for checkbox fields
        if group_type == 'checkbox':
            df_checkboxes = type_groups.get_group(group_type)
            # reduce to only relevant columns
            df_checkboxes = df_checkboxes[['Variable / Field Name',
                                           'Choices, Calculations, OR Slider Labels']]
            for field_name, choices in df_checkboxes.values:
                choice_ids = [c.split(',')[0] for c in choices.split('| ')]

                for cid in choice_ids:
                    if f'{field_name}___{cid}' not in record.columns.values:
                        raise ValueError(f'"{field_name}___{cid}" column '
                                         f'header is missing in record')

        # check that all non-descriptive fields are preserved
        elif group_type != 'descriptive':
            # check if editable field is present
            group_df = type_groups.get_group(group_type)
            for key in group_df['Variable / Field Name'].values:
                if key not in record.columns.values:
                    raise ValueError(
                        f'"{key}" column header is missing in record')

    # Step 2: Check that required fields contain data
    type_groups = template.groupby(template['Required Field?'])
    required_fields_df = type_groups.get_group('y')

    # ignore required 'checkbox' fields
    required_fields_df = required_fields_df.loc[
        required_fields_df['Field Type'] != 'checkbox']
    required_fields = required_fields_df['Variable / Field Name'].values

    for required_field in required_fields:
        empty_record_mask = record[required_field].isnull()
        if empty_record_mask.values.any():
    """
    Load template structure of an instrument

    Parameters
    ----------
    template_file: str 
        zip filename of the template are stored
    instrument: str 
        name of the instrument to load

    Returns
    ----------
    dataframe
        structure of the instrument template
if __name__ == '__main__':
    pass
