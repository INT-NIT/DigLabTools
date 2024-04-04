from pathlib import Path
import yaml
import helper


class DirectoryStructure:
    def __init__(self):
        self.relative_path = "ressources/schema/rules/directories.yaml"
        self.entity_directory = []
        self.all_directory = None
        self.value_directory = None
        self.required_directory = None
        self.optional_directory = None
        self.recommended_directory = None
        self.top_level_directory = None
        self.sub_directory = None
        self.get_detail()

    def load_all_directories(self, relative_path):
        # retrieve absolute path
        absolute_path = Path(relative_path).resolve()

        # check if the file exist
        if absolute_path.exists():
            with open(absolute_path, 'r') as file:
                directory_rules = yaml.safe_load(file)

                if directory_rules:
                    self.all_directory = list(set(helper.find_keys_in_dict(directory_rules, 'level')))
                else:
                    print("Le fichier de règles des répertoires est vide.")
        else:
            print("Le fichier YAML spécifié n'existe pas :", absolute_path)
        return self.all_directory

    def load_all_directoires_all_details(self, relative_path):
        self.entity_directory, self.value_directory, self.required_directory, self.optional_directory, self.recommended_directory, self.top_level_directory = helper.get_directories_with_details(
            relative_path)

    def get_detail(self):
        self.load_all_directories(self.relative_path)
        self.load_all_directoires_all_details(self.relative_path)
        return self

    # Getter pour all_directory
    def get_all_directory(self):
        return self.all_directory

    # Getter pour entity_directory
    def get_entity_directory(self):
        return self.entity_directory

    # Getter pour value_directory
    def get_value_directory(self):
        return self.value_directory

    # Getter pour required_directory
    def get_required_directory(self):
        return self.required_directory

    # Getter pour optional_directory
    def get_optional_directory(self):
        return self.optional_directory

    # Getter pour recommended_directory
    def get_recommended_directory(self):
        return self.recommended_directory

    # Getter pour top_level_directory
    def get_top_level_directory(self):
        return self.top_level_directory


if __name__ == "__main__":
    relative_path = "ressources/schema/rules/directories.yaml"

    common_structure = DirectoryStructure()
    common_structure.get_detail()

    print("All:", common_structure.get_all_directory())
    print("Entity:", common_structure.get_entity_directory())
    print("par Valeur  :", common_structure.get_value_directory())
    print("REQUIRED  :", common_structure.get_required_directory())
    print("optional :", common_structure.get_optional_directory())
    print("top level:", common_structure.get_top_level_directory())
    print("recomende:", common_structure.get_recommended_directory())
