import math
import hashlib


class Calculator:
    """
    Demonstrates function overloading and mathematical functions.
    """

    def __init__(self):
        print("Calculator initialized.")

    # --- Function Overloading ---
    def add(self, a, b=None, c=None):
        """
        Adds one, two, or three numbers.
        """
        if c is not None:
            print(f"\n--- Calling add({a}, {b}, {c}) ---")
            result = a + b + c
            print(f"Sum of three numbers: {result}")
            return result

        elif b is not None:
            print(f"\n--- Calling add({a}, {b}) ---")
            result = a + b
            print(f"Sum of two numbers: {result}")
            return result

        else:
            print(f"\n--- Calling add({a}) ---")
            result = a + 10
            print(f"Adding 10 to single number: {result}")
            return result

    # --- Mathematical Functions ---
    def perform_math_operations(self, x, y, k):
        print(f"\n--- Math Operations (x={x}, y={y}, k={k}) ---")

        print(f"Addition: {x + y}")
        print(f"Subtraction: {x - y}")
        print(f"Multiplication: {x * y}")

        if y != 0:
            print(f"Division: {x / y}")
            print(f"Integer Division: {x // y}")
            print(f"Modulo: {x % y}")
        else:
            print("Division/Modulo by zero not allowed.")

        if k != 0:
            print(f"(x+y)%k = {(x + y) % k}")
            print(f"(x*y)%k = {(x * y) % k}")
        else:
            print("Modulus cannot be zero.")

        print(f"Power: {x ** y}")
        print(f"Square Root: {math.sqrt(abs(x))}")
        print("-" * 30)


class CryptographicFunctions:
    """
    Demonstrates cryptographic hashing functions.
    """

    def __init__(self):
        print("Crypto utility initialized.")

    def generate_sha256_hash(self, data_string):
        print(f"\n--- SHA256 for '{data_string}' ---")

        hashed_data = hashlib.sha256(
            data_string.encode('utf-8')
        ).hexdigest()

        print(f"Hash: {hashed_data}")
        return hashed_data

    def demonstrate_avalanche_effect(self, base_string):
        print("\n--- Avalanche Effect ---")

        hash1 = self.generate_sha256_hash(base_string)

        changed = base_string + "a"
        hash2 = self.generate_sha256_hash(changed)

        print(f"Hash1: {hash1}")
        print(f"Hash2: {hash2}")
        print(f"Different: {hash1 != hash2}")
        print("-" * 30)

    def simple_password_hasher(self, password):
        print("\n--- Password Hashing ---")

        salt = hashlib.sha256(
            b"my_random_salt_for_security"
        ).hexdigest().encode('utf-8')

        hashed_password = hashlib.sha256(
            password.encode('utf-8') + salt
        ).hexdigest()

        print(f"Password: {password}")
        print(f"Hash: {hashed_password}")

        return hashed_password


# ---------------- DEMO ----------------
print("--- Practical 3b Demo ---")

calc = Calculator()

calc.add(5)
calc.add(5, 10)
calc.add(5, 10, 15)

calc.perform_math_operations(10, 3, 7)
calc.perform_math_operations(15, 0, 5)
calc.perform_math_operations(2, 4, 10)

crypto_util = CryptographicFunctions()

crypto_util.generate_sha256_hash("Hello Blockchain")
crypto_util.generate_sha256_hash("The quick brown fox jumps over the lazy dog")
crypto_util.generate_sha256_hash("The quick brown fox jumps over the lazy cog")

crypto_util.demonstrate_avalanche_effect("secret phrase")

crypto_util.simple_password_hasher("mySecretPass123!")
crypto_util.simple_password_hasher("mySecretPass123!")
crypto_util.simple_password_hasher("anotherPassword")

print("\n--- Demonstration Complete ---")
