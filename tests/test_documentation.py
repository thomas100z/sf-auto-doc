import os
import unittest
from main import main

class TestDocumentation(unittest.TestCase):
    def test_documentation_creation(self):
        # move to data directory
        test_data_dir = 'tests/data'
        base_path = os.path.join(test_data_dir, 'force-app/main/default/')
        output_dir = os.path.join(test_data_dir, 'docs')
        output_file = os.path.join(output_dir, 'Account.md')

        main('Account', output_dir, base_path, debug=True)

        # check if the documentation file was created
        self.assertTrue(os.path.exists(output_file), "Documentation file was not created.")

        with open(output_file, 'r') as f:
            content = f.read()

        self.assertIn('| Label | API Name | Type |', content, "Table header is missing.")
        self.assertIn('AccountNumber', content, "Table data is missing.")

        # clean up the created documentation file
        os.remove(output_file)
        os.rmdir(output_dir)

        # assert the file was deleted
        self.assertFalse(os.path.exists(output_file), "Documentation file was not deleted.")
        self.assertFalse(os.path.exists(output_dir), "Documentation directory was not deleted.")

    def test_all_objects_documentation_creation(self):
        # move to data directory
        test_data_dir = 'tests/data'
        base_path = os.path.join(test_data_dir, 'force-app/main/default/')
        output_dir = os.path.join(test_data_dir, 'docs')
        output_file = os.path.join(output_dir, 'Account.md')

        # Invoke main with 'All' to process all objects
        main('All', output_dir, base_path, debug=True)

        # check if the Account documentation file was created
        self.assertTrue(os.path.exists(output_file), "Documentation file for Account was not created.")

        with open(output_file, 'r') as f:
            content = f.read()

        self.assertIn('| Label | API Name | Type |', content, "Table header is missing in Account documentation.")
        self.assertIn('AccountNumber', content, "Table data is missing in Account documentation.")

        # clean up the created documentation file
        os.remove(output_file)
        os.rmdir(output_dir)

        # assert the file and directory were deleted
        self.assertFalse(os.path.exists(output_file), "Documentation file for Account was not deleted.")
        self.assertFalse(os.path.exists(output_dir), "Documentation directory was not deleted.")

if __name__ == "__main__":
    unittest.main()
