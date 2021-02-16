import pandas as pd
import zipfile
import pathlib
import shutil
import redcap
import json


def validate(template, record):
    """
    Validate a RedCap record against a template instrument

    Args:
        template: (dataframe) template structure of an instrument
        record: (dataframe) data of a single record

    Returns:
        True

    Raises:
        ValueError in case of failing validation
    """

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
            empty_record = record.loc[empty_record_mask]
            raise ValueError(
                f'records with {empty_record.index.name}='
                f'{empty_record.index.tolist()} do not contain data in '
                f'required field "{required_field}"')

    return True


def load_template(template_file):
    """
    Load template structure of an instrument

    Args:
        template_file: (str) zip filename of the template are stored
        instrument: (str) name of the instrument to load

    Returns:
        (dataframe): structure of the instrument template
    """

    template_file = pathlib.Path(template_file)

    # unzipping template file
    shutil.rmtree(template_file.with_suffix(''), ignore_errors=True)
    with zipfile.ZipFile(template_file, 'r') as zip_ref:
        zip_ref.extractall(template_file.with_suffix(''))

    instrument_filename = template_file.with_suffix('').joinpath(
        'instrument.csv')

    df = pd.read_csv(instrument_filename)

    # remove temporary unzipped folder
    shutil.rmtree(template_file.with_suffix(''))

    return df


def load_records():
    """
    Load data of a record

    Returns:

    """

    # load config
    dir = pathlib.Path(__file__).parent.absolute()
    with open(dir.joinpath('config.yaml')) as f:
        config = json.load(f)

    assert 'api_token' in config
    assert 'api_url' in config

    redproj = redcap.Project(config['api_url'], config['api_token'])
    data = redproj.export_records(format='df')

    return data


if __name__ == '__main__':
    records = load_records()
    template = load_template()
    for record in records:
        validate(template, record)
