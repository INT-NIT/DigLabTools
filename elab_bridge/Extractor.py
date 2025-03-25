import json

import argparse

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def loadfile(jsonfile):
    try:
        with open(jsonfile, 'r') as f:
            data = json.load(f)
            # tranforme to int all id an dgroupe id in the json file
            for group in data['elabftw']['extra_fields_groups']:
                group['id'] = int(group['id'])
            for field in data['extra_fields'].values():
                field['group_id'] = int(field['group_id'])

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
        savefile(json_output, new_json_structure)

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

    data = loadfile(jsonfile)

    # Increment IDs of existing groups if they are greater than or equal to the new index
    for group in data['elabftw']['extra_fields_groups']:
        if group['id'] >= indice:
            group['id'] += 1

    # Add the new group
    data['elabftw']['extra_fields_groups'].append({'id': indice, 'name': group_name})
    data['elabftw']['extra_fields_groups'] = sorted(data['elabftw']['extra_fields_groups'],
                                                    key=lambda x: x['id'])

    # Update the group_id in existing extra fields
    extra_fields = data.get('extra_fields', {})
    for k, v in extra_fields.items():
        group_id = int(v.get('group_id', 0))
        if group_id >= indice:
            v['group_id'] = group_id + 1

    # Add the new fields to the extra fields
    for a_dict in groupfield_dict_list:
        for field_name, field_data in a_dict.items():
            field_data['group_id'] = indice  # Assign the new group ID as an integer
            extra_fields[field_name] = field_data

    data['extra_fields'] = extra_fields

    if output_jsonfile is not None:
        with open(output_jsonfile, 'w') as f_out:
            json.dump(data, f_out, indent=4)

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

    data = loadfile(jsonfile)

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


def orderjsonfile(jsonfile, list_group_field_name, output_jsonfile=None):
    """
    Orders fields within a JSON file by specified group field names.
    Parameters
    ----------
    jsonfile
    list_group_field_name
    output_jsonfile

    Returns
    -------  the updated JSON data.

    """

    try:
        # Loading the JSON file
        Data = loadfile(jsonfile)
        if output_jsonfile is None:
            output_jsonfile = jsonfile

        # Ensure required keys are present
        if 'elabftw' not in Data or 'extra_fields_groups' not in Data['elabftw']:
            raise KeyError("Missing 'extra_fields_groups' in JSON data.")

        list_group_field = [group['name'] for group in Data['elabftw']['extra_fields_groups']]
        logger.debug(f"List of group fields: {list_group_field}")


        # Validate group names
        missing_groups = [group_name for group_name in list_group_field if
                          group_name not in list_group_field_name]
        if missing_groups:
            raise ValueError(f"Missing groups in data: {missing_groups}")


        # Create mapping for group IDs
        Dict_group_field_map = {}
        for group in Data['elabftw']['extra_fields_groups']:
            if group['name'] in list_group_field_name:
                Dict_group_field_map[group['id']] = list_group_field_name.index(group['name']) + 1
        logger.debug(f"Group field map: {Dict_group_field_map}")

        # Reorganize group fields
        for group in Data['elabftw']['extra_fields_groups']:
            if group['id'] in Dict_group_field_map:
                group['id'] = Dict_group_field_map[group['id']]
        Data['elabftw']['extra_fields_groups'] = sorted(Data['elabftw']['extra_fields_groups'],
                                                        key=lambda x: x['id'])
        logger.debug(f"Reorganized group fields: {Data['elabftw']['extra_fields_groups']}")

        # Reorganize fields
        for field in Data.get('extra_fields', {}).values():
            if field['group_id'] in Dict_group_field_map:
                field['group_id'] = Dict_group_field_map[field['group_id']]
        logger.debug(f"Reorganized fields: {Data.get('extra_fields')}")

        # Save the updated JSON
        savefile(output_jsonfile, Data)
        logger.info(f"Updated JSON saved to {output_jsonfile}")
        return Data

    except AssertionError as e:
        logger.error(f"AssertionError: {str(e)}")
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}")
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
    return None


