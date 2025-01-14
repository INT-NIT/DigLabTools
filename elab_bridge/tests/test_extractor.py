import unittest
import json
import os
from tempfile import NamedTemporaryFile
from elab_bridge.Extractor import (
    loadfile,
    savefile,
    extract_groupfield_detail,
    construct_extracted_json,
    add_a_groupfield,
    complete_groupfield_in_jsonfile,
    complete_jsonfile1_with_jsonfile2_groupefield,
    orderjsonfile,
)


class TestJsonOperations(unittest.TestCase):

    def setUp(self):
        """Setup temporary JSON files for testing."""
        self.temp_file = NamedTemporaryFile(delete=False, mode='w+', suffix='.json')
        self.sample_json = {
            "elabftw": {
                "extra_fields_groups": [
                    {"id": 1, "name": "Group 1"},
                    {"id": 2, "name": "Group 2"}
                ]
            },
            "extra_fields": {
                "field_1": {"group_id": "1", "value": "Test 1"},
                "field_2": {"group_id": "2", "value": "Test 2"}
            }
        }
        json.dump(self.sample_json, self.temp_file)
        self.temp_file.close()

    def tearDown(self):
        """Clean up temporary files."""
        os.unlink(self.temp_file.name)

    def test_loadfile(self):
        """Test loading a valid JSON file."""
        data = loadfile(self.temp_file.name)
        self.assertEqual(data, self.sample_json)

    def test_loadfile_invalid(self):
        """Test loading an invalid JSON file."""
        with open(self.temp_file.name, 'w') as f:
            f.write("{invalid_json")
        with self.assertRaises(ValueError):
            loadfile(self.temp_file.name)

    def test_savefile(self):
        """Test saving data to a JSON file."""
        test_data = {"test": "data"}
        savefile(self.temp_file.name, test_data)
        with open(self.temp_file.name, 'r') as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, test_data)

    def test_extract_groupfield_detail(self):
        """Test extracting groupfield details."""
        group_name, fields = extract_groupfield_detail(self.temp_file.name, 1)
        self.assertEqual(group_name, "Group 1")
        self.assertEqual(fields, [{"field_1": {"group_id": None, "value": "Test 1"}}])

    def test_construct_extracted_json(self):
        """Test constructing extracted JSON."""
        output_file = NamedTemporaryFile(delete=False, mode='w+', suffix='.json')
        result = construct_extracted_json(self.temp_file.name, 1, 10, output_file.name)
        print(result, "resultssss")
        self.assertEqual(
            result["elabftw"]["extra_fields_groups"],
            [{"id": 10, "name": "Group 1"}]
        )
        os.unlink(output_file.name)


    def test_orderjsonfile(self):
        """Test ordering JSON file."""
        # Define ordered group names
        ordered_groups = ["Group 2", "Group 1"]

        # Call the function with valid inputs
        ordered_data = orderjsonfile(self.temp_file.name, ordered_groups)
        print(ordered_data, "ordered_data")
        # Assert ordered_data is not None
        self.assertIsNotNone(ordered_data, "ordered_data is None")

        # Assert 'elabftw' exists in the result
        self.assertIn("elabftw", ordered_data, "'elabftw' key is missing in ordered_data")

        # Assert 'extra_fields_groups' exists and is a list
        self.assertIn("extra_fields_groups", ordered_data["elabftw"],
                      "'extra_fields_groups' key is missing in ordered_data['elabftw']")
        self.assertIsInstance(ordered_data["elabftw"]["extra_fields_groups"], list,
                              "'extra_fields_groups' is not a list")

        # Check that all groups are ordered correctly
        for i, group_name in enumerate(ordered_groups):
            self.assertEqual(ordered_data["elabftw"]["extra_fields_groups"][i]["name"], group_name,
                             f"Group {i} is not ordered correctly")

        # Additional debug print (optional)
        print(
            f"Ordered data groups: {[group['name'] for group in ordered_data['elabftw']['extra_fields_groups']]}")


if __name__ == '__main__':
    unittest.main()
