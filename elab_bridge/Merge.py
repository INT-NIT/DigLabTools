import json
import os
import argparse
from typing import List, Tuple, Dict, Any
from tqdm import tqdm  # For progress indication
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def safe_load_json(filepath: str) -> Dict[str, Any]:
    """
    Safely load a JSON file, handling potential errors.
    Args:
        filepath (str): Path to the JSON file.
    Returns:
        Dict[str, Any]: Parsed JSON data.
    Raises:
        ValueError: If the file is not valid JSON or cannot be read.
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {filepath}")
    except FileNotFoundError:
        raise ValueError(f"File not found: {filepath}")


def get_a_jsonfile_structure(jsonfile: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Extract structure from a JSON file, focusing on 'extra_fields_groups' and 'extra_fields'.
    Args:
        jsonfile (str): Path to the JSON file.
    Returns:
        Tuple[List[Dict[str, Any]], Dict[str, Any]]: Groups and fields.
    """
    data = safe_load_json(jsonfile)

    # Ensure every 'id' in 'extra_fields_groups' is an int
    for group in data['elabftw']['extra_fields_groups']:
        group['id'] = int(group['id'])

    # Ensure every 'group_id' in 'extra_fields' is an int
    for field in data['extra_fields'].values():
        field['group_id'] = int(field['group_id'])
    # check if all id are int
    assert all(isinstance(group['id'], int) for group in data['elabftw']['extra_fields_groups'])
    # check if all group_id are int
    assert all(isinstance(field['group_id'], int) for field in data['extra_fields'].values())
    return data['elabftw']['extra_fields_groups'], data['extra_fields']


def get_indices(extra_fields_groups: List[Dict[str, Any]]) -> int:
    """
    Get the next available index for 'id' fields.
    Args:
        extra_fields_groups (List[Dict[str, Any]]): List of groups.
    Returns:
        int: Next index.
    """
    return max(group['id'] for group in extra_fields_groups) + 1 if extra_fields_groups else 1


def replace_id(
        extra_fields_groups: List[Dict[str, Any]],
        extrat_fields: Dict[str, Dict[str, Any]],
        indice: int
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """
    Replace IDs in groups and fields to ensure uniqueness.
    Args:
        extra_fields_groups (list): List of groups.
        extrat_fields (dict): Fields mapping.
        indice (int): Starting index.
    Returns:
        Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]: Updated groups and fields.
    """
    # Sort 'extra_fields_groups' by 'id' to ensure consistent order
    extra_fields_groups_sorted = sorted(extra_fields_groups, key=lambda group: group['id'])

    # Sort 'extrat_fields' by 'group_id' to ensure fields match the sorted groups
    extrat_fields_sorted = {k: v for k, v in
                            sorted(extrat_fields.items(), key=lambda item: item[1]['group_id'])}

    matched_indices = {}
    for group in extra_fields_groups_sorted:
        old_id = group['id']
        group['id'] = indice
        matched_indices[old_id] = indice
        indice += 1

    for field in extrat_fields_sorted.values():
        if 'group_id' in field and field['group_id'] in matched_indices:
            field['group_id'] = matched_indices[field['group_id']]

    return extra_fields_groups_sorted, extrat_fields_sorted


def merge_jsonfiles(jsonfile_list_sorted: List[str], json_output: str, dry_run: bool = False,
                    compact: bool = False):
    """
    Merge multiple JSON files into one.
    Args:
        jsonfile_list_sorted (List[str]): List of JSON files to merge.
        json_output (str): Output file path.
        dry_run (bool): If True, preview changes without saving.
        compact (bool): If True, save output in compact format.
    """
    base_data = safe_load_json(jsonfile_list_sorted[0])
    main_extra_fields_groups = base_data['elabftw']['extra_fields_groups']
    main_extrat_fields = base_data['extra_fields']
    indice = get_indices(main_extra_fields_groups)

    for jsonfile in tqdm(jsonfile_list_sorted[1:], desc="Merging JSON files"):
        extra_fields_groups, extrat_fields = get_a_jsonfile_structure(jsonfile)
        updated_groups, updated_fields = replace_id(extra_fields_groups, extrat_fields, indice)
        main_extra_fields_groups.extend(updated_groups)
        main_extrat_fields.update(updated_fields)
        indice = max(group['id'] for group in main_extra_fields_groups) + 1

    base_data['elabftw']['extra_fields_groups'] = main_extra_fields_groups
    base_data['extra_fields'] = main_extrat_fields

    if dry_run:
        logger.info("Dry run mode enabled. Changes not saved.")
        logger.info(json.dumps(base_data, indent=4 if not compact else None))
    else:
        with open(json_output, 'w') as f:
            json.dump(base_data, f, indent=None if compact else 4)
        logger.info(f"Output written to {json_output}")


def main():
    # Argument parser initialization
    parser = argparse.ArgumentParser(
        description=(
            "This script merges multiple JSON files into a single output file. "
            "Provide a list of JSON files and the name of the output file."
        ),
        epilog=(
            "Examples:\n"
            "  python Merge.py file1.json file2.json output.json\n"
            "  python Merge.py file1.json file2.json output.json --dry-run\n"
            "  python Merge.py file1.json file2.json output.json --overwrite\n\n"
            "Options:\n"
            "  --dry-run   Preview the result without saving.\n"
            "  --compact   Save the output JSON in a compact format (without extra spaces).\n"
            "  --overwrite Overwrite the output file if it already exists."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--sorted_list_input_files", nargs="+", help="List of JSON files to merge", type=str,
                        required=True)
    parser.add_argument("--output", help="Name of the output JSON file", type=str, required=True)
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without saving")
    parser.add_argument("--compact", action="store_true", help="Save output JSON in compact format")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite the output file if it exists")

    args = parser.parse_args()
    list_of_files = [file for file in args.sorted_list_input_files if file.endswith('.json')]
    if not list_of_files:
        raise ValueError("No valid JSON files found in the input list.")

    output_file = args.output if args.output.endswith('.json') else args.output + '.json'

    if not args.overwrite and os.path.exists(output_file):
        raise FileExistsError(
            f"Output file {output_file} already exists. Use --overwrite to overwrite.")

    merge_jsonfiles(list_of_files, output_file, dry_run=args.dry_run, compact=args.compact)


if __name__ == "__main__":
    main()
