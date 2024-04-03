import json
import os
from Filestructure import FileStructure


class CreatFile:
    def __init__(self, output_path):
        self.output_path = output_path
        self.file_name = []
        self.filestructure = FileStructure()

    def create_empty_file(self, filename):
        file_path = os.path.join(self.output_path, filename)
        with open(file_path, 'w'):
            pass

    def write_json_to_file(self, filename, data):
        file_path = os.path.join(self.output_path, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def dataset_structure(self, input_data):
        self.write_json_to_file('dataset_description.json', input_data)

    def readme_change_licence(self):
        for filename in ['README', 'CHANGES', 'LICENSES']:
            self.create_empty_file(filename)

    def create_file(self, filename):
        self.create_empty_file(filename)

    def citation_file(self):
        self.create_file('CITATION.cff')

    def participant_file(self):
        self.create_file('participants.tsv')
        self.create_file('participants.json')

    def sample_file(self):
        self.create_file('sample.tsv')
        self.create_file('sample.json')

    def dataset_description(self):
        self.create_file('dataset_description.json')

    def build(self):
        self.layout_file()
        for filename in self.file_name:
            self.create_empty_file(filename)

    def get_file_structure(self):
        return self.filestructure

    def layout_file(self):
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
                    #print(path)
                    self.file_name.append(path)
                    if extension != '':
                        path = path[:-len(extension)]

        return self.file_name


if __name__ == "__main__":
    creatfile = CreatFile('Essaie')
    # d = creatfile.get_file_structure()
    # creatfile.layout_file()
    creatfile.build()
    # print(d.get_top_level_files_list())
