from pathlib import Path
import elab_bridge
import json
from elab_bridge import server_interface
from Generator import Generator

from diglab_utils.test_utils import (test_directory, initialize_test_dir)

project_dir = test_directory / 'test files_elab' / 'TestProject'
SERVER_CONFIG_YAML = ('/home/pourtoi/PycharmProjects/DigLabTools/elab_bridge/tests/testfiles_elab/TestProject/project'
                      '.json')

import os


def main():
    output = input("Entrez le chemin du dossier de sortie : ")

    csv_file = os.path.join(output, 'fichier.csv')

    df = elab_bridge.server_interface.download_experiment(csv_file, SERVER_CONFIG_YAML, 247, format='csv')
    print(df)

    json_output_file_abs = os.path.join(output, 'fichier.json')

    with open(json_output_file_abs, 'w') as json_output_file:
        json.dump(df, json_output_file, indent=4)


if __name__ == "__main__":
    main()
