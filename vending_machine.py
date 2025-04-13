import sys
from store.products import get_products_from_file, save_products_to_file
from store.change import get_change_from_file, save_change_to_file
from decorators.auth import auth_decorator

class VendingMachine:
    def __init__(self):
        self.products = {}  # name: {'price': price_in_pence, 'quantity': quantity}
        self.change = {1: 0, 2: 0, 5: 0, 10: 0, 20: 0, 50: 0, 100: 0, 200: 0}  # denomination in pence: count

    def load_products(self, products):
        ## check price to be greater than 0
        for name, info in products.items():
            if 'price' in info and info['price'] > 0 and 'quantity' in info and info['quantity'] > 0:
                self.products[name] = info
            else:
                print('Price and Quantity must be greater than 0')

    def load_change(self, coins):
        is_empty = True
        for coin, count in coins.items():
            if is_empty and count > 0:
                is_empty = False
            self.change[coin] += count
        if is_empty:
            print("\nNo change available, please insert exact values")

    def display_products(self, reloading=False):
        print("\nAvailable Products:")
        for idx, (name, info) in enumerate(self.products.items(), start=1):
            if info['quantity'] > 0 or reloading:
                print(f"{idx}. {name} - £{info['price'] / 100:.2f} ({info['quantity']} in stock)")
        print()

    def select_product(self):
        if not self.products:
            print("\nThere are no available Products, come back later")
            return None
        self.display_products()
        print('Type "exit" to go back')
        choice = input("Select a product by number: ")
        if choice == "exit":
            return None
        try:
            choice = int(choice)
            selected = list(self.products.items())[choice - 1]
            if selected[1]['quantity'] <= 0:
                print("Sorry, that product is out of stock.")
                return None
            return selected
        except (ValueError, IndexError):
            print("Invalid selection.")
            return None

    def insert_money(self, price):
        print(f"Insert coins to reach £{price/100:.2f}")
        inserted = 0
        while inserted < price:
            try:
                coin = int(input(f"Insert coin (1, 2, 5, 10, 20, 50, 100, 200 pence): "))
                if coin in self.change:
                    inserted += coin
                    self.change[coin] += 1
                    print(f"Total inserted: £{inserted/100:.2f}")
                else:
                    print("Invalid coin.")
            except ValueError:
                print("Please insert a valid number.")
        return inserted

    def give_change(self, amount):
        change_to_give = {}
        for coin in sorted(self.change.keys(), reverse=True):
            while amount >= coin and self.change[coin] > 0:
                amount -= coin
                self.change[coin] -= 1
                if coin in change_to_give:
                    change_to_give[coin] += 1
                else:
                    change_to_give[coin] = 1
        if amount == 0:
            return change_to_give
        else:
            print("Sorry, unable to provide exact change. Returning inserted coins.")
            # Roll back the change attempt
            for coin, count in change_to_give.items():
                self.change[coin] += count
            return None

    def buy_product(self):
        selection = self.select_product()
        if not selection:
            return

        name, info = selection
        price = info['price']
        inserted = self.insert_money(price)

        if inserted > price:
            change = inserted - price
            change_given = self.give_change(change)
            if change_given is None:
                print("Transaction cancelled. Please try again.")
                # Return inserted coins
                self.give_change(inserted)
                return None
            else:
                print("Change given:")
                for coin, count in change_given.items():
                    print(f"{count} x {coin}p")

        self.products[name]['quantity'] -= 1
        print(f"Dispensing {name}. Thank you for your purchase!")

    def exit(self):
        save_change_to_file(self.change)
        save_products_to_file(self.products)
        print("Goodbye!")
        sys.exit()

    def start(self):
        while True:
            print("\n--- Vending Machine ---")
            print("1. Buy Product")
            print("2. Reload Products")
            print("3. Reload Change")
            print("4. Exit")
            choice = input("Select an option: ")
            match choice:
                case '1':
                    self.buy_product()
                case '2':
                    self.reload_products_menu()
                case '3':
                    self.reload_change_menu()
                case '4':
                    self.exit()
                case _:
                    print("Invalid choice.")

    @auth_decorator
    def reload_products_menu(self):
        self.display_products(True)
        name = input("Enter product name: ")
        price = int(float(input("Enter product price (£): ")) * 100)
        quantity = int(input("Enter quantity: "))
        if price < 0 or quantity < 0:
            print(f"{name} not added, price and quantity must be greater than 0")
            return None
        self.load_products({name: {'price': price, 'quantity': quantity}})
        print(f"Loaded {quantity} x {name}(s) at £{price/100:.2f} each.")

    @auth_decorator
    def reload_change_menu(self):
        print("Reload change:")
        for coin in self.change.keys():
            amount = int(input(f"How many {coin}p coins to add?: "))
            self.change[coin] += amount
        print("Change reloaded.")


if __name__ == "__main__":
    vm = VendingMachine()
    vm.load_products(get_products_from_file())
    vm.load_change(get_change_from_file())
    vm.start()
