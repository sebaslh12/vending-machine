import unittest
import json
from unittest.mock import patch, mock_open
from store.products import get_products_from_file, save_products_to_file

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.test_product = {"Soda": {"price": 150, "quantity": 9}, "Candy": {"price": 65, "quantity": 19}}
        self.test_file_content = json.dumps(self.test_product)

    @patch("builtins.open", new_callable=mock_open, read_data='{"Soda": {"price": 150, "quantity": 9}, "Candy": {"price": 65, "quantity": 19}}')
    def test_get_products_from_file(self, mock_file):
        """Test reading product from file"""
        result = get_products_from_file()

        # Verify file was opened for reading
        mock_file.assert_called_once()
        # Verify the contents were parsed correctly
        self.assertEqual(result, self.test_product)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_products_to_file(self, mock_file):
        """Test saving product to file"""
        save_products_to_file(self.test_product)

        # Verify file was opened for writing
        mock_file.assert_called_once()
        # Get the data that was written
        written_calls = mock_file().write.call_args_list

        written_data = ''.join(call.args[0] for call in written_calls)

        # Verify the written data matches our test data
        self.assertEqual(json.loads(written_data), self.test_product)

    @patch("builtins.open")
    def test_get_product_file_not_found(self, mock_file):
        """Test handling of missing file"""
        mock_file.side_effect = FileNotFoundError
        result = get_products_from_file()
        self.assertEqual(result, {})

    @patch("builtins.open")
    def test_get_product_invalid_json(self, mock_file):
        """Test handling of invalid JSON"""
        mock_file.return_value.__enter__.return_value.read.return_value = "invalid json"
        result = get_products_from_file()
        self.assertEqual(result, {})

    def test_get_product_with_custom_path(self):
        """Test reading from custom file path"""
        test_path = "custom_product.json"
        with patch("builtins.open", new_callable=mock_open, 
                  read_data=self.test_file_content):
            result = get_products_from_file(test_path)
            self.assertEqual(result, self.test_product)

if __name__ == '__main__':
    unittest.main()