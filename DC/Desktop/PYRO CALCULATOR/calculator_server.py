import Pyro5.api
import math

@Pyro5.api.expose
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return "Division by zero error"
        return a / b

    def sin(self, x):
        return math.sin(math.radians(x))  # Assuming input in degrees

    def cos(self, x):
        return math.cos(math.radians(x))

    def tan(self, x):
        return math.tan(math.radians(x))

    def log(self, x):
        if x <= 0:
            return "Logarithm undefined for non-positive numbers"
        return math.log(x)  # Natural log

    def sqrt(self, x):
        if x < 0:
            return "Square root undefined for negative numbers"
        return math.sqrt(x)

def main():
    daemon = Pyro5.api.Daemon()
    calculator = Calculator()
    uri = daemon.register(calculator, "calculator")
    print("Calculator server is running.")
    print("Server URI:", uri)
    print("Share this URI with the client to connect.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
