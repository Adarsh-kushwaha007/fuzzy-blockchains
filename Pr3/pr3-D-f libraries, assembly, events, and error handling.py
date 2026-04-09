import logging

# ==================== LIBRARY: MATH ====================
class MathUtils:

    @staticmethod
    def square(num):
        return num * num

    @staticmethod
    def safe_divide(numerator, denominator):
        if denominator == 0:
            raise ValueError("Division by zero is not allowed.")
        return numerator / denominator


# ==================== LIBRARY: STRING ====================
class StringUtils:

    @staticmethod
    def concatenate_strings(s1, s2):
        return s1 + s2

    @staticmethod
    def reverse_string(s):
        return s[::-1]


# ==================== EVENT LOGGER ====================
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)


class EventLogger:

    @staticmethod
    def emit_deposit_event(user, amount, balance):
        logging.info(
            f"EVENT: Deposit | User: {user} | Amount: {amount} | Balance: {balance}"
        )

    @staticmethod
    def emit_withdrawal_event(user, amount, balance):
        logging.info(
            f"EVENT: Withdrawal | User: {user} | Amount: {amount} | Balance: {balance}"
        )

    @staticmethod
    def emit_custom_event(event_name, **kwargs):
        msg = f"EVENT: {event_name}"
        for k, v in kwargs.items():
            msg += f", {k}: {v}"
        logging.info(msg)


# ==================== CUSTOM EXCEPTION ====================
class InsufficientFundsError(Exception):

    def __init__(self, sender, requested, available):
        super().__init__(
            f"Sender {sender} requested {requested}, but only has {available}"
        )


# ==================== ACCOUNT MANAGER ====================
class AccountManager:

    def __init__(self):
        self.balances = {}
        print("AccountManager initialized.")

    def deposit(self, user, amount):
        print(f"\nDeposit → {user}: {amount}")

        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.balances[user] = self.balances.get(user, 0) + amount

        EventLogger.emit_deposit_event(user, amount, self.balances[user])

        print(f"New Balance: {self.balances[user]}")

    def withdraw(self, user, amount):
        print(f"\nWithdraw → {user}: {amount}")

        try:
            if amount <= 0:
                raise ValueError("Withdrawal must be positive.")

            balance = self.balances.get(user, 0)

            if balance < amount:
                raise InsufficientFundsError(user, amount, balance)

            self.balances[user] -= amount

            EventLogger.emit_withdrawal_event(
                user, amount, self.balances[user]
            )

            print(f"New Balance: {self.balances[user]}")

        except InsufficientFundsError as e:
            logging.error(f"FAILED: {e}")
        except ValueError as e:
            logging.error(f"INVALID: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    def get_balance(self, user):
        return self.balances.get(user, 0)

    def process_data(self, data_list):
        print(f"\nProcessing: {data_list}")

        try:
            total = 0

            for item in data_list:
                total += MathUtils.square(item)

            logging.info(f"Sum of squares: {total}")

            assert len(data_list) > 0, "Data list cannot be empty!"

            logging.info("Assertion passed.")

        except AssertionError as e:
            logging.critical(f"CRITICAL: {e}")
        except Exception as e:
            logging.error(f"Error: {e}")


# ==================== DEMO ====================
print("--- Practical 3d Demo ---")

acc = AccountManager()

# Library Demo
print("\n--- Library Demo ---")

print("Square:", MathUtils.square(7))

try:
    print("Divide:", MathUtils.safe_divide(10, 2))
    print("Divide:", MathUtils.safe_divide(10, 0))
except ValueError as e:
    print("Caught:", e)

print("Concat:", StringUtils.concatenate_strings("Blockchain", "Python"))
print("Reverse:", StringUtils.reverse_string("Blockchain"))


# Events + Errors
print("\n--- Events Demo ---")

alice = "0xAlice"
bob = "0xBob"

try:
    acc.deposit(alice, 100)
    acc.deposit(bob, 50)
    acc.deposit(alice, -10)
except ValueError as e:
    print("Deposit error:", e)

acc.withdraw(alice, 30)
acc.withdraw(bob, 70)
acc.withdraw(alice, 0)


# Assertion Demo
print("\n--- Assertion Demo ---")

acc.process_data([1, 2, 3, 4, 5])
acc.process_data([])

print("\n--- Done ---")
