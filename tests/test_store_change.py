import unittest
import json
from unittest.mock import patch, mock_open
from store.change import get_change_from_file, save_change_to_file

class TestChange(unittest.TestCase):
    def setUp(self):
        self.test_change = {1: 10, 2: 5, 5: 3, 10: 2}
        self.test_file_content = json.dumps(self.test_change)

    @patch("builtins.open", new_callable=mock_open, read_data='{"1": 10, "2": 5, "5": 3, "10": 2}')
    def test_get_change_from_file(self, mock_file):
        """Test reading change from file"""
        result = get_change_from_file()

        # Verify file was opened for reading
        mock_file.assert_called_once()
        # Verify the contents were parsed correctly
        self.assertEqual(result, self.test_change)
        # Verify keys were converted to integers
        self.assertTrue(all(isinstance(k, int) for k in result.keys()))

    @patch("builtins.open", new_callable=mock_open)
    def test_save_change_to_file(self, mock_file):
        """Test saving change to file"""
        save_change_to_file(self.test_change)

        # Verify file was opened for writing
        mock_file.assert_called_once()
        # Get the data that was written
        written_calls = mock_file().write.call_args_list

        written_data = ''.join(call.args[0] for call in written_calls)
        written_dict = {int(key): val for key,val in json.loads(written_data).items()}
        # Verify the written data matches our test data
        self.assertEqual(written_dict, self.test_change)

    @patch("builtins.open")
    def test_get_change_file_not_found(self, mock_file):
        """Test handling of missing file"""
        mock_file.side_effect = FileNotFoundError
        result = get_change_from_file()
        self.assertEqual(result, {})

    @patch("builtins.open")
    def test_get_change_invalid_json(self, mock_file):
        """Test handling of invalid JSON"""
        mock_file.return_value.__enter__.return_value.read.return_value = "invalid json"
        result = get_change_from_file()
        self.assertEqual(result, {})

    def test_get_change_with_custom_path(self):
        """Test reading from custom file path"""
        test_path = "custom_change.json"
        with patch("builtins.open", new_callable=mock_open, 
                  read_data=self.test_file_content):
            result = get_change_from_file(test_path)
            self.assertEqual(result, self.test_change)

if __name__ == '__main__':
    unittest.main()