import bep32v01
from bep32v01 import *

from DirectoryStructure import DirectoryStructure
from Datatype import DataTypes
from  Entity import  Entity
from Filestructure import FileStructure
from Modality import Modality

class Common_structure:
    def __init__(self, output='.'):
        self.directory = DirectoryStructure()  # Création d'une instance de la classe DirectoryStructure
        self.entity = Entity()
        self.filestructure = FileStructure()
        self.modality = Modality()
        self.datatype = DataTypes()
        self .output = output

    def initialize(self):
        self.directory.get_details()
        self.filestructure.get_detail()
    def create_entity(self):
        self