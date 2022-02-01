import pathlib

import warnings

import numpy as np
import pandas as pd

import redcap_bridge
from redcap_bridge.project_validation import \
    validate_project_against_template_parts
from redcap_bridge.utils import map_header_json_to_csv, get_repo_state

redcap_bridge_dir = pathlib.Path(redcap_bridge.__file__).parent
template_dir = redcap_bridge_dir / 'template_parts'


def build_project(project_csv, output_file=None, include_provenance=True):
    """
    Build a complete RedCap Instrument CSV from a set of template_parts and a
    project csv file.

    Parameters
    ----------
    project_csv: str
        Filepath of the project csv file
    
    output_file: str, None
        Filepath of the resulting, complete project csv (with inserted
        template_parts. If None, the content is only returned and not saved.
        Default: None

    include_provenance: bool
        If True, include hidden fields in the project csv that contain
        git commits of source files
        Default: True

    Returns
    -------
        (list) list containing the lines of the complete project definition
        including the template content
    """
    output = []
    used_template = []
    if isinstance(project_csv, str):
        project_csv = pathlib.Path(project_csv)

    with open(project_csv) as f:
        for line in f.readlines():
            # if line only contains reference then include reference here
            if line[0] == '{' and line.replace(',', '')[-2:] == '}\n':
                cleaned_line = line.replace(',', '')
                template_name = pathlib.Path(cleaned_line[1:-2]).with_suffix('.csv')
                used_template.append(template_name)
                include_file = (template_dir / template_name).resolve()

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

        if include_provenance:

            # collect provenance infos
            diglabtools_hash, diglabtools_state = get_repo_state(redcap_bridge_dir.parent)
            diglabtools_version = open(redcap_bridge_dir.parent / 'VERSION').read()
            project_conf_repo_hash, project_conf_repo_state = get_repo_state(project_csv)

            if not diglabtools_state:
                warnings.warn('DigLabTools repository is in non-clean state.')
            if project_conf_repo_state is None:
                warnings.warn('Project configuration is not part of a version control repository.')
            elif not project_conf_repo_state:
                warnings.warn('Project configuration repository is in non-clean state.')

            # adding hidden rows to capture provenance info
            include_file = template_dir / '_provenance.csv'
            with open(include_file, 'r') as f_include:
                header = f_include.readline()
                if header != output[0]:
                    raise ValueError('Project csv and template do not share'
                                     'the same header. Compare '
                                     f'{project_csv} and {include_file}')

                for l in f_include.readlines():
                    complete_line = l.format(diglabtools_hash=diglabtools_hash,
                                             diglabtools_version=diglabtools_version,
                                             redcap_forms_hash=project_conf_repo_hash)
                    output.append(complete_line)

    if output_file:
        with open(output_file, 'w') as f:
            f.writelines(output)
    # Print of templates used and total number of fields
    print(f"\nUsed template: ", end='')
    for template in used_template:
        print(f"{template} ", end='')
    print(f"with total of : {len(output)} fields", end='')

    return output


def customize_project(project_built_csv, customization_csv, output_file=None):
    """
    Fill in a built project csv with project specific customizations.

    This can be used to e.g. change the default values of fields or customize
    the list of experimenters to be selected

    Parameters
    ----------
    project_built_csv: str
        The filepath to the csv containing the built project (see also `build_project`)
    customization_csv: str
        The filepath to the csv containing the project customizations
    output_file: str
        The path to save the combined csv. Default: None

    Returns
    -------
    dataframe
        pandas dataframe csv representation of the customized project definition
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

    # print number of customizing field
    print(f"\nCustomizing: {len(customization_df)} fields\n", end='')

    # print the field name
    print(f"The following fields were customized:")
    if(len(customization_df)) < 10:
        print(f"{customization_df['Variable / Field Name'].to_csv(index=False)} ", end='')
    else:
        print(f"{customization_df['Variable / Field Name'].values}")

    return combined_df


def extract_customization(project_csv, export_custom_csv, *template_parts):
    """
    Extract custom parts of a project data dict by subtracting template parts

    Parameters
    ----------
        project_csv: path
            path to the complete project csv file
        export_custom_csv: path
            path to store the resulting customization csv file
        *template_parts: (list)
            list of template parts included in the project

    Returns
    -------

    """

    # ensure the project csv is compatible with the templates
    validate_project_against_template_parts(project_csv, *template_parts)

    custom_df = pd.read_csv(project_csv, dtype=str)
    custom_df = custom_df.rename(columns=map_header_json_to_csv)
    custom_df.index = custom_df['Variable / Field Name']
    custom_df.drop('Variable / Field Name', axis=1, inplace=True)

    for template_part in template_parts:
        template_path = (template_dir / template_part).with_suffix('.csv')
        template_df = pd.read_csv(template_path, dtype=str)
        template_df.index = template_df['Variable / Field Name']
        template_df.drop('Variable / Field Name', axis=1, inplace=True)

        mask = ~ template_df.isna()
        custom_df[mask] = np.nan
        # keep variable / field name column entries

    # remove custom structural fields (from structure.csv)
    mask = ((custom_df['Form Name'].isna()) & (custom_df['Field Type'].isna()) &
            (custom_df['Field Label'].isna()))
    custom_df = custom_df.loc[mask]

    # remove rows and columns that don't contain custom infos
    custom_df.dropna(axis=0, how='all', inplace=True)
    custom_df.dropna(axis=1, how='all', inplace=True)

    # save the resulting customization csv
    if export_custom_csv is not None:
        custom_df.to_csv(export_custom_csv, index=True)


if __name__ == '__main__':
    pass
