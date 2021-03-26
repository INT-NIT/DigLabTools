import pathlib
import json
import pandas as pd
import numpy as np
from redcap_bridge.project_validation import validate_project_against_template_parts
from redcap_bridge.utils import map_header_json_to_csv


def build_project(project_csv, output_file=None):
    """
    Build a complete RedCap Instrument CSV from a set of template_parts and a
    project csv file.

    Args:
        project_csv: (str)
            Filepath of the project csv file
        output_file: (str,None)
            Filepath of the resulting, complete project csv (with inserted
            template_parts. If None, the content is only returned and not saved.
            Default: None

    Returns:
        (list) list containing the lines of the complete project definition
        including the template content
    """
    output = []

    with open(project_csv) as f:
        project_dir = pathlib.Path(project_csv).parent
        for line in f.readlines():
            # if line only contains reference then include reference here
            if line[0] == '{' and line[-2:] == '}\n' and not (',' in line):
                include_file = (project_dir / pathlib.Path(line[1:-2])).resolve()

                if not include_file.exists():
                    raise ValueError(f'Can not build project {project_csv}. '
                                     f'Included template {include_file} does '
                                     f'not exist')

                with open(include_file, 'r') as f_include:
                    header = f_include.readline()
                    if header != output[0]:
                        raise ValueError('Project csv and template do not share'
                                         'the same header. Compare '
                                         f'{project_csv} and {include_file}')

                    output.extend(f_include.readlines())
            else:
                output.append(line)

    if output_file:
        with open(output_file, 'w') as f:
            f.writelines(output)

    return output


def customize_project(project_built_csv, customization_csv, output_file=None):
    """
    Fill in a built project csv with project specific customizations.

    This can be used to e.g. change the default values of fields or customize
    the list of experimenters to be selected

    Args:
        project_built_csv: (str)
            The filepath to the csv containing the built project
            (see also `build_project`)
        customization_csv: (str)
            The filepath to the csv containing the project
            customizations
        output_file: (str)
            The path to save the combined csv. Default: None

    Returns:
        (dataframe) pandas dataframe csv representation of the customized
            project definition
    """

    # Loading project and customization data
    project_df = pd.read_csv(project_built_csv, dtype=str)
    project_df.index = project_df['Variable / Field Name']
    customization_df = pd.read_csv(customization_csv, dtype=str)
    customization_df.index = customization_df['Variable / Field Name']

    # Utility functions for combining dataframes and series
    def combine_values(value1, value2):
        """
        Combine values by overwriting `na` with data if possible.

        Raises:
            ValueError if value1 and value2 contain contradicting data
        """
        # return value if identical or both not available
        if value1 == value2 or (pd.isna(value1) and pd.isna(value2)):
            return value1
        elif pd.isna(value1) and not pd.isna(value2):
            return value2
        elif not pd.isna(value1) and pd.isna(value2):
            return value1
        else:
            raise ValueError(f'Can not merge contradicting entries {value1} '
                             f'and {value2}')

    combine_series = lambda x, y: x.combine(y, func=combine_values)

    # combine project and customization
    combined_df = project_df.combine(customization_df, combine_series)

    # restore the original order of columns and rows
    combined_df = combined_df.reindex(columns=project_df.columns,
                                      index=project_df.index)

    if output_file is not None:
        combined_df.to_csv(output_file, index=False)

    return combined_df

def extract_customization(project_csv, custom_csv, *template_csvs):
    """
    Extract custom parts of a project data dict by subtracting template parts

    Args:
        project_csv:
        custom_csv:
        *template_csvs:

    Returns:

    """

    # ensure the project csv is compatible with the templates
    validate_project_against_template_parts(project_csv, *template_csvs)

    custom_df = pd.read_csv(project_csv, dtype=str)
    custom_df = custom_df.rename(columns=map_header_json_to_csv)
    custom_df.index = custom_df['Variable / Field Name']
    custom_df.drop('Variable / Field Name', axis=1, inplace=True)

    for template_csv in template_csvs:
        template_df = pd.read_csv(template_csv, dtype=str)
        template_df.index = template_df['Variable / Field Name']
        template_df.drop('Variable / Field Name', axis=1, inplace=True)

        mask = ~ template_df.isna()
        custom_df[mask] = np.nan
        # keep variable / field name column entries

    # remove rows and columns that don't contain custom infos
    custom_df.dropna(axis=0, how='all', inplace=True)
    custom_df.dropna(axis=1, how='all', inplace=True)

    # save the resulting customization csv
    if custom_csv is not None:
        custom_df.to_csv(custom_csv, index=False)


if __name__ == '__main__':
    # TODO: This should go into tests


    print('Running V4A project build, customization and validation')
    build_project('../projects/V4A/V4A_structure.csv', 'tmp_V4A.csv')
    customize_project('tmp_V4A.csv', '../projects/V4A/V4A_customizations.csv',
                      output_file='tmp_V4A_custom.csv')

    from redcap_bridge.project_validation import validate_project_against_template_parts
    validate_project_against_template_parts('tmp_V4A_custom.csv', '../template_parts/general.csv', '../template_parts/eyelink.csv', '../template_parts/kinarm.csv')


    import redcap
    # TODO: use server_interface functions for this
    print('Download project csv and extract customized fields')
    server_config = json.load(open(
        '../../RedCap_forms_sandbox/projects/V4A/redcap_server_config.json',
                                   'r'))
    redproj = redcap.Project(server_config['api_url'],
                             server_config['api_token'])
    proj_string = redproj.export_metadata(format='csv')
    with open('tmp_V4A_downloaded.csv', 'w') as f:
        f.write(proj_string)

    proj_conf_path = '../../RedCap_forms_sandbox/projects/V4A/V4A.json'
    proj_conf = json.load(open(proj_conf_path, 'r'))
    template_csvs = proj_conf['validation']
    template_csvs = [(pathlib.Path(proj_conf_path).parent / template_csv).resolve()
                     for template_csv in template_csvs]

    extract_customization('tmp_V4A_downloaded.csv',
                          'tmp_V4A_extracted_customization.csv',
                          *template_csvs)

