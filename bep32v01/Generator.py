import sys

from Createfile import CreatFile
from Createdirectory import Createdirectory


class Generator:
    def __init__(self, output, sub_id=1, session_id=1, modality=None):
        self.output = output
        self.modality = modality  # Ensure modality is properly set
        self.directory_builder = Createdirectory(output, sub_id, session_id, self.modality)
        self.file_builder = CreatFile(output)
        if modality and modality.strip():  # Check if modality is not an empty string
            self.generate()

    def generate(self):
        self.directory_builder.build()
        self.file_builder.build()


if __name__ == "__main__":
    output = input("Enter the output folder path: ")
    generator = Generator(output)
    generator.generate()
