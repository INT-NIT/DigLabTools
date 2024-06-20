import json
import os
from BidsFilestructure import FileStructure


class CreatFile:
    def __init__(self, output_path):
        """
        Initialize a CreatFile object with the output path and initialize filestructure.

        Args:
            output_path (str): The path where files will be created.
        """
        self.output_path = output_path
        self.file_name = []
        self.filestructure = FileStructure()

    def create_empty_file(self, filename):
        """
        Create an empty file.

        Args:
            filename (str): The name of the file to create.
        """
        file_path = os.path.join(self.output_path, filename)
        with open(file_path, 'w'):
            pass

    def write_json_to_file(self, filename, data):
        """
        Write JSON data to a file.

        Args:
            filename (str): The name of the file to write.
            data (dict): The JSON data to write to the file.
        """
        file_path = os.path.join(self.output_path, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def dataset_structure(self, input_data):
        """
        Write dataset description JSON data to a file.

        Args:
            input_data (dict): The dataset description data.
        """
        self.write_json_to_file('dataset_description.json', input_data)

    def readme_change_licence(self):
        """
        Create empty README, CHANGES, and LICENSES files.
        """
        for filename in ['README', 'CHANGES', 'LICENSES']:
            self.create_empty_file(filename)

    def create_file(self, filename):
        """
        Create an empty file.

        Args:
            filename (str): The name of the file to create.
        """
        self.create_empty_file(filename)

    def citation_file(self):
        """
        Create a CITATION.cff file.
        """
        self.create_file('CITATION.cff')

    def participant_file(self):
        """
        Create participant.tsv and participant.json files.
        """
        self.create_file('participants.tsv')
        self.create_file('participants.json')

    def sample_file(self):
        """
        Create sample.tsv and sample.json files.
        """
        self.create_file('sample.tsv')
        self.create_file('sample.json')

    def dataset_description(self):
        """
        Create a dataset_description.json file.
        """
        self.create_file('dataset_description.json')

    def build(self):
        """
        Build files based on file structure.
        """
        self.layout_file()
        for filename in self.file_name:
            self.create_empty_file(filename)

    def get_file_structure(self):
        """
        Get the file structure.

        Returns:
            FileStructure: The file structure.
        """
        return self.filestructure

    def layout_file(self):
        """
        Layout files based on file structure.
        """
        all_file = self.filestructure.get_top_level_files_list()

        for filename in all_file:

            info = self.filestructure.get_detail_for_file(filename)

            if 'path' in info:
                self.file_name.append(info['path'])

            elif 'stem' in info:

                path = " "
                path = info['stem']

                for extension in info['extensions']:
                    path = path + extension
                    self.file_name.append(path)
                    if extension != '':
                        path = path[:-len(extension)]

        return self.file_name


if __name__ == "__main__":
    pass
