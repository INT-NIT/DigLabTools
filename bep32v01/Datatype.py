import yaml


def _load_data_types(yaml_path="ressources/schema/objects/datatypes.yaml"):
    with open(yaml_path, 'r') as file:
        data_types_data = yaml.safe_load(file)
    return data_types_data


class DataTypes:
    def __init__(self):
        self.data_types = _load_data_types()

    def get_data_type_value(self, data_type_name):
        return self.data_types.get(data_type_name).get("value")


def main():
    data_types = DataTypes()
    data_type_name = "anat"  # Exemple de nom de type de données
    data_type = data_types.get_data_type_value(data_type_name)
    if data_type:
        print(f"Données de type '{data_type_name}':")
        print(data_type)
    else:
        print(f"Le type de données '{data_type_name}' n'existe pas.")


if __name__ == "__main__":
    main()
