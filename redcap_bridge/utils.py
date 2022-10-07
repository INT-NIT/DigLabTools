import git
import pathlib
import pandas as pd
import re as re
import warnings

# TODO: This can be extracted via the RedCap API
header_json = ['field_name', 'form_name', 'section_header', 'field_type',
               'field_label', 'select_choices_or_calculations', 'field_note',
               'text_validation_type_or_show_slider_number',
               'text_validation_min', 'text_validation_max', 'identifier',
               'branching_logic', 'required_field', 'custom_alignment',
               'question_number', 'matrix_group_name', 'matrix_ranking',
               'field_annotation']
header_csv = ['Variable / Field Name', 'Form Name', 'Section Header',
              'Field Type', 'Field Label',
              'Choices, Calculations, OR Slider Labels', 'Field Note',
              'Text Validation Type OR Show Slider Number',
              'Text Validation Min', 'Text Validation Max', 'Identifier?',
              'Branching Logic (Show field only if...)', 'Required Field?',
              'Custom Alignment', 'Question Number (surveys only)',
              'Matrix Group Name', 'Matrix Ranking?', 'Field Annotation']

map_header_json_to_csv = {json: csv for json, csv in zip(header_json,
                                                         header_csv)}
map_header_csv_to_json = {csv: json for csv, json in zip(header_csv,
                                                         header_json)}


def get_repo_state(path):
    """
    Extract the latest commit hash of a git repository

    Args:
        path: Path to the git repository

    Returns:
        2-tuple (str, bool)
            latest commit id
            repo status: True if repository is in a clean state

    Raises:
        ValueError: if path is not part of a git repository
    """

    repo_root = None
    # find repository root folder
    path = pathlib.Path(path)
    for parent in [path] + list(path.parents):
        if (parent / '.git').exists():
            repo_root = parent
            break

    if repo_root is None:
        return '', None

    repo = git.Repo.init(str(repo_root))
    clean = not repo.is_dirty()
    try:
        commit_hash = repo.head.commit.hexsha
    except ValueError as e:
        commit_hash = ''
        clean = False

    return commit_hash, clean


def compress_record(csv_file, compressed_file=None):
    warnings.warn(f'Compressing {csv_file} does not preserve all original information.'
                  f'This operation is potentially irreversible.')

    df = pd.read_csv(csv_file, na_filter=False, dtype='str')

    # compressing embedded fields
    embedding_columns = df.filter(regex=r'.\(choice=.*\{.*\}\)').columns
    embedded_indexes = df.columns.get_indexer(embedding_columns)
    # ensure header of next columns are empty
    assert all([c.startswith('Unnamed: ') for c in df.columns[embedded_indexes + 1]])
    # copy values to embedded column
    df.iloc[:, embedded_indexes] = df.iloc[:, embedded_indexes + 1]
    # remove duplicate column
    df.drop(df.columns[embedded_indexes + 1], axis='columns', inplace=True)

    # utility function for merging multiple values as a string
    def merge_values(values):
        return ', '.join([v for v in values if v != ''])

    # merge multi-column fields
    names = set([c.split(' (choice=')[0] for c in df.filter(regex=r'. \(choice=.*\)').columns])
    for name in names:
        regex_compatible_name = name

        # avoid duplicate column names
        if name in df.columns:
            new_name = name + '_compressed'
            warnings.warn(f'Duplicate column name {name}. Creating new column with name '
                          f'{new_name} instead.')
            assert new_name not in df.columns
            name = new_name

        for special_char in '\\.^$*+?{}[]|()':
            regex_compatible_name = regex_compatible_name.replace(special_char, "\\" + special_char)
        sub_columns = df.filter(regex=rf'^{regex_compatible_name} \(choice=.').columns
        sub_indexes = df.columns.get_indexer(sub_columns)
        # insert column with merged columns
        df.insert(loc=int(sub_indexes[0]),
                  column=name,
                  value=df[sub_columns].agg(merge_values, axis=1))
        # remove sub-columns (that are now shifted by 1)
        df.drop(df.columns[sub_indexes + 1], axis='columns', inplace=True)

    if compressed_file is None:
        return df
    else:
        df.to_csv(compressed_file, index=False)


def remove_columns(csv_file, compressed_file=None):
    df = pd.read_csv(csv_file, na_filter=False, dtype='str')


def exportCSVtoXLS(csv_file, compressed_file=None):
    read_file = pd.read_csv(csv_file, na_filter=False, dtype='str')
    read_file.to_excel(r'Path', index=None, header=True)


def conversion_csv_to_json(csv_file):
    """
    Test conversion function
    """
    df = pd.read_csv(csv_file)
    df.to_json(
        r'/Users/killianrochet/PycharmProjects/DigLabTools/redcap_bridge/test_redcap/testfiles/elabConversion/pandaJsonConversion..json')
    json_df = pd.read_json(
        '/Users/killianrochet/PycharmProjects/DigLabTools/redcap_bridge/test_redcap/testfiles/elabConversion/pandaJsonConversion..json')
    for i in json_df.columns:
        for j in json_df.index:
            if json_df[i][j] == 'dropdown':
                json_df[i][j] = dropdown_to_json()
            elif json_df[i][j] == 'text':
                json_df[i][j] = text_to_json()
            elif json_df[i][j] == 'notes':
                json_df[i][j] = notes_to_json()
            elif re.search(r'@DEFAULT=.', str(json_df[i][j])):
                print(f"MATCH")
                json_df[i][j] = default_value_to_json()
            else:
                print(f"Other type")



def text_to_json():
    # text mean multiples types in json. Need to define all of them
    return 'number'


def dropdown_to_json():
    # dropdown is always select type in json
    return 'select'


def notes_to_json():
    # notes is always text type in json
    return 'text'

def default_value_to_json():
    return 'defaultValue'
