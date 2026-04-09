class SimpleNFTCollection:
    """
    Simulates ERC-721 NFT logic
    """

    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol
        self._next_token_id = 0

        self._owners = {}
        self._balances = {}
        self._token_approvals = {}
        self._operator_approvals = {}
        self._token_uris = {}

        print(f"NFT Collection '{self._name}' ({self._symbol}) initialized.")

    def name(self):
        return self._name

    def symbol(self):
        return self._symbol

    def _require(self, condition, error):
        if not condition:
            raise ValueError(error)

    def balance_of(self, owner):
        self._require(owner != "0x0", "Invalid address")
        return self._balances.get(owner, 0)

    def owner_of(self, token_id):
        owner = self._owners.get(token_id)
        self._require(owner is not None, "Token does not exist")
        return owner

    def mint(self, to, uri):
        self._require(to != "0x0", "Invalid address")

        token_id = self._next_token_id
        self._next_token_id += 1

        self._owners[token_id] = to
        self._balances[to] = self._balances.get(to, 0) + 1
        self._token_uris[token_id] = uri

        print(f"\nMinted Token {token_id} → {to}")
        return token_id

    def _is_approved_or_owner(self, spender, token_id):
        owner = self.owner_of(token_id)

        return (
            spender == owner or
            self._token_approvals.get(token_id) == spender or
            self._operator_approvals.get(owner, {}).get(spender, False)
        )

    def transfer_from(self, sender, receiver, token_id, caller):
        print(f"\nTransfer {token_id}: {sender} → {receiver}")

        self._require(self.owner_of(token_id) == sender, "Wrong owner")
        self._require(receiver != "0x0", "Invalid receiver")
        self._require(
            self._is_approved_or_owner(caller, token_id),
            "Not authorized"
        )

        self._balances[sender] -= 1
        self._owners[token_id] = receiver
        self._balances[receiver] = self._balances.get(receiver, 0) + 1

        self._token_approvals.pop(token_id, None)

        print("Transfer successful")

    def approve(self, approved, token_id, caller):
        owner = self.owner_of(token_id)

        self._require(approved != owner, "Cannot approve owner")
        self._require(
            caller == owner or self.is_approved_for_all(owner, caller),
            "Not allowed"
        )

        self._token_approvals[token_id] = approved

        print(f"{approved} approved for Token {token_id}")

    def get_approved(self, token_id):
        return self._token_approvals.get(token_id, "0x0")

    def set_approval_for_all(self, operator, status, caller):
        if caller not in self._operator_approvals:
            self._operator_approvals[caller] = {}

        self._operator_approvals[caller][operator] = status

        print(f"{operator} operator status: {status}")

    def is_approved_for_all(self, owner, operator):
        return self._operator_approvals.get(owner, {}).get(operator, False)

    def token_uri(self, token_id):
        self._require(token_id in self._owners, "Token not found")
        return self._token_uris.get(token_id)


# ---------------- DEMO ----------------
print("--- Practical 4b NFT Demo ---")

nft = SimpleNFTCollection("MyNFT", "MNFT")

alice = "0xAlice"
bob = "0xBob"
charlie = "0xCharlie"
market = "0xMarket"

# Mint
t0 = nft.mint(alice, "uri0")
t1 = nft.mint(bob, "uri1")
t2 = nft.mint(alice, "uri2")

# Query
print("Alice balance:", nft.balance_of(alice))
print("Owner t0:", nft.owner_of(t0))
print("URI t1:", nft.token_uri(t1))

# Transfer
nft.transfer_from(alice, charlie, t0, alice)

# Invalid transfer
try:
    nft.transfer_from(alice, bob, t2, bob)
except ValueError as e:
    print("Error:", e)

# Approve + transfer
nft.approve(market, t2, alice)
nft.transfer_from(alice, bob, t2, market)

# Operator
nft.set_approval_for_all(market, True, charlie)
nft.transfer_from(charlie, alice, t0, market)

print("\nFinal Balances:")
print("Alice:", nft.balance_of(alice))
print("Bob:", nft.balance_of(bob))
print("Charlie:", nft.balance_of(charlie))
