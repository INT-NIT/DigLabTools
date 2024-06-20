from pathlib import Path
import elab_bridge
import json
from elab_bridge import server_interface

from diglab_utils.test_utils import (test_directory, initialize_test_dir)

project_dir = test_directory / 'test files_elab' / 'TestProject'
SERVER_CONFIG_YAML = ('/home/pourtoi/PycharmProjects/DigLabTools/elab_bridge/tests/testfiles_elab/TestProject/project'
                      '.json')


def main():
    save_to = '/home/pourtoi/Bureau/Nouveau dossier/BEP/Test/fichier.csv'

    df = elab_bridge.server_interface.download_experiment(save_to, SERVER_CONFIG_YAML, 247, format='csv')
    print(df)
    output_file = '/home/pourtoi/Bureau/Nouveau dossier/BEP/Test/json_output.json'
    with open(output_file, 'w') as output_file:
        json.dump(df, output_file, indent=4)


if __name__ == "__main__":
    main()
