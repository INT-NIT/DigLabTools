import json

import argparse

import argparse


def loadfile(jsonfile):
    try:
        with open(jsonfile, 'r') as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")
    except FileNotFoundError:
        raise ValueError(f"File not found: {jsonfile}")


def savefile(jsonfile, data):
    with open(jsonfile, "w") as f:
        json.dump(data, f, indent=4)


def extract_groupfield_detail(jsonfile, id, new_id=None):
    """
    Extract details of groupfield from a JSON file.

    :param jsonfile: The JSON file path.
    :param id: The groupfield id to match.
    :param new_id: The new id to replace for matching fields.
    :return: groupfield name and all child fields from the group as a list of dictionaries.
    """
    list_group_field = []
    group_name = ""

    # Open and load the JSON data
    with open(jsonfile, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON: {e}")

    # Extract the group name by matching the id
    if 'elabftw' in data and 'extra_fields_groups' in data['elabftw']:
        for group in data['elabftw']['extra_fields_groups']:
            if int(group.get('id')) == id:
                group_name = group.get('name', '')  # Ensure name exists
                break
    else:
        raise KeyError("Expected keys 'elabftw' and 'extra_fields_groups' not found in JSON")

    # Check if 'extra_fields' exists and is a dictionary
    extra_fields = data.get('extra_fields', {})

    if isinstance(extra_fields, dict):
        for k, v in extra_fields.items():
            if v.get('group_id') == str(id) or v.get('group_id') == id:
                v['group_id'] = new_id
                list_group_field.append({k: v})

    return group_name, list_group_field


def construct_extracted_json(jsonfile, id, new_id, json_output=None):
    """
    Construct a new JSON file with the same layout but only the extracted information.

    :param jsonfile: The original JSON file path.
    :param id: The groupfield id to match.
    :param new_id: The new id to replace for matching fields.
    :param json_output: The path to save the new JSON structure.
    :return: A dictionary with the new JSON structure.
    """
    group_name, list_group_field = extract_groupfield_detail(jsonfile, id, new_id)

    new_json_structure = {
        'elabftw': {
            'extra_fields_groups': [
                {
                    'id': new_id,
                    'name': group_name
                }
            ]
        },
        'extra_fields': {field_id: details for field in list_group_field for field_id, details in
                         field.items()}
    }

    if json_output is not None:
        with open(json_output, 'w') as f:
            json.dump(new_json_structure, f, indent=4)

    return new_json_structure


def add_a_groupfield(jsonfile, indice, groupfield_dict_list, group_name, output_jsonfile=None):
    """
    Add a new groupfield to the JSON file.

    :param jsonfile: The JSON file path.
    :param indice: The ID for the new groupfield.
    :param groupfield_dict_list: A list of dictionaries representing the fields to add.
    :param group_name: The name of the new groupfield.
    :param output_jsonfile: The path to save the updated JSON file.
    :return: The updated JSON data.
    """
    with open(jsonfile, 'r') as f:
        data = json.load(f)

    for group in data['elabftw']['extra_fields_groups']:
        if group['id'] >= indice:
            group['id'] += 1

    data['elabftw']['extra_fields_groups'].append({'id': indice, 'name': group_name})
    data['elabftw']['extra_fields_groups'] = sorted(data['elabftw']['extra_fields_groups'],
                                                    key=lambda x: x['id'])

    extra_fields = data.get('extra_fields', {})

    for k, v in extra_fields.items():
        if int(v.get('group_id')) >= indice:
            v['group_id'] += 1

    for a_dict in groupfield_dict_list:
        for k, v in a_dict.items():
            extra_fields[k] = v

    data['extra_fields'] = extra_fields

    if output_jsonfile is not None:
        with open(output_jsonfile, "w") as f:
            json.dump(data, f, indent=4)

    return data


def complete_groupfield_in_jsonfile(jsonfile, groupfield_name, groupfield_detail_list,
                                    json_completed=None):
    """
    Complete the 'extra_fields' section of a JSON file with new fields based on a groupfield name.

    :param jsonfile: The JSON file path.
    :param groupfield_name: The name of the groupfield.
    :param groupfield_detail_list: A list of dictionaries representing the new fields to add.
    :param json_completed: The path to save the updated JSON file.
    :return: The updated JSON data.
    """
    is_completed = False
    new_id = None

    with open(jsonfile, 'r') as f:
        data = json.load(f)

    for group in data['elabftw']['extra_fields_groups']:
        if groupfield_name == group['name']:
            is_completed = True
            new_id = group['id']
            break

    if is_completed and new_id:
        extra_fields = data['extra_fields']

        for a_dict in groupfield_detail_list:
            for k, v in a_dict.items():
                v['group_id'] = new_id
                extra_fields[k] = v

        data['extra_fields'] = extra_fields

        if json_completed is not None:
            with open(json_completed, 'w') as f_out:
                json.dump(data, f_out, indent=4)

        return data

    else:
        raise ValueError(f"Groupfield name '{groupfield_name}' not found in the JSON file.")


def complete_jsonfile1_with_jsonfile2_groupefield(jsonfiletocompleted, jsonfiletoextract, indice,
                                                  new_indice, json_completed=None):
    """
    Extract a groupfield from one JSON file and add it to another JSON file.

    :param jsonfiletocompleted: The JSON file to be completed.
    :param jsonfiletoextract: The JSON file to extract the groupfield from.
    :param indice: The groupfield ID in the source JSON file.
    :param new_indice: The new groupfield ID for the target JSON file.
    :param json_completed: The path to save the completed JSON file.
    :return: The updated JSON data.
    """
    group_name, list_group_field = extract_groupfield_detail(jsonfiletoextract, indice, new_indice)
    if json_completed is None:
        json_completed = jsonfiletocompleted
    return add_a_groupfield(jsonfiletocompleted, new_indice, list_group_field, group_name,
                            output_jsonfile=json_completed)





if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Extract and merge JSON files.")
    parser.add_argument(
        "operation",
        choices=["extract", "merge"],
        help="Specify the operation to perform: 'extract' to extract fields or 'merge' to combine files.",
    )

    # Arguments for extracting
    parser.add_argument("--jsonfile", help="The JSON file path for extraction.", type=str)
    parser.add_argument("--id", help="The groupfield ID to match.", type=int)
    parser.add_argument("--new_id", help="The new ID to replace for matching fields.", type=int)
    parser.add_argument("--json_output", help="The path to save the new JSON structure.", type=str,
                        default=None)

    # Arguments for merging
    parser.add_argument("--jsonfiletocompleted", help="The JSON file to be completed.", type=str)
    parser.add_argument("--jsonfiletoextract", help="The JSON file to extract the groupfield from.",
                        type=str)
    parser.add_argument("--indice", help="The groupfield ID in the source JSON file.", type=int)
    parser.add_argument("--new_indice", help="The new groupfield ID for the target JSON file.",
                        type=int)
    parser.add_argument("--json_completed", help="The path to save the completed JSON file.",
                        type=str, default=None)

    args = parser.parse_args()

    if args.operation == "extract":
        if not all([args.jsonfile, args.id, args.new_id, args.json_output]):
            print("Error: Missing arguments for the 'extract' operation.")
        else:
            construct_extracted_json(args.jsonfile, args.id, args.new_id, args.json_output)
            print(f"Extraction completed and saved to {args.json_output}.")

    elif args.operation == "merge":
        if not all(
                [args.jsonfiletocompleted, args.jsonfiletoextract, args.indice, args.new_indice,
                 args.json_completed]
        ):
            print("Error: Missing arguments for the 'merge' operation.")
        else:
            complete_jsonfile1_with_jsonfile2_groupefield(
                args.jsonfiletocompleted,
                args.jsonfiletoextract,
                args.indice,
                args.new_indice,
                args.json_completed,
            )
            print(f"Merging completed and saved to {args.json_completed}.")
