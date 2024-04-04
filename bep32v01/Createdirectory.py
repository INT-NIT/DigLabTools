import json
import os
from Filestructure import FileStructure
from DirectoryStructure import DirectoryStructure

from Entity import Entity
from Datatype import DataTypes

from pathlib import Path


class Createdirectory:
    def __init__(self, output_path, sub_id=1, session_id=1, modality="micr"):
        self.session_path = None
        self.output_path = output_path
        self.dir_name = []
        self.filestructure = FileStructure()
        self.filestructure.get_detail()
        self.directorystructure = DirectoryStructure()
        self.entity = Entity()
        self.dataType = DataTypes()
        self.sub_id = sub_id
        self.session_id = session_id
        sub_directory = []
        self.modality = modality

    def layout_folder(self):
        top_level_dir = self.directorystructure.get_top_level_directory()
        entity_dir = self.directorystructure.get_entity_directory()
        value_dir = self.directorystructure.get_value_directory()
        all_dir = self.directorystructure.get_all_directory()
        for dir in all_dir:

            path = ""
            if dir in top_level_dir:
                # print(dir)
                if dir in entity_dir:
                    path = self.entity.get_entity_name(dir) + f'-{str(self.sub_id)}'

                elif dir in value_dir:
                    path = self.dataType.get_data_type_value(dir)

                else:
                    path = dir

                self.dir_name.append(path)

    def build(self):
        for dir in self.dir_name:
            first_level_dir = os.path.join(self.output_path, dir)
            print("path: ", first_level_dir)
            if not os.path.exists(first_level_dir):
                os.makedirs(first_level_dir)

        # subdirectory session
        subject_dir = os.path.join(self.output_path, f'sub-{self.sub_id}')
        session_dir = os.path.join(subject_dir, f'ses-{self.session_id}')
        print("subject_dir: ", session_dir)
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
        # subdirectory_modality
        modality_dir = os.path.join(session_dir, self.modality)
        if not os.path.exists(modality_dir):
            os.makedirs(modality_dir)


def main():
    output_path = "Essaie"  # Change this to your desired output path
    creator = Createdirectory(output_path)
    creator.layout_folder()
    creator.build()
    print("Directory layout created successfully.")


if __name__ == "__main__":
    main()
