import os

import yaml


def find_keys_in_dict(dictionary, target_value):
    """
    Search for keys corresponding to the given value in a dictionary.
    :param dictionary: The dictionary to search in.
    :param target_value: The value to search for.
    :return: A list of keys corresponding to the value, or an empty list if the value is not found.
    """
    keys = []

    # Iterate through all key-value pairs in the dictionary
    for key, value in dictionary.items():
        # Check if the value matches the target value

        if target_value in value:

            keys.append(key)
        # If the value is another dictionary,
        # recursively call the function to search within that dictionary
        elif isinstance(value, dict):
            nested_keys = find_keys_in_dict(value, target_value)
            # Extend the keys list with the keys found in the nested dictionary
            keys.extend(nested_keys)

    return keys


def find_value_in_dict(dictionary, target_key):
    """
    Search for a value corresponding to the given key in a dictionary.
    :param dictionary: The dictionary to search in.
    :param target_key: The key to search for.
    :return: The value corresponding to the key, or None if the key is not found.
    """
    # Iterate through all keys and values in the dictionary
    for key, value in dictionary.items():
        # Check if the key matches the target key
        if key == target_key:
            return value
        # If the value is another dictionary,
        # recursively call the function to search within that dictionary
        elif isinstance(value, dict):
            result = find_value_in_dict(value, target_key)
            if result is not None:
                return result
    # If the key is not found in this dictionary or
    # any of its sub-dictionaries, return None
    return None


def find_keys_with_value(dictionary, target_value):
    """
    Find keys containing the given value in a dictionary.
    :param dictionary: The dictionary to search in.
    :param target_value: The value to search for.
    :return: A list of keys containing the value, or an empty list if the value is not found.
    """
    keys = []

    # Iterate through all key-value pairs in the dictionary
    for key, value in dictionary.items():
        # Check if the value matches the target value
        if isinstance(value, list):
            if target_value in value:
                keys.append(key)
        elif value == target_value:
            keys.append(key)
        # If the value is another dictionary,
        # recursively call the function to search within that dictionary
        elif isinstance(value, dict):
            nested_keys = find_keys_with_value(value, target_value)
            # Extend the keys list with the keys found in the nested dictionary
            keys.extend(nested_keys)

    return keys


def get_directories_with_details(yaml_file):
    """
    Get directories with the 'entity' attribute from a YAML file.
    :param yaml_file: Path to the YAML file containing directory information.
    :return: A list of directory names having the 'entity' attribute.
    """
    directories_entities = []
    directories_values = []
    directory_required = []
    directory_optional = []
    direrectory_recomended = []
    top_level_directory = []
    sub_directory = []

    # Load YAML file
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    # Iterate through each directory definition
    for directory, info in data.get('raw', {}).items():

        # Check if the directory definition contains the 'entity' attribute
        if 'entity' in info:
            directories_entities.append(directory)
        if 'value' in info:
            directories_values.append(directory)
        if 'level' in info and info.get('level') == 'required':
            print(info)
            directory_required.append(directory)
        if 'level' in info and info.get('level') == 'optional':
            directory_optional.append(directory)
        if 'recommended' in info:
            direrectory_recomended.append(directory)
    for directory in data.get('raw', {}).get('root', {}).get('subdirs', {}):

        top_level_directory.append(directory)

    return (directories_entities, directories_values, directory_required,
            directory_optional, direrectory_recomended, top_level_directory)
