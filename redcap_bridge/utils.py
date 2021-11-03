import git
import pathlib

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