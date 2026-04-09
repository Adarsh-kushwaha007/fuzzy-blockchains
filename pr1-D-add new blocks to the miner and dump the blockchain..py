import Crypto
import binascii
import datetime
import collections
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


# ==================== CLIENT CLASS ====================
class Client:
    def __init__(self, initial_balance=0):
        random_generator = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random_generator)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)
        self.balance = initial_balance

    @property
    def identity(self):
        return binascii.hexlify(
            self._public_key.exportKey(format='DER')
        ).decode('ascii')

    def __repr__(self):
        return f"Client(ID: {self.identity[:10]}..., Balance: {self.balance})"

    def sign_transaction(self, transaction_dict):
        signer = PKCS1_v1_5.new(self._private_key)
        h = SHA.new(str(transaction_dict).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


# ==================== TRANSACTION CLASS ====================
class Transaction:
    def __init__(self, sender_client, receiver_identity, value):
        self.sender = sender_client
        self.receiver = receiver_identity
        self.value = value
        self.time = datetime.datetime.now()
        self.signature = None

    def to_dict(self):
        sender_identity = "Genesis" if isinstance(self.sender, str) else self.sender.identity
        return collections.OrderedDict({
            'sender': sender_identity,
            'receiver': self.receiver,
            'value': self.value,
            'time': self.time
        })

    def sign(self):
        if isinstance(self.sender, str) and self.sender == "Genesis":
            self.signature = "Genesis Transaction - No Signature"
        else:
            self.signature = self.sender.sign_transaction(self.to_dict())

    def execute_transaction(self, client_map):
        if isinstance(self.sender, str) and self.sender == "Genesis":
            return True

        sender_id = self.sender.identity

        if sender_id in client_map and self.receiver in client_map:
            sender = client_map[sender_id]
            receiver = client_map[self.receiver]

            if sender.balance >= self.value:
                sender.balance -= self.value
                receiver.balance += self.value
                return True

        return False


# ==================== HASH & MINING ====================
def sha256_hash(message):
    return hashlib.sha256(str(message).encode('ascii')).hexdigest()


def mine(block, difficulty=1):
    assert difficulty >= 1
    prefix = "0" * difficulty

    print(f"Mining block with difficulty {difficulty}...")

    for i in range(1000000):
        digest = sha256_hash(str(hash(block)) + str(i))
        if digest.startswith(prefix):
            print(f"Nonce found after {i} iterations: {digest}")
            return digest

    print("Mining failed. Reduce difficulty.")
    return None


# ==================== BLOCK CLASS ====================
class Block:
    def __init__(self, transactions, previous_block_hash=""):
        self.verified_transactions = transactions
        self.previous_block_hash = previous_block_hash
        self.Nonce = ""
        self.timestamp = datetime.datetime.now()

    def __hash__(self):
        return hash((
            tuple(tuple(t.to_dict().items()) for t in self.verified_transactions),
            self.previous_block_hash,
            self.Nonce,
            self.timestamp
        ))


# ==================== BLOCKCHAIN CLASS ====================
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_transaction = Transaction("Genesis", "System", 1000000.0)
        genesis_transaction.sign()

        genesis_block = Block([genesis_transaction], "0")
        genesis_block.Nonce = mine(genesis_block, difficulty=2)

        if genesis_block.Nonce:
            self.chain.append(genesis_block)
            print("Genesis Block created!")

    def add_block(self, block):
        self.chain.append(block)

    def get_last_block_hash(self):
        if not self.chain:
            return "0"

        last_block = self.chain[-1]
        return sha256_hash(str(hash(last_block)) + str(last_block.Nonce))

    def display_transaction(self, transaction):
        tx = transaction.to_dict()
        print("Sender:", tx["sender"])
        print("Receiver:", tx["receiver"])
        print("Value:", tx["value"])
        print("Time:", tx["time"])
        print("Signature:", transaction.signature)

    def dump_blockchain(self):
        print("\n" + "=" * 50)
        print("Blockchain Dump")
        print("Total Blocks:", len(self.chain))

        for i, block in enumerate(self.chain):
            print(f"\nBlock #{i}")
            print("Previous Hash:", block.previous_block_hash)
            print("Nonce:", block.Nonce)
            print("Timestamp:", block.timestamp)

            for tx in block.verified_transactions:
                print("\n--- Transaction ---")
                self.display_transaction(tx)

        print("=" * 50)


# ==================== DEMO ====================
print("-" * 50)
print("Practical 1d: Blockchain Demo")
print("-" * 50)

# Initialize blockchain
my_blockchain = Blockchain()

# Create clients
alice = Client(100)
bob = Client(50)
charlie = Client(20)

all_clients_map = {
    alice.identity: alice,
    bob.identity: bob,
    charlie.identity: charlie
}

print("\nInitial Balances:")
for cid, c in all_clients_map.items():
    print(f"{cid[:10]}...: ₹{c.balance}")

# ---------------- BLOCK 1 ----------------
transactions_block1 = []

tx1 = Transaction(alice, bob.identity, 10.0)
tx1.sign()

tx2 = Transaction(bob, charlie.identity, 5.0)
tx2.sign()

transactions_block1.extend([tx1, tx2])

print("\nCreating Block 1...")
block1 = Block(transactions_block1, my_blockchain.get_last_block_hash())
block1.Nonce = mine(block1, difficulty=3)

if block1.Nonce:
    my_blockchain.add_block(block1)

    print("Executing transactions...")
    for tx in transactions_block1:
        success = tx.execute_transaction(all_clients_map)
        print("Success" if success else "Failed")


# ---------------- BLOCK 2 ----------------
transactions_block2 = []

tx3 = Transaction(charlie, alice.identity, 2.0)
tx3.sign()

tx4 = Transaction(alice, bob.identity, 7.0)
tx4.sign()

transactions_block2.extend([tx3, tx4])

print("\nCreating Block 2...")
block2 = Block(transactions_block2, my_blockchain.get_last_block_hash())
block2.Nonce = mine(block2, difficulty=3)

if block2.Nonce:
    my_blockchain.add_block(block2)

    print("Executing transactions...")
    for tx in transactions_block2:
        success = tx.execute_transaction(all_clients_map)
        print("Success" if success else "Failed")


# Final balances
print("\nFinal Balances:")
for cid, c in all_clients_map.items():
    print(f"{cid[:10]}...: ₹{c.balance}")

# Dump blockchain
my_blockchain.dump_blockchain()
