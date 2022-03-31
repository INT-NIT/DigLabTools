import redcap_bridge
from redcap_bridge.server_interface import download_project_settings
from pathlib import Path


def check_connectivity():
    print(f'RCB location: {Path(redcap_bridge.__file__).parent}')
    test_project = Path(redcap_bridge.__file__).parent / 'test_redcap' / 'testfiles' / 'TestProject' / 'project.json'

    res = download_project_settings(test_project)
    if not res['project_id']:
        raise ValueError('Unsuccessful download')


if __name__ == '__main__':
    check_connectivity()
