from abc import ABC, abstractmethod


# ==================== BASE CONTRACT ====================
class BaseContract:
    def __init__(self, initial_value):
        self.contract_id = id(self)
        self.data_storage = initial_value

        print(
            f"BaseContract (ID: {self.contract_id}) initialized "
            f"with data: {self.data_storage}"
        )

    def get_data(self):
        print(
            f"BaseContract (ID: {self.contract_id}): "
            f"Retrieving data: {self.data_storage}"
        )
        return self.data_storage

    def _internal_helper(self, a, b):
        result = a * b
        print(f"Internal helper: {a} * {b} = {result}")
        return result

    def get_type(self):
        return "BaseContract"


# ==================== DERIVED CONTRACT ====================
class DerivedContract(BaseContract):
    def __init__(self, initial_value, message):
        super().__init__(initial_value)
        self.derived_message = message

        print(
            f"DerivedContract (ID: {self.contract_id}) "
            f"initialized with message: '{self.derived_message}'"
        )

    def get_derived_info(self):
        info = f"Message: {self.derived_message}, Data: {self.data_storage}"
        print(info)
        return info

    def use_base_internal(self, x, y):
        print("Calling base internal helper...")
        return self._internal_helper(x, y)

    def get_type(self):
        return "DerivedContract"


# ==================== INTERFACE ====================
class IToken(ABC):

    @abstractmethod
    def get_total_supply(self):
        pass

    @abstractmethod
    def get_balance(self, address):
        pass

    @abstractmethod
    def transfer(self, sender, receiver, amount):
        pass


# ==================== ABSTRACT CONTRACT ====================
class AbstractERC20Token(IToken):
    def __init__(self, initial_supply, name, symbol):
        self._total_supply = initial_supply
        self._name = name
        self._symbol = symbol
        self._balances = {}

        self._balances["deployer_address"] = initial_supply

        print(
            f"\nToken Initialized: {name} ({symbol}) "
            f"Supply: {initial_supply}"
        )

    def get_total_supply(self):
        return self._total_supply

    @abstractmethod
    def get_balance(self, address):
        pass

    def get_token_info(self):
        return f"{self._name} ({self._symbol}) - Supply: {self._total_supply}"


# ==================== CONCRETE TOKEN ====================
class MyERC20Token(AbstractERC20Token):

    def __init__(self, initial_supply, name, symbol):
        super().__init__(initial_supply, name, symbol)
        print("Concrete token initialized.")

    def get_balance(self, address):
        return self._balances.get(address, 0)

    def transfer(self, sender, receiver, amount):
        print(f"\nTransfer: {sender} → {receiver} ({amount})")

        if self._balances.get(sender, 0) >= amount:
            self._balances[sender] -= amount
            self._balances[receiver] = self._balances.get(receiver, 0) + amount

            print(
                f"Success! Sender: {self.get_balance(sender)}, "
                f"Receiver: {self.get_balance(receiver)}"
            )
            return True
        else:
            print(
                f"Failed! Insufficient balance: "
                f"{self.get_balance(sender)}"
            )
            return False


# ==================== DEMO ====================
print("--- Practical 3c Demo ---")

# Base & Derived
print("\n--- Inheritance Demo ---")

base = BaseContract(10)
base.get_data()
print("Type:", base.get_type())

derived = DerivedContract(50, "Hello World")
derived.get_data()
derived.get_derived_info()
derived.use_base_internal(3, 7)
print("Type:", derived.get_type())

# Abstract + Interface
print("\n--- Token Demo ---")

try:
    AbstractERC20Token(1000, "AbstractCoin", "ABC")
except TypeError as e:
    print("Cannot instantiate abstract class:", e)

token = MyERC20Token(1000, "MyCoin", "MYC")

addr1 = "0xAlice"
addr2 = "0xBob"
addr3 = "0xCharlie"
deployer = "deployer_address"

print("\nInitial Balances:")
print(deployer, token.get_balance(deployer))
print(addr1, token.get_balance(addr1))

# Transfers
token.transfer(deployer, addr1, 200)
token.transfer(addr1, addr2, 50)
token.transfer(addr2, addr3, 10)
token.transfer(addr1, addr2, 500)  # fail

print("\nFinal Balances:")
print(deployer, token.get_balance(deployer))
print(addr1, token.get_balance(addr1))
print(addr2, token.get_balance(addr2))
print(addr3, token.get_balance(addr3))

print("\n--- Demonstration Complete ---")
