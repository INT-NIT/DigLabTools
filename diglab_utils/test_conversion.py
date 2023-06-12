import json

from diglab_utils.conversion import conversion_csv_to_json
from diglab_utils.test_utils import test_directory, initialize_test_dir


def test_conversion_csv_to_json(initialize_test_dir):

    test_dir = test_directory / 'testfiles_redcap' / 'elabConversion'

    f = open(test_dir / 'elabFinal.json')
    elab_final = json.load(f)
    elab_conversion = conversion_csv_to_json(test_dir / 'csvRecord.csv')
    assert elab_conversion == elab_final