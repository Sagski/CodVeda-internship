# -- SIMPLE CALCULATOR PERFORMING 4 PRIMARY OPERATIONS --


"""
Functional Calculator
----------------------
Implements core arithmetic operations (add, subtract, multiply, divide,
modulus, exponent) using basic functions and control flow.
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b




def get_number(prompt):
    """Keep asking until the user enters a valid number."""
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_operation():
    """Display menu and return a valid operation choice."""
    menu = """
Select an operation:
1. Add (+)
2. Subtract (-)
3. Multiply (*)
4. Divide (/)
5. Quit
"""
    valid_choices = {"1", "2", "3", "4", "5"}
    while True:
        print(menu)
        choice = input("Enter choice (1-5): ").strip()
        if choice in valid_choices:
            return choice
        print("Invalid choice. Please select a number from 1 to 5.")


def calculate(choice, a, b):
    """Dispatch to the correct operation based on choice."""
    operations = {
        "1": ("+", add),
        "2": ("-", subtract),
        "3": ("*", multiply),
        "4": ("/", divide),
       
    }
    symbol, func = operations[choice]
    result = func(a, b)
    return symbol, result


def main():
    print("=== Simple Calculator ===")
    while True:
        choice = get_operation()

        if choice == "5":
            print("Goodbye!")
            break

        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")

        try:
            symbol, result = calculate(choice, a, b)
            print(f"\nResult: {a} {symbol} {b} = {result}\n")
        except ZeroDivisionError as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()