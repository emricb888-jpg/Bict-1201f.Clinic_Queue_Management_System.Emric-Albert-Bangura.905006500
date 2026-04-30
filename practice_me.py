def add(x: float, y: float) -> float:
    """Adds two numbers."""
    return x + y


def subtract(x: float, y: float) -> float:
    """Subtracts y from x."""
    return x - y


def multiply(x: float, y: float) -> float:
    """Multiplies two numbers."""
    return x * y


def divide(x: float, y: float) -> float:
    """Divides x by y. Includes a check for division by zero."""
    if y == 0:
        return "Error! Division by zero."
    return x / y


def main():
    print("--- PyCharm Beginner Calculator ---")

    while True:
        print("\nOptions: +, -, *, /, or 'q' to quit")
        choice = input("Enter operation: ").lower()

        if choice == 'q':
            print("Closing the calculator. Goodbye!")
            break

        if choice in ('+', '-', '*', '/'):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input! Please enter numeric values.")
                continue

            if choice == '+':
                print(f"Result: {add(num1, num2)}")
            elif choice == '-':
                print(f"Result: {subtract(num1, num2)}")
            elif choice == '*':
                print(f"Result: {multiply(num1, num2)}")
            elif choice == '/':
                print(f"Result: {divide(num1, num2)}")
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()