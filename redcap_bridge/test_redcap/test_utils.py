from redcap_bridge.utils import compress_record
from diglab_utils.test_utils import test_directory, initialize_test_dir


def test_compressedCSV(initialize_test_dir):

    test_dir = test_directory / 'testfiles' / 'compression_test'

    compress_record(test_dir / 'original_record.csv', test_dir / 'compressed_record.csv')
    with open(test_dir / 'compressed_record.csv') as comp_file:
        with open(test_dir / 'expected_record.csv') as exp_file:
            res = comp_file.read()
            exp = exp_file.read()
            assert res == exp

