import unittest
from unittest.mock import patch
from vending_machine import VendingMachine

class TestVendingMachine(unittest.TestCase):
    def setUp(self):
        """Set up a new VendingMachine instance before each test"""
        self.vm = VendingMachine()
        self.test_products = {
            "Cola": {"price": 150, "quantity": 5},
            "Chips": {"price": 100, "quantity": 3}
        }
        self.test_change = {1: 10, 2: 10, 5: 10, 10: 10,
                           20: 10, 50: 10, 100: 10, 200: 10}

    def test_load_products(self):
        """Test loading products into the vending machine"""
        self.vm.load_products(self.test_products)
        self.assertEqual(len(self.vm.products), 2)
        self.assertEqual(self.vm.products["Cola"]["price"], 150)
        self.assertEqual(self.vm.products["Chips"]["quantity"], 3)

    def test_load_products_invalid_price(self):
        """Test loading products with invalid price"""
        invalid_products = {"Invalid": {"price": -10, "quantity": 1}}
        self.vm.load_products(invalid_products)
        self.assertEqual(len(self.vm.products), 0)

    def test_load_products_invalid_quantity(self):
        """Test loading products with invalid quantity"""
        invalid_products = {"Invalid": {"price": 10, "quantity": -1}}
        self.vm.load_products(invalid_products)
        self.assertEqual(len(self.vm.products), 0)

    def test_load_change(self):
        """Test loading change into the vending machine"""
        self.vm.load_change(self.test_change)
        self.assertEqual(self.vm.change[100], 10)
        self.assertEqual(sum(self.vm.change.values()), 80)

    @patch('builtins.input', side_effect=['1'])
    def test_select_product(self, mock_input):
        """Test product selection with mocked input"""
        self.vm.load_products(self.test_products)
        selected = self.vm.select_product()
        self.assertEqual(selected[0], "Cola")
        self.assertEqual(selected[1]["price"], 150)

    def test_give_change(self):
        """Test giving change functionality"""
        self.vm.load_change(self.test_change)
        change = self.vm.give_change(85)
        self.assertIsNotNone(change)
        self.assertEqual(sum(coin * count for coin, count in change.items()), 85)

    def test_give_change_insufficient(self):
        """Test giving change when insufficient coins available"""
        self.vm.change = {1: 0, 2: 0, 5: 0, 10: 0,
                         20: 0, 50: 0, 100: 0, 200: 0}
        change = self.vm.give_change(50)
        self.assertIsNone(change)

    @patch('builtins.input', side_effect=['4'])
    @patch('vending_machine.save_products_to_file')
    @patch('vending_machine.save_change_to_file')
    def test_start_exit(self, mock_input, mock_save_products, mock_save_change):
        """Test exit option in start menu"""
        with self.assertRaises(SystemExit):
            self.vm.start()

if __name__ == '__main__':
    unittest.main()