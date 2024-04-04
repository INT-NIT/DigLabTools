from pathlib import Path

from pandas import read_csv

import elab_bridge
import json
from elab_bridge import server_interface
from Generator import Generator
import os

from diglab_utils.test_utils import (test_directory, initialize_test_dir)

project_dir = test_directory / 'test files_elab' / 'TestProject'
SERVER_CONFIG_YAML = ('/home/pourtoi/PycharmProjects/DigLabTools/elab_bridge/tests/testfiles_elab/TestProject/project'
                      '.json')


def main():
    output = input(
        "Entrez le chemin du dossier de sortie : ex : /home/pourtoi/PycharmProjects/DigLabTools/bep32v01/Essaie")

    csv_file = os.path.join(output, 'fichier.csv')

    jsonformat = elab_bridge.server_interface.download_experiment(csv_file, SERVER_CONFIG_YAML, 247, format='csv')
    df = read_csv(csv_file)
    print(df)
    print(df['id'][0])

    generator = Generator(output, df['id'][0], df['session_id'][0], "micr")


if __name__ == "__main__":
    main()
