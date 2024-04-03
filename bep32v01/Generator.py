import sys

from Createfile import CreatFile
from Createdirectory import Createdirectory


class Generator:
    def __init__(self, outpout):
        self.outpout = outpout
        self.directoy_builder = Createdirectory(outpout)
        self.file_builder = CreatFile(outpout)

    def generate(self):
        self.directoy_builder.build()
        self.file_builder.build()





if __name__ == "__main__":
    outpout = input("Enter the output folder path: ")
    generator = Generator(outpout)
    generator.generate()
