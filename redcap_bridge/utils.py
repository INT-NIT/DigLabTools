import pandas as pd
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
