import yaml

class FileStructure:
    def __init__(self, relative_path="ressources/schema/rules/files/common/core.yaml"):
        """
        Initialize a FileStructure object with a relative path to a YAML file.

        Args:
            relative_path (str): The relative path to the YAML file containing file structure rules.
        """
        self.relative_path = relative_path
        self.all_files = []
        self.top_level_files = []
        self.top_level_directory = []
        self.top_level_file_details = {}
        self.top_level_directory_detail = {}
        self.get_detail()

    def get_all_files(self):
        """
        Retrieve all file names from the YAML file containing file structure rules.
        """
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
        """
        Retrieve details for all files and directories from a specified YAML file.

        Args:
            relative_path (str): The relative path to the YAML file containing file structure details.
        """
        with open(relative_path, 'r') as file:
            file_rules = yaml.safe_load(file)
            if file_rules:
                for key, value in file_rules.items():
                    if key in self.top_level_files:
                        self.top_level_file_details[key] = value
                    else:
                        self.top_level_directory_detail[key] = value

    def get_detail(self):
        """
        Retrieve file structure details and store them in class attributes.
        """
        self.get_all_files()
        self.get_all_files_detail(self.relative_path)
        self.get_all_files_detail("ressources/schema/rules/files/common/tables.yaml")
        return self

    def get_detail_for_file(self, file_name):
        """
        Retrieve details for a specific file.

        Args:
            file_name (str): The name of the file.

        Returns:
            dict: Details of the file.
        """
        return self.top_level_file_details.get(file_name)

    def get_detail_for_directory(self, directory_name):
        """
        Retrieve details for a specific directory.

        Args:
            directory_name (str): The name of the directory.

        Returns:
            dict: Details of the directory.
        """
        return self.top_level_directory_detail.get(directory_name)

    # Attributes Getters
    def get_relative_path(self):
        """
        Get the relative path to the YAML file containing file structure rules.

        Returns:
            str: The relative path.
        """
        return self.relative_path

    def get_all_files_list(self):
        """
        Get the list of all files.

        Returns:
            list: List of all file names.
        """
        return self.all_files

    def get_top_level_files_list(self):
        """
        Get the list of top-level files.

        Returns:
            list: List of top-level file names.
        """
        return self.top_level_files

    def get_top_level_directory_list(self):
        """
        Get the list of top-level directories.

        Returns:
            list: List of top-level directory names.
        """
        return self.top_level_directory

    def get_top_level_file_details(self):
        """
        Get details of top-level files.

        Returns:
            dict: Dictionary containing details of top-level files.
        """
        return self.top_level_file_details

    def get_top_level_directory_details(self):
        """
        Get details of top-level directories.

        Returns:
            dict: Dictionary containing details of top-level directories.
        """
        return self.top_level_directory_detail


def main():
    """
    Main function to demonstrate the usage of the FileStructure class.
    """
    file_structure = FileStructure()
    file_structure.get_detail()
    print(file_structure.get_all_files_list())


if __name__ == "__main__":
    main()
