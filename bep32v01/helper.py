import os
import yaml


def find_keys_in_dict(dictionary, target_value):
    """
    Search for keys corresponding to the given value in a dictionary.

    Args:
        dictionary (dict): The dictionary to search in.
        target_value: The value to search for.

    Returns:
        list: A list of keys corresponding to the value, or an empty list if the value is not found.
    """
    keys = []

    for key, value in dictionary.items():
        if target_value in value:
            keys.append(key)
        elif isinstance(value, dict):
            nested_keys = find_keys_in_dict(value, target_value)
            keys.extend(nested_keys)

    return keys


def find_value_in_dict(dictionary, target_key):
    """
    Search for a value corresponding to the given key in a dictionary.

    Args:
        dictionary (dict): The dictionary to search in.
        target_key: The key to search for.

    Returns:
        The value corresponding to the key, or None if the key is not found.
    """
    for key, value in dictionary.items():
        if key == target_key:
            return value
        elif isinstance(value, dict):
            result = find_value_in_dict(value, target_key)
            if result is not None:
                return result
    return None


def find_keys_with_value(dictionary, target_value):
    """
    Find keys containing the given value in a dictionary.

    Args:
        dictionary (dict): The dictionary to search in.
        target_value: The value to search for.

    Returns:
        list: A list of keys containing the value, or an empty list if the value is not found.
    """
    keys = []

    for key, value in dictionary.items():
        if isinstance(value, list):
            if target_value in value:
                keys.append(key)
        elif value == target_value:
            keys.append(key)
        elif isinstance(value, dict):
            nested_keys = find_keys_with_value(value, target_value)
            keys.extend(nested_keys)

    return keys


def get_directories_with_details(yaml_file):
    """
    Get directories with the 'entity' attribute from a YAML file.

    Args:
        yaml_file (str): Path to the YAML file containing directory information.

    Returns:
        tuple: A tuple containing lists of directory names categorized based on different criteria.
    """
    directories_entities = []
    directories_values = []
    directory_required = []
    directory_optional = []
    directory_recommended = []
    top_level_directory = []

    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    for directory, info in data.get('raw', {}).items():
        if 'entity' in info:
            directories_entities.append(directory)
        if 'value' in info:
            directories_values.append(directory)
        if 'level' in info and info.get('level') == 'required':
            directory_required.append(directory)
        if 'level' in info and info.get('level') == 'optional':
            directory_optional.append(directory)
        if 'recommended' in info:
            directory_recommended.append(directory)
    for directory in data.get('raw', {}).get('root', {}).get('subdirs', {}):
        top_level_directory.append(directory)

    return (directories_entities, directories_values, directory_required,
            directory_optional, directory_recommended, top_level_directory)
