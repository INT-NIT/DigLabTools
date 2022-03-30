import redcap_bridge.server_interface as si
from pathlib import Path


def check_connectivity():
    test_project = Path(si.__file__).parent / 'test_redcap' / 'testfiles' / 'TestProject' / 'project.json'

    res = si.download_project_settings(test_project)
    if not res['project_id']:
        raise ValueError('Unsuccessful download')


if __name__ == '__main__':
    check_connectivity()
