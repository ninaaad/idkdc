import Pyro5.api

def main():
    uri = input("Enter the server URI: ")
    calculator = Pyro5.api.Proxy(uri)

    while True:
        print("\nCalculator Operations:")
        print("Basic: add, subtract, multiply, divide")
        print("Scientific: sin, cos, tan, log, sqrt")
        print("Type 'exit' to quit")

        operation = input("Enter operation: ").strip().lower()
        if operation == 'exit':
            break

        if operation in ['add', 'subtract', 'multiply', 'divide']:
            try:
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                if operation == 'add':
                    result = calculator.add(a, b)
                elif operation == 'subtract':
                    result = calculator.subtract(a, b)
                elif operation == 'multiply':
                    result = calculator.multiply(a, b)
                elif operation == 'divide':
                    result = calculator.divide(a, b)
                print(f"Result: {result}")
            except ValueError:
                print("Invalid input. Please enter numbers.")
        elif operation in ['sin', 'cos', 'tan', 'log', 'sqrt']:
            try:
                x = float(input("Enter number: "))
                if operation == 'sin':
                    result = calculator.sin(x)
                elif operation == 'cos':
                    result = calculator.cos(x)
                elif operation == 'tan':
                    result = calculator.tan(x)
                elif operation == 'log':
                    result = calculator.log(x)
                elif operation == 'sqrt':
                    result = calculator.sqrt(x)
                print(f"Result: {result}")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("Unknown operation.")

if __name__ == "__main__":
    main()
