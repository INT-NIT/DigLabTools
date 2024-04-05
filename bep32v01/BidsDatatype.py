import yaml


def _load_data_types(yaml_path="ressources/schema/objects/datatypes.yaml"):
    """
    Load data types from a YAML file.

    Args:
        yaml_path (str): The path to the YAML file containing data type data.

    Returns:
        dict: A dictionary containing data type data.
    """
    with open(yaml_path, 'r') as file:
        data_types_data = yaml.safe_load(file)
    return data_types_data


class DataTypes:
    def __init__(self):
        """
        Initialize a DataTypes object and load data types from a YAML file.
        """
        self.data_types = _load_data_types()

    def get_data_type_value(self, data_type_name):
        """
        Get the value of a specific data type.

        Args:
            data_type_name (str): The name of the data type to retrieve.

        Returns:
            str: The value of the data type, or None if the data type does not exist.
        """
        return self.data_types.get(data_type_name, {}).get("value")


def main():
    """
    Main function to demonstrate the usage of the DataTypes class.
    """
    data_types = DataTypes()
    data_type_name = "anat"
    data_type = data_types.get_data_type_value(data_type_name)
    if data_type:
        print(f"Données de type '{data_type_name}':")
        print(data_type)
    else:
        print(f"Le type de données '{data_type_name}' n'existe pas.")


if __name__ == "__main__":
    main()
