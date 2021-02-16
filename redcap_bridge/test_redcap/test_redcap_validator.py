import pathlib
from redcap_bridge.redcap_validator import load_template, load_records, validate


def test_load_template():
    testfile = pathlib.Path('./testfiles/Diglabform_2021-02-15_1731.zip')
    template = load_template(testfile)

    assert not testfile.with_suffix('').exists()

    mandatory_columns = ['Variable / Field Name', 'Form Name', 'Section Header',
                         'Field Type', 'Field Label',
                         'Choices, Calculations, OR Slider Labels',
                         'Field Note',
                         'Text Validation Type OR Show Slider Number',
                         'Text Validation Min', 'Text Validation Max',
                         'Identifier?',
                         'Branching Logic (Show field only if...)',
                         'Required Field?', 'Custom Alignment',
                         'Question Number (surveys only)', 'Matrix Group Name',
                         'Matrix Ranking?', 'Field Annotation']

    for mandatory_column in mandatory_columns:
        assert mandatory_column in template

    mandatory_vars = ['record_id', 'diglab', 'diglab_version',
                      'redcap_form_version']

    for mandatory_var in mandatory_vars:
        assert mandatory_var in template['Variable / Field Name'].values


def test_load_records():
    # NOTE: This test might fail due to connection issues to the server.
    # Ensure to use either lan or wireless connection, but not both at the
    # same time.
    data = load_records()

    assert data is not None


def test_validate():
    records = load_records()
    template = load_template('testfiles/Diglabform_2021-02-15_1731.zip')
    validate(template, records)
