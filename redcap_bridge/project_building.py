import pathlib

import numpy as np
import pandas as pd

import redcap_bridge
from redcap_bridge.project_validation import \
    validate_project_against_template_parts
from redcap_bridge.utils import map_header_json_to_csv

template_dir = pathlib.Path(redcap_bridge.__file__).parent / 'template_parts'


    Parameters
    ----------
    project_csv: str
        Filepath of the project csv file
    
    output_file: str ,None
        Filepath of the resulting, complete project csv (with inserted
        template_parts. If None, the content is only returned and not saved.
        Default: None

    Returns
    -------
    list
        list containing the lines of the complete project definition
        including the template content
            template_parts. If None, the content is only returned and not saved.
            Default: None

    Returns
    -------
        (list) list containing the lines of the complete project definition
        including the template content
    """
    output = []

    if isinstance(project_csv, str):
        project_csv = pathlib.Path(project_csv)

    with open(project_csv) as f:
        for line in f.readlines():
            # if line only contains reference then include reference here
            if line[0] == '{' and line[-2:] == '}\n' and not (',' in line):
                template_name = pathlib.Path(line[1:-2]).with_suffix('.csv')
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

    if output_file:
        with open(output_file, 'w') as f:
            f.writelines(output)
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
        project_built_csv: (str)
            The filepath to the csv containing the built project
            (see also `build_project`)
        customization_csv: (str)
            The filepath to the csv containing the project
            customizations
        output_file: (str)
            The path to save the combined csv. Default: None

    Returns
    -------
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

   Parameters
   ----------
   project_csv:
   custom_csv:
   *template_csvs:

   Returns
   ----------

    return combined_df


def extract_customization(project_csv, export_custom_csv, *template_parts):
    """
    Extract custom parts of a project data dict by subtracting template parts

    Parameters
    ----------
        project_csv: (path)
            of complete project csv file
        export_custom_csv: (path)
            to store the resulting customization csv file
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
