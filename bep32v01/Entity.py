import yaml


class Entity:
    def __init__(self):
        self.entities = self._load_entities()

    def _load_entities(self, yaml_path="ressources/schema/objects/entities.yaml"):
        with open(yaml_path, 'r') as file:
            entities_data = yaml.safe_load(file)
        return entities_data

    def get_entity_name(self, entity_name):
        if entity_name in self.entities:
            return self.entities[entity_name].get("name")
        else:
            return None


def main():
    entities = Entity()
    entity_name = "acquisition"  # Exemple de nom d'entité
    entity_name_output = entities.get_entity_name(entity_name)
    if entity_name_output:
        print(f"Nom de l'entité '{entity_name}': {entity_name_output}")
    else:
        print(f"L'entité '{entity_name}' n'existe pas.")


if __name__ == "__main__":
    main()
