import os
import sys
import shutil
import unittest

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import main

class TestDocumentation(unittest.TestCase):
    def setUp(self):
        # Create test directories if they don't exist
        self.test_data_dir = 'tests/data'
        self.output_dir = os.path.join(self.test_data_dir, 'docs')
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def tearDown(self):
        # Clean up test directories after each test
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_documentation_creation(self):
        base_path = os.path.join(self.test_data_dir, 'force-app/main/default/')
        output_file = os.path.join(self.output_dir, 'Objects', 'Account.md')

        main('Account', self.output_dir, base_path, debug=True)

        # check if the documentation file was created
        self.assertTrue(os.path.exists(output_file), "Documentation file was not created.")

        with open(output_file, 'r') as f:
            content = f.read()

        # Check fields table
        self.assertIn('| Label | API Name | Type |', content, "Fields table header is missing.")
        self.assertIn('AccountNumber', content, "Fields table data is missing.")

        # Check validation rules table
        self.assertIn('| Name | Description | Formula |', content, "Validation rules table header is missing.")
        self.assertIn('dot_in_website', content, "Active validation rule is missing.")
        self.assertNotIn('Billing_Address_Required', content, "Inactive validation rule should not be included.")

    def test_all_objects_documentation_creation(self):
        base_path = os.path.join(self.test_data_dir, 'force-app/main/default/')
        output_file = os.path.join(self.output_dir, 'Objects', 'Account.md')

        # Invoke main with 'all' to process all objects
        main('all', self.output_dir, base_path, debug=True)

        # check if the Account documentation file was created
        self.assertTrue(os.path.exists(output_file), "Documentation file for Account was not created.")

        with open(output_file, 'r') as f:
            content = f.read()

        # Check fields table
        self.assertIn('| Label | API Name | Type |', content, "Fields table header is missing in Account documentation.")
        self.assertIn('AccountNumber', content, "Fields table data is missing in Account documentation.")

        # Check validation rules table
        self.assertIn('| Name | Description | Formula |', content, "Validation rules table header is missing in Account documentation.")
        self.assertIn('dot_in_website', content, "Active validation rule is missing in Account documentation.")
        self.assertNotIn('Billing_Address_Required', content, "Inactive validation rule should not be included in Account documentation.")

if __name__ == "__main__":
    unittest.main()
