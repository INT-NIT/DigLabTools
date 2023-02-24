import pytest


from redcap_bridge.server_elab_interface import (get_elab_config, create_template_without_metadata)


json_file = "/Users/killianrochet/PycharmProjects/DigLabTools/redcap_bridge/test_redcap/testfiles/TestProject/template.json"

elab_config = "/Users/killianrochet/PycharmProjects/DigLabTools/redcap_bridge/test_redcap/testfiles/TestProject/elab_config.json"

def test_create_template_without_metadata():

    res = create_template_without_metadata(server_config_json=elab_config, template_file=json_file)

    assert res is not None

