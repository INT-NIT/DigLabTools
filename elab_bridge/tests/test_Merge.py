import unittest
import tempfile
import os
import json
from elab_bridge.Merge import (
    safe_load_json,
    get_a_jsonfile_structure,
    get_indices,
    replace_id,
    merge_jsonfiles
)


class TestJSONMerge(unittest.TestCase):
    def setUp(self):
        """Set up temporary JSON files for testing."""
        self.temp_files = []
        self.sample_json1 = {
            "elabftw": {
                "extra_fields_groups": [
                    {"id": 1, "name": "Group 1"},
                    {"id": 2, "name": "Group 2"}
                ]
            },
            "extra_fields": {
                "field_1": {"group_id": 1, "value": "Test 1"},
                "field_2": {"group_id": 2, "value": "Test 2"}
            }
        }
        self.sample_json2 = {
            "elabftw": {
                "extra_fields_groups": [
                    {"id": 4, "name": "New group"},
                    {"id": 5, "name": "unwanted group"}
                ]
            },
            "extra_fields": {
                "field_4": {"group_id": 4, "value": "New TEST"},
                "field_5": {"group_id": 5, "value": "unwanted"}
            }
        }
        self.temp_files.append(self._create_temp_file(self.sample_json1))
        self.temp_files.append(self._create_temp_file(self.sample_json2))

    def tearDown(self):
        """Clean up temporary files."""
        for temp_file in self.temp_files:
            os.unlink(temp_file)

    def _create_temp_file(self, data):
        """Helper function to create a temporary file with JSON content."""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        with open(temp_file.name, 'w') as f:
            json.dump(data, f)
        return temp_file.name

    def test_safe_load_json(self):
        """Test safe loading of JSON files."""
        data = safe_load_json(self.temp_files[0])
        self.assertEqual(data, self.sample_json1)

    def test_get_a_jsonfile_structure(self):
        """Test extracting structure from a JSON file."""
        groups, fields = get_a_jsonfile_structure(self.temp_files[0])
        print(groups)
        print(fields)

        self.assertEqual(groups, [{"id": 1, "name": "Group 1"}, {"id": 2, "name": "Group 2"}])
        self.assertEqual(fields, {
            "field_1": {"group_id": 1, "value": "Test 1"},
            "field_2": {"group_id": 2, "value": "Test 2"}
        })

    def test_get_indices(self):
        """Test finding the next available index."""
        groups = [{"id": 1}, {"id": 2}]
        self.assertEqual(get_indices(groups), 3)
        self.assertEqual(get_indices([]), 1)

    def test_replace_id(self):
        """Test replacing IDs in groups and fields."""
        groups = [{"id": 1, "name": "Group 1"}]
        fields = {"field_1": {"group_id": 1, "value": "Value 1"}}
        new_groups, new_fields = replace_id(groups, fields, 10)
        expected_groups = [{"id": 10, "name": "Group 1"}]
        expected_fields = {"field_1": {"group_id": 10, "value": "Value 1"}}
        self.assertEqual(new_groups, expected_groups)
        self.assertEqual(new_fields, expected_fields)

    def test_merge_jsonfiles(self):
        """Test merging multiple JSON files into one."""
        json_output = tempfile.NamedTemporaryFile(delete=False, suffix=".json").name
        merge_jsonfiles(self.temp_files, json_output)
        with open(json_output, 'r') as f:
            merged_data = json.load(f)
        expected_data = {
            "elabftw": {
                "extra_fields_groups": [
                    {"id": 1, "name": "Group 1"},
                    {"id": 2, "name": "Group 2"},
                    {"id": 3, "name": "New group"},
                    {"id": 4, "name": "unwanted group"}
                ]
            },
            "extra_fields": {
                "field_1": {"group_id": 1, "value": "Test 1"},
                "field_2": {"group_id": 2, "value": "Test 2"},
                "field_4": {"group_id": 3, "value": "New TEST"},
                "field_5": {"group_id": 4, "value": "unwanted"}
            }
        }
        self.assertEqual(merged_data, expected_data)


if __name__ == "__main__":
    unittest.main()
