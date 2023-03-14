from redcap_bridge.server_elab_interface import (create_template_without_metadata, create_template_with_metadata)
from redcap_bridge.test_redcap.test_utils import (test_directory, initialize_test_dir)

SERVER_CONFIG_YAML = (test_directory / 'testfiles' / 'TestProject' / 'elab_config.json').resolve()


def test_create_template_without_metadata(initialize_test_dir):
    template_file = test_directory / 'testfiles' / 'elab_template.json'

    res = create_template_without_metadata(server_config_json=SERVER_CONFIG_YAML, template_file=template_file)

    assert res is not None


def test_create_template_with_metadata(initialize_test_dir):
    template_file = test_directory / 'testfiles' / 'elab_template.json'

    res = create_template_with_metadata(server_config_json=SERVER_CONFIG_YAML, template_file=template_file)

    assert res is not None
