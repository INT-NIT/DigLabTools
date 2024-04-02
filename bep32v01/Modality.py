import yaml


class Modality:
    def __init__(self, relative_path="ressources/schema/objects/modalities.yaml"):
        self.relative_path = relative_path
        self.modalities = []

        with open(relative_path, "r") as file:
            modalities_yaml = yaml.safe_load(file)
            if modalities_yaml:
                self.modalities = list(modalities_yaml.keys())


def main():
    modality = Modality()
    print("Modalités :")
    print(modality.modalities)


if __name__ == "__main__":
    main()
