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
                "field_1": {"group_id": 1, "value": "Test 1"},
                "field_2": {"group_id": 2, "value": "Test 2"}
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

    def test_add_a_groupfield(self):
        """Test adding groupfields at various indices."""
        # Define new groupfields
        new_field1 = [{"field_3": {"group_id": 2, "value": "Test 3"}}]
        groupe_name1 = "new group 1"

        new_field2 = [{"field_4": {"group_id": 5, "value": "Test 4"}}]
        groupe_name2 = "middle group"

        new_field3 = [{"field_5": {"group_id": 10, "value": "Test 5"}}]
        groupe_name3 = "final group"

        # Add a groupfield at index 1
        result1 = add_a_groupfield(self.temp_file.name, 1, new_field1, groupe_name1)

        # Add another groupfield in the middle (index 5)
        result2 = add_a_groupfield(self.temp_file.name, 5, new_field2, groupe_name2)

        # Add another groupfield at the final index (index 10)
        result3 = add_a_groupfield(self.temp_file.name, 10, new_field3, groupe_name3)

        # Assertions for the first group
        self.assertIn("elabftw", result1, "'elabftw' key missing in result")
        self.assertIn("extra_fields_groups", result1["elabftw"],
                      "'extra_fields_groups' key missing")
        self.assertTrue(
            any(group['id'] == 1 and group['name'] == groupe_name1 for group in
                result1["elabftw"]["extra_fields_groups"]),
            "New groupfield 1 not added"
        )
        self.assertIn("field_3", result1["extra_fields"], "'field_3' missing in extra_fields")
        self.assertEqual(result1["extra_fields"]["field_3"]["group_id"], 1,
                         "Incorrect group_id for field_3")

        # Assertions for the middle group
        self.assertTrue(
            any(group['id'] == 5 and group['name'] == groupe_name2 for group in
                result2["elabftw"]["extra_fields_groups"]),
            "Middle groupfield not added"
        )
        self.assertIn("field_4", result2["extra_fields"], "'field_4' missing in extra_fields")
        self.assertEqual(result2["extra_fields"]["field_4"]["group_id"], 5,
                         "Incorrect group_id for field_4")

        # Assertions for the final group
        self.assertTrue(
            any(group['id'] == 10 and group['name'] == groupe_name3 for group in
                result3["elabftw"]["extra_fields_groups"]),
            "Final groupfield not added"
        )
        self.assertIn("field_5", result3["extra_fields"], "'field_5' missing in extra_fields")
        self.assertEqual(result3["extra_fields"]["field_5"]["group_id"], 10,
                         "Incorrect group_id for field_5")

    def test_complete_jsonfile1_with_jsonfile2_groupefield(self):
        """Test combining two JSON files by extracting and adding group fields.
        This test does not mock other functions; instead, it tests the function as a whole.
        It qualifies as an integration test, verifying the interaction between all components.
        """

        # Define the source JSON file (to be completed)
        sample_json = {
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

        # Define the JSON file to extract data from
        sample_json2 = {
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

        # Create temporary files for testing
        jsonfiletocompleted = NamedTemporaryFile(delete=False, mode='w+', suffix='.json')
        json.dump(sample_json, jsonfiletocompleted)
        jsonfiletocompleted.close()

        jsonfiletoextract = NamedTemporaryFile(delete=False, mode='w+', suffix='.json')
        json.dump(sample_json2, jsonfiletoextract)
        jsonfiletoextract.close()

        # Define parameters for the function
        indice = 4
        new_indice = 1

        # Call the function under test
        json_completed = complete_jsonfile1_with_jsonfile2_groupefield(
            jsonfiletocompleted.name, jsonfiletoextract.name, indice, new_indice
        )

        # Define the expected result
        expected_json = {
            "elabftw": {
                "extra_fields_groups": [
                    {"id": 1, "name": "New group"},
                    {"id": 2, "name": "Group 1"},
                    {"id": 3, "name": "Group 2"}
                ]
            },
            "extra_fields": {
                "field_4": {"group_id": 1, "value": "New TEST"},
                "field_1": {"group_id": 2, "value": "Test 1"},
                "field_2": {"group_id": 3, "value": "Test 2"}
            }
        }

        # Validate the output
        self.assertEqual(json_completed, expected_json,
                         "The completed JSON does not match the expected structure.")

        # Clean up temporary files
        os.unlink(jsonfiletocompleted.name)
        os.unlink(jsonfiletoextract.name)


if __name__ == '__main__':
    unittest.main()
