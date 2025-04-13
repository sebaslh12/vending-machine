# Vending Machine Exercise

A Python-based vending machine simulator that handles product selection, money insertion, and change calculation.

## Features

- Product management with prices and stock levels
- Coin-based payment system (accepts 1p, 2p, 5p, 10p, 20p, 50p, £1, £2)
- Change calculation and dispensing
  - Rollback operations due to lack of change
- Stock and Change reloading with _authentication_
- Persistent storage of products and change
- Command-line interface

## Requirements

- Python 3.10+ (for match-case statements)
- Authentication module (for admin functions)

## Usage

### Running the Machine

#### Docker
There is a Dockerfile ready to be use, just run

```bash
  docker build -t vending-machine .
  docker run --name vending-machine-app vending-machine
```

If the container already exists:
```bash
  docker start -ai vending-machine-app
```

#### Local

It is advised to create a [virtual env](https://docs.astral.sh/uv/pip/environments/) that matches the python min version requirement:
```bash
python vending_machine.py
```


If either of the files (products or change) is not provided, the machine will be initialized with a default state:
- Empty products: it won't be able to sell
- Empty change: it will allow buying products if the inserted amount is the exact value

### Customer Operations

1. Select "Buy Product" (Option 1)
    - Choose a product by number
    - Insert coins when prompted
    - Give product and return change (if applicable)

### Admin Operations

Protected by authentication decorator:

- Reload Products (Option 2)
- Reload Change (Option 3)

#### Auth Decorator
The auth decorator is meant to hold whichever the auth logic is depending on the context where the machine is going to be used/part of.
For demonstration purposes that logic is omitted.

### Data Storage

Products and change are stored in JSON files:
- `products.json`: Stores product information (name, price, quantity)
- `change.json`: Stores available coins for change

After exiting the machine interface it will save its current state into these files. The storage module was added to make the machine agnostic of what type of storage is being used.

## Testing

Run the test suite:

```bash
python -m unittest discover tests
```

## Class Structure

### VendingMachine

Main class that handles:
- Product management
- Money handling
- User interaction
- Transaction processing
- Change calculation

### Key Methods

- `start()`: Main menu loop
- `buy_product()`: Handles purchase flow
- `insert_money()`: Processes coin insertion
- `give_change()`: Calculates and returns change
- `reload_products_menu()`: Admin interface for restocking
- `reload_change_menu()`: Admin interface for adding coins

## Error Handling

- Invalid coin detection
- Insufficient change scenarios
- Out-of-stock products
- Invalid user input
- File I/O errors

## Future Improvements

- Add a product size restriction: Machines should have a maximum product allocation, after that limit is reached no products can be added only swap is allowed.
- Allow coins to be inserted before the product selection, given the requirements this was not included but it could be a feature added to the machine.
- Card payment support: as the implementation goes adding a new payment method will require changing the function called when selecting the buy product option
- Sales reporting: As it will form part of a more complex system, each machine should be able to report sales given a cycle (daily, weekly)
 - Transaction Logger: This will provided a more atomic report of each of the operations that have taken place
- Inventory Manager: For maintenance puporses is useful to keep track of what has been bought and what products are running out (to potentially send alerts).
- Adding an actual admin interface/dashboard that gives access to some of the functionalities previously listed and also to better protect non-customer actions
