import datetime


class SmartContractSimulation:
    """
    A Python class to conceptually simulate a Solidity smart contract's function types.
    """

    def __init__(self, initial_data=100):
        # State variable
        self.stored_data = initial_data
        print(f"Contract initialized with stored_data: {self.stored_data}")

    # --- Regular Function (Modifies State) ---
    def set_data(self, new_value):
        """
        Modifies stored_data (like Solidity state-changing function)
        """
        print(f"\n--- Calling regular function: set_data({new_value}) ---")
        old_value = self.stored_data
        self.stored_data = new_value
        print(f"Stored data updated from {old_value} to {self.stored_data}")

    # --- View Functions (Read Only) ---
    def get_data(self):
        """
        Reads stored_data without modifying it
        """
        print(f"\n--- Calling view function: get_data() ---")
        print(f"Current stored data: {self.stored_data}")
        return self.stored_data

    def get_status(self):
        """
        Returns combined status info
        """
        print(f"\n--- Calling view function: get_status() ---")
        status = f"Data: {self.stored_data}, Time: {datetime.datetime.now()}"
        print(f"Status report: {status}")
        return status

    # --- Pure Function (No State Access) ---
    @staticmethod
    def calculate_sum(a, b):
        """
        Pure function (no state interaction)
        """
        print(f"\n--- Calling pure function: calculate_sum({a}, {b}) ---")
        result = a + b
        print(f"Result: {result}")
        return result

    # --- Fallback Simulation ---
    def __getattr__(self, name):
        """
        Handles undefined method calls
        """
        print(f"\n--- Fallback triggered for method: {name} ---")

        def method_not_found(*args, **kwargs):
            print(f"Warning: Method '{name}' does not exist.")
            print(f"Args: {args}, Kwargs: {kwargs}")
            return None

        return method_not_found

    # --- Callable Instance ---
    def __call__(self, *args, **kwargs):
        """
        Simulates direct contract call
        """
        print(f"\n--- Instance called directly ---")
        print("Simulating direct interaction or value transfer")
        print(f"Args: {args}, Kwargs: {kwargs}")


# ---------------- DEMO ----------------
print("--- Practical 3a: Function Types Demonstration ---")

# Create contract
my_contract = SmartContractSimulation()

# 1. Regular function
my_contract.set_data(250)
my_contract.set_data(75)

# 2. View functions
current_data = my_contract.get_data()
status_report = my_contract.get_status()

# 3. Pure function
pure_result = SmartContractSimulation.calculate_sum(10, 20)
another_pure_result = SmartContractSimulation.calculate_sum(current_data, 50)

# 4. Fallback simulation
my_contract.non_existent_method("hello", 123, option="test")

# Direct call
my_contract("direct_call_data", amount=10)

print("\n--- Demonstration Complete ---")
print(f"Final stored_data value: {my_contract.stored_data}")
