from redcap_bridge.server_elab_interface import (create_template_without_metadata, create_template_with_metadata,
                                                 create_template_with_converted_csv)
from redcap_bridge.test_redcap.test_utils import (test_directory, initialize_test_dir)

SERVER_CONFIG_YAML = (test_directory / 'testfiles' / 'TestProject' / 'elab_config.json').resolve()

test_file = (test_directory / 'testfiles' / 'elabConversion' / 'csvRecord.csv')


def test_create_template_without_metadata(initialize_test_dir):
    template_file = test_directory / 'testfiles' / 'elab_template.json'

    res = create_template_without_metadata(server_config_json=SERVER_CONFIG_YAML, template_file=template_file)

    assert res is not None


def test_create_template_with_metadata(initialize_test_dir):
    template_file = test_directory / 'testfiles' / 'elab_template.json'

    res = create_template_with_metadata(server_config_json=SERVER_CONFIG_YAML, template_file=template_file)

    assert res is not None


def test_create_template_with_converted_csv(initialize_test_dir):
    csv_file = test_directory / 'testfiles' / 'metadata.csv'


    res = create_template_with_converted_csv(server_config_json=SERVER_CONFIG_YAML, csv_file=csv_file,
                                             title='AUTO CSV')

    assert res is not None
