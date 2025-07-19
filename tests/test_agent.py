import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

# Add project root to the Python path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generate_kb import app

class TestE2EAgent(unittest.TestCase):

    def setUp(self):
        """Set up a test runner and temporary directories."""
        self.runner = CliRunner()
        self.test_sf_path = os.path.join('tests', 'data', 'force-app')
        self.test_db_path = os.path.join('tests', 'temp_chroma_db')
        # Ensure the test directory exists
        os.makedirs(self.test_sf_path, exist_ok=True)
        # Clean up any previous DB runs
        if os.path.exists(self.test_db_path):
            shutil.rmtree(self.test_db_path)

    def tearDown(self):
        """Clean up temporary directories."""
        if os.path.exists(self.test_db_path):
            shutil.rmtree(self.test_db_path)

    @patch('agno.llms.openai.OpenAI.get_chat_response')
    @patch('agno.embeddings.openai.OpenAIEmbedder.get_embedding')
    @patch('rich.prompt.Prompt.ask', side_effect=['What about AccountNumber?', 'exit'])
    def test_fill_and_chat_e2e(self, mock_ask, mock_get_embedding, mock_get_chat_response):
        """Tests the full end-to-end flow: filling the DB and then chatting with it."""
        # --- Arrange Mocks ---
        # Mock the summarization call
        mock_get_chat_response.return_value = "This is a mock summary for the AccountNumber field."
        # Mock the embedding call
        mock_get_embedding.return_value = [0.1, 0.2, 0.3, 0.4, 0.5] # Dummy embedding

        # --- 1. Fill the Knowledge Base ---
        fill_result = self.runner.invoke(
            app, 
            ["fill", "--sf-project-path", self.test_sf_path, "--db-path", self.test_db_path],
            catch_exceptions=False
        )
        
        # --- Fill Assertions ---
        self.assertEqual(fill_result.exit_code, 0, msg=fill_result.stdout)
        self.assertIn("Knowledge base created successfully", fill_result.stdout)
        # Verify that the database directory was actually created on disk
        self.assertTrue(os.path.exists(self.test_db_path))
        # Verify that the LLM was called for summarization
        self.assertTrue(mock_get_chat_response.called)

        # --- 2. Chat with the Agent ---
        # We need a new mock for the final answer generation
        with patch('agno.agent.Agent.print_response') as mock_print_response:
            chat_result = self.runner.invoke(
                app, 
                ["chat", "--db-path", self.test_db_path],
                catch_exceptions=False
            )

            # --- Chat Assertions ---
            self.assertEqual(chat_result.exit_code, 0, msg=chat_result.stdout)
            self.assertIn("Initializing Salesforce Chat Agent", chat_result.stdout)
            # Check that the agent was asked our question
            mock_print_response.assert_called_once_with('What about AccountNumber?')

if __name__ == '__main__':
    unittest.main()