import yaml


class FileStructure:
    def __init__(self, relative_path="ressources/schema/rules/files/common/core.yaml"):
        self.relative_path = relative_path
        self.all_files = []
        self.top_level_files = []
        self.top_level_directory = []
        self.top_level_file_details = {}
        self.top_level_directory_detail = {}
        self.get_detail()

    def get_all_files(self):
        with open("ressources/schema/objects/files.yaml", 'r') as file:
            file_rules = yaml.safe_load(file)
            if file_rules:
                for key in file_rules:
                    self.all_files.append(key)
                    if file_rules.get(key).get("file_type") == "regular":
                        self.top_level_files.append(key)
                    else:
                        self.top_level_directory.append(key)

    def get_all_files_detail(self, relative_path):
        with open(relative_path, 'r') as file:
            file_rules = yaml.safe_load(file)
            if file_rules:
                for key, value in file_rules.items():
                    if key in self.top_level_files:
                        self.top_level_file_details[key] = value
                    else:
                        self.top_level_directory_detail[key] = value

    def get_detail(self):
        self.get_all_files()
        self.get_all_files_detail(self.relative_path)
        self.get_all_files_detail("ressources/schema/rules/files/common/tables.yaml")
        return self

    def get_detail_for_file(self, file_name):
        return self.top_level_file_details.get(file_name)

    def get_detail_for_directory(self, directory_name):
        return self.top_level_directory_detail.get(directory_name)

    # attributes Getters
    def get_relative_path(self):
        return self.relative_path

    def get_all_files_list(self):
        return self.all_files

    def get_top_level_files_list(self):
        return self.top_level_files

    def get_top_level_directory_list(self):
        return self.top_level_directory

    def get_top_level_file_details(self):
        return self.top_level_file_details

    def get_top_level_directory_details(self):
        return self.top_level_directory_detail


def main():
    file_structure = FileStructure()
    file_structure.get_detail()
    print(file_structure.get_all_files_list())


if __name__ == "__main__":
    main()
