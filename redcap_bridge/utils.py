import git
import pathlib
import pandas as pd
import re as re

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


def compressed_record(csv_file, compressed_file=None):
    custom_csv = pd.read_csv(csv_file)
    df = pd.DataFrame(custom_csv)
    compressed_file = df.filter(regex='.___.')
    compressed_file.replace(0,'', inplace=True)
    for column in compressed_file:
        if 1 in compressed_file[column].values:
            style_moda = re.search('___(.+?)', column).group(1)
            compressed_file[column].replace(1, style_moda, inplace=True)
        else:
            compressed_file.pop(column)
    list_column = compressed_file.columns.tolist()

    for i, item in enumerate(list_column):
        name = re.search('(.+?)___', item).group(1)
        if i != 0:
            get_previous = list_column[i-1]
            if name in item and name in get_previous:
                compressed_file[name] = compressed_file[[name, item]].agg(','.join, axis=1)
                compressed_file.pop(item)
            else:
                compressed_file[name] = compressed_file[[item]].agg(','.join, axis=1)
                compressed_file.pop(item)
        else:
            compressed_file[name] = compressed_file[[item]].agg(''.join, axis=1)
            compressed_file.pop(item)

    print(compressed_file)

    compressed_file.to_csv('test.csv', index=False)
    return compressed_file