def replicate_groupfield(jsonfile, id, n_replicat, samefieldname=False, erase_existing=False,
                         json_output=None):
    """
        Replicate a groupfield in a JSON file.
        Extract a groupfield from a JSON file and replicate it n times
        where for each replication the groupfield id is incremented by 1 and the groupfield name is the parent groupfield name + index.

        :param jsonfile: The JSON file path.
        :param id: The groupfield id to replicate.
        :param n_replicat: The number of groupfield to replicate.
        :param json_output: The path to save the updated JSON file.
        :param erase_existing: Boolean to indicate if existing data should be erased.
        :return: The updated JSON data.
        """
    data = loadfile(jsonfile)
    groupfield_name, list_group_field = extract_groupfield_detail(jsonfile, id, id)

    if samefieldname:
        list_group_field_name = [groupfield_name for i in range(n_replicat)]
    else:
        list_group_field_name = [groupfield_name + str(i) for i in range(1, n_replicat + 1)]
    list_id = [id + i for i in range(1, n_replicat + 1)]
    list_group_field_name.insert(0, groupfield_name)

    new_fields = []
    for field in list_group_field:
        for k, v in field.items():
            for i in range(1, n_replicat + 1):
                new_k = f"{k}{i}"
                new_v = v.copy()
                new_v['group_id'] = id + i
                new_fields.append({new_k: new_v})

    if erase_existing:
        data['elabftw']['extra_fields_groups'] = []
        data['extra_fields'] = {}
    else :
        # Increment IDs of existing groups if they are greater than or equal to the new index
        for group in data['elabftw']['extra_fields_groups']:
            if n_replicat +1 <= group['id'] > id:
                group['id'] += n_replicat+int(group['id'], 0)

        # Update the group_id in existing extra fields
        extra_fields = data.get('extra_fields', {})
        for k, v in extra_fields.items():
            group_id = int(v.get('group_id', 0))
            if n_replicat +1 <= group['id'] > id:

                v['group_id'] = group_id + n_replicat+int(group['id'], 0)
    # Replicate the groupfield n times
    for new_id, name in zip(list_id, list_group_field_name[1:]):
        data['elabftw']['extra_fields_groups'].append({'id': new_id, 'name': name})

    data['extra_fields'].update(
        {field_id: details for field in new_fields for field_id, details in field.items()})

    if json_output is not None:
        savefile(json_output, data)
    return data


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=(
            "This script provides tools to manipulate JSON files, including:\n"
            "- Extracting specific fields from a JSON file and creating a new structured JSON.\n"
            "- Merging two JSON files based on group field IDs: Extracting a group field from one "
            "JSON file and appending it to another.\n"
            "- Ordering fields within a JSON file by specified group field names.\n"
            "- Replicating a group field in a JSON file."
        ),
        epilog=(
            "Examples of usage:\n"
            "  Extract fields:\n"
            "python Extractor.py extract --jsonfile_extract input.json --id 1 --new_id 2 "
            "--json_output output.json\n\n"

            "  Merge JSON files:\n"
            "python Extractor.py merge --jsonfiletocompleted file1.json --jsonfiletoextract "
            "file2.json --id 3 --new_id 4 --json_completed merged.json\n\n"
            "  Order JSON fields:\n"
            "python Extractor.py order --jsonfile input.json --list_group_field_name field1 "
            "field2 --output_jsonfile ordered.json\n\n"
            "  Replicate group field:\n"
            "python Extractor.py replicate --jsonfile input.json --id 1 --n_replicat 3 "
            "--json_output replicated.json\n\n"
            "Options:\n"
            "  extract   Extracts fields from a JSON file and saves the output.\n"
            "  merge     Complete a JSON file by adding a group field from another JSON file.\n"
            "  order     Orders fields in a JSON file by the specified group field names.\n"
            "  replicate Replicates a group field in a JSON file."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "operation",
        choices=["extract", "merge", "order", "replicate"],
        help="Specify the operation to perform: 'extract' to extract fields, 'merge' to combine "
             "files, 'order' to order fields, or 'replicate' to replicate a group field.",
    )

    # Arguments for extracting
    parser.add_argument("--jsonfile_extract", '-e', help="The JSON file path for extraction.",
                        type=str)

    parser.add_argument("--id", help="The groupfield ID to match.", type=int)
    parser.add_argument("--new_id", help="The new ID to replace for matching fields.", type=int)
    parser.add_argument("--json_output", '-u', help="The path to save the new JSON structure.",
                        type=str,
                        default=None)

    # Arguments for merging
    parser.add_argument("--jsonfiletocompleted", '-c', help="The JSON file to be completed.",
                        type=str)
    parser.add_argument("--jsonfiletoextract", '-x', help="The JSON file to extract the "
                                                          "groupfield from.",
                        type=str)
    parser.add_argument("--json_completed", '-C', help="The path to save the completed JSON file.",
                        type=str, default=None)

    # Arguments for ordering
    parser.add_argument("--jsonfile", '-j', help="The JSON file path for ordering.", type=str)
    parser.add_argument("--list_group_field_name", '-l', help="The list of group field names to "
                                                              "order.",
                        type=str, nargs='+')
    parser.add_argument("--output_jsonfile", '-o', help="The path to save the ordered JSON file.",
                        type=str, default=None)

    # Arguments for replicating
    parser.add_argument("--n_replicat", '-n', help="The number of groupfield to replicate",
                        type=int)
    parser.add_argument("--samefieldname", '-y', help="identical field name for all groupfield",
                        action='store_true')
    parser.add_argument("--erase_existing", '-r', help="keep only replicat", action='store_true')

    args = parser.parse_args()

    if args.operation == "extract":
        if not all([args.jsonfile_extract, args.id, args.new_id, args.json_output]):
            print("Error: Missing arguments for the 'extract' operation.")
        else:
            construct_extracted_json(args.jsonfile_extract, args.id, args.new_id, args.json_output)
            print(f"Extraction completed and saved to {args.json_output}.")

    elif args.operation == "merge":
        if not all(
                [args.jsonfiletocompleted, args.jsonfiletoextract, args.id, args.new_id,
                 args.json_completed]
        ):
            print("Error: Missing arguments for the 'merge' operation.")
        else:
            complete_jsonfile1_with_jsonfile2_groupefield(
                args.jsonfiletocompleted,
                args.jsonfiletoextract,
                args.id,
                args.new_id,
                args.json_completed,
            )
            print(f"Merging completed and saved to {args.json_completed}.")

    elif args.operation == "order":
        if not all([args.jsonfile, args.list_group_field_name]):
            print("Error: Missing arguments for the 'order' operation.")
        else:
            orderjsonfile(args.jsonfile, args.list_group_field_name, args.output_jsonfile)
            print(f"Ordering lunch and will be save  to {args.jsonfile}.")

    elif args.operation == "replicate":
        if not all([args.jsonfile, args.id, args.n_replicat]):
            print("Error: Missing arguments for the 'replicate' operation.")
        else:
            replicate_groupfield(args.jsonfile, args.id, args.n_replicat, args.samefieldname,
                                 args.erase_existing, args.json_output)
            print(f"Replication completed and saved to {args.json_output}.")
