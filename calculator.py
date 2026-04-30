def add(x: float, y: float) -> float:
    return x + y
def subtraction(x: float, y: float) -> float:
    return x - y
def multiply(x: float, y: float) -> float:
    return x * y
def division(x: float, y: float) -> float:
    return x / y
def divide(x: float, y: float) -> float:
    if y == 0:
        return "Error! Division by zero."
    return x / y
def main()
    Print("---Haw Beginner Calculator---")
    While True:
    print("\nOption: +, -, *, / or 'q' to quit")
    choice = input("enter Operation: ").lower()
    if choice == 'q':
        print("Closing the calculator. Goodbye!")
        breakpoint()
        if choice in ('+', '-', '*', '/'):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except valueerror:
                print





